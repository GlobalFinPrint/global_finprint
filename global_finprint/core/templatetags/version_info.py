from django import template
from ..version import VersionInfo
register = template.Library()


@register.simple_tag
def release_date():
    return ' '.join(VersionInfo.get_version_info()[VersionInfo.Fields.date].split()[:-1])


@register.simple_tag
def current_version():
    return VersionInfo.get_version_info()[VersionInfo.Fields.git_version].split('-')[0]
