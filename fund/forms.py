

from django import forms
from .models import Project, User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'total_target', 'start_time', 'end_time', 'category', 'tags']
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
            else:
                self._pending_tags = tag_ids
            return instance




class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),  
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),  
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password','confirm_password', 'mobile_phone', 'profile_picture']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data
