from django.contrib.auth import get_user_model
User = get_user_model()
print('exists', User.objects.filter(username='admin').exists())
