from django.conf.urls import url

from ...bruv.views.benthic_category import BenthicCategoryView

urlpatterns = [
    url(r"habitat/substrate/$", BenthicCategoryView.as_view(), name="ajax_substrate"),
]
