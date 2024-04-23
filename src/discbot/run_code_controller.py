from dataclasses import dataclass
from typing import List
from typing import Optional

import requests

from src.config import EXECUTE_API_URL
from src.config import LANG_API_URL


@dataclass
class CodeExecutionResponse:
    stdout: str
    stderr: str
    exitcode: int
    timeout: bool

    def to_discord_chat_response(self) -> str:
        return self.stdout + "\n" + self.stderr


def execute_code(language: str, code: str) -> Optional[CodeExecutionResponse]:
    pload = {"language": language, "code": code}

    r = requests.post(EXECUTE_API_URL, data=pload)
    if r.status_code != 200:
        return None
    respond = r.json()
    return CodeExecutionResponse(
        stdout=respond["data"]["stdout"],
        stderr=respond["data"]["stderr"],
        exitcode=respond["data"]["exit_code"],
        timeout=respond["time_out"],
    )


def check_input(language: str, code: str) -> str:
    try:
        langs = __get_supported_languages()
    except requests.exceptions.RequestException:
        return "Service is down :("
    if language not in langs:
        return f"'{language}' is not in supoorted languages list: {langs}"

    if code.startswith("````"):
        return 'Your code must start with: "```"'
    if code.endswith("````"):
        return 'You code must end with: "```"'
    return ""


def __get_supported_languages() -> List[str]:
    r = requests.get(LANG_API_URL)
    if r.status_code != 200:
        raise requests.exceptions.RequestException()
    langs = r.json()["data"]
    return langs
