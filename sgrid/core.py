import json
from typing import Union

from selenium import webdriver


class RequestBase:
    driver: Union[webdriver.Remote, webdriver.Chrome, webdriver.Firefox]

    def get(self, url, **kwargs):
        raise NotImplementedError()

    def get_page_source(self, url, **kwargs):
        self.get(url=url, **kwargs)
        return self.driver.page_source

    def get_json(self, url, **kwargs):
        self.get(url=url, **kwargs)
        body = self.driver.find_element_by_tag_name("body")
        return json.loads(body.text)
