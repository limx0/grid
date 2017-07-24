
import docker
from grid import start_grid, stop_grid, SeleniumGrid, grid_request

client = docker.from_env()
stop_grid()


def test_grid_start():
    start_grid(4)
    container_names = [c.name for c in client.containers.list()]
    assert all(x in container_names for x in ['hub'] + ['grid_chrome_%s' % i for i in range(1, 4)])


def test_grid_stop():
    start_grid(1)
    stop_grid()
    container_names = [c.name for c in client.containers.list()]
    assert not any(x in container_names for x in ['hub'] + ['grid_chrome_%s' % i for i in range(1, 4)])


def test_context_mgr():
    url = 'https://www.google.com'
    n_nodes = 1
    with SeleniumGrid(num_nodes=n_nodes):
        resps = [grid_request(url) for _ in range(n_nodes)]
    assert resps