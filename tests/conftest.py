import time

import docker
import lxml.html
import pytest
import requests

from sgrid import SeleniumGrid


@pytest.fixture(scope='function')
def client():
    return docker.from_env()


@pytest.fixture(scope='module')
def single_grid():
    with SeleniumGrid(num_nodes=1) as grid:
        yield grid


def proxy_list():
    resp = requests.get('https://free-proxy-list.net/', headers={'User-Agent': 'Mozilla/5.0'})
    tree = lxml.html.fromstring(resp.content)
    return [(x[0], x[1]) for x in [row.xpath('.//text()') for row in tree.xpath('//tbody//tr')]]


@pytest.fixture(scope='function')
def proxy():
    for host, port in proxy_list():
        proxies = {'http': f'{host}:{port}', 'https': f'{host}:{port}'}
        resp = requests.get('http://ifconfig.me/ip', proxies=proxies)
        ip = resp.content.decode()
        if host == ip:
            return proxies
        time.sleep(2)
