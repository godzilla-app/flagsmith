from datetime import timedelta

import pytest
from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils import timezone
from pytest_django.fixtures import SettingsWrapper
from pytest_mock import MockerFixture
from rest_framework.test import APIClient

from organisations.models import (
    Organisation,
    OrganisationSubscriptionInformationCache,
    Subscription,
)
from sales_dashboard.views import OrganisationList
from users.models import FFAdminUser


@pytest.mark.parametrize(
    "allowed_calls_30d, actual_calls_30d, expected_overage",
    ((1000000, 500000, 0), (1000000, 1100000, 100000), (0, 100000, 100000)),
)
def test_organisation_subscription_get_api_call_overage(
    organisation: Organisation,
    allowed_calls_30d: int,
    actual_calls_30d: int,
    expected_overage: int,
    rf: RequestFactory,
) -> None:
    OrganisationSubscriptionInformationCache.objects.create(
        organisation=organisation,
        allowed_30d_api_calls=allowed_calls_30d,
        api_calls_30d=actual_calls_30d,
    )

    request = rf.get("/sales-dashboard")
    view = OrganisationList()
    view.request = request
    result = view.get_queryset().get(pk=organisation.id)

    assert result.overage == expected_overage


@pytest.mark.freeze_time("2023-01-19T09:09:47.325132+00:00")
def test_get_organisation_info__get_event_list_for_organisation(
    organisation: Organisation,
    superuser_client: APIClient,
    settings: SettingsWrapper,
    mocker: MockerFixture,
) -> None:
    # Given
    settings.INFLUXDB_TOKEN = "AFancyToken"

    url = reverse("sales_dashboard:organisation_info", args=[organisation.id])

    event_list_mock = mocker.patch(
        "sales_dashboard.views.get_event_list_for_organisation"
    )
    event_list_mock.return_value = (
        {"traits": [], "identities": [], "flags": [], "environment-document": []},
        ["label1", "label2"],
    )
    mocker.patch("sales_dashboard.views.get_events_for_organisation")

    # When
    response = superuser_client.get(url)

    # Then
    assert "label1" in str(response.content)
    assert "label2" in str(response.content)
    date_start = timezone.now() - timedelta(days=180)
    event_list_mock.assert_called_once_with(organisation.id, date_start)


def test_list_organisations_search_by_name(
    organisation: Organisation,
    superuser_client: Client,
) -> None:
    # Given
    # use the truncated organisation name to ensure fuzzy search works
    search_term = organisation.name[1:-1]

    url = "%s?search=%s" % (reverse("sales_dashboard:index"), search_term)

    # When
    response = superuser_client.get(url)

    # Then
    assert response.status_code == 200

    assert list(response.context_data["organisation_list"]) == [organisation]


def test_list_organisations_search_by_subscription_id(
    organisation: Organisation,
    chargebee_subscription: Subscription,
    superuser_client: Client,
) -> None:
    # Given
    search_term = chargebee_subscription.subscription_id

    url = "%s?search=%s" % (reverse("sales_dashboard:index"), search_term)

    # When
    response = superuser_client.get(url)

    # Then
    assert response.status_code == 200
    assert list(response.context_data["organisation_list"]) == [organisation]


def test_list_organisations_search_by_user_email(
    organisation: Organisation,
    superuser_client: Client,
    admin_user: FFAdminUser,
) -> None:
    # Given
    search_term = admin_user.email

    url = "%s?search=%s" % (reverse("sales_dashboard:index"), search_term)

    # When
    response = superuser_client.get(url)

    # Then
    assert response.status_code == 200
    assert list(response.context_data["organisation_list"]) == [organisation]


def test_list_organisations_filter_plan(
    organisation: Organisation,
    chargebee_subscription: Subscription,
    superuser_client: Client,
) -> None:
    # Given
    url = "%s?filter_plan=%s" % (
        reverse("sales_dashboard:index"),
        chargebee_subscription.plan,
    )

    # When
    response = superuser_client.get(url)

    # Then
    assert response.status_code == 200
    assert list(response.context_data["organisation_list"]) == [organisation]


def test_list_organisations_fails_if_not_staff(
    organisation: Organisation,
    client: Client,
) -> None:
    # Given
    user = FFAdminUser.objects.create(email="notastaffuser@example.com")
    client.force_login(user)

    url = reverse("sales_dashboard:index")

    # When
    response = client.get(url)

    # Then
    assert response.status_code == 302
    assert response.url == "/admin/login/?next=/sales-dashboard/"


def test_get_email_usage_fails_if_not_staff(
    organisation: Organisation,
    client: Client,
) -> None:
    # Given
    user = FFAdminUser.objects.create(email="notastaffuser@example.com")
    client.force_login(user)

    url = reverse("sales_dashboard:email-usage")

    # When
    response = client.get(url)

    # Then
    assert response.status_code == 302
    assert response.url == "/admin/login/?next=/sales-dashboard/email-usage/"


def test_post_email_usage_fails_if_not_staff(
    organisation: Organisation,
    client: Client,
) -> None:
    # Given
    user = FFAdminUser.objects.create(email="notastaffuser@example.com")
    client.force_login(user)

    url = reverse("sales_dashboard:email-usage")

    # When
    response = client.post(url)

    # Then
    assert response.status_code == 302
    assert response.url == "/admin/login/?next=/sales-dashboard/email-usage/"
