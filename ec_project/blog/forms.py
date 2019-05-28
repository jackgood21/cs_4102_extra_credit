from django import forms

class QueryForm(forms.Form):
    query_text = forms.CharField(widget=forms.Textarea)
