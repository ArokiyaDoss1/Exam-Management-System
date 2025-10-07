import os
import sys
import django

# Ensure project root is on sys.path so 'backend' can be imported
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from backend.core.models import User  # noqa: E402


def main():
	username = 'admin'
	user = User.objects.get(username=username)
	user.role = 'ADMIN'
	user.save()
	print('Updated role:', user.username, user.role)


if __name__ == '__main__':
	main()


