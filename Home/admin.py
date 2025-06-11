from django.contrib import admin
from .models import (
    HeroSection,
    AboutSection,
    FeatureItem,
    ServiceSection,
    ServiceCard,
    Step,
    Skill,
    Experience,
    ContactInfo,
    Blog,
    ContactMessage,
    Testimonial,
)


# You can customize the admin interface for better usability
class FeatureItemInline(admin.TabularInline):
    model = FeatureItem
    extra = 1  # Number of empty forms to display


class AboutSectionAdmin(admin.ModelAdmin):
    inlines = [FeatureItemInline]


class ServiceCardInline(admin.TabularInline):
    model = ServiceCard
    extra = 1


class ServiceSectionAdmin(admin.ModelAdmin):
    inlines = [ServiceCardInline]


admin.site.register(HeroSection)
admin.site.register(AboutSection, AboutSectionAdmin)
admin.site.register(ServiceSection, ServiceSectionAdmin)
admin.site.register(Step)
admin.site.register(Skill)
admin.site.register(Experience)
admin.site.register(ContactInfo)
admin.site.register(Blog)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "timestamp", "is_read")
    list_filter = ("is_read", "timestamp")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("timestamp",)  # Don't allow timestamp to be edited in admin
    actions = ["mark_as_read", "mark_as_unread"]  # Custom actions

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, "Selected messages marked as read.")

    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, "Selected messages marked as unread.")

    mark_as_unread.short_description = "Mark selected messages as unread"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "company_name",
        "is_approved",
        "rating",
        "submitted_at",
    )
    list_filter = ("is_approved", "rating", "submitted_at")
    search_fields = ("client_name", "company_name", "testimonial_text")
    readonly_fields = ("submitted_at",)
    actions = ["mark_as_approved", "mark_as_pending"]

    # Fields to display in the admin edit form, including image fields
    fields = (
        "client_name",
        "client_title",
        "company_name",
        "client_image",
        "company_logo",  # <-- Add these here
        "linkedin_url",
        "testimonial_text",
        "rating",
        "is_approved",
        "submitted_at",
    )
