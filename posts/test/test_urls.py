from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls.base import reverse

from ..models import Group, Post

User = get_user_model()


class PostFormModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create(username='Nikita')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
                title='Тестовый заголовок',
                description='Тестовое описание',
                slug='test-slug',
                name_group='Тестовое название'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст потса',
            pub_date='2020-12-15',
            author=cls.user,
            group=cls.group
        )
        cls.authorized_client_1 = Client()
        cls.user_1 = User.objects.create(username='Alena')
        cls.authorized_client_1.force_login(cls.user_1)
        cls.post_1 = Post.objects.create(
            text='Тестовый текст потса 1',
            author=cls.user_1,
        )

    def test_index_url_exists_at_desired_location(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_url_exists_at_desired_location(self):
        response = self.authorized_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, 200)

    def test_new_url_exists_at_desired_location(self):
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_list_url_redirect_anonymous_on_admin_login(self):
        response = self.guest_client.get('/new/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/new/')

    def test_profile_exists_at_desired_location(self):
        response = self.authorized_client.get('/Nikita/')
        self.assertEqual(response.status_code, 200)

    def test_post_view_exists_at_desired_location(self):
        response = self.authorized_client.get('/Nikita/1/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit_not_authorized(self):
        response = self.guest_client.get('/Nikita/1/edit/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/Nikita/1/edit/')

    def test_post_edit_authorized_user_not_the_author(self):
        response = self.authorized_client_1.post(
            reverse('post_edit',
                    kwargs={'username': 'Nikita', 'post_id': '1'}),
            follow=True)
        self.assertRedirects(
            response, '/Nikita/1/')

    def test_post_edit_authorized_user_is_the_author(self):
        response = self.authorized_client.get('/Nikita/1/edit/')
        self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        '''С тестом не справился'''
        templates_url_names = {
            'index.html': reverse('index'),
            'group.html': '/group/test-group/',
            'post_new.html': '/new/',
            'post_new.html': '/Nikita/1/edit/',
            'post.html': '/Nikita/1/',
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
