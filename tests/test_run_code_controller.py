from src.discbot.run_code_controller import *


def test_check_input():
    assert (
        check_input("python", '````print("hello")')
        == 'Your code must start with: "```"'
    )
    assert check_input("python", '```print("hello)```') == ""
    assert (
        check_input("python", 'print("hello")````') == 'You code must end with: "```"'
    )


def test_execute_code():
    assert execute_code("python3", 'print("hello")') == CodeExecutionResponse(
        stdout="hello\n", stderr="", exitcode=0, timeout=False
    )

    res = execute_code("python", "oasfiasjfoaj")
    assert res.stderr != ""
    assert res.stdout == ""
    assert res.exitcode != 0
    assert not res.timeout
