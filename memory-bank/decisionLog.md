# Decision Log

This file records architectural and implementation decisions using a list format.
2025-03-31 01:25:47 - Log of updates made.

* 2025-04-01 00:09:00 - Moved XML serialization/deserialization logic from models to repositories

## Decision

* Separated persistence concerns from domain models
* Moved all XML conversion logic to repository layer
* Updated test locations to match new architecture

## Rationale 

* Follows Single Responsibility Principle - models shouldn't know about persistence
* Makes it easier to change storage implementations
* Better separation of concerns
* More maintainable and testable code

## Implementation Details

* Created XML conversion functions in repositories
* Removed XML methods from models (where they existed)
* Moved XML-related tests to tests/repositories/
* Kept domain models clean and focused on business logic