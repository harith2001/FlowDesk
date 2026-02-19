from __future__ import annotations

from typing import Optional

from django.http import HttpRequest

from .models import Organization


class CurrentOrganizationMiddleware:
    """
    Simple multi-tenant middleware.

    For now, it expects an `X-Organization-Slug` header and attaches the
    matching Organization instance to `request.organization`.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        request.organization = self._get_organization_from_request(request)
        return self.get_response(request)

    def _get_organization_from_request(
        self, request: HttpRequest
    ) -> Optional[Organization]:
        slug = request.headers.get("X-Organization-Slug") or request.META.get(
            "HTTP_X_ORGANIZATION_SLUG"
        )
        if not slug:
            return None
        try:
            return Organization.objects.get(slug=slug)
        except Organization.DoesNotExist:
            return None

