from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from user_auth.settings import MAX_INVALID_LOG_IN_TRY, ACCOUNT_LOCKED_FOR_MINUTES
from users.models import CustomUser


def validate_login(email, password):
    """
        :type: Login authenticate function
        :param email: Get from request
        :param password: Get from request
        :return: HTTP status code and message
    """
    # Get user details for further validations
    user_details = CustomUser.objects.get_user_details(pk="", email=email)

    # Try to authenticate login for provided credentials
    user = authenticate(email=email, password=password)

    # Check if any user exist for provided credentials or not
    if user_details:
        # Check if user email is confirmed or not. If not then return a message
        if user_details.is_email_confirmed:
            # If user account is locked then get user details for further validations
            if user_details.locked_at is not None:
                current_time = datetime.now()
                locked_until = user_details.locked_at + timedelta(minutes=ACCOUNT_LOCKED_FOR_MINUTES)
                remaining_time = (locked_until - current_time).seconds

            # If account is locked after maximum invalid try and not yet unlocked then return 423 status code and
            # relevant message
            if user_details.is_locked == True and current_time < locked_until:
                message = "Sorry. Your Account Is Locked Due To Several Incorrect Login Attempts. " \
                          "Please Try Again After %s Seconds(s)." % remaining_time

                return 423, message

            # If provided credentials are correct then return 200 status code and relevant message
            elif user:
                login_attempt = 0
                is_locked = False
                locked_at = None
                user = CustomUser.objects.update_user(email=email, login_attempt=login_attempt,
                                                      is_locked=is_locked, locked_at=locked_at)
                message = "You Have Been Logged In Successfully With %s This Email." % email
                return 200, message

            # If incorrect password provided then update invalid try count and return 401 status code and
            # relevant message
            elif user is None:
                if user_details.is_locked == True:
                    login_attempt = 1
                else:
                    login_attempt = user_details.login_attempt + 1

                try_left = MAX_INVALID_LOG_IN_TRY - login_attempt

                if try_left == 0:
                    is_locked = True
                    locked_at = datetime.now()
                else:
                    is_locked = False
                    locked_at = None

                user = CustomUser.objects.update_user(email=email, login_attempt=login_attempt,
                                                      is_locked=is_locked, locked_at=locked_at)
                message = "Your Logged In Request Failed For %s This Email. " % email
                message = message + "Incorrect Password Provided!! Please Try Again Carefully. " \
                                    "You Have Only %s Attemt(s) Left." % try_left
                return 401, message

        # If user account not yet confirmed then return 400 status code and relevant message
        else:
            message = "Your Account Not Yet Activated For %s This Email. " % email
            message += "Please Confirm Your Email And Try Again."
            return 400, message

    # If user not exist for provided credentials then return 404 status code and relevant message
    else:
        message = "Your Logged In Request Is Failed For %s This Email. " % email
        message = message + "No User Exist With %s This Email." % email
        return 404, message