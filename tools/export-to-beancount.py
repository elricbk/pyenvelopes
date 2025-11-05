#!/usr/bin/env python3
"""Export envelope data to Beancount format."""

import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Optional

import click

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.repositories.envelope import (
    create_envelope_repository,
    EnvelopeRepository,
)
from lib.repositories.expense import (
    create_expense_repository,
    ExpenseRepository,
)
from lib.models.envelope import Envelope
from lib.models.expense import Expense
from lib.well_known_envelope import WellKnownEnvelope

if TYPE_CHECKING:
    from lib.repositories.envelope import EnvelopeRepository
    from lib.repositories.expense import ExpenseRepository


@dataclass
class ConversionOptions:
    """Options for Beancount conversion."""

    currency: str = "RUB"
    separate_income_leftover: bool = False
    single_expense_account: bool = False
    start_date: Optional[datetime] = None


def sanitize_account_name(name: str) -> str:
    """Sanitize envelope name for use in Beancount account names.

    Transliterates Cyrillic to Latin, replaces emojis with names, removes underscores and capitalizes
    the letter following them.
    """
    # Emoji replacement map
    emoji_map = {
        "💊": "Pill",
        "🚗": "Car",
    }

    # First, replace emojis with their names
    for emoji, replacement in emoji_map.items():
        name = name.replace(emoji, replacement)

    # Transliterate Cyrillic to Latin
    transliteration_map = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "yo",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "sch",
        "ъ": "",
        "ы": "y",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "G",
        "Д": "D",
        "Е": "E",
        "Ё": "Yo",
        "Ж": "Zh",
        "З": "Z",
        "И": "I",
        "Й": "Y",
        "К": "K",
        "Л": "L",
        "М": "M",
        "Н": "N",
        "О": "O",
        "П": "P",
        "Р": "R",
        "С": "S",
        "Т": "T",
        "У": "U",
        "Ф": "F",
        "Х": "H",
        "Ц": "Ts",
        "Ч": "Ch",
        "Ш": "Sh",
        "Щ": "Sch",
        "Ъ": "",
        "Ы": "Y",
        "Ь": "",
        "Э": "E",
        "Ю": "Yu",
        "Я": "Ya",
    }

    result = []
    for char in name:
        result.append(transliteration_map.get(char, char))

    name = "".join(result)

    # Replace spaces with underscores
    name = name.replace(" ", "_")

    # Remove invalid characters for Beancount (excluding emojis since they're already replaced)
    invalid_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
    for char in invalid_chars:
        name = name.replace(char, "")

    # Remove underscores and capitalize the following letter
    parts = name.split("_")
    result_parts = []
    for i, part in enumerate(parts):
        if part:  # Skip empty parts
            # Capitalize first letter of all parts
            result_parts.append(
                part[0].upper() + part[1:] if len(part) > 0 else ""
            )

    return "".join(result_parts)


def is_weekly_envelope(envelope: Envelope) -> bool:
    """Check if envelope is a weekly envelope (format: Week_YYYY_WW)."""
    parts = envelope.name.split("_")
    if len(parts) != 3:
        return False
    if parts[0] != "Week":
        return False
    try:
        int(parts[1])  # year
        int(parts[2])  # week
        return True
    except ValueError:
        return False


def should_skip_transaction(
    expense: Expense,
    envelope_repo: EnvelopeRepository,
    from_name: str,
    to_name: str,
) -> bool:
    """Determine if transaction should be skipped.

    Skip automatic transfers between weekly envelopes.
    """
    from_is_weekly = is_weekly_envelope(
        envelope_repo._envelopes[expense.from_id]
    )
    to_is_weekly = is_weekly_envelope(envelope_repo._envelopes[expense.to_id])

    # Skip automatic transfers between weekly envelopes
    if from_is_weekly and to_is_weekly and not expense.manual:
        return True

    return False


