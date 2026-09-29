from django.core.management.base import BaseCommand

from mes.models import (
    Plant,
    Segment,
    SegmentType,
    State,
    StateMachine,
)


class Command(BaseCommand):
    help = "Create the initial Lucas-Nülle MES configuration."

    def handle(self, *args, **options):
        self.stdout.write("Seeding MES configuration...")

        # ---------------------------------------------------------
        # Plant
        # ---------------------------------------------------------

        plant, created = Plant.objects.get_or_create(
            code="ERP1",
            defaults={
                "name": "ERP Lab",
                "description": (
                    "Lucas-Nülle ERP Lab production environment."
                ),
                "enabled": True,
            },
        )

        self.stdout.write(
            f"Plant ERP1: {'created' if created else 'already exists'}"
        )

        # ---------------------------------------------------------
        # Segment type
        # ---------------------------------------------------------

        segment_type, created = SegmentType.objects.get_or_create(
            code="TRANSPORT",
            defaults={
                "name": "Transport",
                "description": (
                    "Transport and production-line segment."
                ),
                "enabled": True,
            },
        )

        self.stdout.write(
            "Segment type TRANSPORT: "
            f"{'created' if created else 'already exists'}"
        )

        # ---------------------------------------------------------
        # State machine
        # ---------------------------------------------------------

        state_machine, created = StateMachine.objects.get_or_create(
            code="LN_STANDARD",
            defaults={
                "name": "Lucas-Nülle Standard State Machine",
                "description": (
                    "State machine structure used by the "
                    "Lucas-Nülle ERP Lab."
                ),
                "enabled": True,
            },
        )

        self.stdout.write(
            "State machine LN_STANDARD: "
            f"{'created' if created else 'already exists'}"
        )

        # ---------------------------------------------------------
        # States
        # ---------------------------------------------------------

        states = [
            {
                "number": 0,
                "name": "Idle",
                "description": "Initial / idle state.",
            },
            {
                "number": 10,
                "name": "Reading Carrier",
                "description": "Reading the carrier.",
            },
            {
                "number": 18,
                "name": "Working",
                "description": "Production / working state.",
            },
            {
                "number": 19,
                "name": "Finish",
                "description": "Production step finished.",
            },
            {
                "number": 24,
                "name": "Transfer Back",
                "description": "Transfer carrier back.",
            },
        ]

        for state_data in states:
            state, created = State.objects.get_or_create(
                state_machine=state_machine,
                number=state_data["number"],
                defaults={
                    "name": state_data["name"],
                    "description": state_data["description"],
                },
            )

            self.stdout.write(
                f"State {state.number}: "
                f"{'created' if created else 'already exists'}"
            )

        # ---------------------------------------------------------
        # Lucas-Nülle segments
        # ---------------------------------------------------------

        segments = [
            ("IMS1", "IMS1"),
            ("IMS3A", "IMS3A"),
            ("IMS3B", "IMS3B"),
            ("IMS4A", "IMS4A"),
            ("IMS4B", "IMS4B"),
            ("IMS5A", "IMS5A"),
            ("IMS5B", "IMS5B"),
            ("IMS7", "IMS7"),
        ]

        for code, name in segments:
            segment, created = Segment.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "plant": plant,
                    "segment_type": segment_type,
                    "state_machine": state_machine,
                    "enabled": True,
                },
            )

            self.stdout.write(
                f"Segment {segment.code}: "
                f"{'created' if created else 'already exists'}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                "MES configuration seeded successfully."
            )
        )
