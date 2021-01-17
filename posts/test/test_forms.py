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

    def test_create_PostForm(self):
        post_count = Post.objects.count()

        form_data = {
            'group': self.group.id,
            'text': self.post.text,
        }
        response = self.authorized_client.post(
            reverse('post_new'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), post_count+1)
        self.assertTrue(Post.objects.filter(
            text=self.post.text,
            group=self.group.id,
            author=self.post.author).exists())

    def test_edit_post(self):
        post_count = Post.objects.count()
        form_data = {
            'group': 5,
            'text': 'Измененный текст',
        }
        self.authorized_client.post(
            reverse(
                'post_edit',
                args=[self.post.author, self.post.id]
            ),
            data=form_data, follow=True
        )
        self.assertTrue(
            Post.objects.filter(
                text=self.post.text,
                group=self.group.id,
                author=self.post.author
            ).exists()
        )
        self.assertEqual(Post.objects.count(), post_count)
