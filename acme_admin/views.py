import requests
import json
import os
from dotenv import load_dotenv
from django.contrib.auth.models import Group
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DetailView,DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import permission_required
from Acme_Support.helpers import EmailOrUsernameModelBackend as user
from acme_users.forms import CreateTicketsForm
from Acme_Support.decorators import method_decorator_adaptor
from .forms import *
from .models import Department, Tickets

load_dotenv()
# Create your views here.


class IndexView(TemplateView):
    '''
    TemplateView is a more powerfullway to use generic views ,
    it is used ti handle one template and here it is index.html
    '''
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user'] = get_user_model().objects.get(pk=self.request.session.get('user',None))
        return context


class SignInView(View):
    '''
      get_user_model is a function inside django auth which return the auth user..
    
       ---initializing form_class and model class and other here-------
    '''
    model = get_user_model()
    render_template = 'registrations/sign-in.html'
    redirect_url = 'index_url'


    def get(self,request):
        '''
          this method for rendering login template by initial loading and also
          we can pass any data to template using context or simple we can use locals func
          to pass all local variables to template.....
        '''
        if request.session.get('user',None) is not None:
            return redirect(self.redirect_url)
        return render(request,self.render_template,locals())

    def post(self,request):
        '''
          this method for get input value by template we get a dict object with key value in request.POST
          and we can access each key with this method mension below and also pass None to get function if a key is not fouind default None will returned....

        '''
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        user_ = get_user_model().objects.get(username=username)
        # user_ = user.authenticate(self,username=username,password=password)
        print(user_)
        if user_ is not None:
            request.session['user'] = user_.id
            if user_.is_user:
                return redirect('user_index')
            return redirect('index_url')
        return render(request,self.render_template)

class LogoutView(View):

    def get(self,request):
        session = request.session.get('user',None)
        if session is not None:
            try:
                del request.session['user']
            except Exception:
                pass
            return redirect('signin')
        return redirect('signin')
        

class ListRolesView(ListView):
    '''
      --initializing form_class and model class and other here------
    '''
    model = Group
    render_template = 'roles/list_roles.html'

    def get(self,request):
        queryset = self.get_queryset()
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        return render(request,self.render_template,locals())

class CreateRolesView(CreateView):
    '''
      django generic views CreateView is used here for create purpose
      I abstracted the CreateView class in my custom CreateUsersView class...

      In this Generic views only create will work..

      initializing form_class and model class and others here---
    '''
    
    form_class = CreateRolesForm
    render_template = 'roles/add_roles.html'
    redirect_url = 'list_roles'

    def get(self,request):
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        forms = self.form_class()
        return render(request,self.render_template,locals())

    def post(self,request):
        form = self.form_class(request.POST)
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        if form.is_valid():
            form.save()
            return redirect(self.redirect_url)
        return render(request,self.render_template)

class SetPermissionsView(DetailView):
    '''
      django generic views DetailView is used here for View a specific instance purpose
      I abstracted the DetailView class in my custom SetPermissionsView class...

      in Detailview only pass slug 

      In this Generic views only create will work..

      initializing form_class and model class and others here---
    '''
    
    form_class = SetPermissionsForm
    model = Group
    render_template = 'roles/set_permissions.html'
    redirect_url = 'list_roles'

    def get(self,request,**kwargs):
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        roles_id = kwargs.get('slug')
        forms = self.form_class(initial={
            'permissions' : self.model.objects.get(id=roles_id).permissions.all(),
            'name' : self.model.objects.get(id=roles_id).name
            
        })

        return render(request,self.render_template,locals())

    @method_decorator_adaptor(permission_required, 'permission.can_add_permission')
    def post(self,request,**kwargs):
        roles_id = kwargs.get('slug')
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        form = self.form_class(request.POST,instance=self.model.objects.get(pk=roles_id))
        if form.is_valid():
            form.save()
            return redirect(self.redirect_url)
        return render(self.form_class)

class ListDepartmentView(ListView):
    '''
      --initializing form_class and model class and other here------
    '''
    model = Department
    render_template = 'departments/list_departments.html'

    def get(self,request):
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        queryset = self.get_queryset()
        print(queryset,"lll")
        return render(request,self.render_template,locals())


class CreateDepartmentsView(CreateView):
    '''
      django generic views CreateView is used here for create purpose
      I abstracted the CreateView class in my custom CreateUsersView class...

      In this Generic views only create will work..

      initializing form_class and model class and others here---
    '''
    
    form_class = CreateDepartmentForm
    render_template = 'departments/add_department.html'
    redirect_url = 'list_departments'

    def get(self,request):
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        forms = self.form_class()
        return render(request,self.render_template,locals())

    def post(self,request):
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.redirect_url)
        return render(self.render_template)

