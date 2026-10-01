"""
Bidirectional Adapter Pattern: Two-Way Coordinate System Integration.

Design goal:
Provide transparent interoperability between Cartesian and Polar coordinate
systems in two-dimensional space without tight coupling between their concrete
implementations, using degree-based angular representations.

Key decisions:
- Abstract both coordinate systems into explicit target interfaces.
- Express all polar angular components strictly in degrees (0 to 360).
- Define a unified TwoWayPointAdapter that implements both CartesianPointInterface
  and PolarPointInterface simultaneously, maintaining an internal representation
  and adapting queries and translations dynamically.
- Vectors in either coordinate system are adapted to a shared translation contract
  to support arbitrary point-vector translation combinations.

When justified:
- When a system integrates two independent subsystems with incompatible contracts
  where entities must be treated as either contract interchangeably.

When unnecessary:
- When only one-way translation is required, or when an internal canonical coordinate
  system can be enforced across all subsystems.

Trade-offs:
- Pros: True bidirectional interoperability; clients expecting either interface can
  interact with the same adapted object seamlessly.
- Cons: Increases interface surface area; requires maintaining consistency across
  both representations upon state mutation.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass


# Target Interface
class VectorInterface(ABC):
    """
    Common contract for 2D displacement vectors.

    Design goal:
    Provide uniform displacement deltas regardless of the coordinate system
    used to define the vector.
    """

    @abstractmethod
    def to_cartesian_deltas(self) -> tuple[float, float]:
        """Return displacement as Cartesian deltas (dx, dy)."""
        raise NotImplementedError

    @abstractmethod
    def to_polar_deltas(self) -> tuple[float, float]:
        """Return displacement as Polar deltas (magnitude, angle_deg)."""
        raise NotImplementedError


# Adaptee / Concrete Implementation
@dataclass(frozen=True, slots=True)
class CartesianVector(VectorInterface):
    """
    Displacement vector expressed in Cartesian coordinates.

    Trade-offs:
    - Pros: Direct mapping for grid-based transformations.
    - Cons: Polar delta conversion incurs trigonometric computation overhead.
    """

    dx: float
    dy: float

    def to_cartesian_deltas(self) -> tuple[float, float]:
        return self.dx, self.dy

    def to_polar_deltas(self) -> tuple[float, float]:
        magnitude = math.hypot(self.dx, self.dy)
        angle_deg = math.degrees(math.atan2(self.dy, self.dx))
        return magnitude, angle_deg


# Adaptee / Concrete Implementation
@dataclass(frozen=True, slots=True)
class PolarVector(VectorInterface):
    """
    Displacement vector expressed in Polar coordinates with angle in degrees.

    Trade-offs:
    - Pros: Natural representation for directional movement and speed in degrees.
    - Cons: Cartesian delta conversion incurs trigonometric computation overhead.
    """

    magnitude: float
    angle_deg: float

    def to_cartesian_deltas(self) -> tuple[float, float]:
        rad = math.radians(self.angle_deg)
        dx = self.magnitude * math.cos(rad)
        dy = self.magnitude * math.sin(rad)
        return dx, dy

    def to_polar_deltas(self) -> tuple[float, float]:
        return self.magnitude, self.angle_deg


# Target Interface
class CartesianPointInterface(ABC):
    """
    Target contract for 2D points in a Cartesian coordinate system.

    Design goal:
    Expose standard Cartesian coordinates and Cartesian-oriented translation.
    """

    @abstractmethod
    def get_x(self) -> float:
        """Return the horizontal coordinate."""
        raise NotImplementedError

    @abstractmethod
    def get_y(self) -> float:
        """Return the vertical coordinate."""
        raise NotImplementedError

    @abstractmethod
    def translate_cartesian(self, vector: VectorInterface) -> None:
        """Apply a translation vector to the point."""
        raise NotImplementedError


# Target Interface
class PolarPointInterface(ABC):
    """
    Target contract for 2D points in a Polar coordinate system with angle in degrees.

    Design goal:
    Expose standard Polar coordinates and Polar-oriented translation.
    """

    @abstractmethod
    def get_radius(self) -> float:
        """Return the radial distance from origin."""
        raise NotImplementedError

    @abstractmethod
    def get_angle_deg(self) -> float:
        """Return the angular position in degrees."""
        raise NotImplementedError

    @abstractmethod
    def translate_polar(self, vector: VectorInterface) -> None:
        """Apply a translation vector to the point."""
        raise NotImplementedError


# Adaptee / Concrete Implementation
class CartesianPoint(CartesianPointInterface):
    """
    Concrete Cartesian point representation.

    Design goal:
    Encapsulate point manipulation strictly within Cartesian space.
    """

    def __init__(self, x: float, y: float) -> None:
        self._x = float(x)
        self._y = float(y)

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def translate_cartesian(self, vector: VectorInterface) -> None:
        dx, dy = vector.to_cartesian_deltas()
        self._x += dx
        self._y += dy

    def __repr__(self) -> str:
        return f"CartesianPoint(x={self._x:.4f}, y={self._y:.4f})"


# Adaptee / Concrete Implementation
class PolarPoint(PolarPointInterface):
    """
    Concrete Polar point representation using degrees.

    Design goal:
    Encapsulate point manipulation strictly within Polar space.
    """

    def __init__(self, radius: float, angle_deg: float) -> None:
        self._radius = float(radius)
        self._angle_deg = float(angle_deg)

    def get_radius(self) -> float:
        return self._radius

    def get_angle_deg(self) -> float:
        return self._angle_deg

    def translate_polar(self, vector: VectorInterface) -> None:
        current_rad = math.radians(self._angle_deg)
        current_x = self._radius * math.cos(current_rad)
        current_y = self._radius * math.sin(current_rad)

        dx, dy = vector.to_cartesian_deltas()
        new_x = current_x + dx
        new_y = current_y + dy

        self._radius = math.hypot(new_x, new_y)
        self._angle_deg = math.degrees(math.atan2(new_y, new_x))

    def __repr__(self) -> str:
        return f"PolarPoint(radius={self._radius:.4f}, angle_deg={self._angle_deg:.4f})"


# Two-Way Adapter
class TwoWayPointAdapter(CartesianPointInterface, PolarPointInterface):
    """
    Two-Way Adapter bridging Cartesian and Polar coordinate contracts.

    Design goal:
    Provide an adapter that satisfies both CartesianPointInterface and
    PolarPointInterface simultaneously, enabling either coordinate client to
    interact with the same entity without knowing its underlying representation.

    Key decisions:
    - Maintain canonical Cartesian coordinates internally to avoid continuous
      precision degradation during repeated mutations.
    - Express all polar output angles in degrees.
    - Expose factory constructors to adapt existing points transparently.

    Trade-offs:
    - Pros: Complete interchangeability across distinct client systems.
    - Cons: Polar read queries compute trigonometry on demand.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self._x = float(x)
        self._y = float(y)

    @classmethod
    def from_cartesian(cls, point: CartesianPointInterface) -> TwoWayPointAdapter:
        """Factory constructor adapting an existing Cartesian point."""
        return cls(x=point.get_x(), y=point.get_y())

    @classmethod
    def from_polar(cls, point: PolarPointInterface) -> TwoWayPointAdapter:
        """Factory constructor adapting an existing Polar point."""
        radius = point.get_radius()
        rad = math.radians(point.get_angle_deg())
        x = radius * math.cos(rad)
        y = radius * math.sin(rad)
        return cls(x=x, y=y)

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_radius(self) -> float:
        return math.hypot(self._x, self._y)

    def get_angle_deg(self) -> float:
        return math.degrees(math.atan2(self._y, self._x))

    def translate_cartesian(self, vector: VectorInterface) -> None:
        dx, dy = vector.to_cartesian_deltas()
        self._x += dx
        self._y += dy

    def translate_polar(self, vector: VectorInterface) -> None:
        dx, dy = vector.to_cartesian_deltas()
        self._x += dx
        self._y += dy

    def __repr__(self) -> str:
        return (
            f"TwoWayPointAdapter(x={self._x:.4f}, y={self._y:.4f}, "
            f"radius={self.get_radius():.4f}, angle_deg={self.get_angle_deg():.4f})"
        )


