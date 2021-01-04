from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase
#import unittest
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10  

#class NewVistorTest(unittest.TestCase):
class NewVistorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_for_one_user(self):
        # Merlin heard about an online to-do app. 
        # He goes to the homepage
        #self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)    

        # He is able to add to-do items straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Obtain eye of newt" into the text box
        # (Merlin's hobby is magic)
        inputbox.send_keys('Obtain eye of newt')

        # When he presses enter, the page updates, and it now lists the item
        # "1: Obtain eye of newt" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Obtain eye of newt")
        #time.sleep(1)

        #self.check_for_row_in_list_table('1: Obtain eye of newt')
        #self.assertTrue(
        #    any(row.text == '1: Obtain eye of newt' for row in rows),
        #    f"New to-do item did not appear in table. Contents were:\n{table.text}"
        #)

        # There is still a text box avaliable for use.
        # He enters "Combine all ingredients in cauldron"
        inputbox = self.browser.find_element_by_id('id_new_item')    
        inputbox.send_keys('Combine all ingredients in cauldron')    
        inputbox.send_keys(Keys.ENTER)    
        #time.sleep(1)

        # The page updates again, and now shows both items on his list
        self.wait_for_row_in_list_table('1: Obtain eye of newt')    
        self.wait_for_row_in_list_table('2: Combine all ingredients in cauldron')
        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        #self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        #self.assertIn(
        #    '2: Use peacock feathers to make a fly',
        #    [row.text for row in rows]
        #)

        # Merlin is curious if the site will remember his list
        # He notices some explanatory text that the site has generated a unique url for him
        #self.fail('Finish the test!')

        # He visits that URL - her to-do list is still there.

        # Content with this, he returns to reading his spell book. 
        self.fail('Finish the test!')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Merlin starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # He notices that hisr list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:  
            try:
                table = self.browser.find_element_by_id('id_list_table')  
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return  
            except (AssertionError, WebDriverException) as e:  
                if time.time() - start_time > MAX_WAIT:  
                    raise e  
                time.sleep(0.5)  

    def test_layout_and_styling(self):        
        # Edith goes to the home page        
        self.browser.get(self.live_server_url)        
        self.browser.set_window_size(1024, 768)        
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

    # She starts a new list and sees the input is nicely
    # centered there too
    

#if __name__ == '__main__':
#    unittest.main(warnings='ignore')
