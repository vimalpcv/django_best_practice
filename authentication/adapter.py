from django.core.exceptions import ValidationError
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        raise ValidationError("No account found with provided email. "
                              "Link your existing account on profile page or Contact admin for help.")


class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):

    def complete_login(self, request, app, token, **kwargs):
        login = super().complete_login(request, app, token, **kwargs)

        '''
        # we can write custom logic here
        if not login.user.is_superuser:
            raise ValidationError("This user is not a superuser.")
        '''

        return login
