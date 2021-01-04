from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from unittest import skip

from lists.models import Item
from lists.views import home_page
#from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class HomePageTest(TestCase):

    # @skip
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertTemplateUsed(response, 'home.html')

    def test_uses_home_template(self):    
        response = self.client.get('/')    
        self.assertTemplateUsed(response, 'home.html')

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})        
        new_list = List.objects.first()        
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class ListViewTest(TestCase):    
    def test_uses_list_template(self):        
        list_ = List.objects.create()        
        response = self.client.get(f'/lists/{list_.id}/')        
        self.assertTemplateUsed(response, 'list.html')    

    def test_displays_only_items_for_that_list(self):        
        correct_list = List.objects.create()        
        Item.objects.create(text='itemey 1', list=correct_list)        
        Item.objects.create(text='itemey 2', list=correct_list)        
        other_list = List.objects.create()        
        Item.objects.create(text='other list item 1', list=other_list)        
        Item.objects.create(text='other list item 2', list=other_list)       

        response = self.client.get(f'/lists/{correct_list.id}/')        

        self.assertContains(response, 'itemey 1')        
        self.assertContains(response, 'itemey 2')        
        self.assertNotContains(response, 'other list item 1')        
        self.assertNotContains(response, 'other list item 2')

        def test_passes_correct_list_to_template(self):        
            other_list = List.objects.create()        
            correct_list = List.objects.create()        
            response = self.client.get(f'/lists/{correct_list.id}/')        
            self.assertEqual(response.context['list'], correct_list)

class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

        #request = HttpRequest()
        #response = home_page(request)
        #html = response.content.decode('utf8')
        #self.assertTrue(html.startswith('<html>'))
        #self.assertIn('<title>To-Do lists</title>', html)
        #self.assertTrue(html.endswith('</html>'))  
        ##self.assertTrue(html.strip().endswith('</html>'))


    #def test_bad_maths(self):
        #self.assertEqual(1 + 1, 3)
    
# class FunctionalTest(StaticLiveServerTestCase):    def setUp(self):        [...]    def tearDown(self):        [...]    def wait_for_row_in_list_table(self, row_text):        [...]class NewVisitorTest(FunctionalTest):    def test_can_start_a_list_for_one_user(self):        [...]    def test_multiple_users_can_start_lists_at_different_urls(self):        [...]class LayoutAndStylingTest(FunctionalTest):    def test_layout_and_styling(self):        [...]class ItemValidationTest(FunctionalTest):    @skip    def test_cannot_add_empty_list_items(self):        [...]    

    
