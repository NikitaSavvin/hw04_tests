from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create(username='Никита')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
                title='Тестовый заголовок',
                description='Тестовое описание',
                slug='test-group',
                name_group='Тестовое название'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст потса',
            pub_date='2020-12-15',
            author=cls.user,
            group=cls.group
        )

    def test_create_PostForm(self):
        post_count = Post.objects.count()

        form_data = {
            "group": '1',
            "text": 'Тестовый текст.',
        }
        response = self.authorized_client.post(
            reverse('post_new'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, "/")
        self.assertEqual(Post.objects.count(), post_count+1)
        self.assertTrue(Group.objects.filter(slug='test-group').exists())
        self.assertTrue(Post.objects.filter(
            text='Тестовый текст потса').exists())

    def test_edit_post(self):
        form_data = {'text': 'Тестовый текст.'}
        PostFormTests.authorized_client.post(
            reverse('post_edit',
                    kwargs={'username': 'Никита', 'post_id': '1'}),
            data=form_data,
            follow=True,)
        self.assertEqual(Post.objects.first().text, form_data['text'])
