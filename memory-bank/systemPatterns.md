# System Patterns *Optional*

This file documents recurring patterns and standards used in the project.
It is optional, but recommended to be updated as the project evolves.
2025-03-31 01:25:52 - Log of updates made.

* 2025-04-01 00:10:00 - Updated persistence patterns to reflect separation of concerns

## Coding Patterns

*   **PySide6 Signals/Slots:** Used for event handling between UI elements and the `MainForm` controller logic (e.g., `@Slot()` decorators).
*   **Helper Functions:** Utility functions exist for formatting data for display (e.g., `item_type_to_str`, `frequency_to_str` in `MainForm.py`, `formatValue`, `unwrap` in `lib/utils.py`).
*   **Enum/Match:** Python `enum` (like `ItemType`, `Frequency`) and `match` statements are used for handling discrete sets of values.
*   **Logging:** Standard Python `logging` module used for application logging, configured in `EnvelopesApp.py`.
*   **Data Classes:** Python `@dataclass` is used for defining data model objects (e.g., `Expense` in `lib/models/expense.py`).
*   **UUIDs:** `uuid.uuid4` is used for generating unique IDs for data model instances.
*   **Date Handling:** `datetime` module and `dateutil.parser` are used for date/time operations and parsing from strings.
*   **Regex Input Parsing:** The `re` module and multiple regex patterns are used in `lib/parse_expense.py` to parse user-provided strings into structured `ParsedExpense` objects, handling different input formats.
*   **UUIDs:** `uuid.uuid4` is used for generating unique IDs for data model instances.
*   **Date Handling:** `datetime` module and `dateutil.parser` are used for date/time operations and parsing from strings.
*   **Regex Input Parsing:** The `re` module and multiple regex patterns are used in `lib/parse_expense.py` to parse user-provided strings into structured `ParsedExpense` objects, handling different input formats.
*   **Internationalization (i18n):** UI strings use `QCoreApplication.translate` (seen in `ui_MainForm.py`), enabling potential translation.
*   **UI Helper Modules:** Dedicated modules exist for UI-related utilities (e.g., `lib/controls/pastel_colors.py` for generating consistent colors).
*   **Timestamp:** [2025-03-31 12:02:00] - Added UI helper module pattern.
*   **Timestamp:** [2025-03-31 12:00:00] - Added UI generation and i18n patterns.
*   **Timestamp:** [2025-03-31 11:59:30] - Added pattern for regex-based input parsing.
*   **Timestamp:** [2025-03-31 11:59:00] - Added patterns observed in model classes (`expense.py`).
*   **Timestamp:** [2025-03-31 01:48:00] - Identified basic coding patterns from MainForm.py analysis.

## Architectural Patterns

*   **MVC-like Structure:**
    *   **View:** Defined visually with Qt Designer (`.ui` file), compiled to `ui_MainForm.py`. Uses standard PySide6 widgets and custom controls (`lib/controls/`). The `MainForm` class acts as the window containing the UI defined by `Ui_MainWindow`.
    *   **Controller:** `MainForm.py` handles UI events (via signals/slots connected in `setupUi`), orchestrates data flow, and contains core business logic.
    *   **Model:** Data structures defined in `lib/models/`.
    *   **Persistence:** Handled by repositories (`lib/repositories/`).
*   **UI Generation:** Qt Designer (`.ui`) + `pyside6-uic` generates the Python UI code (`ui_MainForm.py`).
*   **Custom UI Controls:** Reusable custom widgets are developed in `lib/controls/` (e.g., `AutoCompleteEdit`, `ExpenseTreeWidget`). These often inherit from standard PySide6 widgets, utilize composition (like `QCompleter`), implement custom models (`QAbstractListModel`), override event handlers (`keyPressEvent`), and may use custom item delegates (`QStyledItemDelegate`) or override drawing methods (`drawRow` with `QPainter`) for highly customized appearance and behavior. They are integrated into the `.ui` design or instantiated directly in code.
*   **Repository Pattern:** Data access is encapsulated in repository classes (`ExpenseRepository`, `EnvelopeRepository`, etc.), isolating XML persistence logic.
*   **Implicit Dependency Injection:** Repositories are created in `MainForm` and dependencies (like `ExpenseRepository` into `EnvelopeRepository`, or `idToName` function into `ExpenseTreeWidget`) are set manually via methods.
*   **Clean Domain Models:** Models contain only business logic and data, with no knowledge of persistence mechanisms.
*   **Timer-Based Events:** A `QTimerEvent` in `MainForm` triggers periodic actions (`_apply_rules_automatically`).
*   **Timestamp:** [2025-03-31 12:02:00] - Refined Custom UI Controls and Dependency Injection descriptions based on `ExpenseTreeWidget`.
*   **Timestamp:** [2025-03-31 12:00:00] - Updated View description and added UI generation/custom control patterns.
*   **Timestamp:** [2025-03-31 01:48:00] - Identified architectural patterns from MainForm.py analysis.

## Testing Patterns

*   **Framework:** `pytest` is used for test execution and assertions.
*   **Structure:** Tests are organized as functions within files in the `tests/` directory (e.g., `test_parse_expense.py`). Test functions follow the `test_` naming convention.
*   **Assertions:** Standard `assert` statements are used for verification. `pytest.raises` is used for testing expected exceptions.
*   **Focus:** Primarily unit tests focusing on specific functions or classes (e.g., testing `parse_expense` logic).
*   **Timestamp:** [2025-03-31 12:03:00] - Identified testing patterns based on `test_parse_expense.py`.
*   **Timestamp:** [2025-03-31 01:48:00] - Noted existence of a `tests/` directory.

## Data Persistence Patterns

*   **XML Structure:** Data is persisted in XML files located in the data directory specified at runtime. Each file corresponds to a repository class in `lib/repositories/`.
    *   **`expenses.xml`**: `<Expenses><Expense id="..." date="..." value="..." desc="..." fromId="..." toId="..." line="..." manual="..."/></Expenses>`
    *   **`envelopes.xml`**: `<Envelopes><Envelope id="..." name="..." desc="..."/></Envelopes>`
    *   **`rules.xml`**: `<ExpenseRules><ExpenseRule id="..." amount="..." fromId="..." toId="..."/></ExpenseRules>`
    *   **`business_plan.xml`**: `<BusinessPlan><Item id="..." type="..." amount="..." name="..." freq="..."/></BusinessPlan>`
    *   **`rules_applied.xml`**: `<RulesApplied><Item weekId="..."/></RulesApplied>`
*   **Handling:** Repositories use `lxml` (`etree.parse`, `lxml.builder.E`) for parsing and writing XML.
*   **Model Serialization:** Model classes (`lib/models/`) define static `from_xml(element)` and instance `to_xml()` methods for conversion between objects and XML elements.
*   **Safe Save:** Repositories write changes to a temporary file (`.temp` suffix) and then use `shutil.move` to replace the original file, ensuring atomicity and preventing data loss on write errors.
*   **Conversion Functions:** Standalone functions in repositories handle conversion between models and XML (e.g., `expense_to_xml`, `xml_to_expense`).
*   **Separation of Concerns:** Models are completely decoupled from persistence logic, making it easier to change storage implementations.
*   **Timestamp:** [2025-03-31 01:57:00] - Refined persistence patterns based on `ExpenseRepository` analysis.
*   **Timestamp:** [2025-03-31 01:34:48] - Documented initial XML data structures.