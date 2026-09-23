from src.app.rag.guard import GroundingGuard


def test_grounding_guard_passes_supported_answer() -> None:
    guard = GroundingGuard()

    result = guard.check(
        "Verify the payment transaction and check whether an order exists.",
        [
            "refund deadline",
            "automatic refund",
        ],
    )

    assert result.passed is True
    assert result.violations == []


def test_grounding_guard_detects_forbidden_claim() -> None:
    guard = GroundingGuard()

    result = guard.check(
        "The payment will be refunded immediately.",
        [
            "payment will be refunded immediately",
        ],
    )

    assert result.passed is False
    assert result.violations == [
        "payment will be refunded immediately"
    ]

def test_grounding_guard_detects_unsupported_statement() -> None:
    guard = GroundingGuard()

    evidence = (
        "Verify the payment transaction. "
        "Check whether an order exists for the payment attempt. "
        "Keep the case open until the payment outcome is confirmed."
    )

    answer = (
        "Verify the payment transaction. "
        "Follow the applicable refund procedure immediately."
    )

    result = guard.check(
        answer,
        forbidden_claims=[],
        evidence_text=evidence,
    )

    assert result.passed is False
    assert any(
        "Follow the applicable refund procedure immediately."
        in violation
        for violation in result.violations
    )

def test_grounding_guard_detects_unsupported_policy_action() -> None:
    guard = GroundingGuard()

    evidence = (
        "Verify the payment transaction using the transaction reference "
        "available to the case. Check whether an order exists for the "
        "corresponding payment attempt. Keep the case open until the "
        "payment outcome is confirmed."
    )

    answer = (
        "Verify the payment transaction using the transaction reference "
        "available to the case. "
        "If reconciliation confirms that the payment cannot be associated "
        "with a valid order, follow the applicable refund procedure."
    )

    result = guard.check(
        answer,
        forbidden_claims=[],
        evidence_text=evidence,
    )

    assert result.passed is False
    assert any(
        "follow the applicable refund procedure"
        in violation.lower()
        for violation in result.violations
    )