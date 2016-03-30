from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(required=True)

class RefinedSearchForm(forms.Form):
    search = forms.CharField(required=True)
    refined_search = forms.CharField(required=True)
