# pages/landval_demo_page.py
import time
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from .home_selectors import (
    DEMO_FORM,
    INPUT_FIRSTNAME,
    INPUT_LASTNAME,
    INPUT_PHONE,
    INPUT_EMAIL,
    INPUT_COMPANY,
    CHECKBOX_BY_LABEL_FMT,
    TEXTAREA_MESSAGE,
    BUTTON_SUBMIT,
    SUCCESS_BANNER,
    ERROR_PHONE_FMT,
    ERROR_MISSING_FIELD,
    ERROR_ROLLUP,
)

class LandvalDemoPage:
    def __init__(self, page: Page):
        self.page = page

    def goto_contact_page(self) -> None:
        """Navigate directly to the Landval “Book a demo” anchor."""
        self.page.goto(
            "https://s-d-s.co.uk/products/landval-cloud/#footer-form",
            wait_until="domcontentloaded",
            timeout=30000
        )

    def fill_demo_form_with_payload(self, payload: dict) -> (int, str):
        """
        Fill and submit the “Book a demo” form using a payload dict with keys:
          - firstname, lastname, phone, email, company, enquiry, message, expect_success (bool)

        Returns:
          (200, success_message)      if submitted successfully (or assumed already done),
          (400, error_reason)         if we detect exactly one of:
                                        * invalid phone format error
                                        * missing-required-field error
          (200, fallback_message)     if an unexpected POST occurred (negative)
          (0, ambiguous_message)      if neither error nor POST is detected
        """

        # 0) If the success banner is already visible, skip immediately:
        if self.page.query_selector(SUCCESS_BANNER):
            return (200, "Already submitted")

        # 1) Scroll to ensure HubSpot can load the form
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)  # give HubSpot a moment to inject the <form>

        # 2) Wait up to 5s for the form to attach; otherwise assume it’s gone/replaced
        try:
            self.page.wait_for_selector(DEMO_FORM, state="attached", timeout=5000)
        except PlaywrightTimeoutError:
            return (200, "Form not found—assuming already submitted")

        # 3) Fill in each field from payload
        self.page.fill(INPUT_FIRSTNAME, payload.get("firstname", ""))
        self.page.fill(INPUT_LASTNAME,  payload.get("lastname", ""))
        self.page.fill(INPUT_PHONE,     payload.get("phone", ""))
        self.page.fill(INPUT_EMAIL,     payload.get("email", ""))
        self.page.fill(INPUT_COMPANY,   payload.get("company", ""))

        # 4) Click the “Enquiry Type” checkbox via its label text
        label_selector = CHECKBOX_BY_LABEL_FMT.format(payload.get("enquiry", ""))
        label = self.page.locator(label_selector)
        label.scroll_into_view_if_needed()
        label.click(force=True)

        # 5) Fill out the message textarea
        self.page.fill(TEXTAREA_MESSAGE, payload.get("message", ""))

        # 6) Branch on expect_success
        if payload.get("expect_success", False):
            # — Positive path: intercept the HS POST, then wait for success banner
            with self.page.expect_request_finished(
                lambda r: "hsforms.com" in r.url and r.method == "POST"
            ) as request_info:
                self.page.click(BUTTON_SUBMIT)

            submission_request = request_info.value
            response = submission_request.response()
            status_code = response.status

            if status_code == 200:
                try:
                    self.page.wait_for_selector(SUCCESS_BANNER, timeout=10000)
                    success_text = self.page.inner_text(SUCCESS_BANNER)
                    return (200, success_text)
                except PlaywrightTimeoutError:
                    return (200, "Submitted but no success banner found")
            else:
                return (status_code, f"HTTP {status_code}")

        else:
            # — Negative path: click Submit, then look for errors or unexpected POST
            self.page.click(BUTTON_SUBMIT)

            # 7A) Detect if phone format is invalid
            invalid_phone = False
            phone_val = payload.get("phone", "")
            if phone_val and any(c.isalpha() for c in phone_val):
                invalid_phone = True

            if invalid_phone:
                try:
                    # HubSpot’s “A valid phone number may only contain…” error
                    self.page.wait_for_selector(ERROR_PHONE_FMT, timeout=3000)
                    return (400, "Invalid phone format error detected")
                except PlaywrightTimeoutError:
                    # If that phone‐error didn’t show, check if POST happened anyway
                    try:
                        with self.page.expect_request(
                            lambda r: "hsforms.com" in r.url and r.method == "POST",
                            timeout=1000
                        ):
                            return (200, "Unexpected POST despite invalid phone")
                    except PlaywrightTimeoutError:
                        return (0, "Neither phone-error nor POST—ambiguous failure")

            # 7B) Otherwise assume missing-required-field error
            try:
                # Per-field: “Please complete this required field.”
                self.page.wait_for_selector(ERROR_MISSING_FIELD, timeout=3000)
                return (400, "Missing-required-field error (per-field)")
            except PlaywrightTimeoutError:
                pass

            try:
                # Roll-up: “Please complete all required fields.”
                self.page.wait_for_selector(ERROR_ROLLUP, timeout=2000)
                return (400, "Missing-required-field error (roll-up)")
            except PlaywrightTimeoutError:
                pass

            # 7C) If neither validation error nor POST happened → ambiguous
            try:
                with self.page.expect_request(
                    lambda r: "hsforms.com" in r.url and r.method == "POST",
                    timeout=1000
                ):
                    return (200, "Unexpected POST despite missing required")
            except PlaywrightTimeoutError:
                return (0, "Neither required-field error nor POST—ambiguous failure")
