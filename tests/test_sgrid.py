import subprocess

import pytest

from sgrid import SeleniumGrid, SeleniumNode, grid_request


@pytest.fixture(scope='function', autouse=True)
def check_docker_running():
    assert subprocess.check_output(['docker', '-v'])


def test_grid_start_and_stop(client):
    def container_exists(name):
        return any(c.name.startswith(name) for c in client.containers.list())

    required = [
        'hub',
        'sgrid_chrome_1',
        'sgrid_chrome_2'
    ]
    with SeleniumGrid(num_nodes=2, shutdown_on_exit=True):
        assert all(map(container_exists, required))

    assert not any(map(container_exists, required))


def test_context_mgr(single_grid):
    resp = grid_request('https://www.google.com')
    assert resp


def test_selenium_node():
    with SeleniumNode() as node:
        node.driver.get('https://www.google.com')
        assert 'https://www.google.com' in node.driver.page_source


def test_proxy(proxy):
    with SeleniumNode(proxy=proxy['http']) as node:
        ip_addr_proxy = node.get_json('https://ifconfig.me/all.json')['ip_addr']

    assert ip_addr_proxy == proxy['http'].split(':')[0]