def map_account(
    envelope_id: int,
    envelope_repo: EnvelopeRepository,
    options: ConversionOptions,
    is_source: bool = False,
) -> str:
    """Map envelope ID to Beancount account name.

    Args:
        envelope_id: ID of the envelope
        envelope_repo: Envelope repository
        options: Conversion options
        is_source: Whether this is the source envelope (for expense mapping)

    Returns:
        Beancount account name
    """
    envelope = envelope_repo._envelopes[envelope_id]

    # Handle special envelopes
    if envelope_id == WellKnownEnvelope.Income.value:
        return "Income:General"

    if envelope_id == WellKnownEnvelope.Leftover.value:
        if options.separate_income_leftover:
            return "Income:Leftover"
        else:
            return "Income:General"

    if envelope_id == WellKnownEnvelope.TrashBin.value:
        # This shouldn't be used directly as an account
        return "Expenses:General"

    # Handle weekly envelopes
    if is_weekly_envelope(envelope):
        return "Assets:WeeklyEnvelope"

    # Handle regular envelopes
    safe_name = sanitize_account_name(envelope.name)
    return f"Assets:Envelopes:{safe_name}"


def format_transaction(
    expense: Expense,
    envelope_repo: EnvelopeRepository,
    options: ConversionOptions,
) -> Optional[str]:
    """Format transaction in Beancount format with metadata.

    Returns None if transaction should be skipped.
    """
    from_name = envelope_repo.envelope_name_for_id(expense.from_id)
    to_name = envelope_repo.envelope_name_for_id(expense.to_id)

    # Skip automatic transfers between weekly envelopes
    if should_skip_transaction(expense, envelope_repo, from_name, to_name):
        return None

    from_envelope = envelope_repo._envelopes[expense.from_id]
    to_envelope = envelope_repo._envelopes[expense.to_id]

    # Determine account types
    from_is_trash = expense.from_id == WellKnownEnvelope.TrashBin.value
    to_is_trash = expense.to_id == WellKnownEnvelope.TrashBin.value
    from_is_income = expense.from_id == WellKnownEnvelope.Income.value
    to_is_income = expense.to_id == WellKnownEnvelope.Income.value

    # Build transaction
    date_str = expense.date.strftime("%Y-%m-%d")
    # Escape quotes in description
    escaped_desc = expense.desc.replace('"', '\\"')
    lines = [f'{date_str} * "{escaped_desc}"']

    # Add metadata
    lines.append(f'  uuid: "{expense.id}"')
    lines.append(f'  manual: "{expense.manual}"')
    if expense.line:
        # Escape quotes in line
        escaped_line = expense.line.replace('"', '\\"')
        lines.append(f'  line: "{escaped_line}"')

    # Determine source and target accounts
    if from_is_income or to_is_income:
        # Income transaction
        if from_is_income:
            source_account = map_account(
                expense.from_id, envelope_repo, options, is_source=True
            )
            target_account = map_account(
                expense.to_id, envelope_repo, options, is_source=False
            )
        else:
            source_account = map_account(
                expense.from_id, envelope_repo, options, is_source=True
            )
            target_account = map_account(
                expense.to_id, envelope_repo, options, is_source=False
            )
    elif from_is_trash or to_is_trash:
        # Expense transaction
        if from_is_trash:
            # Money going to trash (shouldn't happen normally)
            source_account = map_account(
                expense.from_id, envelope_repo, options, is_source=True
            )
            target_account = map_account(
                expense.to_id, envelope_repo, options, is_source=False
            )
        else:
            # Money from envelope to trash
            source_account = map_account(
                expense.from_id, envelope_repo, options, is_source=True
            )
            if options.single_expense_account:
                target_account = "Expenses:General"
            else:
                # Check if source is weekly envelope
                from_envelope = envelope_repo._envelopes[expense.from_id]
                if is_weekly_envelope(from_envelope):
                    target_account = "Expenses:Weekly"
                else:
                    # Use source envelope name for expense account
                    safe_name = sanitize_account_name(from_name)
                    target_account = f"Expenses:{safe_name}"
    else:
        # Regular transfer between envelopes
        source_account = map_account(
            expense.from_id, envelope_repo, options, is_source=True
        )
        target_account = map_account(
            expense.to_id, envelope_repo, options, is_source=False
        )

    # Special handling: if source is weekly and target is trash, use Expenses:Weekly
    from_is_weekly = is_weekly_envelope(
        envelope_repo._envelopes[expense.from_id]
    )
    if from_is_weekly and expense.to_id == WellKnownEnvelope.TrashBin.value:
        target_account = "Expenses:Weekly"

    # Add postings
    lines.append(
        f"  {source_account:<40} {-expense.value:>12.2f} {options.currency}"
    )
    lines.append(
        f"  {target_account:<40} {expense.value:>12.2f} {options.currency}"
    )

    return "\n".join(lines)


