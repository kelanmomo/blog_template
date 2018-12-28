from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.contrib.auth.models import User

from ..views import home, category_list, category_new
from ..models import Category, Post
from ..forms import NewPostForm

# Create your tests here.

class HomeTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Blog')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolvers_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_list_page(self):
        category_list_url = reverse('category_list', kwargs={'pk':self.category.pk})
        self.assertContains(self.response, 'href="{0}"'.format(category_list_url))

class CategoryListTests(TestCase):
    def setUp(self):
        Category.objects.create(name='Blog')
    
    def test_category_list_view_success_status_code(self):
        url = reverse('category_list', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_category_list_view_not_found_status_code(self):
        url = reverse('category_list', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_category_list_url_resolves_category_list_view(self):
        view = resolve('/categorys/1/')
        self.assertEquals(view.func, category_list)
    
    def test_category_list_view_contains_link_back_to_homepage(self):
        category_list_url = reverse('category_list', kwargs={'pk':1})
        response = self.client.get(category_list_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
    
    def test_category_list_view_contains_navigation_links(self):
        category_list_url = reverse('category_list', kwargs={'pk':1})
        response = self.client.get(category_list_url)
        new_post_url = reverse('category_new', kwargs={'pk':1})
        home_page_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(home_page_url))
        # self.assertContains(response, 'href="{0}"'.format(new_post_url))
        
class NewPostTests(TestCase):
    def setUp(self):
        Category.objects.create(name='blog')
        User.objects.create_user(username='ZouTing', email="ellen1005@sina.com", password="abcd1234")

    def test_new_post_view_success_status_code(self):
        url = reverse('category_new', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_new_post_view_not_found_status_code(self):
        url = reverse('category_new', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_new_post_url_resolves_new_post_view(self):
        view = resolve('/categorys/1/new/')
        self.assertEquals(view.func, category_new)
    
    def test_new_post_view_contains_link_back_to_category_list_view(self):
        new_post_url = reverse('category_new', kwargs={'pk':1})
        category_list_url = reverse('category_list', kwargs={'pk':1})
        response = self.client.get(new_post_url)
        self.assertContains(response, 'href="{0}"'.format(category_list_url))

    def test_csrf(self):
        url = reverse('category_new', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_new_blog_valid_post_data(self):
        url = reverse('category_new', kwargs={'pk':1})
        data = {
            'title':'Test title',
            'text_body':'Test text body'
        }
        response = self.client.post(url, data)
        self.assertTrue(Post.objects.exists())
    
    def test_new_blog_invalid_post_data(self):
        url = reverse('category_new', kwargs={'pk':1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_blog_invalid_post_empty_data(self):
        url = reverse('category_new', kwargs={'pk':1})
        data = {
            'title':'',
            'text_body':''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Post.objects.exists())
    
    def test_contains_form(self):
        url = reverse('category_new', kwargs={'pk':1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewPostForm)