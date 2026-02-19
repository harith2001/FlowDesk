from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MembershipViewSet, OrganizationViewSet


router = DefaultRouter()
router.register("organizations", OrganizationViewSet, basename="organization")
router.register("memberships", MembershipViewSet, basename="membership")


urlpatterns = [
    path("", include(router.urls)),
]

