import docker
import pytest

from sgrid import SeleniumGrid


@pytest.fixture(scope='function')
def client():
    return docker.from_env()


@pytest.fixture(scope='module')
def single_grid():
    with SeleniumGrid(num_nodes=1) as grid:
        yield grid
