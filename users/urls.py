from django.urls import path
from users.views import Registration, UserActivation, Login

urlpatterns = [
    path('registration/', Registration.as_view(), name='registration'),
    path('activate/', UserActivation.as_view(), name='activate'),
    path('login/', Login.as_view(), name='login'),
]

