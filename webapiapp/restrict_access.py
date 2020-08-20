from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import render
from allauth.exceptions import ImmediateHttpResponse

class iitrpr_access(DefaultSocialAccountAdapter):
    def pre_social_login(self,request,sociallogin):
        u = sociallogin.user
        if not u.email.split('@')[1] == "iitrpr.ac.in":
            raise ImmediateHttpResponse(render(request,"intro/error.html"))
