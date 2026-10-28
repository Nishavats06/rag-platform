from app.models.document import DocumentStatus

ALLOWED_TRANSITIONS: dict[DocumentStatus, set[DocumentStatus]] = {
    DocumentStatus.UPLOADED: {DocumentStatus.PROCESSING},
    DocumentStatus.PROCESSING: {DocumentStatus.READY, DocumentStatus.FAILED},
    DocumentStatus.FAILED: {DocumentStatus.PROCESSING},
    DocumentStatus.READY: set(),
}


class InvalidTransitionError(Exception):
    """Raised when a status change is not allowed by the document lifecycle."""


def ensure_transition(current: DocumentStatus, new: DocumentStatus) -> None:
    if new not in ALLOWED_TRANSITIONS[current]:
        raise InvalidTransitionError(
            f"Cannot move a document from {current.value} to {new.value}"
        )