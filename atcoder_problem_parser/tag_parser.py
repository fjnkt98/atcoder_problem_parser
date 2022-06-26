from typing import List
import bs4


def parse_p(element: bs4.element.Tag) -> List[str]:
    """Parse <p> tag into some paragraphs.

    Args:
        element (bs4.element.Tag): <p> tag to parse.
        It must be a <p> tag.

    Returns:
        List[str]: Paragraphs formatted for markdown.
    """

    assert element.name == "p"

    # List retaining the formatted paragraphs
    result: List[str] = []

    # Buffer list
    buffer: List[str] = []
    # Get each elements in <p> tag
    for e in element:
        if isinstance(e, bs4.element.NavigableString):
            # When the element is just a text, simply append it as a string.
            buffer.append(str(e).strip())
        elif e.name == "code":
            # When the element is <code>, format it as markdown code block and append it.
            buffer.append("`" + str(e.get_text(strip=True)) + "`")
        elif e.name == "var":
            # When the element is <var>, format it as katex literal and append it.
            buffer.append("$" + str(e.get_text(strip=True)) + "$")
        elif e.name == "br":
            # When the element is <br>, break this line.
            # Store the line with leading quotation mark.
            result.append("> " + "".join(buffer))
            buffer.clear()

    # Empty check
    if buffer:
        result.append("> " + "".join(buffer))
        buffer.clear()

    return result


def parse_itemize(element: bs4.element.Tag, type: str = "ul") -> List[str]:
    """Parse <ul> or <ol> tag into some list items.

    This function supports nested and mixed itemize.

    Args:
        element (bs4.element.Tag): <ul> or <ol>tag to parse.

    Returns:
        List[str]: List items formatted for markdown.

    """

    # List retaining the formatted list items.
    result: List[str] = []
    # Prefix string for markdown list items.
    assert type == "ul" or type == "ol"
    prefix: str = "- " if type == "ul" else "1. "

    # Process each elements in item list
    for item in element:
        if isinstance(item, bs4.element.NavigableString):
            # Skip empty string
            continue
        # Buffer list
        buffer: List[str] = []
        for e in item:
            if e.name == "p":
                # TODO: use regular expression
                p: List[str] = parse_p(e)
                result.append(p[0].replace("> ", "> - "))
            else:
                if isinstance(e, bs4.element.NavigableString):
                    buffer.append(str(e).strip())
                elif isinstance(e, bs4.element.Tag):
                    if e.name == "var":
                        buffer.append("$" + str(e.get_text(strip=True)) + "$")
                    elif e.name == "code":
                        buffer.append("`" + str(e.get_text(strip=True)) + "`")
                    elif e.name == "ul":
                        result.append(f"> {prefix}" + "".join(buffer))
                        result.extend(
                            list(
                                map(
                                    lambda s: s.replace("> ", ">   "),
                                    parse_itemize(e, "ul"),
                                )
                            )
                        )
                    elif e.name == "ol":
                        result.append(f"> {prefix}" + "".join(buffer))
                        result.extend(
                            list(
                                map(
                                    lambda s: s.replace("> ", ">   "),
                                    parse_itemize(e, "ol"),
                                )
                            )
                        )

        if "".join(buffer) != "":
            # When the buffer is not empty, dump the buffer contents.
            result.append(f"> {prefix}" + "".join(buffer))
            buffer.clear()

    return result
