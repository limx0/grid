
import os
import time
import subprocess
from selenium.webdriver import Remote
from retrying import retry


class SeleniumGrid:

    _compose_binary = None
    _compose_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docker-compose.yml')

    def __init__(self, num_nodes=1, shutdown_on_exit=False):

        self.num_nodes = num_nodes
        self.shutdown_on_exit = shutdown_on_exit

    def __enter__(self):
        self.start_grid(self.num_nodes)

    def __exit__(self, *args):
        if self.shutdown_on_exit:
            self.stop_grid()

    @property
    def compose_binary(self):
        if self._compose_binary is None:
            if 'DOCKER_COMPOSE_BIN' in os.environ:
                self._compose_binary = os.environ['DOCKER_COMPOSE_BIN']
            else:
                self._compose_binary = 'docker-compose'
        return self._compose_binary

    def compose_call(self, command):
        cmd = (
            '{compose_binary} -f {compose_file} {command}'
            .format(compose_binary=self.compose_binary, compose_file=self._compose_file, command=command)
        )
        return subprocess.check_output(cmd, shell=True)

    def start_grid(self, num_nodes=1):
        print('Starting grid with %s nodes' % num_nodes)
        self.compose_call('up -d --scale chrome={num_nodes}'.format(num_nodes=num_nodes))
        print(subprocess.check_output('docker ps', shell=True).decode('UTF-8'))

    def stop_grid(self):
        print('Stopping grid')
        self.compose_call('down')


@retry(stop_max_attempt_number=10, wait_fixed=500)
def get_remote_grid_driver():
    return Remote('http://127.0.0.1:4444/wd/hub', desired_capabilities={'browserName': 'chrome'})


def grid_request(url, extra_sleep=None):
    driver = get_remote_grid_driver()
    driver.get(url)
    if extra_sleep:
        time.sleep(extra_sleep)
    source = driver.page_source
    driver.quit()
    return source
