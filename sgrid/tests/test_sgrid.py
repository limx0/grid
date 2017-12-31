
from sgrid import SeleniumGrid, grid_request


def test_grid_start_and_stop(client):
    required = ['hub', 'sgrid_chrome_1', 'sgrid_chrome_2']
    with SeleniumGrid(num_nodes=2, shutdown_on_exit=True):
        container_names = [c.name for c in client.containers.list()]
        assert all(name in container_names for name in required)

    container_names = [c.name for c in client.containers.list()]
    assert not any(name in container_names for name in required)


def test_context_mgr(single_grid):
    resp = grid_request('https://www.google.com')
    assert resp
