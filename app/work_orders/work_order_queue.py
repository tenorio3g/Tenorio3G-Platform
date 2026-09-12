def filter_items_by_scope(
    items,
    scope: str,
    person_code: str | None,
):

    normalized_scope = str(
        scope or "ALL"
    ).strip().upper()

    if normalized_scope != "MINE":
        return list(
            items
        )

    if not person_code:
        return []

    normalized_person_code = str(
        person_code
    ).strip().upper()

    return [
        item
        for item in items
        if normalized_person_code
        in {
            str(code).strip().upper()
            for code in item.technician_codes
        }
    ]
