from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TreeType:
    name: str
    color: str
    texture: str

    def draw(self, canvas: Canvas, horizontal_position: int, vertical_position: int) -> None:
        canvas.draw_tree(
            name=self.name,
            color=self.color,
            texture=self.texture,
            horizontal_position=horizontal_position,
            vertical_position=vertical_position,
        )


class TreeFactory:
    _tree_types: dict[tuple[str, str, str], TreeType] = {}

    @classmethod
    def get_tree_type(cls, name: str, color: str, texture: str) -> TreeType:
        key = (name, color, texture)

        if key not in cls._tree_types:
            cls._tree_types[key] = TreeType(
                name=name,
                color=color,
                texture=texture,
            )

        return cls._tree_types[key]

    @classmethod
    def total_tree_types(cls) -> int:
        return len(cls._tree_types)


@dataclass
class Tree:
    horizontal_position: int
    vertical_position: int
    tree_type: TreeType

    def draw(self, canvas: Canvas) -> None:
        self.tree_type.draw(
            canvas=canvas,
            horizontal_position=self.horizontal_position,
            vertical_position=self.vertical_position,
        )


class Forest:
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

        tree = Tree(
            horizontal_position=horizontal_position,
            vertical_position=vertical_position,
            tree_type=tree_type,
        )

        self.trees.append(tree)

    def draw(self, canvas: Canvas) -> None:
        for tree in self.trees:
            tree.draw(canvas)

    def total_trees(self) -> int:
        return len(self.trees)


class Canvas:
    def draw_tree(
        self,
        name: str,
        color: str,
        texture: str,
        horizontal_position: int,
        vertical_position: int,
    ) -> None:
        print(
            f"Drawing {color} {name} with {texture} texture "
            f"at ({horizontal_position}, {vertical_position})"
        )


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

    print(f"Total trees: {forest.total_trees()}")
    print(f"Total tree types: {TreeFactory.total_tree_types()}")
