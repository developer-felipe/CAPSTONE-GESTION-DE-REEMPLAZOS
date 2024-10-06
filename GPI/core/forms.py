from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario", 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Usuario'
        })
    )
    
    password = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Contraseña'
        })
    )