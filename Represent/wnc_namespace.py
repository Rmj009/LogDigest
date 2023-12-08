from dataclasses import dataclass


@dataclass(frozen=True)
class Storage:
    meter: float
    unit: float

    def __str__(self):
        a = 'N' if self.meter >= 0 else 'S'
        b = 'E' if self.unit >= 0 else 'W'
        return f'{abs(self.meter):.1f}°{a}, {abs(self.unit):.1f}°{b}'
