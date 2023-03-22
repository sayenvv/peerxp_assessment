from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.db.models import AutoField 
from .models import Department


def copy_model_instance(obj):  
    """
    Create a copy of a model instance. 
    M2M relationships are currently not handled, i.e. they are not copied. (Fortunately, you don't have any in this case)
    See also Django #4027. From http://blog.elsdoerfer.name/2008/09/09/making-a-copy-of-a-model-instance/
    """  
    initial = dict([(f.name, getattr(obj, f.name)) for f in obj._meta.fields if not isinstance(f, AutoField) and not f in obj._meta.parents.values()])  
    return obj.__class__(**initial)  

class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','email','phone','is_user','is_active','is_staff','user_department','user_roles')

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email or Phone'
        self.fields['phone'].widget.attrs['placeholder'] = 'Phone or Email'
        self.fields['user_department'].widget.attrs['placeholder'] = 'Department'
        self.fields['user_roles'].widget.attrs['placeholder'] = 'Roles'
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control '})


    def save(self,request,commit=True,*args,**kwargs):
        m = super(CreateUserForm, self).save(commit=False, *args, **kwargs)
        m_new = copy_model_instance(m)
        m_new.is_user = True
        m_new.created_by = request.user
        m_new.save()
        return m_new
    

class CreateDepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ("__all__")
    
    def __init__(self, *args, **kwargs):
        super(CreateDepartmentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'department name'
        self.fields['description'].widget.attrs['placeholder'] = 'description'
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control '})

class CreateRolesForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super(CreateRolesForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Role name'
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control '})

class SetPermissionsForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('permissions','name')

    def __init__(self, *args, **kwargs):
        super(SetPermissionsForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control '})


class AssignDepartmentForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ("user_department",)
    
    def __init__(self, *args, **kwargs):
        super(AssignDepartmentForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control '})

