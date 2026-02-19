from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/organizations/", include("organizations.urls")),
    path("api/v1/projects/", include("projects.urls")),
    path("api/v1/tasks/", include("tasks.urls")),
    path("api/v1/billing/", include("billing.urls")),
    path("api/v1/notifications/", include("notifications.urls")),
    path("api/v1/analytics/", include("analytics.urls")),
    path("api/v1/audit/", include("audit.urls")),
]

