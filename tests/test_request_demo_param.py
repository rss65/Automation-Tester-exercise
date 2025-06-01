# tests/test_request_demo_param.py
import pytest
import json
from pages.landval_demo_page import LandvalDemoPage

with open("data/demo_form_data.json") as f:
    DEMO_DATA = json.load(f)

@pytest.mark.parametrize("payload", DEMO_DATA)
def test_demo_form_payload(page, payload):
    demo = LandvalDemoPage(page)
    demo.goto_contact_page()

    status, message = demo.fill_demo_form_with_payload(payload)

    if payload["expect_success"]:
        assert status == 200
        assert "Thank you for reaching out" in message
    else:
        assert status == 400, f"Expected client‐side validation, but got {status}: {message}"
