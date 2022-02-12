from model_mommy.recipe import Recipe

from carbon_usage.models import Usage, UsageTypes

base_usage = Recipe(Usage)
base_usage_types = Recipe(UsageTypes)
