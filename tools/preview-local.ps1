[CmdletBinding()]
param(
    [switch]$NoServe
)

$ErrorActionPreference = "Stop"

function Test-PortUsable {
    param(
        [int]$Port
    )

    $listener = $null
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $Port)
        $listener.Start()
        $listener.Stop()
        return $true
    } catch {
        if ($listener) {
            try { $listener.Stop() } catch {}
        }
        return $false
    }
}

function Test-PythonPortUsable {
    param(
        [string]$PythonExe,
        [int]$Port
    )

    $probe = @'
import socket
import sys

port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.bind(("127.0.0.1", port))
except OSError:
    raise SystemExit(1)
finally:
    sock.close()
'@

    $probe | & $PythonExe - $Port | Out-Null
    return ($LASTEXITCODE -eq 0)
}

function Get-AvailablePort {
    param(
        [int]$Preferred = 8000,
        [int]$MaxAttempts = 16
    )

    if ((Test-PortUsable -Port $Preferred) -and (Test-PythonPortUsable -PythonExe $pythonExe -Port $Preferred)) {
        return $Preferred
    }

    return Get-RandomPreviewPort -MaxAttempts $MaxAttempts
}

function Get-RandomPreviewPort {
    param(
        [int]$MaxAttempts = 16
    )

    for ($attempt = 0; $attempt -lt $MaxAttempts; $attempt++) {
        $fallback = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, 0)
        try {
            $fallback.Start()
            $candidate = [int]$fallback.LocalEndpoint.Port
        } finally {
            $fallback.Stop()
        }

        if ((Test-PortUsable -Port $candidate) -and (Test-PythonPortUsable -PythonExe $pythonExe -Port $candidate)) {
            return $candidate
        }
    }

    throw "Unable to find a usable localhost port for the preview server."
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$previewRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("amw-preview-{0}" -f ([Guid]::NewGuid().ToString("N")))
New-Item -ItemType Directory -Path $previewRoot -Force | Out-Null

$pythonExe = Join-Path $repoRoot "venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

Write-Host "== Build Temp Preview =="

$buildScript = @'
import json
import os
import shutil
import sys
from pathlib import Path

repo_root = Path(sys.argv[1])
preview_dir = Path(sys.argv[2])
assets_src = repo_root / "asset"
assets_dst = preview_dir / "asset"
shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)

def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

roster = load_json(assets_src / "roster.json", [])
raw = load_json(assets_src / "raw_roster.json", [])
timeline = load_json(assets_src / "timeline.json", [])

sys.path.insert(0, str(repo_root))
os.chdir(preview_dir)

from render.html_dashboard import generate_html_dashboard

generate_html_dashboard(roster, {}, timeline, raw, {}, {}, {})
print(preview_dir)
'@

$buildScript | & $pythonExe - $repoRoot $previewRoot
if ($LASTEXITCODE -ne 0) {
    throw "Preview build failed."
}

$port = Get-AvailablePort

if ($NoServe) {
    Write-Host "Preview built without starting a server."
    Write-Host "Preview directory: $previewRoot"
    Write-Host "Manual server command:"
    Write-Host "  $pythonExe -m http.server $port --bind 127.0.0.1 --directory `"$previewRoot`""
    Write-Host "Open: http://127.0.0.1:$port/index.html"
    return
}

$serveScript = @'
import functools
import http.server
import os
import pathlib
import sys

preview_dir = pathlib.Path(sys.argv[1])
port = int(sys.argv[2])

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(preview_dir))

try:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
except OSError as exc:
    print(f"Unable to start preview server on 127.0.0.1:{port}: {exc}", file=sys.stderr)
    raise SystemExit(1)

print(f"Preview directory: {preview_dir}")
print(f"Preview URL: http://127.0.0.1:{port}/index.html")
print("Press Ctrl+C to stop the preview server.")

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
'@

$attempts = 0
$lastFailure = $null
while ($attempts -lt 4) {
    $attempts++
    Write-Host "Starting foreground server (attempt $attempts)..."
    $serveScript | & $pythonExe - $previewRoot $port
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Preview server stopped."
        return
    }

    $lastFailure = $LASTEXITCODE
    Write-Host "Preview server failed to start on port $port. Retrying with another port..."
    $port = Get-RandomPreviewPort
}

throw "Unable to start the preview server after multiple port attempts. Try rerunning the script or using -NoServe. Last exit code: $lastFailure"
