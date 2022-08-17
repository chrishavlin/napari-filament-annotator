import os
import shutil
import tempfile

import numpy as np
import pytest


@pytest.fixture(scope='module')
def polygons():
    return [[[([0., 73., 12.]),
              ([0., 73., 25.]),
              ([0., 73., 38.]),
              ([0., 73., 55.]),
              ([0., 73., 69.])],
             [([100., 85., 12.]),
              ([100., 85., 25]),
              ([100., 85., 38]),
              ([100., 85., 55.]),
              ([100., 85., 69.])]],
            [[([0., 85., 15.]),
              ([0., 85., 29.]),
              ([0., 85., 41.]),
              ([0., 85., 54.]),
              ([0., 85., 61.]),
              ([0., 85., 72.])],
             [([100., 73., 15.]),
              ([100., 73., 29.]),
              ([100., 73., 41.]),
              ([100., 73., 54.]),
              ([100., 73., 61.]),
              ([100., 73., 72.])]]]


@pytest.fixture(scope='module')
def tetragons(polygons):
    npt1 = polygons[0][0]
    npt2 = polygons[1][0]
    fpt1 = polygons[0][1]
    fpt2 = polygons[1][1]

    p1 = [npt1[0], npt1[1], fpt1[1], fpt1[1]]
    p2 = [npt2[0], npt2[1], fpt2[1], fpt2[0]]
    return p1, p2


@pytest.fixture(scope='module')
def paths():
    n = np.random.randint(5, 10)
    paths = []
    for i in range(n):
        l = np.random.randint(10, 15)
        path = np.random.randint(0, 100, (l, 3))
        paths.append(path)
    return paths


@pytest.fixture(scope='module')
def tmp_path():
    path = tempfile.mkdtemp()
    os.makedirs(path, exist_ok=True)
    yield path
    shutil.rmtree(path)
