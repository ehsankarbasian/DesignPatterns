# Pythonic Abstract Factory – Quick Reference

## Dataclass + Dependency Injection
Represent the factory as a lightweight dataclass holding references to product classes. The client receives the factory and instantiates the related objects through those references.
<br>**Example:** `multi_platform_ui.py`

## Provider Functions
Define a function that returns a set of related creators or instances. The returned bundle acts as the abstract factory for that product family.
<br>**Example:** `multi_database.py`

## Configuration‑Selected Factory
Select a factory implementation using configuration (environment, settings, or dependency injection container). Each configuration maps to a compatible product family.
<br>**Example:** `multi_storage_logger.py`

## Attribute‑Based Factory Class
Use a simple class whose attributes reference product classes. Methods instantiate them, avoiding heavy inheritance hierarchies while preserving the product family concept.
<br>**Example:** `multi_theme_ui.py`
