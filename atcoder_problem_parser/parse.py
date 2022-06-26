from typing import List
import bs4


class Parser:
    def __init__(self):
        pass


def parse(text: str) -> List[str]:
    """Parse the html and extract destination paragraphs

    Args:
        - text (str): HTML document for parse.

    Returns:
        - List[str]: The result of parse.
    """
    # Parse the html document by using BeautifulSoup4
    soup = bs4.BeautifulSoup(text, "html.parser")

    # List for containing the parse result
    # At first, try to extract problem statements
    result: List[str] = ["### 問題文", ""]
    for element in soup.select(
        "h3:-soup-contains('問題文') ~ p, h3:-soup-contains('問題文') ~ ul, h3:-soup-contains('問題文') ~ ol"
    ):
        if element.name == "p":
            result.extend(parse_p(element))
            result.append("> ")
        elif element.name == "ul":
            result.extend(parse_itemize(element, "ul"))
            result.append("> ")
        elif element.name == "ol":
            result.extend(parse_itemize(element, "ol"))

    # Make trailing line blank.
    if result[-1] == "> ":
        result[-1] = ""

    # Next, try to extract problem constraints statements
    result.extend(["### 制約", ""])

    # Extract logic is same as above
    # Assuming that <br> tag doesn't exist in constraints statements
    constraint = soup.select("h3:-soup-contains('制約') ~ ul > li")
    for p in constraint:
        strings = []
        for t in p:
            if isinstance(t, bs4.element.NavigableString):
                strings.append(str(t).strip())
            elif isinstance(t, bs4.element.Tag):
                if t.name == "var":
                    strings.append("$" + str(t.get_text(strip=True)) + "$")
                elif t.name == "code":
                    strings.append("`" + str(t.get_text(strip=True)) + "`")
        result.append("> - " + "".join(strings))
    result.append("")

    return result
