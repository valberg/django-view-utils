import nox


@nox.session(python=["3.10", "3.11"])
@nox.parametrize("django", ["4.0", "4.1", "4.2b1"])
def tests(session, django):
    session.install(f"django=={django}")
    session.install("-r", "test_requirements.txt")
    session.run("pytest", "tests", *session.posargs)
