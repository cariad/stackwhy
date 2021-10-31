from io import StringIO

from mock import Mock
from pytest import raises

from stackwhy import Event, StackWhy


def make_event(physical_id: str = "") -> Event:
    return Event(
        logical_id="",
        physical_id=physical_id,
        status="",
        status_reason="",
        type="",
    )


def test_events() -> None:
    response = {
        "StackEvents": [
            {
                "LogicalResourceId": "LogicalResourceId0",
                "PhysicalResourceId": "PhysicalResourceId0",
                "ResourceStatus": "ResourceStatus0",
                "ResourceStatusReason": "ResourceStatusReason0",
                "ResourceType": "ResourceType0",
            },
            {
                "LogicalResourceId": "LogicalResourceId1",
                "PhysicalResourceId": "PhysicalResourceId1",
                "ResourceStatus": "ResourceStatus1",
                "ResourceStatusReason": "ResourceStatusReason1",
                "ResourceType": "ResourceType1",
            },
            {
                "LogicalResourceId": "LogicalResourceId2",
                "PhysicalResourceId": "foo",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceStatusReason": "ResourceStatusReason2",
                "ResourceType": "ResourceType2",
            },
            {
                "LogicalResourceId": "LogicalResourceIdX",
                "PhysicalResourceId": "PhysicalResourceIdX",
                "ResourceStatus": "ResourceStatusX",
                "ResourceStatusReason": "ResourceStatusReasonX",
                "ResourceType": "ResourceTypeX",
            },
        ],
    }

    describe_stack_events = Mock(return_value=response)
    client = Mock()
    client.describe_stack_events = describe_stack_events
    session = Mock()
    session.client = Mock(return_value=client)

    sw = StackWhy("foo", session=session)

    assert sw.events == [
        Event(
            logical_id="LogicalResourceId2",
            physical_id="foo",
            status="CREATE_IN_PROGRESS",
            status_reason="ResourceStatusReason2",
            type="ResourceType2",
        ),
        Event(
            logical_id="LogicalResourceId1",
            physical_id="PhysicalResourceId1",
            status="ResourceStatus1",
            status_reason="ResourceStatusReason1",
            type="ResourceType1",
        ),
        Event(
            logical_id="LogicalResourceId0",
            physical_id="PhysicalResourceId0",
            status="ResourceStatus0",
            status_reason="ResourceStatusReason0",
            type="ResourceType0",
        ),
    ]


def test_has_any_physical_id__false() -> None:
    sw = StackWhy("foo")
    setattr(
        sw,
        "events",
        [
            make_event(),
            make_event(),
        ],
    )
    assert not sw.has_any_physical_id


def test_has_any_physical_id__true() -> None:
    sw = StackWhy("foo")
    setattr(
        sw,
        "events",
        [
            make_event(),
            make_event(physical_id="x"),
        ],
    )
    assert sw.has_any_physical_id


def test_render() -> None:
    writer = StringIO()
    sw = StackWhy("foo")
    setattr(
        sw,
        "events",
        [
            Event(
                logical_id="a",
                physical_id="b",
                status="c",
                status_reason="d",
                type="e",
            )
        ],
    )
    sw.render(writer)
    assert (
        writer.getvalue()
        == """\x1b[1mLogical ID\x1b[22m    \x1b[1mPhysical ID\x1b[22m    \x1b[1mResource Type\x1b[22m    \x1b[1mStatus\x1b[22m    \x1b[1mReason\x1b[22m
\x1b[38;5;10ma\x1b[39m             \x1b[38;5;10mb\x1b[39m              \x1b[38;5;10me\x1b[39m                \x1b[38;5;10mc\x1b[39m         \x1b[38;5;10md\x1b[39m
"""
    )


def test_render__no_physical_ids() -> None:
    writer = StringIO()
    sw = StackWhy("foo")
    setattr(
        sw,
        "events",
        [
            Event(
                logical_id="a",
                physical_id="",
                status="c",
                status_reason="d",
                type="e",
            )
        ],
    )
    sw.render(writer)
    assert (
        writer.getvalue()
        == """\x1b[1mLogical ID\x1b[22m    \x1b[1mResource Type\x1b[22m    \x1b[1mStatus\x1b[22m    \x1b[1mReason\x1b[22m
\x1b[38;5;10ma\x1b[39m             \x1b[38;5;10me\x1b[39m                \x1b[38;5;10mc\x1b[39m         \x1b[38;5;10md\x1b[39m
"""
    )
