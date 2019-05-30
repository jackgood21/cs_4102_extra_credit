from django import forms

class QueryForm(forms.Form):

    CHOICES = (('URL', 'URL'), ('Plaintext', 'Plaintext'))
    text_format = forms.ChoiceField(choices=CHOICES, label = "")
    query_text = forms.CharField(widget=forms.Textarea, label = "")
