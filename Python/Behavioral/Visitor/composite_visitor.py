"""
Composite + Visitor pattern implementation based on a File System domain.

Purpose & Context:
Demonstrates how the Visitor pattern operates over an arbitrary hierarchical tree
managed by the Composite pattern. Elements (files and directories) remain focused
on representing tree structure and metadata, while operations (calculating total
stats, finding the largest file) are completely decoupled into visitors.

Key Concepts:
- Composite Traversal: Directory instances dispatch accept to themselves first,
  then propagate the visitor down to each child element.
- Open/Closed Principle: Adding a new query or report (e.g. LargestFileVisitor or
  FileSystemStatsVisitor) requires no changes to File or Directory classes.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# Pattern Role: Component / Visitee Interface
class FileSystemItem(ABC):

    def __init__(self, name: str) -> None:
        self.name = name

    # First Dispatch entry point: element accepts the visitor
    @abstractmethod
    def accept(self, visitor: FileSystemVisitor) -> None:
        pass


# Pattern Role: Leaf / Concrete Visitee
class File(FileSystemItem):

    def __init__(self, name: str, size: int) -> None:
        super().__init__(name)
        self.size = size

    # Second Dispatch: binds concrete File type to visitor.visit_file
    def accept(self, visitor: FileSystemVisitor) -> None:
        visitor.visit_file(self)


# Pattern Role: Composite / Concrete Visitee & Branch Traversal Node
class Directory(FileSystemItem):

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._children: list[FileSystemItem] = []

    def add(self, item: FileSystemItem) -> None:
        self._children.append(item)

    def remove(self, item: FileSystemItem) -> None:
        self._children.remove(item)

    @property
    def children(self) -> list[FileSystemItem]:
        return self._children

    # Pre-order composite traversal:
    # 1. Dispatches visitor operation for the current directory itself.
    # 2. Recursively propagates accept call down to all child items.
    def accept(self, visitor: FileSystemVisitor) -> None:
        visitor.visit_directory(self)
        for child in self._children:
            child.accept(visitor)


# Pattern Role: Visitor Interface
class FileSystemVisitor(ABC):

    @abstractmethod
    def visit_file(self, file: File) -> None:
        pass

    @abstractmethod
    def visit_directory(self, directory: Directory) -> None:
        pass


# Pattern Role: Concrete Visitor (Query / Search Operation)
class LargestFileVisitor(FileSystemVisitor):

    def __init__(self) -> None:
        self.largest_file: File | None = None

    # Inspects individual file sizes to track the largest element found
    def visit_file(self, file: File) -> None:
        if self.largest_file is None or file.size > self.largest_file.size:
            self.largest_file = file

    # Directories carry no file payload; no-op for this operation
    def visit_directory(self, directory: Directory) -> None:
        pass


# Pattern Role: Concrete Visitor (Report / Accumulation Operation)
class FileSystemStatsVisitor(FileSystemVisitor):

    def __init__(self) -> None:
        self.total_size: int = 0
        self.file_count: int = 0
        self.directory_count: int = 0

    # Accumulates file count and total byte size
    def visit_file(self, file: File) -> None:
        self.file_count += 1
        self.total_size += file.size

    # Accumulates directory count in the traversal path
    def visit_directory(self, directory: Directory) -> None:
        self.directory_count += 1


# Pattern Role: Client Code
if __name__ == "__main__":

    # Construct the composite tree hierarchy
    root = Directory("root")
    bin_dir = Directory("bin")
    home_dir = Directory("home")
    user_dir = Directory("ehsan")

    root.add(bin_dir)
    root.add(home_dir)
    home_dir.add(user_dir)

    bin_dir.add(File("bash", size=1200))
    bin_dir.add(File("python", size=4500))

    user_dir.add(File("app.py", size=350))
    user_dir.add(File("dataset.csv", size=8900))
    user_dir.add(File("notes.txt", size=80))

    # Execute Stats Visitor operation across the entire tree
    stats_visitor = FileSystemStatsVisitor()
    root.accept(stats_visitor)

    print("File System Statistics:")
    print(f"Total directories: {stats_visitor.directory_count}")
    print(f"Total files: {stats_visitor.file_count}")
    print(f"Total size: {stats_visitor.total_size} KB")

    # Execute Largest File Visitor operation across the entire tree
    largest_visitor = LargestFileVisitor()
    root.accept(largest_visitor)

    if largest_visitor.largest_file:
        print(f"\nLargest file: {largest_visitor.largest_file.name} ({largest_visitor.largest_file.size} KB)")
