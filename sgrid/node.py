import docker
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from sgrid.core import RequestBase
from sgrid.util import ping_service


class SeleniumNode(RequestBase):
    client = docker.from_env()

    def __init__(self, image="selenium/standalone-chrome", proxy=None):
        self.image = image
        self.container = None
        self.proxy = proxy

    @property
    def desired_capabilities(self):
        desired_capabilities = DesiredCapabilities.CHROME
        if self.proxy:
            desired_capabilities["proxy"] = {
                "httpProxy": self.proxy,
                "ftpProxy": self.proxy,
                "sslProxy": self.proxy,
                "noProxy": None,
                "proxyType": "MANUAL",
                "class": "org.openqa.selenium.Proxy",
                "autodetect": False,
            }
        return desired_capabilities

    def start(self):
        self.container = self.client.containers.run(
            image=self.image, ports={4444: None}, detach=True, shm_size="2g"
        )
        addr = self.client.api.inspect_container(self.container.id)["NetworkSettings"][
            "Ports"
        ]["4444/tcp"]
        url = "http://%s:%s/wd/hub" % (addr[0]["HostIp"], addr[0]["HostPort"])
        ping_service(url)
        self.driver = webdriver.Remote(
            command_executor=url, desired_capabilities=self.desired_capabilities
        )

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.driver.quit()
        self.container.stop()
        self.container.remove()

    def get(self, **kwargs):
        return self.driver.get(**kwargs)
