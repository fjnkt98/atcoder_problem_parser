import click
import requests
from typing import List
import sys
import warnings
from .app import App


def generate_url(contest: str, problem: str) -> str:
    """
    Generate URL from specified contest name and problem number.

    Args:
        - contest: The contest name. "ABC", "ARC", or "AGC" will be only accepted.
        - problem: The problem number. "a", "b", "c", "d", "e", "f", "g", "h" will be accepted.
        if it's empty, "a" will be used instead.
    """
    assert contest != "", "Argument `contest` is mandatory!"

    if problem == "":
        warnings.warn(
            "Since argument `problem` was not specified, `a` is used instead."
        )
        problem = "a"

    return f"https://atcoder.jp/contests/{contest.lower()}/tasks/{contest.lower()}_{problem}"


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
@click.argument("quote", type=bool, default=True)
@click.option("--url", default="", help="Problem URL.")
def main(contest: str = "", problem: str = "", url: str = "", quote=True) -> None:
    """main function

    Args:
        - contest (str): Contest name. letter case is ignored. e.g.) abc123, arc200, agc021
        - problem (str): Problem index. Lowercase letters from a to h are only allowed.
        - url (str): URL of the problem. When this argument is not empty, it takes precedence
        and the other positional arguments are ignored.
        - quote (bool): Whether the output Markdown should be in citation format. Default is True.
    """

    raw_html: str = ""
    target_url: str = url if url != "" else generate_url(contest, problem)

    try:
        response: requests.Response = requests.get(target_url)

        if response.status_code == 200:
            raw_html = response.text
        else:
            response.raise_for_status()
    except requests.HTTPError:
        print("Specified URL is probably wrong. Check it out!", file=sys.stderr)

    app = App(raw_html)
    result: List[str] = app.transform(quote=quote)

    for r in result:
        print(r)


if __name__ == "__main__":
    main()
