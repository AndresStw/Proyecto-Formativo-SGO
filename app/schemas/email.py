"""Email validation that permits reserved `.test` addresses locally."""

from typing import Annotated

from email_validator import EmailNotValidError, validate_email
from pydantic import AfterValidator

from app.core.config import get_settings


def _validate_email(value: str) -> str:
    email = value.strip()
    try:
        return validate_email(email, check_deliverability=False).normalized
    except EmailNotValidError as error:
        domain = email.rpartition("@")[2].lower()
        environment = get_settings().app_env.lower()
        if domain.endswith(".test") and environment in {"development", "testing", "local"}:
            try:
                return validate_email(
                    email,
                    check_deliverability=False,
                    test_environment=True,
                ).normalized
            except EmailNotValidError as test_error:
                raise ValueError(str(test_error)) from test_error
        raise ValueError(str(error)) from error


EmailAddress = Annotated[str, AfterValidator(_validate_email)]
