from dataclasses import dataclass


@dataclass(frozen=True)
class RegistryStatisticsViewModel:

    total: int

    primitives: int
    components: int
    patterns: int
    utilities: int

    stable: int
    development: int
    pending: int
    deprecated: int