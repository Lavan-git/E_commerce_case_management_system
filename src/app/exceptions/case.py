from app.exceptions.base import ApplicationError


class CaseError(ApplicationError):
    """Base exception for case-related errors."""


class InvalidCaseActorError(CaseError):
    """Raised when both/neither customer and vendor are supplied."""


class CaseNotFoundError(CaseError):
    """Raised when a requested case does not exist."""


class InvalidCaseTypeError(CaseError):
    """Raised when the case type is not supported."""


class InvalidCaseStatusError(CaseError):
    """Raised when an invalid status is supplied."""


class InvalidCaseStatusTransitionError(CaseError):
    """Raised when a status transition is not allowed."""


class InvalidCaseResolutionError(CaseError):
    """Raised when resolution data conflicts with case status."""