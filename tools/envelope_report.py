#!/usr/bin/env python3
"""Command-line tool for generating envelope budget reports."""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from lib.repositories.envelope import create_envelope_repository
from lib.repositories.expense import create_expense_repository
from lib.repositories.business_plan import create_business_plan_repository


def calculate_yearly_totals(expense_repo, envelope_repo, year_filter: int = None) -> dict:
    """Calculate yearly spending/adding totals per envelope.

    Args:
        expense_repo: Expense repository instance
        envelope_repo: Envelope repository instance
        year_filter: Optional year to filter by
    Returns:
        Dictionary of {year: {envelope_id: {'spent': X, 'added': Y}}}
    """
    yearly_totals = {}

    for expense in expense_repo.expenses:
        year = expense.date.year
        if year_filter and year != year_filter:
            continue

        if year not in yearly_totals:
            yearly_totals[year] = {}

        # Track spending (fromId)
        from_id = str(expense.from_id)
        if from_id not in yearly_totals[year]:
            yearly_totals[year][from_id] = {'spent': 0.0, 'added': 0.0}
        yearly_totals[year][from_id]['spent'] += expense.value

        # Track additions (toId)
        to_id = str(expense.to_id)
        if to_id not in yearly_totals[year]:
            yearly_totals[year][to_id] = {'spent': 0.0, 'added': 0.0}
        yearly_totals[year][to_id]['added'] += expense.value

    return yearly_totals


def main():
    parser = argparse.ArgumentParser(description='Generate envelope budget reports')
    parser.add_argument('data_dir', help='Path to directory containing data files')
    parser.add_argument('--year', type=int, help='Filter report for specific year')
    args = parser.parse_args()

    data_dir = Path(args.data_dir)

    # Initialize repositories
    expense_repo = create_expense_repository(data_dir / 'expenses.xml')
    envelope_repo = create_envelope_repository(data_dir / 'envelopes.xml')
    envelope_repo.set_expense_repository(expense_repo)
    business_plan_repo = create_business_plan_repository(data_dir / 'business_plan.xml')

    # Calculate yearly totals with optional year filter
    yearly_totals = calculate_yearly_totals(
        expense_repo,
        envelope_repo,
        year_filter=args.year
    )

    # Generate and print report with business plan comparison
    print(generate_report(
        yearly_totals,
        envelope_repo,
        business_plan_repo
    ))


def calculate_planned_values(business_plan_repo) -> dict:
    """Calculate planned yearly values per envelope from business plan items."""
    planned = {}
    if business_plan_repo and business_plan_repo.items:
        for item in business_plan_repo.items:
            if item.name not in planned:
                planned[item.name] = 0.0
            planned[item.name] += item.weekly_value * 52  # Convert weekly to yearly
    return planned

def generate_report(yearly_totals: dict,
                   envelope_repo,
                   business_plan_repo = None) -> str:
    """Format yearly totals with optional business plan comparison.

    Args:
        yearly_totals: Calculated yearly totals
        envelope_repo: Envelope repository
        business_plan_repo: Optional business plan repository for comparison
    """
    report_lines = []
    planned_values = calculate_planned_values(business_plan_repo)

    for year in sorted(yearly_totals.keys()):
        year_total_spent = 0.0
        year_total_added = 0.0
        year_lines = []

        # Header
        report_lines.append(f"\nYear: {year}")
        report_lines.append("-" * 80)
        report_lines.append(
            f"{'Envelope':<20} {'Planned':>15} {'Added':>15} {'Spent':>15} {'Diff':>15}"
        )
        report_lines.append("-" * 80)

        # Envelope rows
        for env_id in yearly_totals[year]:
            try:
                env_name = envelope_repo.envelope_name_for_id(int(env_id))
            except:
                env_name = f"[ID: {env_id}]"

            totals = yearly_totals[year][env_id]
            planned = planned_values.get(env_name, 0.0)
            diff = totals['added'] - totals['spent']

            year_lines.append(
                f"{env_name:<20} {planned:>15.2f} {totals['added']:>15.2f} {totals['spent']:>15.2f} {diff:>15.2f}"
            )

            year_total_spent += totals['spent']
            year_total_added += totals['added']

        # Sort by envelope name
        report_lines.extend(sorted(year_lines))

        # Year totals
        report_lines.append("-" * 80)
        report_lines.append(
            f"{'TOTAL':<20} {'':>15} {year_total_added:>15.2f} {year_total_spent:>15.2f} {year_total_added - year_total_spent:>15.2f}"
        )

        if not planned_values:
            report_lines.append("Note: Business plan data not available or empty")

    return "\n".join(report_lines)


if __name__ == '__main__':
    main()
