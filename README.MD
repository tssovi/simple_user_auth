## Simple User Auth System


**Tools And Technology Used**

1. Python3
2. Django
3. SQLite3

**Notes**

* I am assuming that you already installed Python3 and Git in you system.
* Create a virtual environment and activate that environment.
* Follow the below mentioned steps.


**Project Cloning Commands**
> **`git clone https://github.com/tssovi/simple_user_auth.git`**
>


**Manually Project Execution Commands**
> **`pip install -r requirements.txt`**
>
> **`python manage.py makemigrations`**\
> **`python manage.py migrate`**
>
> **`python manage.py runserver`**
>


**Project Testing Execution Command**
> **`pytest users`**
>
>


**Sample Urls**

- [127.0.0.1:8000/user/registration/?email=user1@test.test&password=pass123](http://127.0.0.1:8000/user/registration/?email=user1@test.test&password=pass123)

- [127.0.0.1:8000/user/activate/?uid=Mg&token=5hp-b483d0f351fb6d360c79](http://127.0.0.1:8000/user/activate/?uid=Mg&token=5hp-b483d0f351fb6d360c79)

- [127.0.0.1:8000/user/login/?email=user1@test.test&password=pass123](http://127.0.0.1:8000/user/login/?email=user1@test.test&password=pass123)

