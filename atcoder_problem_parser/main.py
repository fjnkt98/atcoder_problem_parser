import click
import requests
import bs4
from typing import List
import sys


def parse(text: str):
    soup = bs4.BeautifulSoup(text, "html.parser")

    result: List[str] = ["### 問題文", ""]
    for p in soup.select("h3:-soup-contains('問題文') ~ p"):
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
                    result.append("> " + "".join(strings))
                    strings = []
        if strings:
            result.append("> " + "".join(strings))
        result.append("> ")
    result[-1] = ""

    result.extend(["### 制約", ""])

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

    return parse(response.text)


@click.command()
@click.option("--contest", default="", help="Type of contest. abc, arc, or agc.")
@click.option("--problem", default="", help="Problem index. a, b, c, ..., h")
@click.option("--url", default="", help="Problem URL.")
def main(contest: str = "", problem: str = "", url: str = "") -> None:
    result = app(contest, problem, url)

    for r in result:
        print(r)


if __name__ == "__main__":
    main()
