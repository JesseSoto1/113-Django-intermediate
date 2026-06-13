from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


# Create your views here.
class SignUpview(CreateView):
    template_name = 'registration/signup.html'
    # form_class attribute allow us to create objects from a form class
    # we use this when we want to have a custom form
    form_class = UserCreationForm
    success_url = reverse_lazy('login')