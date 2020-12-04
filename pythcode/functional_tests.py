from selenium import webdriver
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

        # He notices the page titl and header mention to-lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # He is able to add to-do items straight away


        # He types "Obtain eye of newt" into the text box
        # (Merlin's hobby is magic)

        # When he presses enter, the page updates, and it now lists the item
        # "1: Obtain eye of newt" as an item in a to-do list

        # There is still a text box avaliable for use.
        # He enters "Combine all ingredients in cauldron"

        # The page updates again, and now shows both items on his list

        # Merlin is curious if the site will remember his list
        # He notices some explanatory text that the site has generated a unique url for him

        # He visits that URL - her to-do list is still there.

        # Content with this, he returns to reading his spell book. 

if __name__ == '__main__':
    unittest.main(warnings='ignore')
