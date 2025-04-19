from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50, label="Username", required=True)
    password = forms.CharField(
        widget=forms.PasswordInput, label="Password", required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password", required=True)
    first_name = forms.CharField(
        max_length=50, label="First Name", required=True)
    last_name = forms.CharField(
        max_length=50, label="Last Name", required=True)
    phone_number = forms.CharField(
        max_length=20, label="Phone Number", required=True)
    email = forms.EmailField(label="Email", required=True)
    position = forms.CharField(max_length=50, label="Position", required=True)
    department = forms.CharField(
        max_length=50, label="Department", required=True)
    department = forms.CharField(
        max_length=50, label="Department", required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
