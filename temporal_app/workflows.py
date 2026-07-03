"""Temporal workflows for async processing."""

from __future__ import annotations

from datetime import timedelta

from temporalio import activity, workflow


@activity.defn
def send_email(to: str, subject: str, body: str) -> str:
    """Send email activity."""
    # Integrate with your email service
    print(f"Sending email to {to}: {subject} - {body}")
    return f"Email sent to {to}"


@activity.defn
def process_report(user_id: int) -> str:
    """Process report activity."""
    # Integrate with your report processing logic
    print(f"Processing report for user {user_id}")
    return f"Report processed for user {user_id}"


@workflow.defn  # type: ignore[call-overload]
async def onboarding_workflow(user_id: int, email: str) -> str:
    """User onboarding workflow."""
    # Send welcome email
    result = await workflow.execute_activity(
        send_email,
        args=[email, "Welcome!", "Welcome to My API Project"],
        start_to_close_timeout=timedelta(seconds=5),
    )

    # Process initial report
    report_result = await workflow.execute_activity(
        process_report,
        args=[user_id],
        start_to_close_timeout=timedelta(seconds=60),
    )

    return f"Onboarding complete for user {user_id}: {result} | Report: {report_result}"


@workflow.defn  # type: ignore[call-overload]
async def payment_workflow(user_id: int, amount: float) -> str:
    """Payment processing workflow."""
    # Validate payment
    # Process payment
    # Send confirmation
    # Handle retries

    return f"Payment of ${amount:.2f} processed for user {user_id}"
