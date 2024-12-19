from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.http import HttpRequest
from accounts.models import User, Ranking, Code, UserHistory, Waste, ScanData
from .admin import CodeAdmin, ScanDataAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.utils import IntegrityError
from django.urls import reverse





# Simula una instancia de AdminSite
site = AdminSite()


class AdminFormFieldTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.code_admin = CodeAdmin(Code, site)

    def test_formfield_labels(self):
        """Prueba que las etiquetas de los formularios personalizados sean correctas."""
        form = self.code_admin.get_form(HttpRequest())()
        self.assertEqual(form.fields["material"].label, "Material")


class ScanDataAdminTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin = ScanDataAdmin(ScanData, site)

        # Obtener el modelo de usuario personalizado
        User = get_user_model()

        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='password')

        # Asignar permisos al usuario
        permission = Permission.objects.get(codename='view_scandata')  # Usar el nombre del permiso correspondiente
        self.user.user_permissions.add(permission)

        # Crear datos de prueba
        self.scan1 = ScanData.objects.create(
            waste_type="Plastic", container="A1", user=self.user
        )
        self.scan2 = ScanData.objects.create(
            waste_type="Metal", container="B2", user=self.user
        )

    def test_changelist_view_with_date_filters(self):
        """Prueba que changelist_view filtre los datos correctamente."""
        # Crear una solicitud y asociar un usuario
        request = self.factory.get('/admin/app/scandata/?waste_type=Plastic')
        request.user = self.user  # Asignar el usuario de prueba a la solicitud

        # Llamar al changelist_view
        response = self.admin.changelist_view(request)

        # Verificar que la respuesta sea 200 OK
        self.assertEqual(response.status_code, 200)


#PRUEBAS MODELS
class UserModelTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='password', email='testuser@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.experience_points, 0)  # Default value
        self.assertEqual(user.profile_picture, None)  # Cambiado de assertIsNone a assertEqual

    def test_email_unique(self):
        User.objects.create_user(username='user1', password='password', email='test@example.com')
        with self.assertRaises(IntegrityError):  # Expecting an IntegrityError
            User.objects.create_user(username='user2', password='password', email='test@example.com')


class RankingModelTests(TestCase):

    def test_create_ranking(self):
        ranking = Ranking.objects.create(
            name='Bronze', level=1, from_points=0, to_points=100, image='path_to_image.jpg'
        )
        self.assertEqual(ranking.name, 'Bronze')
        self.assertEqual(ranking.level, 1)
        self.assertEqual(ranking.from_points, 0)
        self.assertEqual(ranking.to_points, 100)

    def test_ranking_str(self):
        ranking = Ranking.objects.create(name='Silver', level=2, from_points=101, to_points=200)
        self.assertEqual(str(ranking), '2 - Silver')


class CodeModelTests(TestCase):

    def test_create_code(self):
        user = User.objects.create_user(username='testuser', password='password', email='testuser@example.com')
        code = Code.objects.create(
            id_physical_location='Location1',
            consecutive=1,
            id_container=123,
            id_model='ModelA',
            material=456,
            success=1,
            user=user
        )
        self.assertEqual(code.id_physical_location, 'Location1')
        self.assertEqual(code.consecutive, 1)
        self.assertEqual(code.material, 456)
        self.assertEqual(code.success, 1)
        self.assertEqual(code.user.username, 'testuser')

    def test_code_str(self):
        user = User.objects.create_user(username='testuser', password='password', email='testuser@example.com')
        code = Code.objects.create(
            id_physical_location='Location1', consecutive=1, id_container=123, id_model='ModelA', material=456, success=1, user=user
        )
        self.assertEqual(str(code), f'{code.id} - testuser - Location1')


class UserHistoryModelTests(TestCase):

    def test_create_user_history(self):
        user = User.objects.create_user(username='testuser', password='password', email='testuser@example.com')
        history = UserHistory.objects.create(
            type_of_activity='QR_SCAN',
            accumulated_points=100,
            user=user
        )
        self.assertEqual(history.type_of_activity, 'QR_SCAN')
        self.assertEqual(history.accumulated_points, 100)
        self.assertEqual(history.user.username, 'testuser')

    def test_user_history_str(self):
        user = User.objects.create_user(username='testuser', password='password', email='testuser@example.com')
        history = UserHistory.objects.create(type_of_activity='QR_SCAN', accumulated_points=100, user=user)
        self.assertEqual(str(history), f'{history.id} - {history.user.username} - 100')


