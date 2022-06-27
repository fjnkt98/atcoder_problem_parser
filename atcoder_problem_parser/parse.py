from typing import List, Set
import bs4
import re

inlines: Set[str] = {
    "a",
    "addr",
    "acronym",
    "b",
    "basefont",
    "bdo",
    "big",
    "br",
    "cite",
    "code",
    "dfn",
    "em",
    "font",
    "i",
    "img",
    "input",
    "kbd",
    "label",
    "q",
    "s",
    "stamp",
    "select",
    "small",
    "span",
    "strike",
    "strong",
    "sub",
    "sup",
    "textarea",
    "tt",
    "u",
    "var",
}


class Parser:
    def __init__(self, html: str):
        self.raw_html: str = html

        entire_body = bs4.BeautifulSoup(html, "html.parser")

        self.problem_html = entire_body.select_one(
            "div.part:has(h3:-soup-contains('問題文')) > section"
        )
        self.constraint_html = entire_body.select_one(
            "div.part:has(h3:-soup-contains('制約')) > section"
        )

        self.problem_markdown: List[str] = self.parse(self.problem_html)
        self.constraint_markdown: List[str] = self.parse(self.constraint_html)

    def problem(self) -> List[str]:
        return self.problem_markdown

    def constraint(self) -> List[str]:
        return self.constraint_markdown

    def parse(self, element: bs4.element.Tag) -> List[str]:
        result: List[str] = []

        buffer: List[str] = []
        for e in element.children:
            if isinstance(e, bs4.element.Tag) and e.name not in inlines:
                result.extend(self.parse(e))

            if isinstance(e, bs4.element.NavigableString):
                buffer.append(str(e).strip())
            else:
                if e.name == "code":
                    buffer.append("`" + str(e.get_text(strip=True)) + "`")
                elif e.name == "var":
                    # When the element is <var>, format it as katex literal and append it.
                    buffer.append("$" + str(e.get_text(strip=True)) + "$")
                elif e.name == "br":
                    # When the element is <br>, break this line.
                    # Store the line with leading quotation mark.
                    buffer.append("  \n")
                elif e.name == "strong":
                    buffer.append("**" + str(e.get_text(strip=True)) + "**")

        if "".join(buffer) != "":
            result.append("".join(buffer))

        if element.name == "p":
            result.append("")
        elif element.name == "blockquote":
            result = ["> " + s for s in result]
            result.append("")
        elif element.name == "ul":
            result = ["- " + s for s in result]
            result.append("")
        elif element.name == "ol":
            result = ["1. " + s for s in result]
            result.append("")
        else:
            m = re.search(r"h(\d)", element.name)
            if m is not None:
                result = ["#" * int(m.groups()[0]) + " " + s for s in result]
                result.append("")

        return result
