from .xml.business_plan import BusinessPlan


def create_business_plan_repository(fname: str) -> BusinessPlan:
    """Factory function to create a BusinessPlan repository instance."""
    # Note: The original class was named BusinessPlan, not BusinessPlanRepository
    return BusinessPlan(fname=fname)