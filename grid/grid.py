
import os
import subprocess

compose_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docker-compose.yml')


def start_grid(num_nodes):
    subprocess.check_output('docker-compose -f %s up -d --scale chrome=%s' % (compose_filename, num_nodes))


def stop_grid():
    subprocess.check_output('docker-compose down')


class SeleniumGrid:
    def __init__(self, worker_count):
        self.worker_count = worker_count

    def __enter__(self):
        start_grid(self.worker_count)

    def __exit__(self, *args):
        stop_grid()


if __name__ == '__main__':
    start_grid(num_nodes=4)
    stop_grid()
