from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Nikita')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
                title='Тестовый заголовок',
                description='Тестовое описание',
                slug='test-group',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст потса',
            author=cls.user,
            group=cls.group
        )
        cls.group_2 = Group.objects.create(
            title="Тестовый заголовок 2",
            slug="test-group_2",
            description="Тестовое описание_2",
        )

    def test_create_post_form(self):
        post_count = Post.objects.count()

        form_data = {
            'group': self.group_2.id,
            'text': 'Измененный текст',
        }
        response = self.authorized_client.post(
            reverse('post_new'),
            data=form_data,
            follow=True,
        )
        post_edit = response.context['post']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post_edit.text, form_data['text'])
        self.assertEqual(post_edit.group, self.group_2)
        self.assertEqual(post_edit.author, self.user)
        self.assertEqual(Post.objects.count(), post_count+1)

    def test_edit_post(self):
        post_count = Post.objects.count()
        form_data = {
            'group': self.group_2.id,
            'text': 'Измененный текст',
        }
        response = self.authorized_client.post(
            reverse(
                'post_edit', args=[self.post.author, self.post.id]
            ),
            data=form_data, follow=True
        )
        post_edit = response.context['post']
        self.assertEqual(post_edit.text, form_data['text'])
        self.assertEqual(post_edit.group, self.group_2)
        self.assertEqual(post_edit.author, self.user)
        self.assertEqual(Post.objects.count(), post_count)
