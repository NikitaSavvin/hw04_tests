from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostFormModelTest(TestCase):
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
                slug='test-slug',
                name_group='Тестовое название'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст потса',
            pub_date='2020-12-15',
            author=cls.user,
            group=cls.group
        )
        cls.group_1 = Group.objects.create(
            title='test-group-1',
            slug='test-slug-1',
            description='Tестовое описание 1',
            name_group='Тестовое название 1'
        )
        cls.user_1 = User.objects.create(username='Алена')

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            'index.html': reverse('index'),
            'post_new.html': reverse('post_new'),
            'group.html': (
                reverse('group_posts', kwargs={'slug': 'test-slug'})
            ),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_show_correct_context(self):
        response = self.authorized_client.get(reverse('index'))
        post_text_0 = response.context.get('page')[0].text
        post_author_0 = response.context.get('page')[0].author
        pub_date_0 = response.context.get('page')[0].pub_date
        self.assertEqual(post_text_0, 'Тестовый текст потса')
        self.assertEqual(post_author_0, PostFormModelTest.post.author)
        self.assertEqual(pub_date_0, PostFormModelTest.post.pub_date)

    def test_group_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={"slug": "test-slug"})
        )
        group_title_0 = response.context.get('group').title
        group_slug_0 = response.context.get('group').slug
        group_description_0 = response.context.get('group').description
        self.assertEqual(group_title_0, 'Тестовый заголовок')
        self.assertEqual(group_slug_0, 'test-slug')
        self.assertEqual(group_description_0, 'Тестовое описание')

    def test_post_new_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('post_new'))
        form_fields = {
            "group": forms.fields.ChoiceField,
            "text": forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_view_correct_context(self):
        response = self.authorized_client.get(
            reverse('post', kwargs={'username': 'Никита', 'post_id': '1'})
        )
        task_author_0 = response.context.get('post').author
        task_text_0 = response.context.get('post').text
        self.assertEqual(task_author_0, PostFormModelTest.post.author)
        self.assertEqual(task_text_0, 'Тестовый текст потса')

    def test_profile_correct_context(self):
        response = self.authorized_client.get(
            reverse('profile', kwargs={'username': 'Никита'})
        )
        task_author_0 = response.context.get('page')[0].author
        self.assertEqual(task_author_0, PostFormModelTest.post.author)

    def test_edit_correct_context(self):
        response = self.authorized_client.get(
            reverse('post_edit', kwargs={'username': 'Никита', 'post_id': '1'})
        )
        form_fields = {
            "group": forms.fields.ChoiceField,
            "text": forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_not_in_group_off(self):
        response = self.authorized_client.get(
            reverse("group_posts",
                    kwargs={"slug": "test-slug-1"})
        )
        response_posts = response.context.get("posts")
        self.assertNotIn(PostFormModelTest.post, response_posts)

    def test_post_in_pages(self):
        pages = {
            "index": reverse("index"),
            "group": (
                reverse("group_posts", kwargs={"slug": "test-slug"})
            )
        }
        for page, slugs in pages.items():
            with self.subTest(page=page):
                response = self.authorized_client.get(slugs)
                response_posts = response.context.get("posts")
                self.assertIn(PostFormModelTest.post, response_posts)


class PaginatorViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        cls.user = User.objects.create(
            username='Nikita'
        )
        cls.group = Group.objects.create(
                title='Тестовый заголовок',
                slug='test-slug',
                name_group='Тестовое название'
        )
        for i in range(0, 13):
            Post.objects.create(
                text=f'Тестовый текст потса {i}',
                author=PaginatorViewTest.user,
                group=PaginatorViewTest.group
            )

    def test_first_page_containse_ten_records(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_containse_three_records(self):
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)
