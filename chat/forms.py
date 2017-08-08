from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
	fname = forms.CharField(help_text="Email.")
	sname = forms.CharField(help_text="Email.")
	page = forms.CharField(help_text="Email.")
	gender = forms.CharField(help_text="Email.")
	telno = forms.CharField(help_text="Email.")
	password = forms.CharField(widget=forms.PasswordInput(), help_text="Password.")
	email = forms.CharField(help_text="Email.")
	username = forms.CharField(help_text="Username.")
	street = forms.CharField(help_text="street.")
	city = forms.CharField(help_text="City.")
	state = forms.CharField(help_text="State.")
	zip_code = forms.CharField(help_text="zip_code.")
	specialty = forms.CharField(help_text="City.")
	role = forms.CharField(help_text="Role.")

	class Meta:
		model = User
		fields = ['username', 'email', 'password']





class CreateAdminUserForm(forms.Form):

    """
    Form for migrating user phonebook
    """
    email = forms.EmailField(required=True, max_length=255)
    username = forms.CharField(required=True, max_length=255)
    telno = forms.CharField(required=True, max_length=255)
    password = forms.CharField(required=True, max_length=255)
    password2 = forms.CharField(required=True, max_length=255)
    profile_pic = forms.CharField(required=True, max_length=255)
    role = forms.CharField(required=True, max_length=255)
   

    def clean(self):

        # check passwords
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data
