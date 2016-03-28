from django import forms


class SearchForm(forms.Form):
    xquery = forms.CharField(required=True)
