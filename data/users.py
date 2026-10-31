from dataclasses import dataclass

from config import settings


@dataclass(frozen=True)
class User:
    username: str
    password: str


STANDARD = User(settings.APP_USERNAME, settings.APP_PASSWORD)
LOCKED_OUT = User("locked_out_user", settings.APP_PASSWORD)
PROBLEM = User("problem_user", settings.APP_PASSWORD)
INVALID = User("unknown_user", "wrong_password")

BY_NAME = {
    "standard": STANDARD,
    "locked_out": LOCKED_OUT,
    "problem": PROBLEM,
    "invalid": INVALID,
}
