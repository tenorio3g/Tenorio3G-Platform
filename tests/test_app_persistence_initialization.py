from __future__ import annotations

import app as app_module


class FakeEnsureDefaultMapLayers:
    def __init__(
        self,
        calls: list[str],
    ) -> None:
        self._calls = calls

    def execute(self) -> None:
        self._calls.append(
            "ensure_default_map_layers"
        )


class FakeEnsureDefaultMapPlans:
    def __init__(
        self,
        calls: list[str],
    ) -> None:
        self._calls = calls

    def execute(self) -> None:
        self._calls.append(
            "ensure_default_map_plans"
        )


def test_should_initialize_persistence_in_order(
    monkeypatch,
) -> None:
    calls: list[str] = []

    monkeypatch.setattr(
        app_module,
        "initialize_database",
        lambda: calls.append(
            "initialize_database"
        ),
    )

    monkeypatch.setattr(
        app_module,
        "ensure_default_map_layers",
        FakeEnsureDefaultMapLayers(
            calls
        ),
    )

    monkeypatch.setattr(
        app_module,
        "ensure_default_map_plans",
        FakeEnsureDefaultMapPlans(
            calls
        ),
        raising=False,
    )

    monkeypatch.setattr(
        app_module,
        "load_demo_physical_locations",
        lambda: calls.append(
            "load_demo_physical_locations"
        ),
    )

    monkeypatch.setattr(
        app_module,
        "load_demo_assets",
        lambda: calls.append(
            "load_demo_assets"
        ),
    )

    app_module._initialize_persistence()

    assert calls == [
        "initialize_database",
        "ensure_default_map_layers",
        "ensure_default_map_plans",
        "load_demo_physical_locations",
        "load_demo_assets",
    ]
