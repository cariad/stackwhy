from sys import argv, stdout

from boto3.session import Session

from stackwhy.cli import entry


def cli_entry() -> None:
    exit(entry(argv[1:], session=Session(), writer=stdout))


if __name__ == "__main__":
    cli_entry()
