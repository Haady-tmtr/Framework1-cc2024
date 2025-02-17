from django.forms import ModelForm
from collec_management.models import Collec, Element
from django import forms

class CollecForm(ModelForm):
    class Meta:
        model = Collec
        fields = ["title", "description"]

    def __init__(self, *args, **kwargs):
        super(CollecForm, self).__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields["date"] = forms.DateTimeField(
                initial=self.instance.date, 
                widget=forms.TextInput(attrs={"readonly": "readonly"})
            )


class ElementForm(ModelForm):
    class Meta:
        model = Element
        fields = ['title', 'description', 'value', 'quantity']
        
