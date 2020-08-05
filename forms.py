from django import forms
from NurtureHealthApp.models import add_treatment

class add_treatment_form(forms.ModelForm):
    class Meta:
        model = add_treatment
        fields = ["treatment_name","treatment_category","treatment_originalprice","treatment_actualprice","treatment_image","details"] 