from django.urls import path

from .views import (
    ActiveProjectsView,
    RevenuePerMonthView,
    TaskCompletionRateView,
    UserProductivityView,
)


urlpatterns = [
    path("revenue-per-month/", RevenuePerMonthView.as_view(), name="revenue-per-month"),
    path("active-projects/", ActiveProjectsView.as_view(), name="active-projects"),
    path(
        "task-completion-rate/",
        TaskCompletionRateView.as_view(),
        name="task-completion-rate",
    ),
    path(
        "user-productivity/",
        UserProductivityView.as_view(),
        name="user-productivity",
    ),
]
