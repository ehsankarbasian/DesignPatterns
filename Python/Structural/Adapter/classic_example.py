from __future__ import annotations


class RoundHole:
    
    def __init__(self, radius: float):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    def fits(self, peg: RoundPeg):
        return self.radius >= peg.radius


# Target
class RoundPeg:
    
    def __init__(self, radius: float):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius


# Adaptee
class SquarePeg:
    
    def __init__(self, width: float):
        self._width = width
    
    @property
    def width(self):
        return self._width


# Adapter
class SquarePegAdapter:
    
    def __init__(self, peg: SquarePeg):
        self._peg = peg
    
    @property
    def radius(self):
        return self._peg.width * (2**0.5 / 2)


# Client code
if __name__ == "__main__":

    hole = RoundHole(5)

    # Target works directly
    round_peg = RoundPeg(5)
    print("Round peg fits:", hole.fits(round_peg))


    # Adaptee (cannot be used directly)
    small_square = SquarePeg(5)
    large_square = SquarePeg(10)

    # Adapter converts SquarePeg -> RoundPeg interface
    small_adapter = SquarePegAdapter(small_square)
    large_adapter = SquarePegAdapter(large_square)

    print("Small square peg fits:", hole.fits(small_adapter))
    print("Large square peg fits:", hole.fits(large_adapter))
