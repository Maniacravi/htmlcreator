import base64
import pathlib
from io import BytesIO

import numpy as np
import PIL
from PIL import Image


class HTMLDocument:

    def __init__(self):
        self.style = ''
        self.title = self.__class__.__name__
        self.head = ''
        self.body = ''
        self._set_default_style()

    def __str__(self):
        return (
            '<!DOCTYPE html>\n'
            '<html lang="en">\n'
            '<head>\n'
            '<meta charset="UTF-8">\n'
            f'<title> {self.title} </title>\n'
            f'<style type="text/css">\n{self.style}</style>\n'
            f'{self.head}'
            '</head>\n'
            '<body>\n'
            f'{self.body}'
            '</body>\n'
            '</html>\n'
        )

    def add_header(self, header, level='h2', align='left'):
        self.body += (
            f'<{level} style="text-align: {align}">'
            f'{header}'
            f'</{level}>\n'
        )

    def add_text(self, text, indent='0', align='left'):
        self.body += (
            f'<p style="text-indent: {indent}; text-align: {align}">'
            f'{text}'
            f'</p>\n'
        )

    def add_line_break(self):
        self.body += '<br>\n'

    def add_page_break(self):
        self.body += '<p style="page-break-after: always;">&nbsp;</p>\n'

    def add_table(self, df):
        self.body += f'{df.to_html()}\n'

    def add_image(self, image, title=None, height=None, width=None, pixelated=False):
        image_encoded_str = self._encode_image(image)
        image_tag = f'<img src="data:image/png;base64, {image_encoded_str}"'
        if title:
            image_tag += f' title={title}'
        if height:
            image_tag += f' height={height}'
        if width:
            image_tag += f' width={width}'
        image_tag += ' style="border:1px solid #021a40; margin: 3px 3px'
        if pixelated:
            image_tag += '; image-rendering: pixelated'
        image_tag += '"'
        image_tag += '>\n'
        self.body += image_tag

    def set_style(self, style):
        self.style = style

    def set_title(self, title):
        self.title = title

    def write(self, filepath):
        with open(filepath, 'w') as f:
            f.write(str(self))

    def _encode_image(self, image):
        if isinstance(image, np.ndarray):
            if image.dtype != np.uint8:
                raise RuntimeError(
                    f'image.dtype is {image.dtype}, but it should be uint8.'
                )
            if not (image.ndim == 2 or image.ndim == 3):
                raise RuntimeError(
                    f'image.ndim is {image.ndim}, but it should be 2 or 3.'
                )
            buff = BytesIO()
            Image.fromarray(image).save(buff, format='PNG')
            encoded = base64.b64encode(buff.getvalue())
        elif isinstance(image, PIL.Image.Image):
            buff = BytesIO()
            image.save(buff, format='PNG')
            encoded = base64.b64encode(buff.getvalue())
        elif isinstance(image, pathlib.Path):
            encoded = base64.b64encode(open(str(image), 'rb').read())
        elif isinstance(image, str):
            encoded = base64.b64encode(open(image, 'rb').read())
        else:
            raise TypeError(
                f'image is of type {type(image)}, but it should be one of: '
                f'{np.ndarray}, {PIL.Image.Image}, {pathlib.Path} or {str}.'
            )
        image_encoded_str = encoded.decode('utf-8')
        return image_encoded_str

    def _set_default_style(self):
        self_filename = pathlib.Path(__file__)
        self_filepath = self_filename.resolve()
        package_dirpath = self_filepath.parent
        style_filepath = package_dirpath / 'style.css'
        with open(str(style_filepath)) as f:
            style = f.read()
        self.set_style(style)
