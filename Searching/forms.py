from django import forms

class SearchForm1(forms.Form):
    hgvs = forms.CharField()
    
class SearchForm2(forms.Form):
    symbol = forms.CharField()


class SearchForm3(forms.Form):
    medicine = forms.CharField()

class TextForm(forms.Form):
    text = forms.CharField()
