from pathlib import Path

import pandas as pd


OUTPUT = Path("data/sources/cases.parquet")


def main() -> None:
    data = pd.DataFrame(
        [
            {
                "case_identifier": 107,
                "actor_id": 1,
                "type": "PAYMENT",
                "severity": "HIGH",
                "state": "OPEN",
                "reason": "PAYMENT_NOT_REFLECTED",
                "details": "Payment deducted but order was not created.",
                "created": "2026-09-22T14:00:00",
            },
            {
                "case_identifier": 108,
                "actor_id": 2,
                "type": "DELIVERY",
                "severity": "MEDIUM",
                "state": "IN_PROGRESS",
                "reason": "DELIVERY_DELAY",
                "details": "Order has not arrived yet.",
                "created": "2026-09-22T14:30:00",
            },
            {
                "case_identifier": 109,
                "actor_id": 3,
                "type": "REFUND",
                "severity": "CRITICAL",
                "state": "OPEN",
                "reason": "REFUND_DELAY",
                "details": "Refund has not been received.",
                "created": "2026-09-22T15:00:00",
            },
        ]
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    data.to_parquet(OUTPUT, index=False)

    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()