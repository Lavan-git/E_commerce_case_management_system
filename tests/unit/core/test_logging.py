import json
import logging

from app.core.logging import JsonFormatter


def test_json_formatter_outputs_valid_json():
    formatter = JsonFormatter()

    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Test log message",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)
    payload = json.loads(output)

    assert payload["level"] == "INFO"
    assert payload["logger"] == "test.logger"
    assert payload["message"] == "Test log message"
    assert "timestamp" in payload


def test_json_formatter_includes_request_context():
    formatter = JsonFormatter()

    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=20,
        msg="Request completed",
        args=(),
        exc_info=None,
    )

    record.request_id = "test-request-id"
    record.case_id = 42
    record.status_code = 200
    record.duration_ms = 12.5

    output = formatter.format(record)
    payload = json.loads(output)

    assert payload["request_id"] == "test-request-id"
    assert payload["case_id"] == 42
    assert payload["status_code"] == 200
    assert payload["duration_ms"] == 12.5


def test_json_formatter_includes_exception_information():
    formatter = JsonFormatter()

    try:
        raise ValueError("test error")
    except ValueError:
        record = logging.LogRecord(
            name="test.logger",
            level=logging.ERROR,
            pathname=__file__,
            lineno=40,
            msg="Something failed",
            args=(),
            exc_info=True,
        )

        # LogRecord does not automatically contain the exception tuple
        # created in the surrounding except block.
        import sys

        record.exc_info = sys.exc_info()

    output = formatter.format(record)
    payload = json.loads(output)

    assert payload["level"] == "ERROR"
    assert payload["message"] == "Something failed"
    assert "exception" in payload
    assert "ValueError" in payload["exception"]