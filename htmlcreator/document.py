import base64
import pathlib
from io import BytesIO
from typing import Optional, Union

import numpy as np
import pandas as pd
import PIL
from PIL import Image


class HTMLDocument:
    """HTML Document class."""

    def __init__(self) -> None:
        self.style = ''
        self.title = self.__class__.__name__
        self.head = ''
        self.body = ''
        self._set_default_style()

    def __str__(self) -> str:
        return (
            '<!DOCTYPE html>\n'
            '<html lang="en">\n'
            '<head>\n'
            '<meta charset="UTF-8">\n'
            f'<title>{self.title}</title>\n'
            f'<style type="text/css">\n{self.style}</style>\n'
            f'{self.head}'
            '</head>\n'
            '<body>\n'
            f'{self.body}'
            '</body>\n'
            '</html>\n'
        )

    def add_header(
        self,
        header: str,
        level: str = 'h2',
        align: str = 'left',
    ) -> None:
        """Add header."""
        self.body += (
            f'<{level} style="text-align: {align}">'
            f'{header}'
            f'</{level}>\n'
        )

    def add_text(
        self,
        text: str,
        size: str = '16px',
        indent: str = '0',
        align: str = 'left',
    ) -> None:
        """Add text paragraph."""
        self.body += (
            f'<p style="font-size:{size}; text-indent: {indent}; text-align: {align}">'
            f'{text}'
            f'</p>\n'
        )

    def add_line_break(self) -> None:
        """Add line break."""
        self.body += '<br>\n'

    def add_page_break(self) -> None:
        """Add page break."""
        self.body += '<p style="page-break-after: always;">&nbsp;</p>\n'

    def add_table(self, df: pd.DataFrame) -> None:
        """Embed pandas DataFrame."""
        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f'df is of type {type(df)}, but it should be of type {pd.DataFrame}.'
            )
        self.body += (
            '<div class="pandas-dataframe">\n'
            f'{df.to_html()}\n'
            '</div>\n'
        )

    def add_image(
        self,
        image: Union[np.ndarray, PIL.Image.Image, pathlib.Path, str],
        title: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
        pixelated: bool = False,
    ) -> None:
        """Embed image."""
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
        image_tag += '">\n'
        self.body += image_tag

    def set_style(self, style: str) -> None:
        """Set CSS style."""
        self.style = style

    def set_title(self, title: str) -> None:
        """Set title."""
        self.title = title

    def write(self, filepath: str) -> None:
        """Save to filepath."""
        with open(filepath, 'w') as f:
            f.write(str(self))

    def _encode_image(
        self,
        image: Union[np.ndarray, PIL.Image.Image, pathlib.Path, str],
    ) -> str:
        """Encode image to base64 string."""
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

    def _set_default_style(self) -> None:
        """Set default style."""
        self_filename = pathlib.Path(__file__)
        self_filepath = self_filename.resolve()
        package_dirpath = self_filepath.parent
        style_filepath = package_dirpath / 'style.css'
        with open(str(style_filepath)) as f:
            style = f.read()
        self.set_style(style)
