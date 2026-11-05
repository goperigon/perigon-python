import os
from collections.abc import Iterator

import pytest
import respx


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Run live Perigon API tests. Requires PERIGON_API_KEY.",
    )
    parser.addoption(
        "--unit",
        action="store_true",
        default=False,
        help="With --integration, also run the offline tests.",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """Choose which suite runs.

    The default run is offline. ``--integration`` runs the live tests.
    ``--integration --unit`` runs both. ``uv run pytest`` stays offline.
    """
    integration = config.getoption("--integration")
    unit = config.getoption("--unit")
    if integration and not os.environ.get("PERIGON_API_KEY"):
        raise pytest.UsageError("PERIGON_API_KEY must be set to run integration tests.")

    def keep(item: pytest.Item) -> bool:
        live = _is_integration(item)
        if integration and unit:
            return True
        if integration:
            return live
        return not live

    selected = [item for item in items if keep(item)]
    deselected = [item for item in items if item not in selected]
    if deselected:
        config.hook.pytest_deselected(items=deselected)
    items[:] = selected


def _is_integration(item: pytest.Item) -> bool:
    return item.get_closest_marker("integration") is not None


@pytest.fixture(autouse=True)
def block_real_http(request: pytest.FixtureRequest) -> Iterator[None]:
    """Fail any HTTP call that a test did not mock.

    Integration tests opt out so they can call the Perigon API.
    """
    if request.node.get_closest_marker("integration") is not None:
        yield
        return
    # No parentheses: routes added with respx.get/post/route join this router.
    # Parentheses would open a separate router and leave those routes unused.
    # assert_all_mocked is already on, so a request with no route fails.
    with respx.mock:
        yield
