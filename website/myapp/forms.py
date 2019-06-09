from django import forms

class sign_in(forms.Form):
    username = forms.CharField(label='USERNAME', max_length=100, widget=forms.TextInput(attrs={'class' : 'w3-input w3-border w3-sand'}))
    password = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(attrs={'class' : 'w3-input w3-border w3-sand'}))

class sign_up(forms.Form):
    username = forms.CharField(label='USERNAME', max_length=100, widget=forms.TextInput(attrs={'class' : 'w3-input w3-border w3-sand'}))
    password = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(attrs={'class' : 'w3-input w3-border w3-sand'}))
    first_name = forms.CharField(label='FIRST NAME', widget=forms.TextInput(attrs={'class' : 'w3-input w3-border w3-sand'}))
    last_name = forms.CharField(label='LAST NAME', widget=forms.TextInput(attrs={'class' : 'w3-input w3-border w3-sand'}))
    email = forms.EmailField(label   ='EMAIL', widget=forms.TextInput(attrs={'class' : 'w3-input w3-border w3-sand'}))