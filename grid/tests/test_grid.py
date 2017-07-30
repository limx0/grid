
import docker
from grid import Grid, grid_request

client = docker.from_env()


def test_compose_binary():
    g = Grid()
    assert g.compose_binary.endswith('/bin/docker-compose')


def test_grid_start():
    with Grid():
        container_names = [c.name for c in client.containers.list()]
        assert all(x in container_names for x in ['hub'] + ['grid_chrome_%s' % i for i in range(1, 4)])


def test_grid_stop():
    with Grid(shutdown_on_exit=True):
        container_names = [c.name for c in client.containers.list()]
    assert not any(x in container_names for x in ['hub'] + ['grid_chrome_%s' % i for i in range(1, 4)])


def test_context_mgr():
    url = 'https://www.google.com'
    n_nodes = 1
    with Grid(num_nodes=n_nodes):
        resps = [grid_request(url) for _ in range(n_nodes)]
    assert resps