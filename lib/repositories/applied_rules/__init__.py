from .xml.applied_rules import AppliedRulesRepository


def create_applied_rules_repository(fname: str) -> AppliedRulesRepository:
    """Factory function to create an AppliedRulesRepository instance."""
    return AppliedRulesRepository(fname=fname)