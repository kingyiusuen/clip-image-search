import pytest
from lambda_function import lambda_handler


@pytest.mark.parametrize(
    "event",
    [
        {"input_type": "text", "query": "two cats"},
        {"input_type": "image", "query": "https://i.imgur.com/jlFgGpe.jpeg"},
    ],
)
def test_text_input(event):
    response = lambda_handler(event, None)
    assert response["status_code"] == 200
    assert len(response["body"]) == 10


@pytest.mark.parametrize(
    "event", [{}, {"input_type": "text"}, {"query": "two cats"}, {"input_type": "language", "query": "two cats"}]
)
def test_missing_keys_and_unrecognized_input_type(event):
    response = lambda_handler(event, None)
    assert response["status_code"] == 400
