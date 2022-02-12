from rest_framework import routers

from carbon_usage.views import UsageViewSet, UsageTypesViewSet

app_name = "carbon-usage"

router = routers.SimpleRouter()
router.register(r'usage', UsageViewSet, basename="usage")
router.register(r'usage_types', UsageTypesViewSet, basename="usage_types")
urlpatterns = router.urls
