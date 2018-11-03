
from sgrid import SeleniumGrid, SeleniumNode, grid_request


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
