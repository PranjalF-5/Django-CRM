from django.contrib import admin
from .models import Model1, Subject, Model2


class SubjectInline(admin.TabularInline):
    """
    Inline display for subjects within a branch.
    """
    model = Subject
    extra = 1  # Show one empty row by default for adding a new subject


@admin.register(Model1)
class Model1Admin(admin.ModelAdmin):
    """
    Admin panel configuration for Model1 (Branches).
    """
    list_display = ('name', 'type', 'date_added')  # Fields to display in the admin list view
    list_filter = ('type', 'date_added')  # Add filters in the admin panel
    search_fields = ('name', 'type')  # Add a search box for name and type
    inlines = [SubjectInline]  # Add inline editing for subjects


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Subject.
    """
    list_display = ('name', 'branch')  # Fields to display in the admin list view
    list_filter = ('branch',)  # Add a filter for branches
    search_fields = ('name', 'branch__name')  # Search by subject or branch name


@admin.register(Model2)
class Model2Admin(admin.ModelAdmin):
    """
    Admin panel configuration for Model2 (User-Subject relationship).
    """
    list_display = ('user', 'subject')  # Fields to display in the admin list view
    list_filter = ('subject', 'user')  # Add filters for users and subjects
    search_fields = ('user__username', 'subject__name')  # Search by username or subject name
