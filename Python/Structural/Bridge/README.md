
# Bridge Pattern (Summary)

## Overview
Bridge pattern separates Abstraction from Implementation using composition.

## Structure
- Abstraction: RemoteControl
- Refined Abstraction: ExtendedRemoteControl
- Implementation: AbstractDevice
- Concrete Implementations: TV, Radio

## Benefits
- Independent evolution of hierarchies
- Avoids class explosion
- Promotes composition over inheritance
