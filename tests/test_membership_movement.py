import unittest

from wow.membership_movement import build_membership_movement_events


class MembershipMovementTests(unittest.TestCase):
    def test_joined_member_detection(self):
        events = build_membership_movement_events(
            ["Charlie"],
            [],
            scan_id="scan-1",
            detected_at="2026-04-29T10:00:00Z",
        )

        self.assertEqual(len(events), 1)
        self.assertEqual(
            events[0],
            {
                "scan_id": "scan-1",
                "character_name": "Charlie",
                "event_type": "joined",
                "detected_at": "2026-04-29T10:00:00Z",
                "previous_status": None,
                "current_status": "active",
            },
        )

    def test_departed_member_detection(self):
        events = build_membership_movement_events(
            ["Alpha"],
            [
                {"character_name": "Alpha", "status": "active"},
                {"character_name": "Bravo", "status": "active"},
            ],
            scan_id="scan-2",
            detected_at="2026-04-29T10:05:00Z",
        )

        self.assertEqual(len(events), 1)
        self.assertEqual(
            events[0],
            {
                "scan_id": "scan-2",
                "character_name": "Bravo",
                "event_type": "departed",
                "detected_at": "2026-04-29T10:05:00Z",
                "previous_status": "active",
                "current_status": "departed",
            },
        )

    def test_rejoined_member_detection(self):
        events = build_membership_movement_events(
            ["Alpha"],
            [{"character_name": "alpha", "status": "departed"}],
            scan_id="scan-3",
            detected_at="2026-04-29T10:10:00Z",
        )

        self.assertEqual(len(events), 1)
        self.assertEqual(
            events[0],
            {
                "scan_id": "scan-3",
                "character_name": "Alpha",
                "event_type": "rejoined",
                "detected_at": "2026-04-29T10:10:00Z",
                "previous_status": "departed",
                "current_status": "active",
            },
        )

    def test_unchanged_active_and_departed_members_produce_no_events(self):
        events = build_membership_movement_events(
            ["Alpha"],
            [
                {"character_name": "ALPHA", "status": "active"},
                {"character_name": "Bravo", "status": "departed"},
            ],
            scan_id="scan-4",
            detected_at="2026-04-29T10:15:00Z",
        )

        self.assertEqual(events, [])

    def test_name_normalization_and_event_ordering(self):
        events = build_membership_movement_events(
            ["  charlie  ", "", None, "Alpha"],
            [
                {"character_name": "alpha", "status": "departed"},
                {"character_name": "Delta", "status": "active"},
            ],
            scan_id="scan-5",
            detected_at="2026-04-29T10:20:00Z",
        )

        self.assertEqual(
            [event["event_type"] for event in events],
            ["joined", "rejoined", "departed"],
        )
        self.assertEqual(
            [event["character_name"] for event in events],
            ["Charlie", "Alpha", "Delta"],
        )
        self.assertTrue(all(event["scan_id"] == "scan-5" for event in events))
        self.assertTrue(all(event["detected_at"] == "2026-04-29T10:20:00Z" for event in events))


if __name__ == "__main__":
    unittest.main()
