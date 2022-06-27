from typing import List, Set
import bs4
import re

# Tag names of HTML elements that are inline elements
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
    """Parser class"""

    def __init__(self, html: str):
        """
        Args:
            - html (str): HTML string to be parsed.
        """
        # Copy the html string.
        self.raw_html: str = html

        # Create BeautifulSoup4 instance
        entire_body = bs4.BeautifulSoup(html, "html.parser")

        # Get the part of problem sentence
        self.problem_html = entire_body.select_one(
            "div.part:has(h3:-soup-contains('問題文')) > section"
        )
        # Get the part of constraint sentence
        self.constraint_html = entire_body.select_one(
            "div.part:has(h3:-soup-contains('制約')) > section"
        )

        # Parse the problem sentence
        self.problem_markdown: List[str] = self.parse(self.problem_html)
        # Parse the constraint sentence
        self.constraint_markdown: List[str] = self.parse(self.constraint_html)

    def problem(self) -> List[str]:
        """
        Return the parse result of the problem sentence.

        Returns:
            List[str]: Markdown formatted sentences.
        """
        return self.problem_markdown

    def constraint(self) -> List[str]:
        """
        Return the parse result of the constraint sentence.

        Returns:
            List[str]: Markdown formatted sentences.
        """
        return self.constraint_markdown

    def parse(self, element: bs4.element.Tag) -> List[str]:
        """Parse the HTML tree recursively.

        Args:
            - element (BeautifulSoup4.element.Tag): HTML tag to be parse.

        Returns:
            List[str]: Result of parsing the partial tree below the
            specified HTML tag.
        """
        # List for retaining the parse result.
        result: List[str] = []

        # Buffer list to hold results during parse processing
        buffer: List[str] = []

        # Traversing the children of the element
        for e in element.children:
            # If it's a block element tag, explore recursively.
            if isinstance(e, bs4.element.Tag) and e.name not in inlines:
                result.extend(self.parse(e))

            # If it's a plain string, buffer it.
            if isinstance(e, bs4.element.NavigableString):
                buffer.append(str(e).strip())
            else:
                # Convert each inline tag to corresponding Markdown format
                if e.name == "code":
                    buffer.append("`" + str(e.get_text(strip=True)) + "`")
                elif e.name == "var":
                    # When the element is <var>, format it as katex literal and append it.
                    buffer.append("$" + str(e.get_text(strip=True)) + "$")
                elif e.name == "br":
                    buffer.append("  \n")
                elif e.name == "strong":
                    buffer.append("**" + str(e.get_text(strip=True)) + "**")

        # When the buffer is not empty, append it to result.
        if "".join(buffer) != "":
            result.append("".join(buffer))

        # Convert to the corresponding Markdown format
        # depending on the type of the block element.
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

        # Return the result
        return result
