import nox
import nox_poetry.patch
from nox.sessions import Session

python = ["3.6", "3.7", "3.8", "3.9"]
locations = "src", "tests"

nox.options.sessions = ["tests", "lint", "mypy"]


@nox.session(python="3.8")
def black(session: Session) -> None:
    """Run black code formatter"""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python="3.8")
def isort(session: Session) -> None:
    """Sort imports using isort"""
    args = session.posargs or locations
    session.install("isort")
    session.run("isort", *args)


@nox.session(python="3.8")
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-black",
        "flake8-bugbear",
        "flake8-isort",
    )
    session.run("flake8", *args)


@nox.session(python="3.8")
def mypy(session: Session) -> None:
    """Run static type analysis with mypy"""
    args = session.posargs or locations
    session.install("-e", ".[dev,test]")
    session.install("mypy")
    session.run("mypy", *args)


@nox.session(python=python)
def tests(session: Session) -> None:
    """Run the tests"""
    # session.install("-e", ".[test]")
    session.install(".")
    session.install("pytest", "hypothesis")
    tests = session.posargs or ["tests"]
    session.run("pytest", *tests)
