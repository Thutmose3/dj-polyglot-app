from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class SourceProject(models.Model):
    """Model for SourceProject."""

    name = models.CharField(max_length=500, blank=False, null=False, unique=True)
    default_context = models.CharField(max_length=50000, blank=True, null=True)
    users = models.ManyToManyField(User, blank=True, related_name="source_project_users")
    admins = models.ManyToManyField(User, blank=True, related_name="source_project_admins")

    uuid = models.UUIDField(editable=False, unique=True, null=True, blank=True)
    pageviews = models.PositiveIntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    flagged = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_total_strings(self):
        """Get total strings."""
        return TranslatableString.objects.filter(source_project=self).count()

    def get_total_translated_strings(self, language):
        """Get total translated strings."""
        return TranslatedString.objects.filter(string__source_project=self, language=language).count()


class TranslatableString(models.Model):
    """Model for Brand."""

    source_project = models.ForeignKey(SourceProject, on_delete=models.CASCADE, null=False, blank=False)
    string = models.CharField(max_length=50000, blank=False, null=False)
    context = models.CharField(max_length=50000, blank=True, null=True)

    uuid = models.UUIDField(editable=False, unique=True, null=True, blank=True)
    pageviews = models.PositiveIntegerField(default=0, null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    flagged = models.BooleanField(default=False)

    archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.string)

    def get_absolute_url(self):
        """Get absolute url."""
        return reverse("homepage")

    def get_translated_string(self, language):
        """Get translation."""
        return TranslatedString.objects.get_or_create(string=self, language=language)[0]

    class Meta:
        unique_together = ("source_project", "string", "context")


class TranslatedString(models.Model):
    """Model for Brand."""

    string = models.ForeignKey(TranslatableString, on_delete=models.CASCADE, null=False, blank=False)
    language = models.CharField(max_length=10, blank=False, null=False)

    translated_string = models.CharField(max_length=50000, blank=False, null=False)
    translated_at = models.DateTimeField(null=True, blank=True)
    translated_by_ai = models.BooleanField(default=False)
    translated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="translated_by"
    )
    validated = models.BooleanField(default=False)
    validated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="validated_by"
    )
    validated_at = models.DateTimeField(null=True, blank=True)

    uuid = models.UUIDField(editable=False, unique=True, null=True, blank=True)
    pageviews = models.PositiveIntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    flagged = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.string.string

    class Meta:
        unique_together = ("string", "language")
