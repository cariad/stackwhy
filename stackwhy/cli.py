from argparse import ArgumentParser
from typing import IO, List

from boto3.session import Session

from stackwhy.stack_why import StackWhy
from stackwhy.version import get_version


def entry(args: List[str], session: Session, writer: IO[str]) -> int:
    parser = ArgumentParser(
        description="Explains an Amazon Web Services CloudFormation stack failure.",
        epilog="Made with love by Cariad Eccleston: https://github.com/cariad/stackwhy",
    )

    parser.add_argument("stack", help="Stack ARN, ID or name", nargs="?")
    parser.add_argument("--version", help="show version and exit", action="store_true")

    ns = parser.parse_args(args)

    if ns.version:
        writer.write(get_version() + "\n")
        return 0

    if not ns.stack:
        writer.write(parser.format_help())
        return 0

    StackWhy(ns.stack, session=session).render(writer)
    return 0
