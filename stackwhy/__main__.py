from stackwhy.version import get_version


def cli_entry() -> None:
    print(get_version())


if __name__ == "__main__":
    cli_entry()
