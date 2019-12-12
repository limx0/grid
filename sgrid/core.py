import json
from typing import Union

from seleniumwire import webdriver


class RequestBase:
    driver: Union[webdriver.Remote, webdriver.Chrome, webdriver.Firefox]

    def get(self, url, **kwargs):
        raise NotImplementedError()

    def check_resp(self):
        for request in self.driver.requests:
            if request.response:
                print(
                    request.path,
                    request.response.status_code,
                    request.response.headers['Content-Type']
                )

    def get_page_source(self, url, **kwargs):
        self.get(url=url, **kwargs)
        self.check_resp()
        return self.driver.page_source

    def get_json(self, url, **kwargs):
        self.get(url=url, **kwargs)
        body = self.driver.find_element_by_tag_name("body")
        return json.loads(body.text)
