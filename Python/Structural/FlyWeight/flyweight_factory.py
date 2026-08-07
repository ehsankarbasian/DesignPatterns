from __future__ import annotations

from dataclasses import dataclass


class Canvas:
    """Drawing target."""


# Flyweight: shared state used by many trees.
@dataclass(frozen=True)
class TreeType:
    """Stores intrinsic state shared by multiple trees."""

    name: str
    color: str
    texture: str


    def draw(
        self,
        canvas: Canvas,
        horizontal_position: int,
        vertical_position: int,
    ) -> None:
        
        print(
            f"Drawing {self.color} {self.name} with {self.texture} texture "
            f"at ({horizontal_position}, {vertical_position})"
        )


# Factory: reuses an existing flyweight or creates it once.
class TreeFactory:
    """Prevents duplicate TreeType objects with the same shared state."""

    _tree_types: dict[tuple[str, str, str], TreeType] = {}


    @classmethod
    def get_tree_type(
        cls,
        name: str,
        color: str,
        texture: str,
    ) -> TreeType:
        
        key = (name, color, texture)

        if key not in cls._tree_types:
            cls._tree_types[key] = TreeType(
                name=name,
                color=color,
                texture=texture,
            )

        return cls._tree_types[key]


# Context: unique state of an individual tree.
@dataclass
class Tree:
    """Stores a tree position and references a shared TreeType."""

    horizontal_position: int
    vertical_position: int
    tree_type: TreeType


    def draw(self, canvas: Canvas) -> None:
        self.tree_type.draw(
            canvas=canvas,
            horizontal_position=self.horizontal_position,
            vertical_position=self.vertical_position,
        )


# Client: creates contexts and requests shared flyweights.
class Forest:
    """Stores many trees that reuse shared TreeType objects."""

    def __init__(self) -> None:
        self.trees: list[Tree] = []


    def plant_tree(
        self,
        horizontal_position: int,
        vertical_position: int,
        name: str,
        color: str,
        texture: str,
    ) -> None:
        
        tree_type = TreeFactory.get_tree_type(
            name=name,
            color=color,
            texture=texture,
        )

        self.trees.append(
            Tree(
                horizontal_position=horizontal_position,
                vertical_position=vertical_position,
                tree_type=tree_type,
            )
        )


    def draw(self, canvas: Canvas) -> None:
        for tree in self.trees:
            tree.draw(canvas)


if __name__ == "__main__":
    forest = Forest()
    canvas = Canvas()

    forest.plant_tree(
        horizontal_position=10,
        vertical_position=20,
        name="Oak",
        color="Green",
        texture="Rough",
    )

    forest.plant_tree(
        horizontal_position=30,
        vertical_position=40,
        name="Oak",
        color="Green",
        texture="Rough",
    )

    forest.plant_tree(
        horizontal_position=50,
        vertical_position=60,
        name="Pine",
        color="Dark Green",
        texture="Needle-like",
    )

    forest.draw(canvas)

    print(f"Total trees: {len(forest.trees)}")
    print(f"Total tree types: {len(TreeFactory._tree_types)}")
