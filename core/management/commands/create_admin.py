from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from core.models import Usuarios


class Command(BaseCommand):
    help = 'Crea un usuario administrador con rol de admin'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='admin@neontech.com',
            help='Email del admin'
        )
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username del admin'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Contraseña del admin'
        )
        parser.add_argument(
            '--firstname',
            type=str,
            default='Admin',
            help='Nombre del admin'
        )
        parser.add_argument(
            '--lastname',
            type=str,
            default='User',
            help='Apellido del admin'
        )

    def handle(self, *args, **options):
        email = options['email']
        username = options['username']
        password = options['password']
        first_name = options['firstname']
        last_name = options['lastname']

        # Verificar si existe
        if Usuarios.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'❌ El email "{email}" ya existe')
            )
            return

        if Usuarios.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'❌ El username "{username}" ya existe')
            )
            return

        try:
            admin = Usuarios.objects.create_user(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                rol='admin'  # ← IMPORTANTE
            )
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Admin creado exitosamente:\n'
                    f'   Email: {email}\n'
                    f'   Username: {username}\n'
                    f'   Rol: admin'
                )
            )
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {e}'))
