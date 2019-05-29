from django import forms

class QueryForm(forms.Form):
    query_text = forms.CharField(widget=forms.Textarea)
    CHOICES = (('URL', 'URL'), ('Plaintext', 'Plaintext'))
    text_format = forms.ChoiceField(choices=CHOICES)
