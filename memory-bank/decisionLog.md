# Decision Log

This file records architectural and implementation decisions using a list format.
2025-03-31 01:25:47 - Log of updates made.

* 2025-04-01 00:09:00 - Moved XML serialization/deserialization logic from models to repositories
* 2025-04-03 00:17:30 - Removed deprecated add_expense_for_rule method

## Decision

* Separated persistence concerns from domain models
* Moved all XML conversion logic to repository layer
* Updated test locations to match new architecture
* Removed deprecated add_expense_for_rule method from ExpenseRepository
* Consolidated expense creation logic through add_expense method

## Rationale 

* Follows Single Responsibility Principle - models shouldn't know about persistence
* Makes it easier to change storage implementations
* Better separation of concerns
* More maintainable and testable code
* Reduces duplicate code paths for expense creation
* Makes expense creation more explicit at call sites

## Implementation Details

* Created XML conversion functions in repositories
* Removed XML methods from models (where they existed)
* Moved XML-related tests to tests/repositories/
* Kept domain models clean and focused on business logic
* Updated all call sites to use add_expense(Expense) directly
* Removed deprecated add_expense_for_rule method