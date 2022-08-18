import numpy as np
import pytest

from napari_filament_annotator import AnnotatorWidget


# make_napari_viewer is a pytest fixture that returns a napari viewer object
# capsys is a pytest fixture that captures stdout and stderr output streams
@pytest.fixture
def annotator(make_napari_viewer, capsys):
    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()

    widget = AnnotatorWidget(viewer)
    viewer.add_image(np.random.random((12, 100, 100)))
    widget.add_annotation_layer()
    return widget.annotator


def test_add_delete(annotator, polygons):
    layer = annotator.annotation_layer
    assert layer.nshapes == 1

    annotator.near_points = polygons[0][0].copy()
    annotator.far_points = polygons[0][1].copy()
    annotator.draw_polygon(layer)
    assert layer.nshapes == 2

    annotator.delete_the_last_point(layer)
    assert layer.nshapes == 2
    assert len(polygons[0][0]) == len(annotator.near_points) + 1 == len(annotator.far_points) + 1

    annotator.delete_the_last_shape(layer)
    assert layer.nshapes == 1


def test_intersection(annotator, polygons):
    layer = annotator.annotation_layer
    annotator.near_points = polygons[0][0].copy()
    annotator.far_points = polygons[0][1].copy()
    assert len(annotator.near_points) > 0
    annotator.draw_polygon(layer)
    annotator.calculate_intersection(layer)
    assert layer.nshapes == 2
    assert len(annotator.polygons) == 1
    assert len(annotator.near_points) == len(annotator.far_points) == 0

    annotator.near_points = polygons[1][0].copy()
    annotator.far_points = polygons[1][1].copy()
    annotator.draw_polygon(layer)
    annotator.calculate_intersection(layer)
    assert layer.nshapes == 2
    assert len(annotator.near_points) == len(annotator.far_points) == len(annotator.polygons) == 0