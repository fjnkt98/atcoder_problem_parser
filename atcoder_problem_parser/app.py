from typing import List
from .parse import Parser


class App:
    def __init__(self, html: str):
        self.html: str = html

    def transform(self, quote=True) -> List[str]:
        """
        結果を返す関数

        """

        parser = Parser(self.html)

        result: List[str] = parser.problem() + parser.constraint()

        if quote:
            result = ["> " + s for s in result]

        return result
