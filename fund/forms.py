from django import forms
from .models import Project, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm


class SignupForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'mobile_phone', 'profile_picture')

	first_name = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
	}))

	last_name = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
	}))

	username = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
	}))

	email = forms.CharField(widget=forms.EmailInput(attrs={
		'class': 'form-control',
	}))

	password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
		'class': 'form-control',
	}))

	password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
		'class': 'form-control',
	}))

	mobile_phone = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
	}))

	profile_picture = forms.ImageField(widget=forms.FileInput(attrs={
		'class': 'form-control',
	}))


class LoginForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control',
  }))

  password = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control',
  }))  


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['title', 'details', 'total_target', 'start_time', 'end_time', 'category', 'tags']
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project title'}),
			'details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter project details', 'rows': 4}),
			'total_target': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter target amount'}),
			'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
			'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
			'category': forms.Select(attrs={'class': 'form-select'}),
			'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
		}

	def save(self, commit=True):
		instance = super().save(commit=False)
		tags_value = self.cleaned_data.get('tags')

		if isinstance(tags_value, str):
			tag_ids = [int(x) for x in tags_value.split(',') if x]
		else:
			tag_ids = [tag.id for tag in tags_value]

		if commit:
			instance.save()
			instance.tags.set(tag_ids)

		return instance


class UserUpdateForm(UserChangeForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'mobile_phone', 'profile_picture', 'birthdate', 'facebook_profile', 'country')

	first_name = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
	}))

	last_name = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
	}))

	username = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
	}))

	password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
		'class': 'form-control',
	}))

	password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
		'class': 'form-control',
	}))

	mobile_phone = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
	}))

	profile_picture = forms.ImageField(widget=forms.FileInput(attrs={
		'class': 'form-control',
	}))

	birthdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

	facebook_profile = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))

	country = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
