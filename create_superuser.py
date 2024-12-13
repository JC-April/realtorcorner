# import os
# from django.core.management import execute_from_command_line
# from django.contrib.auth import get_user_model

# User = get_user_model()

# def create_superuser():
#     username=os.getenv('DJANGO_SUPERUSER_USERNAME'),
#     email=os.getenv('DJANGO_SUPERUSER_EMAIL'),
#     password=os.getenv('DJANGO_SUPERUSER_PASSWORD')

#     if username and email and password:
#         if not User.objects.filter(username=username).exists():
#             User.objects.create_superuser(
#                 username=os.getenv('DJANGO_SUPERUSER_USERNAME'),
#                 email=os.getenv('DJANGO_SUPERUSER_EMAIL'),
#                 password=os.getenv('DJANGO_SUPERUSER_PASSWORD')
#             )
#             print(f"superuser {username} created")
#         else:
#             print(f"superuser {username} already exists")
#     else:
#         print(f"environment variables not properly set for superuser creation")

# if __name__ == '__main__':
#     create_superuser()


import os
from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    username = os.getenv('DJANGO_SUPERUSER_USERNAME')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

    if username and email and password:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"Superuser {username} created.")
        else:
            print(f"Superuser {username} already exists.")
    else:
        print("Environment variables not properly set for superuser creation.")

if __name__ == '__main__':
    create_superuser()
