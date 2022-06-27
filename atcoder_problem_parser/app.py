from typing import List
from .parse import Parser


class App:
    """
    App class

    Args
    """

    def __init__(self, html: str):
        """
        Args:
            - html (str): HTML string to be parsed.
        """
        self.html: str = html

    def transform(self, quote=True) -> List[str]:
        """
        Parse and format the parse result.

        Args:
            - quote (bool): Whether the output Markdown should be in citation format. Default is True.
        """

        # Parse the HTML
        parser = Parser(self.html)
        result: List[str] = parser.problem() + parser.constraint()

        # Put the entire Markdown text into citation format
        if quote:
            result = ["> " + s for s in result]

        return result
