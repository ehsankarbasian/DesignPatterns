# Pythonic Factory Method – Quick Reference

This document lists common **Pythonic implementations of the Factory Method pattern**.  
Instead of heavy inheritance hierarchies, Python implementations often rely on dictionaries, registries, configuration, or class methods.


## Registry Pattern
Maintain a registry (usually a dictionary) mapping identifiers to creators.  
New implementations can register themselves without modifying the factory logic.  
This approach is widely used in plugin systems.
<br>**Example:** `notification_system.py`


## Simple Function Factory
Use a plain function that returns different objects based on an argument. Often implemented with a mapping dictionary instead of conditionals to keep it extensible and readable.
<br>**Example:** `parsers.py`


## Classmethod Factory
Define the factory method directly on the class using `@classmethod`

The class decides which concrete instance should be created based on input parameters.

This approach is useful when object creation logic naturally belongs to the class itself.

**Example:** `doc_render.py`


## Configuration‑Driven Factory
Create objects based on configuration data (dict/JSON/env/settings/...)<br>The factory interprets configuration and instantiates the correct implementation.
<br>**Example:** `payment.py`
