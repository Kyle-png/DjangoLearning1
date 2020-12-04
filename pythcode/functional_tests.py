from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVistorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Merlin heard about an online to-do app. 
        # He goes to the homepage
        self.browser.get('http://localhost:8000')

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
        inputbox.send_keys('Buy peacock feathers')

        # When he presses enter, the page updates, and it now lists the item
        # "1: Obtain eye of newt" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )

        # There is still a text box avaliable for use.
        # He enters "Combine all ingredients in cauldron"
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on his list

        # Merlin is curious if the site will remember his list
        # He notices some explanatory text that the site has generated a unique url for him

        # He visits that URL - her to-do list is still there.

        # Content with this, he returns to reading his spell book. 

if __name__ == '__main__':
    unittest.main(warnings='ignore')
