from setuptools import setup

setup(
    name="atcoder_problem_parser",
    version="0.1.0",
    install_requires=["requests", "click", "beautifulsoup4"],
    extras_require={"develop": ["mypy", "flake8", "black"]},
    entry_points={"console_scripts": ["app = atcoder_problem_parser.main:main"]},
)
