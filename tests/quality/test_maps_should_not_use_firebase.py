from pathlib import Path


MAPS_ROOT = Path("app/maps")


def test_maps_should_not_use_firebase() -> None:
    forbidden_terms = (
        "firebase",
        "firestore",
        "db.collection",
        "equipos-beaf1",
    )

    violations: list[str] = []

    for path in MAPS_ROOT.rglob("*"):
        if not path.is_file():
            continue

        if "__pycache__" in path.parts:
            continue

        if path.suffix.lower() not in {
            ".py",
            ".js",
            ".html",
        }:
            continue

        content = path.read_text(
            encoding="utf-8"
        ).lower()

        for term in forbidden_terms:
            if term.lower() in content:
                violations.append(
                    f"{path}: {term}"
                )

    assert not violations, (
        "Maps todavia contiene dependencias "
        "de Firebase:\n"
        + "\n".join(violations)
    )
