import os
import sys
import django

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from backend.core.models import User  # noqa: E402


def main():
	username = 'admin'
	password = 'admin@123'
	email = 'admin@example.com'
	user, created = User.objects.get_or_create(username=username, defaults={
		'email': email,
	})
	user.is_staff = True
	user.is_superuser = True
	user.role = 'ADMIN'
	user.set_password(password)
	user.save()
	print('Admin user ready:', user.username, 'created=' + str(created))


if __name__ == '__main__':
	main()


