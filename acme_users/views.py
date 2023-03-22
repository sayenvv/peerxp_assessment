from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from acme_admin.models import Tickets
from .forms import *
from Acme_Support.decorators import method_decorator_adaptor
import requests
from django.contrib import messages
from Acme_Support.utils_constants import *

# Create your views here.
class UserIndexView(TemplateView):
    '''
    TemplateView is a more powerfullway to use generic views ,
    it is used ti handle one template and here it is index.html
    '''
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(UserIndexView, self).get_context_data(**kwargs)
        context['user'] = get_user_model().objects.get(pk=self.request.session.get('user',None))
        return context

class list_MyTickets(ListView):
    '''
      --initializing form_class and model class and other here------
    '''
    model = Tickets
    render_template = 'tickets/list_mytickets.html'

    @method_decorator_adaptor(permission_required, 'ticket.can_add_ticket')
    def get(self,request):
        queryset = self.get_queryset().filter(created_by__id=request.session.get('user',None))
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        return render(request,self.render_template,locals())


class CreateMyTickets(CreateView):
    model = Tickets
    form_class = CreateTicketsForm
    render_template = 'tickets/create_tickets.html'
    redirect_url = 'my_tickets'
    zendesk_domain = ''
    '''your required api url provide here'''
    url = '%s/api/v2/tickets'%(zendesk_domain)

    def get(self,request):
        forms = self.form_class()
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        return render(request,self.render_template,locals())

    def post(self,request):
        forms = self.form_class(request.POST)
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        if forms.is_valid():
            params = {
                "ticket": {
                    "comment": {
                    "body": "The smoke is very colorful."
                    },
                    "priority": instance.priority,
                    "subject": instance.subject
                }
            }
            '''
            change method from get to post when calling url eith post method
            params that we giving to urls as arguments
            '''
            response = requests.post(url,params=params_)
            if response.status_code == 200:
                messages.success(request,message_constants['ticket_created'])
            return redirect(self.redirect_url)
        return render(request,self.render_template,locals())