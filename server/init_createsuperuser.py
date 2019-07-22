from django.contrib.auth.models import User;

username = 'administrator';
password = 'administrator';
email = 'administrator@local';

if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped.');