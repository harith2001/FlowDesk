from django.conf import settings
from django.db import models

from core.models import OrganizationScopedModel, TimeStampedModel
from projects.models import Project


class Task(OrganizationScopedModel):
    STATUS_TODO = "todo"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"

    STATUS_CHOICES = [
        (STATUS_TODO, "To Do"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_DONE, "Done"),
    ]

    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_TODO
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM,
    )
    order = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.title


class TaskComment(TimeStampedModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_comments",
    )
    body = models.TextField()


class TaskAttachment(TimeStampedModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    file = models.FileField(upload_to="task_attachments/")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_attachments",
    )

