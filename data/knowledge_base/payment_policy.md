# Payment Dispute Policy

**Document type:** Policy  
**Domain:** Payment disputes  
**Version:** 1.0  
**Status:** Active

## Purpose

This policy defines how payment-related customer cases should be handled when a payment attempt does not result in the expected order or payment state.

## Payment deducted but order not created

When a customer reports that money was deducted but no order was created:

1. Verify the payment transaction using the transaction reference available to the case.
2. Check whether an order exists for the corresponding payment attempt.
3. If the payment is successful and no order exists, create or maintain a payment reconciliation case.
4. Do not ask the customer to pay again until the original transaction outcome has been determined.
5. Keep the case open until the payment outcome is confirmed.
6. If reconciliation confirms that the payment cannot be associated with a valid order, follow the applicable refund procedure.

## Pending payments

A payment in a pending state must not be treated as a confirmed failure.

The case should remain under investigation until the payment reaches a final state or the payment provider's reconciliation process determines the outcome.

## Failed payments

When a payment is confirmed as failed and no successful debit occurred, the case may be resolved as a failed payment after the payment status has been verified.

## Required evidence

A payment dispute should, where available, include:

- payment transaction identifier
- payment status
- customer identifier
- timestamp of the payment attempt
- related order identifier, when one exists

## Resolution principle

The support agent should rely on the verified payment state rather than the customer's description alone when determining the next operational step.
