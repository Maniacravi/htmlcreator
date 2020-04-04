import os
import pathlib

import numpy as np
import pandas as pd
from PIL import Image

from htmlcreator import HTMLDocument

np.random.seed(123)

_TEST_IMAGE_PATH = '_test_image.jpg'
_TEST_DOCUMENT_PATH = '_test_document.html'


def test_HTMLDocument():
    document = HTMLDocument()

    assert document.style != ''

    document.set_title(title='title')

    document.add_header(header='header', level='h2', align='left')

    document.add_text(text='text', size='15px', indent='0', align='left')

    document.add_line_break()

    document.add_page_break()

    document.add_table(df=_get_df())

    try:
        document.add_table(df=[_get_df()])
    except Exception as e:
        assert isinstance(e, TypeError)
        assert str(e) == "df is of type <class 'list'>, but it should be of type <class 'pandas.core.frame.DataFrame'>."

    document.add_image(image=_get_image_array(), title='title', height=320, width=480, pixelated=False)

    document.add_image(image=_get_PIL_Image())

    _create_test_image()

    document.add_image(image=_TEST_IMAGE_PATH)

    document.add_image(image=pathlib.Path(_TEST_IMAGE_PATH))

    _remove_test_image()

    try:
        document.add_image(image=_get_image_array().astype(np.float32))
    except Exception as e:
        assert isinstance(e, RuntimeError)
        assert str(e) == 'image.dtype is float32, but it should be uint8.'

    try:
        document.add_image(image=np.random.randint(0, 256, size=(1, 200, 200, 3)).astype(np.uint8))
    except Exception as e:
        assert isinstance(e, RuntimeError)
        assert str(e) == 'image.ndim is 4, but it should be 2 or 3.'

    try:
        document.add_image(image=[_get_image_array()])
    except Exception as e:
        assert isinstance(e, TypeError)
        assert str(e) == "image is of type <class 'list'>, but it should be one of: <class 'numpy.ndarray'>, <class 'PIL.Image.Image'>, <class 'pathlib.Path'> or <class 'str'>."

    document.write(_TEST_DOCUMENT_PATH)

    assert os.path.exists(_TEST_DOCUMENT_PATH)

    _remove_test_document()


def _get_df():
    num_rows = 5
    num_cols = 10
    df = pd.DataFrame(
        data=np.random.randn(num_rows, num_cols),
        index=pd.date_range('19700101', periods=num_rows),
        columns=[f'c{i}' for i in range(num_cols)],
    )
    df['col_str'] = 'value_str'
    return df


def _get_image_array():
    return np.random.randint(0, 256, size=(200, 200, 3)).astype(np.uint8)


def _get_PIL_Image():
    return Image.fromarray(_get_image_array())


def _create_test_image():
    _get_PIL_Image().save(_TEST_IMAGE_PATH)


def _remove_test_image():
    if os.path.exists(_TEST_IMAGE_PATH):
        os.remove(_TEST_IMAGE_PATH)


def _remove_test_document():
    if os.path.exists(_TEST_DOCUMENT_PATH):
        os.remove(_TEST_DOCUMENT_PATH)
