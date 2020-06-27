from django.views import View
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.models import CustomUser
from common.validate_login import validate_login
from common.tokens import account_activation_token


class Registration(View):
    def get(self, request):
        message = ""
        email = request.GET.get('email', None)
        password = request.GET.get('password', None)

        try:
            user = CustomUser.objects.create_user(email=email, password=password)
        except:
            message = "An User Already Registered With %s This Email." % email
            return HttpResponse(message, status=403)

        if message == "":
            current_site = get_current_site(request)
            domain = current_site.domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            subject = 'Activate Your Account'
            message = "You Have Been Registered Successfully With %s This Email." % user
            message += "\nPlease Click On The Link Below To Confirm Your Registration:"
            message += "\nhttp://{}/user/activate/?uid={}&token={}".format(domain, uid, token)
            user.email_user(subject=subject, message=message)
            return HttpResponse(message, status=200)


class Login(View):
    def get(self, request):
        email = request.GET.get('email', None)
        password = request.GET.get('password', None)

        status_code, message = validate_login(email=email, password=password)

        return HttpResponse(message, status=status_code)


class UserActivation(View):
    def get(self, request):
        try:
            res_uid = request.GET.get('uid', None)
            res_token = request.GET.get('token', None)
            uid = force_str(urlsafe_base64_decode(res_uid))
            user = CustomUser.objects.get_user_details(pk=uid, email="")
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        res = account_activation_token.check_token(user, res_token)

        if user is not None and res:
            user.is_active = True
            user.is_email_confirmed = True
            user.save()
            message = "Your Account Has Been Activated Successfully."
            return HttpResponse(message, status=200)
        else:
            message = "The Confirmation Link Is Invalid, Possibly Because It Has Already Been Used."
            return HttpResponse(message, status=400)
