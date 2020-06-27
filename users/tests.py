import re
import pytest
from user_auth.settings import MAX_INVALID_LOG_IN_TRY
from users.views import Registration, UserActivation, Login


rex_pattern = r"http[s]?://[^\s]+"

@pytest.mark.django_db(transaction=True)
def test_user_registration_with_valid_credentials(rf):
  reg_view = Registration.as_view()

  request = rf.get('/user/registration/?email=user1@test.com&password=password')
  response = reg_view(request=request)
  res_status_code = response.status_code

  assert res_status_code == 200

@pytest.mark.django_db(transaction=True)
def test_user_registration_with_existing_credentials(rf):
  reg_view = Registration.as_view()

  request = rf.get('/user/registration/?email=user1@test.com&password=password')
  response = reg_view(request=request)

  request = rf.get('/user/registration/?email=user1@test.com&password=password')
  response = reg_view(request=request)
  res_status_code = response.status_code

  assert res_status_code == 403

@pytest.mark.django_db(transaction=True)
def test_user_activation_url_with_valid_token(rf):
  reg_view = Registration.as_view()
  activate_view = UserActivation.as_view()

  request = rf.get('/user/registration/?email=user1@test.com&password=password')
  response = reg_view(request=request)

  res_message = response.content.decode("utf-8")
  pick_url = re.findall(rex_pattern, res_message)[0]
  activation_url = "/user" + pick_url.split("user")[1]
  request = rf.get(activation_url)
  response = activate_view(request=request)
  res_status_code = response.status_code

  assert res_status_code == 200

@pytest.mark.django_db(transaction=True)
def test_user_activation_url_with_invalid_token(rf):
  reg_view = Registration.as_view()
  activate_view = UserActivation.as_view()

  request = rf.get('/user/registration/?email=user1@test.com&password=password')
  response = reg_view(request=request)

  res_message = response.content.decode("utf-8")
  pick_url = re.findall(rex_pattern, res_message)[0]
  activation_url = "/user" + pick_url.split("user")[1]
  request = rf.get(activation_url)

  response = activate_view(request=request)
  response = activate_view(request=request)

  res_status_code = response.status_code

  assert res_status_code == 400

@pytest.mark.django_db(transaction=True)
def test_user_login_with_valid_credentials(rf):
  reg_view = Registration.as_view()
  activate_view = UserActivation.as_view()
  login_view = Login.as_view()

  request = rf.get('/user/registration/?email=user1@test.com&password=password')
  response = reg_view(request=request)

  res_message = response.content.decode("utf-8")
  pick_url = re.findall(rex_pattern, res_message)[0]
  activation_url = "/user" + pick_url.split("user")[1]
  request = rf.get(activation_url)
  response = activate_view(request=request)

  request = rf.get('/user/login/?email=user1@test.com&password=password')
  response = login_view(request=request)
  res_status_code = response.status_code

  assert res_status_code == 200

@pytest.mark.django_db(transaction=True)
def test_user_login_with_invalid_password(rf):
  reg_view = Registration.as_view()
  activate_view = UserActivation.as_view()
  login_view = Login.as_view()

  request = rf.get('/user/registration/?email=user1@test.com&password=password')
  response = reg_view(request=request)

  res_message = response.content.decode("utf-8")
  pick_url = re.findall(rex_pattern, res_message)[0]
  activation_url = "/user" + pick_url.split("user")[1]
  request = rf.get(activation_url)
  response = activate_view(request=request)

  request = rf.get('/user/login/?email=user1@test.com&password=password1')
  response = login_view(request=request)

  assert response.status_code == 401

@pytest.mark.django_db(transaction=True)
def test_user_login_witn_invalid_email(rf):
  login_view = Login.as_view()

  request = rf.get('/user/login/?email=user11@test.com&password=password')
  response = login_view(request=request)

  assert response.status_code == 404

@pytest.mark.django_db(transaction=True)
def test_user_login_witn_valid_credentials_when_locked(rf):
  reg_view = Registration.as_view()
  activate_view = UserActivation.as_view()
  login_view = Login.as_view()

  request = rf.get('/user/registration/?email=user1@test.com&password=password')
  response = reg_view(request=request)

  res_message = response.content.decode("utf-8")
  pick_url = re.findall(rex_pattern, res_message)[0]
  activation_url = "/user" + pick_url.split("user")[1]
  request = rf.get(activation_url)
  response = activate_view(request=request)

  for i in range(MAX_INVALID_LOG_IN_TRY):
    request = rf.get('/user/login/?email=user1@test.com&password=password1')
    response = login_view(request=request)

  request = rf.get('/user/login/?email=user1@test.com&password=password')
  response = login_view(request=request)

  assert response.status_code == 423

