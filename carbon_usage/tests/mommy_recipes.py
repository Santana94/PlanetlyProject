from django.contrib.auth.models import User
from model_bakery.recipe import Recipe

from carbon_usage.models import Usage, UsageTypes

base_user = Recipe(User)
base_usage = Recipe(Usage)
base_usage_types = Recipe(UsageTypes)