class UpdateDepartmentsView(UpdateView):
    form_class = CreateDepartmentForm
    model = Department
    render_template = 'departments/update_department.html'

    def get(self,request,**kwargs):
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        department_id = kwargs.get('slug')
        forms = self.form_class(initial={
            'name' : self.model.objects.get(pk=department_id).name,
            'description' : self.model.objects.get(pk=department_id).description

        })
        return render(request,self.render_template,locals())

    def post(self,request,**kwargs):
        department_id = kwargs.get('slug')
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        forms = self.form_class(request.POST,instance=self.model.objects.get(pk=department_id))
        if forms.is_valid():
            forms.save()
            return redirect('list_departments')
        return render(request,self.render_template,locals())


class DeleteDepartmentsView(DeleteView):
    model = Department

    def get(self,request,**kwargs):
        department_id = kwargs.get('slug')
        queryset = self.model.objects.filter(pk=department_id)
        if queryset.exists():
            queryset.delete()
            return redirect(request.META.get('HTTP_REFERER',None))
        return redirect(request.META.get('HTTP_REFERER'))

class ListUsersView(ListView):
    '''
      --initializing form_class and model class and other here------
    '''
    model = get_user_model()
    render_template = 'list_users.html'

    def get(self,request):
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        queryset = self.get_queryset().filter(is_user=True)
        return render(request,self.render_template,locals())

class CreateUsersView(CreateView):

    '''
      django generic views CreateView is used here for create purpose
      I abstracted the CreateView class in my custom CreateUsersView class...

      In this Generic views only create will work..

      initializing form_class and model class and others here---
    '''
    model_class = get_user_model()
    form_class = CreateUserForm
    render_template = 'users/add_users.html'
    redirect_url = 'list_users'

    def get(self,request):
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        forms = self.form_class()
        return render(request,self.render_template,locals())

    def post(self,request):
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        forms = self.form_class(request.POST)
        if forms.is_valid():
            forms.save(request)
            return redirect(self.redirect_url)
      

        return render(request,self.render_template,locals())


class AssignDepartmentView(UpdateView):
    model = get_user_model()
    render_template = 'users/assign_department.html'
    form_class = AssignDepartmentForm

    def get(self,request,**kwargs):
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        pk = kwargs.get('pk')
        queryset = self.model.objects.filter(id=pk)
        forms = self.form_class(initial={
            'user_department' : self.model.objects.get(pk=pk).user_department
        })
        user = queryset.first()
        return render(request,self.render_template,locals())

    def post(self,request,**kwargs):
        pk = kwargs.get('pk')
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        forms = self.form_class(request.POST,instance=self.model.objects.get(pk=pk)) 
        if forms.is_valid():
            forms.save()
            return redirect('list_users')
        return render(request,self.render_template)


class TicketVIEW(ListView):
    render_template = 'tickets/list_tickets.html'
    model = Tickets

    def get(self,request):
        email = os.getenv("email")
        token = os.getenv("token")
        print(token,"+++++++")
        url = "https://cloudium.zendesk.com/api/v2/tickets"
        username = email + '/token'
        password = token
        # queryset = self.get_queryset().all()
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        response = requests.get(
                url,
                auth=(username, password)
            )
        print(response.status_code,"++++")
        queryset = response.json().get('tickets')
        # print([i for i in response.json().get('tickets')][0])
        return render(request,self.render_template,locals())
    
class CreateTicketsView(CreateView):
    model = Tickets
    form_class = CreateTicketsForm
    render_template = 'tickets/create_tickets.html'
    redirect_url = 'list_ticket'

    def get(self,request):
        forms = self.form_class()
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        return render(request,self.render_template,locals())

    def post(self,request):
        
        email = os.getenv("email")
        token = os.getenv("token")
        
        url = "https://cloudium.zendesk.com/api/v2/tickets"
        username = email + '/token'
        password = token
        payload = {
        "ticket": {
            "comment": {
            "body": "The smoke is very colorful."
            },
            "priority": "urgent",
            "subject": "My printer is on fire!"
        }
        }

        forms = self.form_class(request.POST)
        user = get_user_model().objects.get(pk=request.session.get('user',None))
        if forms.is_valid():
            priority = forms.cleaned_data.get("priority")
            subject = forms.cleaned_data.get("subject")
            payload.get("ticket").update({"priority":priority,"subject":subject})
            response = requests.post(
                url,
                auth=(username, password),
                json=json.loads(json.dumps(payload))
            )
            # if response.status_code()
            return redirect(self.redirect_url)
        return render(request,self.render_template,locals())