def get_all_accounts(
    envelope_repo: EnvelopeRepository,
    expense_repo: ExpenseRepository,
    options: ConversionOptions,
) -> set[str]:
    """Get all unique accounts used in transactions."""
    accounts = set()

    # Add special accounts
    accounts.add("Income:General")
    if options.separate_income_leftover:
        accounts.add("Income:Leftover")

    # Add envelope accounts
    for envelope in envelope_repo._envelopes.values():
        if is_weekly_envelope(envelope):
            accounts.add("Assets:WeeklyEnvelope")
        elif envelope.id not in [
            WellKnownEnvelope.Income.value,
            WellKnownEnvelope.TrashBin.value,
            WellKnownEnvelope.Leftover.value,
        ]:
            safe_name = sanitize_account_name(envelope.name)
            accounts.add(f"Assets:Envelopes:{safe_name}")

    # Add expense accounts
    # Always add Expenses:General as it's used for various transactions
    accounts.add("Expenses:General")

    if not options.single_expense_account:
        # Collect all expense accounts from transactions
        for expense in expense_repo.expenses:
            if expense.to_id == WellKnownEnvelope.TrashBin.value:
                from_name = envelope_repo.envelope_name_for_id(expense.from_id)
                # Check if it's a weekly envelope
                from_envelope = envelope_repo._envelopes[expense.from_id]
                if is_weekly_envelope(from_envelope):
                    accounts.add("Expenses:Weekly")
                else:
                    safe_name = sanitize_account_name(from_name)
                    accounts.add(f"Expenses:{safe_name}")
            elif expense.from_id == WellKnownEnvelope.TrashBin.value:
                to_name = envelope_repo.envelope_name_for_id(expense.to_id)
                safe_name = sanitize_account_name(to_name)
                accounts.add(f"Expenses:{safe_name}")

    # Add weekly expense account if needed
    for expense in expense_repo.expenses:
        from_is_weekly = is_weekly_envelope(
            envelope_repo._envelopes[expense.from_id]
        )
        if from_is_weekly and expense.to_id == WellKnownEnvelope.TrashBin.value:
            accounts.add("Expenses:Weekly")
            break

    return accounts


def find_last_transaction_date(
    envelope_id: int, expense_repo: ExpenseRepository
) -> Optional[datetime]:
    """Find the date of the last transaction for an envelope."""
    last_date = None
    for expense in expense_repo.expenses:
        if expense.from_id == envelope_id or expense.to_id == envelope_id:
            if last_date is None or expense.date > last_date:
                last_date = expense.date
    return last_date


