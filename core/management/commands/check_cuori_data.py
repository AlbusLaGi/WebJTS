from django.core.management.base import BaseCommand
from core.models import Cuori

class Command(BaseCommand):
    help = 'Checks if a Cuori with a given cedula exists and prints its data.'

    def add_arguments(self, parser):
        parser.add_argument('cedula', type=str, help='The cedula of the Cuori to check')

    def handle(self, *args, **options):
        cedula = options['cedula']
        cuori = Cuori.objects.filter(cedula=cedula).first()

        if cuori:
            self.stdout.write(self.style.SUCCESS('Cuori encontrado:'))
            self.stdout.write(f'  Nombre: {cuori.nombre_completo}')
            self.stdout.write(f'  Cédula: {cuori.cedula}')
            self.stdout.write(f'  Contacto 1: {cuori.numero_contacto}')
            self.stdout.write(f'  Contacto 2: {cuori.numero_contacto_2}')
            self.stdout.write(f'  Email: {cuori.email_contacto}')
            self.stdout.write(f'  País: {cuori.pais}')
            self.stdout.write(f'  Departamento: {cuori.departamento}')
            self.stdout.write(f'  Ciudad: {cuori.ciudad}')
        else:
            self.stdout.write(self.style.WARNING(f'Cuori con cédula {cedula} no encontrado.'))