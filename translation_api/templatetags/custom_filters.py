from django import template

register = template.Library()


@register.filter
def total_translated_strings(project, language):
    """Filter to get total translated strings for a project and language."""
    return project.get_total_translated_strings(language)
