import click
import requests
import bs4
from typing import List
import sys


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
    for p in soup.select("h3:-soup-contains('問題文') ~ p"):
        # Buffer list
        strings: List[str] = []
        for t in p:
            if isinstance(t, bs4.element.NavigableString):
                strings.append(str(t).strip())
            elif isinstance(t, bs4.element.Tag):
                if t.name == "var":
                    strings.append("$" + str(t.get_text(strip=True)) + "$")
                elif t.name == "code":
                    strings.append("`" + str(t.get_text(strip=True)) + "`")
                elif t.name == "br":
                    # WHen <br> tag is there, break line.
                    # Store the result in citation format
                    result.append("> " + "".join(strings))
                    strings = []

        if strings:
            # If the buffer is not empty, extract all contents
            # Store the result in citation format
            result.append("> " + "".join(strings))
        result.append("> ")

    # Eliminate last line
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


def app(contest: str = "", problem: str = "", url: str = "") -> List[str]:
    print(contest)
    target_problem: str = ""
    target_url: str = ""
    if url == "":
        assert contest != "", "Argument `contest` is mandatory!"

        if problem == "":
            print(
                "Since argument `problem` was not specified, `a` is used instead.",
                file=sys.stderr,
            )
            target_problem = "a"
        else:
            target_problem = problem.lower()

        target_url = f"https://atcoder.jp/contests/{contest.lower()}/tasks/{contest.lower()}_{problem.lower()}"
    else:
        target_url = url

    response: requests.Response = requests.get(target_url)
    if response.status_code == 200:
        return parse(response.text)
    else:
        response.raise_for_status()
        return []


def validate(context: click.Context, parameter: click.Parameter, value: str):
    """Validate function for command argument"""

    # When the value (contest name) is empty, let it pass for direct url specification
    if value == "":
        return value

    # Copy the value
    contest: str = value

    if len(contest) != 6:
        # Length of the contest name should be 6.
        raise click.BadParameter("Invalid contest name.")
    if contest[:3].lower() not in ["abc", "arc", "agc"]:
        # The first three letters must be fixed.
        raise click.BadParameter(
            "Invalid contest name. This parameter must be 'abc', 'arc', or 'agc'."
        )
    if not (0 <= int(contest[3:]) < 1000):
        # The last 3 letters must be within the range.
        raise click.BadParameter("Invalid contest number.")

    # Return lowercased string to simplify code.
    return contest.lower()


@click.command()
@click.argument(
    "contest",
    type=str,
    default="",
    callback=validate,
)
@click.argument(
    "problem",
    type=click.Choice(
        ["a", "b", "c", "d", "e", "f", "g", "h", ""], case_sensitive=False
    ),
    default="",
)
@click.option("--url", default="", help="Problem URL.")
def main(contest: str = "", problem: str = "", url: str = "") -> None:
    """main function

    Args:
        - contest (str): Contest name. letter case is ignored. e.g.) abc123, arc200, agc021
        - problem (str): Problem index. Lowercase letters from a to h are only allowed.
        - url (str): URL of the problem. When this argument is not empty, it takes precedence
        and the other positional arguments are ignored.
    """
    try:
        # Get the parse result.
        result = app(contest, problem, url)

        # Output the result to stdout.
        for r in result:
            print(r)
    except requests.HTTPError:
        if url != "":
            print("Specified URL is probably wrong. Check it out!", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
