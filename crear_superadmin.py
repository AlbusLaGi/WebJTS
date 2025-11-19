from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

def crear_superuser():
    username = input("Nombre de usuario para el superusuario: ")
    email = input("Email para el superusuario: ")
    password = input("Contraseña para el superusuario: ")
    
    try:
        user = User.objects.create_superuser(username, email, password)
        print(f'Superusuario {username} creado exitosamente.')
    except Exception as e:
        print(f'Error al crear el superusuario: {e}')

if __name__ == '__main__':
    crear_superuser()