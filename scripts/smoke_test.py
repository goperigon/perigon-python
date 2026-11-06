"""Check that an installed perigon build imports and reports its own version."""

import importlib.metadata

import perigon


def main() -> None:
    installed = importlib.metadata.version("perigon")
    if perigon.__version__ != installed:
        raise SystemExit(
            f"perigon.__version__ is {perigon.__version__}, "
            f"installed distribution is {installed}"
        )
    if perigon.V1Api is None or perigon.ApiClient is None:
        raise SystemExit("perigon.V1Api and perigon.ApiClient must be importable")


if __name__ == "__main__":
    main()
