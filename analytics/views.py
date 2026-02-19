from datetime import date

from django.db.models import Count, F, Q, Sum
from rest_framework import permissions, response, views

from organizations.permissions import IsOrganizationMember
from billing.models import Invoice
from projects.models import Project
from tasks.models import Task


class RevenuePerMonthView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]

    def get(self, request, *args, **kwargs):
        org = getattr(request, "organization", None)

        qs = (
            Invoice.objects.filter(organization=org, status__in=[Invoice.STATUS_PENDING, Invoice.STATUS_PAID, Invoice.STATUS_OVERDUE])
            .values(year=F("issue_date__year"), month=F("issue_date__month"))
            .annotate(total=Sum("total_amount"))
            .order_by("year", "month")
        )

        data = [
            {"year": row["year"], "month": row["month"], "total": row["total"] or 0}
            for row in qs
        ]
        return response.Response(data)


class ActiveProjectsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]

    def get(self, request, *args, **kwargs):
        org = getattr(request, "organization", None)
        today = date.today()

        count_active = Project.objects.filter(
            organization=org,
            status__in=[Project.STATUS_ACTIVE, Project.STATUS_PLANNED],
        ).count()
        count_overdue = Project.objects.filter(
            organization=org,
            end_date__lt=today,
            status__in=[Project.STATUS_PLANNED, Project.STATUS_ACTIVE],
        ).count()

        return response.Response(
            {
                "active_projects": count_active,
                "overdue_projects": count_overdue,
            }
        )


class TaskCompletionRateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]

    def get(self, request, *args, **kwargs):
        org = getattr(request, "organization", None)

        total = Task.objects.filter(organization=org).count()
        done = Task.objects.filter(organization=org, status=Task.STATUS_DONE).count()

        rate = (done / total) * 100 if total > 0 else 0.0

        return response.Response(
            {
                "total_tasks": total,
                "completed_tasks": done,
                "completion_rate": rate,
            }
        )


class UserProductivityView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]

    def get(self, request, *args, **kwargs):
        org = getattr(request, "organization", None)

        qs = (
            Task.objects.filter(organization=org, status=Task.STATUS_DONE, assignee__isnull=False)
            .values(user_id=F("assignee"))
            .annotate(completed_tasks=Count("id"))
            .order_by("-completed_tasks")
        )

        data = [
            {
                "user_id": row["user_id"],
                "completed_tasks": row["completed_tasks"],
            }
            for row in qs
        ]
        return response.Response(data)

