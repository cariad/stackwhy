from io import StringIO

from mock import Mock

from stackwhy.cli import entry

valid_arn = "arn:aws:cloudformation:eu-west-2:000000000000:stack/X/00000000-0000-0000-0000-000000000000"


def test_help() -> None:
    writer = StringIO()
    assert entry([], session=Mock(), writer=writer) == 0
    assert writer.getvalue().startswith("usage:")


def test_render() -> None:
    response = {
        "StackEvents": [
            {
                "LogicalResourceId": "LogicalResourceId1",
                "PhysicalResourceId": "PhysicalResourceId1",
                "ResourceStatus": "ResourceStatus1",
                "ResourceStatusReason": "ResourceStatusReason1",
                "ResourceType": "ResourceType1",
            },
            {
                "LogicalResourceId": "LogicalResourceId2",
                "PhysicalResourceId": valid_arn,
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceStatusReason": "ResourceStatusReason2",
                "ResourceType": "ResourceType2",
            },
        ],
    }

    describe_stack_events = Mock(return_value=response)
    client = Mock()
    client.describe_stack_events = describe_stack_events
    session = Mock()
    session.client = Mock(return_value=client)

    writer = StringIO()
    assert (
        entry(
            [valid_arn],
            session=session,
            writer=writer,
        )
        == 0
    )
    assert (
        writer.getvalue()
        == """\x1b[1mLogical ID\x1b[22m          \x1b[1mPhysical ID\x1b[22m          \x1b[1mResource Type\x1b[22m    \x1b[1mStatus\x1b[22m              \x1b[1mReason\x1b[22m
\x1b[38;5;10mLogicalResourceId2\x1b[39m                       \x1b[38;5;10mResourceType2\x1b[39m    \x1b[38;5;10mCREATE IN PROGRESS\x1b[39m  \x1b[38;5;10mResourceStatusReason2\x1b[39m
\x1b[38;5;10mLogicalResourceId1\x1b[39m  \x1b[38;5;10mPhysicalResourceId1\x1b[39m  \x1b[38;5;10mResourceType1\x1b[39m    \x1b[38;5;10mResourceStatus1\x1b[39m     \x1b[38;5;10mResourceStatusReason1\x1b[39m
"""
    )


def test_version() -> None:
    writer = StringIO()
    assert entry(["--version"], session=Mock(), writer=writer) == 0
    assert writer.getvalue() == "-1.-1.-1\n"
