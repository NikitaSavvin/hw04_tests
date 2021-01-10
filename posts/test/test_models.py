from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostFormModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
                title='Тестовый заголовок',
                description='Тестовое описание',
                slug='test-group',
                name_group='Тестовое название'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст потса',
            pub_date='2020-12-15',
            author=User.objects.create(username='testuser'),
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create(username='Никита')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_verbose_name_group(self):
        group = PostFormModelTest.group
        field_verboses = {
            'title': 'Заголовок',
            'slug': 'Адрес для страницы с группой',
            'description': 'Описание',
            'name_group': 'Название группы'
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)

    def test_verbose_name_post(self):
        post = PostFormModelTest.post
        field_verboses = {
            'text': 'Текст',
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_help_text_group(self):
        group = PostFormModelTest.group
        field_help_texts = {
            'title': 'Заголовок группы',
            'slug': ('Укажите адрес для страницы группы. Используйте только '
                     'латиницу, цифры, дефисы и знаки подчёркивания'),
            'description': 'Дайте описание группы',
            'name_group': 'Дайте название вашей группе'
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected)

    def test_help_text_post(self):
        post = PostFormModelTest.post
        field_help_texts = {
            'text': 'Напишите текст поста',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)
