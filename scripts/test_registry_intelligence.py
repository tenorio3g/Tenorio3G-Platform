from app.foundation.services import (
    RegistryIntelligenceService,
)


service = RegistryIntelligenceService()

statistics = service.statistics()

print("Total:", statistics.total)
print("Primitives:", statistics.primitives)
print("Components:", statistics.components)
print("Patterns:", statistics.patterns)
print("Utilities:", statistics.utilities)

print("Stable:", statistics.stable)
print("Development:", statistics.development)
print("Pending:", statistics.pending)
print("Deprecated:", statistics.deprecated)

print("\nTag layout:")

for item in service.by_tag("layout"):
    print("-", item.id, item.name)


print("\nSearch panel:")

for item in service.search("panel"):
    print("-", item.id, item.name)


print("\nSorted by name:")

for item in service.sort_by_name():
    print("-", item.name)


print("\nComponents sorted by name:")

for item in service.sort_by_name(
    service.components()
):
    print("-", item.name)


print("\nSorted by category:")

for item in service.sort_by_category():
    print(
        "-",
        item.category.value,
        item.name,
    )


print("\nSorted by status:")

for item in service.sort_by_status():
    print(
        "-",
        item.status.value,
        item.name,
    )