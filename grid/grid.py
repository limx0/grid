
import os
import time
import subprocess
from selenium.webdriver import Remote
from retrying import retry


COMPOSE_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docker-compose.yml')


def start_grid(num_nodes=1):
    print('Starting grid with %s nodes' % num_nodes)
    subprocess.check_output('docker-compose -f %s up -d --scale chrome=%s' % (COMPOSE_FILE, num_nodes))
    print(subprocess.check_output('docker ps').decode('UTF-8'))


def stop_grid():
    print('Stopping grid')
    subprocess.check_output('docker-compose -f %s down' % COMPOSE_FILE)


class SeleniumGrid:
    def __init__(self, num_nodes=1):
        self.num_nodes = num_nodes

    def __enter__(self):
        try:
            start_grid(self.num_nodes)
        except Exception as e:
            print(e, 'ere')

    def __exit__(self, *args):
        # stop_grid()
        pass


@retry(stop_max_attempt_number=10, wait_fixed=500)
def connect_to_grid():
    return Remote('http://127.0.0.1:4444/wd/hub', desired_capabilities={'browserName': 'chrome'})


def grid_request(url, extra_sleep=None):
    driver = connect_to_grid()
    driver.get(url)
    if extra_sleep:
        time.sleep(extra_sleep)
    source = driver.page_source
    driver.quit()
    return source
