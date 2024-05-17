from django.db import models
from django.contrib.auth.models import AbstractUser
from lounges.models import Lounge

# Adapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field, user_username

class User(AbstractUser):
    subscriptions = models.ManyToManyField('self', symmetrical=False, related_name='subscribers')
    profile_path = models.ImageField(blank=True)
    nickname = models.CharField(max_length=30)
    

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):

        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        # nickname field added
        nickname = data.get("nickname") 
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        # nickname field added
        if nickname:
            user_field(user, "nickname", nickname)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user