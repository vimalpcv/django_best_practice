import jwt
from django.conf import settings
from django.core.exceptions import ValidationError
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        if settings.SOCIAL_REGISTRATION:
            raise ValidationError("No account found with provided email. "
                                  "Link your existing account on profile page or Contact admin for help.")
        else:
            return super().is_open_for_signup(request, sociallogin)


class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):

    def complete_login(self, request, app, token, response, **kwargs):
        """
        we can write custom social login logic here
        """
        if settings.SOCIAL_SAME_EMAIL_CONNECT:
            try:
                identity_data = jwt.decode(
                    response["id_token"],
                    options={"verify_signature": False,"verify_iss": True,"verify_aud": True,"verify_exp": True,},
                    issuer=self.id_token_issuer,audience=app.client_id,
                )
            except jwt.PyJWTError as e:
                raise OAuth2Error("Invalid id_token") from e
            if identity_data.get('email') != request.user.email:
                raise ValidationError("Email does not match with the email of the logged in user.")

        login = super().complete_login(request, app, token, response, **kwargs)
        return login