def generate_beancount_file(
    envelope_repo: EnvelopeRepository,
    expense_repo: ExpenseRepository,
    options: ConversionOptions,
) -> str:
    """Generate complete Beancount file content."""
    lines = []

    # Find the earliest transaction date
    earliest_date = None
    for expense in expense_repo.expenses:
        if earliest_date is None or expense.date < earliest_date:
            earliest_date = expense.date

    # Use one year before earliest transaction, or 2010 if no transactions
    if earliest_date:
        open_date = (earliest_date - timedelta(days=365)).strftime("%Y-%m-%d")
    else:
        open_date = "2010-01-01"

    # Header
    lines.append("; Generated from pyenvelopes data")
    lines.append(
        f"; Export date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    lines.append("")
    lines.append('option "title" "PyEnvelopes Export"')
    lines.append(f'option "operating_currency" "{options.currency}"')
    lines.append("")

    # Account declarations with metadata
    lines.append("; Account declarations")
    accounts = get_all_accounts(envelope_repo, expense_repo, options)

    # Build mapping of sanitized names to original names for metadata
    name_mapping = {}
    for envelope in envelope_repo._envelopes.values():
        if not is_weekly_envelope(envelope):
            safe_name = sanitize_account_name(envelope.name)
            if envelope.id not in [
                WellKnownEnvelope.Income.value,
                WellKnownEnvelope.TrashBin.value,
                WellKnownEnvelope.Leftover.value,
            ]:
                name_mapping[f"Assets:Envelopes:{safe_name}"] = envelope.name

    for account in sorted(accounts):
        # Add metadata with original name if available
        if account in name_mapping:
            original_name = name_mapping[account]
            # Escape quotes in original name
            escaped_name = original_name.replace('"', '\\"')
            lines.append(f"{open_date} open {account}")
            lines.append(f'  original_name: "{escaped_name}"')
        else:
            lines.append(f"{open_date} open {account}")
    lines.append("")

    # Transactions
    lines.append("; Transactions")
    transactions = []
    for expense in expense_repo.expenses:
        if options.start_date and expense.date < options.start_date:
            continue

        formatted = format_transaction(expense, envelope_repo, options)
        if formatted:
            transactions.append((expense.date, formatted))

    # Sort by date
    transactions.sort(key=lambda x: x[0])
    for _, formatted in transactions:
        lines.append(formatted)
        lines.append("")

    # Archived accounts (close directives)
    lines.append("; Archived accounts")
    for envelope in envelope_repo._envelopes.values():
        if envelope.archived:
            last_date = find_last_transaction_date(envelope.id, expense_repo)
            # Only close if there were transactions
            if last_date:
                close_date = (last_date + timedelta(days=1)).strftime(
                    "%Y-%m-%d"
                )

                safe_name = sanitize_account_name(envelope.name)
                if is_weekly_envelope(envelope):
                    account = "Assets:WeeklyEnvelope"
                else:
                    account = f"Assets:Envelopes:{safe_name}"

                lines.append(f"{close_date} close {account}")

    return "\n".join(lines)


@click.command()
@click.argument(
    "data_dir", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.argument("output_file", type=click.Path())
@click.option(
    "--start-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Filter transactions from this date onwards",
)
@click.option(
    "--separate-income-leftover",
    is_flag=True,
    help="Separate Income and Leftover into different accounts",
)
@click.option(
    "--single-expense-account",
    is_flag=True,
    help="Use single Expenses:General account instead of per-envelope accounts",
)
def main(
    data_dir: str,
    output_file: str,
    start_date: Optional[datetime],
    separate_income_leftover: bool,
    single_expense_account: bool,
) -> None:
    """Export pyenvelopes data to Beancount format.

    DATA_DIR: Directory containing envelopes.xml and expenses.xml
    OUTPUT_FILE: Path to output .beancount file
    """
    data_path = Path(data_dir)

    # Load repositories
    envelope_repo = create_envelope_repository(str(data_path / "envelopes.xml"))
    expense_repo = create_expense_repository(str(data_path / "expenses.xml"))
    envelope_repo.set_expense_repository(expense_repo)

    # Create options
    options = ConversionOptions(
        currency="RUB",
        separate_income_leftover=separate_income_leftover,
        single_expense_account=single_expense_account,
        start_date=start_date,
    )

    # Generate Beancount file
    content = generate_beancount_file(envelope_repo, expense_repo, options)

    # Write output
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    click.echo(f"✓ Exported to {output_file}")
    click.echo(
        f"  Transactions: {len([e for e in expense_repo.expenses if not (options.start_date and e.date < options.start_date)])}"
    )
    click.echo(
        f"  Accounts: {len(get_all_accounts(envelope_repo, expense_repo, options))}"
    )


if __name__ == "__main__":
    main()