def run_cartesian_client(point: CartesianPointInterface, vector: VectorInterface) -> None:
    """Execute operations strictly via Cartesian interface."""
    point.translate_cartesian(vector)


def run_polar_client(point: PolarPointInterface, vector: VectorInterface) -> None:
    """Execute operations strictly via Polar interface."""
    point.translate_polar(vector)


if __name__ == "__main__":
    tolerance = 1e-6

    # Verify Cartesian point translation using both vector representations
    cart_point = CartesianPoint(x=3.0, y=4.0)
    cart_point.translate_cartesian(CartesianVector(dx=1.0, dy=-1.0))
    assert math.isclose(cart_point.get_x(), 4.0, abs_tol=tolerance)
    assert math.isclose(cart_point.get_y(), 3.0, abs_tol=tolerance)

    polar_vector = PolarVector(magnitude=5.0, angle_deg=0.0)
    cart_point.translate_cartesian(polar_vector)
    assert math.isclose(cart_point.get_x(), 9.0, abs_tol=tolerance)
    assert math.isclose(cart_point.get_y(), 3.0, abs_tol=tolerance)

    # Verify Polar point translation using both vector representations
    polar_point = PolarPoint(radius=5.0, angle_deg=0.0)
    polar_point.translate_polar(CartesianVector(dx=0.0, dy=5.0))
    assert math.isclose(polar_point.get_radius(), math.hypot(5.0, 5.0), abs_tol=tolerance)
    assert math.isclose(polar_point.get_angle_deg(), 45.0, abs_tol=tolerance)

    # Verify Two-Way Adapter operating transparently across both client contracts
    two_way = TwoWayPointAdapter.from_cartesian(CartesianPoint(x=0.0, y=0.0))

    # Apply a polar movement of 10 units at 90 degrees (along positive y-axis)
    run_cartesian_client(two_way, PolarVector(magnitude=10.0, angle_deg=90.0))
    assert math.isclose(two_way.get_x(), 0.0, abs_tol=tolerance)
    assert math.isclose(two_way.get_y(), 10.0, abs_tol=tolerance)
    assert math.isclose(two_way.get_radius(), 10.0, abs_tol=tolerance)
    assert math.isclose(two_way.get_angle_deg(), 90.0, abs_tol=tolerance)

    # Apply a cartesian movement of dx=10, dy=-10 (returning to x=10, y=0)
    run_polar_client(two_way, CartesianVector(dx=10.0, dy=-10.0))
    assert math.isclose(two_way.get_x(), 10.0, abs_tol=tolerance)
    assert math.isclose(two_way.get_y(), 0.0, abs_tol=tolerance)
    assert math.isclose(two_way.get_radius(), 10.0, abs_tol=tolerance)
    assert math.isclose(two_way.get_angle_deg(), 0.0, abs_tol=tolerance)

    assert isinstance(two_way, CartesianPointInterface)
    assert isinstance(two_way, PolarPointInterface)
