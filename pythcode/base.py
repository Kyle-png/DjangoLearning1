    def wait_for(self, fn):          start_time = time.time()        while True:            try:                table = self.browser.find_element_by_id('id_list_table')                  rows = table.find_elements_by_tag_name('tr')                self.assertIn(row_text, [row.text for row in rows])                return            except (AssertionError, WebDriverException) as e:                if time.time() - start_time > MAX_WAIT:                    raise e                time.sleep(0.5)