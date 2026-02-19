#!/usr/bin/env python
"""
Simple script to test FlowDesk API endpoints.

Usage:
    python test_api.py

Make sure the Django server is running first:
    python manage.py runserver
"""

import json
import requests

BASE_URL = "http://localhost:8000"

# Step 1: Get JWT token
def get_token(username, password):
    """Obtain JWT access token."""
    url = f"{BASE_URL}/api/v1/accounts/token/"
    response = requests.post(url, json={"username": username, "password": password})
    response.raise_for_status()
    data = response.json()
    return data["access"]


# Step 2: Create organization
def create_organization(token, name, slug):
    """Create a new organization."""
    url = f"{BASE_URL}/api/v1/organizations/organizations/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        url, json={"name": name, "slug": slug}, headers=headers
    )
    response.raise_for_status()
    return response.json()


# Step 3: Helper to make org-scoped requests
def org_request(method, endpoint, token, org_slug, **kwargs):
    """Make a request with JWT and organization header."""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Organization-Slug": org_slug,
        "Content-Type": "application/json",
    }
    if "headers" in kwargs:
        headers.update(kwargs.pop("headers"))
    return requests.request(method, url, headers=headers, **kwargs)


def main():
    print("🚀 FlowDesk API Test Script\n")

    # Get credentials
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    try:
        # Step 1: Get JWT
        print("\n1️⃣  Getting JWT token...")
        token = get_token(username, password)
        print(f"   ✅ Token obtained: {token[:20]}...")

        # Step 2: Create organization
        print("\n2️⃣  Creating organization...")
        org_name = input("Organization name (default: Test Org): ").strip() or "Test Org"
        org_slug = input("Organization slug (default: test-org): ").strip() or "test-org"
        org = create_organization(token, org_name, org_slug)
        print(f"   ✅ Created: {org['name']} (slug: {org['slug']})")

        # Step 3: Create a project
        print("\n3️⃣  Creating a project...")
        project_data = {
            "name": "Sample Project",
            "description": "A test project",
            "status": "active",
        }
        response = org_request("POST", "/api/v1/projects/projects/", token, org_slug, json=project_data)
        response.raise_for_status()
        project = response.json()
        print(f"   ✅ Created project: {project['name']} (ID: {project['id']})")

        # Step 4: Create a task
        print("\n4️⃣  Creating a task...")
        task_data = {
            "project": project["id"],
            "title": "Sample Task",
            "description": "A test task",
            "status": "todo",
            "priority": "high",
        }
        response = org_request("POST", "/api/v1/tasks/tasks/", token, org_slug, json=task_data)
        response.raise_for_status()
        task = response.json()
        print(f"   ✅ Created task: {task['title']} (ID: {task['id']})")

        # Step 5: Create an invoice
        print("\n5️⃣  Creating an invoice...")
        from datetime import date
        invoice_data = {
            "client_name": "Test Client",
            "client_email": "client@example.com",
            "issue_date": str(date.today()),
            "due_date": str(date.today()),
            "status": "draft",
        }
        response = org_request("POST", "/api/v1/billing/invoices/", token, org_slug, json=invoice_data)
        response.raise_for_status()
        invoice = response.json()
        print(f"   ✅ Created invoice: {invoice['number']} (ID: {invoice['id']})")

        # Step 6: Get analytics
        print("\n6️⃣  Fetching analytics...")
        response = org_request("GET", "/api/v1/analytics/task-completion-rate/", token, org_slug)
        response.raise_for_status()
        analytics = response.json()
        print(f"   ✅ Task completion rate: {analytics['completion_rate']:.1f}%")

        # Step 7: Check audit logs
        print("\n7️⃣  Checking audit logs...")
        response = org_request("GET", "/api/v1/audit/audit-logs/", token, org_slug)
        response.raise_for_status()
        logs = response.json()
        print(f"   ✅ Found {len(logs.get('results', logs))} audit log entries")

        print("\n✨ All tests passed!")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"   Response: {e.response.text}")
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")


if __name__ == "__main__":
    main()
