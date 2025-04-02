# Repository Refactoring Plan

**Goal:** Reorganize the `lib/repositories/` directory to make the current XML-based persistence an implementation detail. Each repository's logic will move into its own package, with XML specifics in a nested `xml` package. Factory functions will be provided to create repository instances.

**Analysis Summary:**
*   `EnvelopeRepository` depends on `ExpenseRepository`.
*   `ExpenseRuleRepository` depends on `ExpenseRepository`.
*   `ExpenseRepository`, `AppliedRulesRepository`, and `BusinessPlan` have no dependencies on other repositories.
*   `MainForm` instantiates all repositories and handles dependency injection.
*   Tests (`test_envelope.py`, `test_expense_rule.py`, `test_expense.py`) likely import directly from `lib.repositories.<module_name>`.

**Refactoring Steps:**

```mermaid
graph TD
    A[Start Refactoring] --> B{For each repository file};
    B -- applied_rules.py --> C1[Create lib/repositories/applied_rules/];
    B -- business_plan.py --> C2[Create lib/repositories/business_plan/];
    B -- envelope.py --> C3[Create lib/repositories/envelope/];
    B -- expense_rule.py --> C4[Create lib/repositories/expense_rule/];
    B -- expense.py --> C5[Create lib/repositories/expense/];

    C1 --> D1[Create lib/repositories/applied_rules/xml/];
    C2 --> D2[Create lib/repositories/business_plan/xml/];
    C3 --> D3[Create lib/repositories/envelope/xml/];
    C4 --> D4[Create lib/repositories/expense_rule/xml/];
    C5 --> D5[Create lib/repositories/expense/xml/];

    D1 --> E1[Move applied_rules.py to xml/applied_rules.py];
    D2 --> E2[Move business_plan.py to xml/business_plan.py];
    D3 --> E3[Move envelope.py to xml/envelope.py];
    D4 --> E4[Move expense_rule.py to xml/expense_rule.py];
    D5 --> E5[Move expense.py to xml/expense.py];

    E1 --> F1[Create __init__.py in applied_rules/];
    E2 --> F2[Create __init__.py in business_plan/];
    E3 --> F3[Create __init__.py in envelope/];
    E4 --> F4[Create __init__.py in expense_rule/];
    E5 --> F5[Create __init__.py in expense/];

    F1 --> G1[Add factory create_applied_rules_repository() to applied_rules/__init__.py];
    F2 --> G2[Add factory create_business_plan_repository() to business_plan/__init__.py];
    F3 --> G3[Add factory create_envelope_repository() to envelope/__init__.py];
    F4 --> G4[Add factory create_expense_rule_repository() to expense_rule/__init__.py];
    F5 --> G5[Add factory create_expense_repository() to expense/__init__.py];

    G1 &amp; G2 &amp; G3 &amp; G4 &amp; G5 --> H[Update internal imports within moved repository files];
    H --> I[Update external imports and instantiation in MainForm.py];
    I --> J[Update imports in test files (test_*.py)];
    J --> K[Remove original repository files from lib/repositories/];
    K --> L[Add __init__.py to lib/repositories/];
    L --> M[End Refactoring];

    style C1 fill:#f9f,stroke:#333,stroke-width:2px
    style C2 fill:#f9f,stroke:#333,stroke-width:2px
    style C3 fill:#f9f,stroke:#333,stroke-width:2px
    style C4 fill:#f9f,stroke:#333,stroke-width:2px
    style C5 fill:#f9f,stroke:#333,stroke-width:2px
    style D1 fill:#f9f,stroke:#333,stroke-width:2px
    style D2 fill:#f9f,stroke:#333,stroke-width:2px
    style D3 fill:#f9f,stroke:#333,stroke-width:2px
    style D4 fill:#f9f,stroke:#333,stroke-width:2px
    style D5 fill:#f9f,stroke:#333,stroke-width:2px
    style E1 fill:#ccf,stroke:#333,stroke-width:2px
    style E2 fill:#ccf,stroke:#333,stroke-width:2px
    style E3 fill:#ccf,stroke:#333,stroke-width:2px
    style E4 fill:#ccf,stroke:#333,stroke-width:2px
    style E5 fill:#ccf,stroke:#333,stroke-width:2px
    style F1 fill:#f9f,stroke:#333,stroke-width:2px
    style F2 fill:#f9f,stroke:#333,stroke-width:2px
    style F3 fill:#f9f,stroke:#333,stroke-width:2px
    style F4 fill:#f9f,stroke:#333,stroke-width:2px
    style F5 fill:#f9f,stroke:#333,stroke-width:2px
    style G1 fill:#ccf,stroke:#333,stroke-width:2px
    style G2 fill:#ccf,stroke:#333,stroke-width:2px
    style G3 fill:#ccf,stroke:#333,stroke-width:2px
    style G4 fill:#ccf,stroke:#333,stroke-width:2px
    style G5 fill:#ccf,stroke:#333,stroke-width:2px
    style H fill:#ccf,stroke:#333,stroke-width:2px
    style I fill:#ccf,stroke:#333,stroke-width:2px
    style J fill:#ccf,stroke:#333,stroke-width:2px
    style K fill:#f9f,stroke:#333,stroke-width:2px
    style L fill:#f9f,stroke:#333,stroke-width:2px
```

**Detailed Implementation Steps (for Code mode):**

1.  **Create Directories & `__init__.py` files:** Create the new directory structure (`lib/repositories/<repo_name>/` and `lib/repositories/<repo_name>/xml/`) and add empty `__init__.py` files to make them Python packages.
2.  **Move & Rename:** Move each original repository file (e.g., `lib/repositories/envelope.py`) into its corresponding `xml` sub-package (e.g., `lib/repositories/envelope/xml/envelope.py`).
3.  **Update Internal Imports:** Modify import statements *within* the moved repository files to use relative imports reflecting the new structure (e.g., `from ..expense.xml.expense import ExpenseRepository`, `from ....models.envelope import Envelope`).
4.  **Create Factory Functions:** Implement the `create_<repo_name>_repository()` functions in each `lib/repositories/<repo_name>/__init__.py`. These functions will import the class from the `xml` sub-package and return an instance.
    ```python
    # Example for lib/repositories/envelope/__init__.py
    from .xml.envelope import EnvelopeRepository

    def create_envelope_repository(*args, **kwargs):
        # Pass any necessary arguments (like data_dir, other repos)
        return EnvelopeRepository(*args, **kwargs)
    ```
5.  **Update External Usage (`MainForm.py`):** Change imports in `lib/MainForm.py` from `from lib.repositories.envelope import EnvelopeRepository` to `from lib.repositories.envelope import create_envelope_repository`. Update the instantiation calls to use the factory functions: `self.envelope_repo = create_envelope_repository(...)`.
6.  **Update Test Imports:** Modify imports in any relevant test files (e.g., in `tests/repositories/`) to use the new factory functions or import paths.
7.  **Cleanup:** Delete the original repository files from `lib/repositories/`. Add an `__init__.py` to `lib/repositories/` itself.