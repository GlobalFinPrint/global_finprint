from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from django import template
register = template.Library()


@register.simple_tag
def page_link(request, page):
    url = urlparse(request.get_full_path())._asdict()
    query_dict = parse_qs(url['query'])
    query_dict['page'] = page
    url['query'] = urlencode(query_dict, True)
    return urlunparse(url.values())
