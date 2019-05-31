from django import forms

class QueryForm(forms.Form):

    CHOICES = (('Plaintext', 'Plaintext'), ('URL', 'URL'))
    text_format = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'style': 'width:120px'}), label = "")
    query_text = forms.CharField(widget=forms.Textarea, label = "")
