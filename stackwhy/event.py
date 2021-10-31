from dataclasses import dataclass


@dataclass
class Event:
    logical_id: str
    """Logical ID of the resource referenced by this event."""

    physical_id: str
    """Physical ID of the resource referenced by this event."""

    status: str
    """Status of the resource referenced by this event."""

    status_reason: str
    """Reason for the status of the resource referenced by this event."""

    type: str
    """Type of the resource referenced by this event."""

    def is_start(self, arn: str) -> bool:
        return self.physical_id == arn and self.status in [
            "CREATE_IN_PROGRESS",
            "UPDATE_IN_PROGRESS",
        ]
