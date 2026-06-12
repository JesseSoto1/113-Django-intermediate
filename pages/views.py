from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Jesse'
        context['address'] = '123 Main St'
        return context
    
class AboutPageView(TemplateView):
    template_name = 'about.html'

def contact_me(request):
    return render(request,'contact.html')




def get_contact_info(request):
    contact_info = {
        "name": "John Wilkes Booth",
        "address":"123 Main St" ,
        "telephone": "123-123-1234",
        "email":"osok@gmail.com"
    }

    return render(request, "contact.html", contact_info)