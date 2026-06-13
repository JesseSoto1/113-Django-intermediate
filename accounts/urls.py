from django.urls import path
from .views import SignUpview

urlpatterns = [
    path('signup/', SignUpview.as_view(), name='signup'),
    
]