from functools import cached_property
from sys import stdout
from textwrap import wrap
from typing import IO, List, Optional

from ansiscape import bright_green, bright_red, bright_yellow, heavy
from boto3.session import Session
from tabulate import tabulate

from stackwhy.event import Event


class StackWhy:
    """
    Visualises the most recent events on an Amazon Web Services CloudFormation
    stack.

    Arguments:
        stack:   Stack ARN
        session: Session (defaults to a new session)
    """

    def __init__(self, stack: str, session: Optional[Session] = None) -> None:
        self.session = session or Session()
        self.stack = stack

    @cached_property
    def events(self) -> List[Event]:
        """Gets the most recent events on the stack."""

        client = self.session.client(
            "cloudformation",
        )  # pyright: reportUnknownMemberType=false
        response = client.describe_stack_events(StackName=self.stack)
        wip: List[Event] = []

        for e in response["StackEvents"]:
            event = Event(
                logical_id=e.get("LogicalResourceId", ""),
                physical_id=e.get("PhysicalResourceId", ""),
                status=e.get("ResourceStatus", ""),
                status_reason=e.get("ResourceStatusReason", ""),
                type=e.get("ResourceType", ""),
            )

            wip.insert(0, event)
            if event.is_start(self.stack):
                break

        return wip

    @cached_property
    def has_any_physical_id(self) -> bool:
        """
        Returns ``True`` if any of the discovered events describe a physical ID.
        """

        for event in self.events:
            if event.physical_id and event.physical_id != self.stack:
                return True
        return False

    def render(self, writer: Optional[IO[str]] = None) -> None:
        """
        Renders a table of events.

        Arguments:
            writer: Writer (defaults to ``stdout``)
        """

        header = [
            heavy("Logical ID").encoded,
            heavy("Resource Type").encoded,
            heavy("Status").encoded,
            heavy("Reason").encoded,
        ]

        if self.has_any_physical_id:
            header.insert(1, heavy("Physical ID").encoded)

        rows = [
            header,
        ]

        for event in self.events:
            rollback = "ROLLBACK_IN_PROGRESS" in event.status
            failed = "FAILED" in event.status
            color = (
                bright_red if failed else bright_yellow if rollback else bright_green
            )

            row = [
                color(event.logical_id).encoded,
                color(event.type).encoded,
                color(event.status).encoded,
                color("\n".join(wrap(event.status_reason, width=60))).encoded,
            ]

            if self.has_any_physical_id:
                p_id = (
                    color(event.physical_id).encoded
                    if event.physical_id != self.stack
                    else ""
                )
                row.insert(1, p_id)

            rows.append(row)

        t = tabulate(rows, headers="firstrow", tablefmt="plain")
        (writer or stdout).write(t + "\n")
