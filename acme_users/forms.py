from django import forms
from django.db.models import AutoField 
from acme_admin.models import Tickets
from Acme_Support.helpers import get_user_or_none

def copy_model_instance(obj):  
    """
    Create a copy of a model instance. 
    M2M relationships are currently not handled, i.e. they are not copied. (Fortunately, you don't have any in this case)
    See also Django #4027. From http://blog.elsdoerfer.name/2008/09/09/making-a-copy-of-a-model-instance/
    """  
    initial = dict([(f.name, getattr(obj, f.name)) for f in obj._meta.fields if not isinstance(f, AutoField) and not f in obj._meta.parents.values()])  
    return obj.__class__(**initial)  

class CreateTicketsForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super(CreateTicketsForm, self).__init__(*args, **kwargs)
        self.fields['ticket_id'].widget.attrs['placeholder'] = 'ticket id'
        self.fields['subject'].widget.attrs['placeholder'] = 'subject'
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control '})

    def save(self,request,commit=True,*args,**kwargs):
        m = super(CreateTicketsForm, self).save(commit=False, *args, **kwargs)
        m_new = copy_model_instance(m)
        m_new.created_by = get_user_or_none(pk=request.session.get('user',None))
        m_new.save()
        return m_new