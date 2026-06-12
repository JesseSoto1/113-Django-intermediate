from django.urls import path
from .views import (
    HomePageView, 
    AboutPageView, 
    contact_me,
    get_contact_info,

)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", get_contact_info, name="contact"),
]