class WasteModelTests(TestCase):

    def test_create_waste(self):
        waste = Waste.objects.create(
            iteration=1,
            date='2024-12-01T00:00:00Z',
            name_ima_before='image_before.jpg',
            name_ima_after='image_after.jpg',
            mode=1,
            folder='/path/to/folder',
            res=0,
            rec=1,
            ecological_point='A',
            model_version='1.0',
            success=1
        )
        self.assertEqual(waste.iteration, 1)
        self.assertEqual(waste.mode, 1)
        self.assertEqual(waste.ecological_point, 'A')

    def test_waste_str(self):
        waste = Waste.objects.create(
            iteration=1,
            date='2024-12-01T00:00:00Z',
            name_ima_before='image_before.jpg',
            name_ima_after='image_after.jpg',
            mode=1,
            folder='/path/to/folder',
            res=0,
            rec=1,
            ecological_point='A',
            model_version='1.0',
            success=1
        )
        self.assertEqual(str(waste), f'Iteration {waste.iteration} - {waste.date}')


class ScanDataModelTests(TestCase):

    def test_create_scan_data(self):
        user = User.objects.create_user(username='testuser', password='password', email='testuser@example.com')
        scan = ScanData.objects.create(
            waste_type="Plastic",
            container="A1",
            user=user
        )
        self.assertEqual(scan.waste_type, 'Plastic')
        self.assertEqual(scan.container, 'A1')
        self.assertEqual(scan.user.username, 'testuser')

    def test_scan_data_str(self):
        user = User.objects.create_user(username='testuser', password='password', email='testuser@example.com')
        scan = ScanData.objects.create(waste_type='Plastic', container='A1', user=user)
        self.assertEqual(str(scan), f'Plastic - A1 - {scan.timestamp}')


#PRUEBAS VIEWS
class TestViews(TestCase):

    def setUp(self):
        # Crear un usuario de prueba
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com',
        )

    def test_login_view_get(self):
        """Probar la vista de login GET."""
        response = self.client.get(reverse('accounts.login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post_invalid_credentials(self):
        """Probar la vista de login POST con credenciales inválidas."""
        response = self.client.post(reverse('accounts.login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El nombre de usuario o la contraseña no son correctos.')

    def test_login_view_post_valid_credentials(self):
        """Probar la vista de login POST con credenciales válidas."""
        response = self.client.post(reverse('accounts.login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('home.index'))

    def test_logout_view(self):
        """Probar la vista de logout."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('accounts.logout'))
        self.assertRedirects(response, reverse('home.index'))

    def test_signup_view_get(self):
        """Probar la vista de signup GET."""
        response = self.client.get(reverse('accounts.signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signup_view_post_valid_data(self):
        """Probar la vista de signup POST con datos válidos."""
        response = self.client.post(reverse('accounts.signup'), {
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'newuser@example.com',
        })
        self.assertEqual(get_user_model().objects.count(), 2)  # Asegurarse que se haya creado un nuevo usuario
        self.assertRedirects(response, reverse('home.index'))

    def test_profile_view_get(self):
        """Probar la vista de perfil GET."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('accounts.profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_upload_json_view(self):
        """Probar la vista de carga de JSON."""
        self.client.login(username='testuser', password='password123')
        test_json = [{
            'iteration': 1,
            'date': '01/01/2023/12:00:00',
            'name_ima_before': 'image1.jpg',
            'name_ima_after': 'image2.jpg',
            'mode': 'manual',
            'folder': 'folder1',
            'res': 'res1',
            'rec': 'rec1',
            'ecological_point': 10,
            'model_version': 'v1',
            'success': 1,
        }]
        response = self.client.post(reverse('accounts.upload_json'), {'json_file': test_json}, format='json')
        self.assertRedirects(response, '/')
