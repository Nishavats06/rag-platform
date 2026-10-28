import pytest

from app.models.document import DocumentStatus
from app.services.document_states import InvalidTransitionError, ensure_transition


def test_happy_path_is_allowed():
    ensure_transition(DocumentStatus.UPLOADED, DocumentStatus.PROCESSING)
    ensure_transition(DocumentStatus.PROCESSING, DocumentStatus.READY)


def test_failed_document_can_be_retried():
    ensure_transition(DocumentStatus.FAILED, DocumentStatus.PROCESSING)


@pytest.mark.parametrize(
    ("current", "new"),
    [
        (DocumentStatus.READY, DocumentStatus.PROCESSING),
        (DocumentStatus.UPLOADED, DocumentStatus.READY),
        (DocumentStatus.READY, DocumentStatus.FAILED),
    ],
)
def test_illegal_transitions_are_rejected(current, new):
    with pytest.raises(InvalidTransitionError):
        ensure_transition(current, new)