from rest_framework import routers

from carbon_usage.views import UsageViewSet, UsageTypesViewSet

router = routers.SimpleRouter()
router.register(r'usage', UsageViewSet)
router.register(r'usage_types', UsageTypesViewSet)
urlpatterns = router.urls
