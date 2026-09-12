from pathlib import Path
import re


TEMPLATE_PATH = Path(
    "app/templates/pages/work_orders_index.html"
)

ROUTES_PATH = Path(
    "app/work_orders/routes.py"
)


def test_work_orders_index_should_offer_scope_filters():

    source = TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )

    assert (
        "Todas las "
        + chr(243)
        + "rdenes"
    ) in source

    assert (
        "Mis "
        + chr(243)
        + "rdenes"
    ) in source

    assert "selected_scope" in source


def test_work_orders_links_should_preserve_scope():

    source = TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )

    assert "scope=selected_scope" in source


def test_work_orders_search_should_preserve_scope():

    source = TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )

    assert 'name="scope"' in source
    assert 'value="{{ selected_scope }}"' in source


def test_status_filter_links_should_preserve_scope():

    source = TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )

    match = re.search(
        r"{%\s*for code, label in status_filters\s*%}"
        r"(.*?)"
        r"{%\s*endfor\s*%}",
        source,
        flags=re.DOTALL,
    )

    assert match is not None

    status_filter_block = match.group(1)

    assert "scope=selected_scope" in status_filter_block


def test_route_should_build_summary_from_scoped_items():

    source = ROUTES_PATH.read_text(
        encoding="utf-8"
    )

    assert "WorkOrderSummaryViewModel" in source

    assert re.search(
        r"WorkOrderSummaryViewModel\s*\("
        r"\s*items=scoped_items\s*"
        r"\)",
        source,
        flags=re.DOTALL,
    )
