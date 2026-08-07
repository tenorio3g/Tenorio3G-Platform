from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TechnicalDataViewModel:
    equipment_type: str
    manufacturer: str
    model: str
    serial_number: str
    voltage: str
    phases: str
    frequency: str
    motor_power: str
    observations: str