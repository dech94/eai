import sys
try:
    import django
    with open('django_version.txt', 'w') as f:
        f.write(django.get_version())
except ImportError:
    with open('django_version.txt', 'w') as f:
        f.write("Django not installed")
except Exception as e:
    with open('django_version.txt', 'w') as f:
        f.write(str(e))
