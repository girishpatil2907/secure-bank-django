from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    mpin = forms.CharField(
        widget=forms.PasswordInput,
        label="4-Digit MPIN",
        validators=[
            MinLengthValidator(4),
            MaxLengthValidator(4),
            # --- YEH MESSAGE ENGLISH MEIN HO GAYA HAI ---
            RegexValidator(r'^\d{4}$', 'MPIN must be exactly 4 digits.')
        ]
    )
    confirm_mpin = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm 4-Digit MPIN",
        max_length=4
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        mpin = cleaned_data.get("mpin")
        confirm_mpin = cleaned_data.get("confirm_mpin")

        if password and confirm_password and password != confirm_password:
            # --- YEH MESSAGE ENGLISH MEIN HO GAYA HAI ---
            self.add_error('confirm_password', "Passwords do not match!")
        
        if mpin and confirm_mpin and mpin != confirm_mpin:
            # --- YEH MESSAGE ENGLISH MEIN HO GAYA HAI ---
            self.add_error('confirm_mpin', "The two MPIN fields did not match.")
        
        return cleaned_data