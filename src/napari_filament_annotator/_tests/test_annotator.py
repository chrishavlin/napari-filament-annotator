import os

import numpy as np
import pandas as pd
import pytest
from napari_filament_annotator import AnnotatorWidget
from napari_filament_annotator.utils.const import COLS
from napari_filament_annotator.utils.io import annotation_to_pandas


# make_napari_viewer is a pytest fixture that returns a napari viewer object
# capsys is a pytest fixture that captures stdout and stderr output streams
@pytest.fixture
def annotator_widget(make_napari_viewer, capsys):
    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()
    widget = AnnotatorWidget(viewer)
    widget.add_annotation_layer()
    assert widget.annotation_layer_exists() is False
    return widget


@pytest.fixture
def annotator_widget_with_image(annotator_widget):
    annotator_widget.viewer.add_image(np.random.randint(0, 100, (50, 100, 100)))
    return annotator_widget


@pytest.fixture
def annotator(annotator_widget_with_image):
    annotator_widget_with_image.add_annotation_layer()
    assert annotator_widget_with_image.annotation_layer_exists()
    return annotator_widget_with_image.annotator


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


def test_params(annotator):
    # test that all parameters are set
    params = ['scale', 'sigma', 'line_width', 'alpha',
              'beta', 'gamma', 'n_iter', 'n_interp', 'end_coef', 'remove_corners']
    for param in params:
        assert param in vars(annotator.params)
    assert len(annotator.params.scale) == len(annotator.params.sigma) == 3


def test_add_annotation_layer(annotator_widget):
    # call "add annotation layer" without image and assert no shape layers were added
    annotator_widget.add_annotation_layer()
    assert annotator_widget.annotation_layer_exists() is False

    # add an image
    annotator_widget.viewer.add_image(np.random.randint(0, 100, (50, 100, 100)))

    # call "add annotation layer" again and assert a new shape layer was added
    annotator_widget.add_annotation_layer()
    assert annotator_widget.annotation_layer_exists()


def test_maxval(annotator_widget_with_image):
    annotator_widget_with_image.sld.setValue(50)
    assert annotator_widget_with_image.get_image_layer().data.max() == 50


def test_io(annotator_widget_with_image, tmp_path, paths):
    fn = os.path.join(tmp_path, 'annotations.csv')
    df = annotation_to_pandas(paths)
    df.to_csv(fn)
    annotator_widget_with_image.load_annotations(fn)
    assert annotator_widget_with_image.annotation_layer_exists()
    assert len(annotator_widget_with_image.annotation_layer.data) - 1 == len(paths)

    annotator_widget_with_image.get_annotation_filename(fn)
    df2 = pd.read_csv(fn)
    assert (df[COLS].values == df2[COLS].values).all()
