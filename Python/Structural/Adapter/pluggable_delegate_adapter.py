"""
Evolution of pluggable tree adaptation from subclass hooks to delegate objects.

Design goal:
    Demonstrate how a reusable hierarchy visualizer (TreeDisplay) transitions
    from inheritance-based customization (abstract operations) to object
    composition (delegate objects) when adapting heterogeneous domain models.

Key decisions:
    - Model domain file system entities with explicit interface contracts and
      domain-native APIs, keeping them fully decoupled from presentation concerns.
    - Provide a subclass-driven display requiring specialized subclasses to hook
      into traversal and graphic creation steps.
    - Extract hierarchy navigation and graphical translation into a dedicated
      TreeAccessorDelegateInterface, allowing the display engine to remain closed
      for modification while staying open for arbitrary domain structures.

When justified:
    - Use when a UI engine or core component must display arbitrary hierarchical
      trees without forcing domain objects to inherit from display-specific classes.

When unnecessary:
    - When domain objects already conform natively to the display engine's expected
      node interface or when tree traversal never varies across domain models.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence


class FileSystemEntityInterface(ABC):
    """Abstract base entity representing a component in the storage hierarchy."""

    def __init__(self, name: str) -> None:
        self._name: str = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def get_size_bytes(self) -> int:
        """Calculate and return the size in bytes for this entity."""
        raise NotImplementedError


class FileItem(FileSystemEntityInterface):
    """Concrete leaf entity containing raw file data."""

    def __init__(self, name: str, size_bytes: int) -> None:
        super().__init__(name=name)
        self._size_bytes: int = size_bytes

    def get_size_bytes(self) -> int:
        return self._size_bytes


class Directory(FileSystemEntityInterface):
    """Concrete composite entity containing nested files and sub-directories."""

    def __init__(self, name: str) -> None:
        super().__init__(name=name)
        self._children: list[FileSystemEntityInterface] = []

    def add(self, entity: FileSystemEntityInterface) -> None:
        self._children.append(entity)

    def get_children(self) -> Sequence[FileSystemEntityInterface]:
        return tuple(self._children)

    def get_size_bytes(self) -> int:
        return sum(child.get_size_bytes() for child in self._children)


class GraphicNode:
    """Visual presentation node produced for rendering by the tree display engine."""

    def __init__(self, label: str, is_container: bool) -> None:
        self._label: str = label
        self._is_container: bool = is_container

    @property
    def label(self) -> str:
        return self._label

    @property
    def is_container(self) -> bool:
        return self._is_container

    def render(self, depth: int = 0) -> str:
        prefix = "  " * depth + ("[-] " if self._is_container else "[o] ")
        return f"{prefix}{self._label}"


class SubclassHookTreeDisplay(ABC):
    """
    Tree display engine customized through inheritance and abstract operations.

    Trade-offs:
        - Coupling: The core layout algorithm and domain-adaptation logic are bound
          in the same class hierarchy.
        - Rigidity: To support a new domain hierarchy, a new subclass of this widget
          must be created, causing subclass explosion if the widget itself evolves.
        - Inflexibility: The adaptation strategy cannot be swapped at runtime on an
          existing display instance.
    """

    def display(self, root_entity: object) -> list[str]:
        """Render the tree structure into formatted lines using template operations."""
        lines: list[str] = []
        self._build_tree(node=root_entity, depth=0, accumulator=lines)
        return lines

    def _build_tree(self, node: object, depth: int, accumulator: list[str]) -> None:
        graphic = self.create_graphic_node(node)
        accumulator.append(graphic.render(depth=depth))
        for child in self.get_children_of(node):
            self._build_tree(node=child, depth=depth + 1, accumulator=accumulator)

    @abstractmethod
    def get_children_of(self, node: object) -> Sequence[object]:
        """
        Abstract operation: navigate child entities from the adaptee.

        Forcing subclasses to implement this tightly couples widget inheritance
        with domain navigation details.
        """
        raise NotImplementedError

    @abstractmethod
    def create_graphic_node(self, node: object) -> GraphicNode:
        """
        Abstract operation: map an arbitrary adaptee node into a GraphicNode.
        """
        raise NotImplementedError


class DirectorySubclassTreeDisplay(SubclassHookTreeDisplay):
    """Specialized display subclass adapting FileSystemEntityInterface via inheritance."""

    def get_children_of(self, node: object) -> Sequence[object]:
        if isinstance(node, Directory):
            return node.get_children()
        return ()

    def create_graphic_node(self, node: object) -> GraphicNode:
        if isinstance(node, Directory):
            return GraphicNode(
                label=f"{node.name}/ ({node.get_size_bytes()} bytes)",
                is_container=True,
            )
        if isinstance(node, FileItem):
            return GraphicNode(
                label=f"{node.name} ({node.get_size_bytes()} bytes)",
                is_container=False,
            )
        raise TypeError(f"Unsupported node type: {type(node).__name__}")


class TreeAccessorDelegateInterface(ABC):
    """
    Accessor contract isolating tree navigation and presentation translation.

    Trade-offs:
        - Favor Composition: Extracts domain-specific structural knowledge out of
          the display widget into a standalone adapter.
        - Single Responsibility: Display widget focuses solely on indentation
          and traversal; the delegate focuses on domain extraction.
    """

    @abstractmethod
    def get_children(self, node: object) -> Sequence[object]:
        """Extract and return child nodes for hierarchy progression."""
        raise NotImplementedError

    @abstractmethod
    def create_graphic_node(self, node: object) -> GraphicNode:
        """Translate the given domain entity into a displayable GraphicNode."""
        raise NotImplementedError


class DelegatedTreeDisplay:
    """
    Reusable tree display engine parameterized by a delegate accessor.

    Unlike SubclassHookTreeDisplay, this class never requires subclassing when
    new domain structures are introduced; it simply receives a different delegate.
    """

    def __init__(self, delegate: TreeAccessorDelegateInterface) -> None:
        self._delegate: TreeAccessorDelegateInterface = delegate

    def set_delegate(self, delegate: TreeAccessorDelegateInterface) -> None:
        """Enable dynamic swapping of the domain adapter at runtime."""
        self._delegate = delegate

    def display(self, root_entity: object) -> list[str]:
        """Render hierarchy using the configured delegate accessor."""
        lines: list[str] = []
        self._build_tree(node=root_entity, depth=0, accumulator=lines)
        return lines

    def _build_tree(self, node: object, depth: int, accumulator: list[str]) -> None:
        graphic = self._delegate.create_graphic_node(node)
        accumulator.append(graphic.render(depth=depth))
        for child in self._delegate.get_children(node):
            self._build_tree(node=child, depth=depth + 1, accumulator=accumulator)


class FileSystemAccessorDelegate(TreeAccessorDelegateInterface):
    """Concrete delegate adapting FileSystemEntity hierarchies for DelegatedTreeDisplay."""

    def get_children(self, node: object) -> Sequence[object]:
        if isinstance(node, Directory):
            return node.get_children()
        return ()

    def create_graphic_node(self, node: object) -> GraphicNode:
        if isinstance(node, Directory):
            return GraphicNode(
                label=f"{node.name}/ ({node.get_size_bytes()} bytes)",
                is_container=True,
            )
        if isinstance(node, FileItem):
            return GraphicNode(
                label=f"{node.name} ({node.get_size_bytes()} bytes)",
                is_container=False,
            )
        raise TypeError(f"Unsupported node type: {type(node).__name__}")


if __name__ == "__main__":
    project_root = Directory("my_project")
    src_dir = Directory("src")
    src_dir.add(FileItem("main.py", 1024))
    src_dir.add(FileItem("utils.py", 512))
    project_root.add(src_dir)
    project_root.add(FileItem("README.md", 256))

    # Verification of Subclass-based Hook display
    subclass_display = DirectorySubclassTreeDisplay()
    rendered_by_subclass = subclass_display.display(project_root)

    # Verification of Delegation-based display
    delegate_adapter = FileSystemAccessorDelegate()
    delegated_display = DelegatedTreeDisplay(delegate=delegate_adapter)
    rendered_by_delegate = delegated_display.display(project_root)

    # Parity verification between both evolution stages
    assert rendered_by_subclass == rendered_by_delegate
    assert len(rendered_by_subclass) == 4
    assert rendered_by_subclass[0] == "[-] my_project/ (1792 bytes)"
    assert rendered_by_subclass[1] == "  [-] src/ (1536 bytes)"
    assert rendered_by_subclass[2] == "    [o] main.py (1024 bytes)"
    assert rendered_by_subclass[3] == "    [o] utils.py (512 bytes)"

    for line in rendered_by_delegate:
        print(line)
