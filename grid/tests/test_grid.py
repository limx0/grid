
import docker
from operator import attrgetter
from grid import SeleniumGrid, grid_request

client = docker.from_env()


def test_grid_start_and_stop():
    n_nodes = 2
    list_names = ['hub'] + ['grid_chrome_%s' % i for i in range(1, n_nodes + 1)]
    with SeleniumGrid(num_nodes=n_nodes, shutdown_on_exit=True):
        assert all(name in map(attrgetter('name'), client.containers.list()) for name in list_names)
    assert not any(name in map(attrgetter('name'), client.containers.list()) for name in list_names)


def test_context_mgr():
    url = 'https://www.google.com'
    n_nodes = 1
    with SeleniumGrid(num_nodes=n_nodes):
        resps = [grid_request(url) for _ in range(n_nodes)]
    assert resps