# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db.models import Count, Q

from organisations.models import Organisation, Subscription, UserOrganisation
from projects.models import Project


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 0
    show_change_link = True


class SubscriptionInline(admin.StackedInline):
    model = Subscription
    extra = 0
    show_change_link = True
    verbose_name_plural = "Subscription"


class UserOrganisationInline(admin.TabularInline):
    model = UserOrganisation
    extra = 0
    show_change_link = True
    autocomplete_fields = ("user",)
    verbose_name_plural = "Users"


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    inlines = [
        ProjectInline,
        SubscriptionInline,
        UserOrganisationInline,
    ]
    list_display = (
        "id",
        "name",
        "subscription_id",
        "subscription_plan",
        "num_users",
        "num_projects",
        "created_date",
    )
    list_display_links = ("name",)
    list_filter = ("subscription__plan",)
    search_fields = ("id", "name", "subscription__subscription_id", "users__email")

    def get_queryset(self, request):  # pragma: no cover
        return (
            Organisation.objects.select_related("subscription")
            .annotate(
                num_users=Count(
                    "users", distinct=True, filter=Q(users__is_active=True)
                ),
                num_projects=Count(
                    "projects",
                    distinct=True,
                    filter=Q(projects__deleted_at__isnull=True),
                ),
            )
            .all()
        )

    def num_users(self, instance: Organisation) -> int:
        return instance.num_users

    def num_projects(self, instance: Organisation) -> int:
        return instance.num_projects

    def subscription_id(self, instance: Organisation) -> str:
        if instance.subscription and instance.subscription.subscription_id:
            return instance.subscription.subscription_id
        return ""

    def subscription_plan(self, instance: Organisation) -> str:
        if instance.subscription and instance.subscription.plan:
            return instance.subscription.plan
        return ""
