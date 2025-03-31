# Product Context

This file provides a high-level overview of the project and the expected product that will be created. Initially it is based upon projectBrief.md (if provided) and all other available project-related information in the working directory. This file is intended to be updated as the project evolves, and should be used to inform all other modes of the project's goals and context.
2025-03-31 01:25:02 - Log of updates made will be appended as footnotes to the end of this file.

*

## Project Goal

*   A simple desktop application (built with PySide6) for personal expense tracking using the envelope budgeting method.

## Key Features

*   Manages income/expenses via a business plan.
*   Tracks expenses against budget envelopes.
*   Supports automatic fund allocation rules (e.g., weekly transfers between envelopes).
*   Parses user input strings for quick expense entry.
*   Displays data (expenses, envelopes, rules, business plan) in tables/trees within the UI.
*   Handles automatic weekly envelope creation and fund transfers based on rules and the business plan.

## Overall Architecture

*   **UI:** PySide6 (`MainForm.py`, `ui_MainForm.py`). Uses custom controls (`lib/controls/`).
*   **Entry Point:** `EnvelopesApp.py` initializes the application and main window.
*   **Core Logic:** `MainForm.py` orchestrates UI interactions, data loading/saving, and business logic execution (rule application, expense parsing).
*   **Data Models:** Defined in `lib/models/` (e.g., `Envelope`, `Expense`, `BusinessPlanItem`, `ExpenseRule`).
*   **Persistence:** `lib/repositories/` classes manage data storage in separate XML files (e.g., `expenses.xml`, `envelopes.xml`, `rules.xml`, `business_plan.xml`). These files need manual creation initially as per `README.md`.
*   **Dependencies:** Requires `lxml` for XML processing and `PySide6` for the GUI.
*   **Utilities:** Helper functions in `lib/utils.py` and expense parsing logic in `lib/parse_expense.py`.
*   **Notes:** Contains some Russian language strings in the UI and code.

---
*Footnotes:*
*   2025-03-31 01:28:41 - Initial population based on analysis of `README.md`, `EnvelopesApp.py`, and `lib/MainForm.py`.