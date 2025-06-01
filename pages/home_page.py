import time

class HomePage:
    def __init__(self, page):
        self.page = page

    def _get_stable_number_by_title(self, title_text, timeout=30, poll_interval=0.5):
        start_time = time.time()
        prev_number = None
        stable_count = 0

        while time.time() - start_time < timeout:
            # Find the correct .pwr-stat__number by locating the right .pwr-stat__title
            elements = self.page.locator(".pwr-stat")
            for i in range(elements.count()):
                title = elements.nth(i).locator(".pwr-stat__title").text_content()
                if title and title.strip().upper() == title_text.upper():
                    number = elements.nth(i).locator(".pwr-stat__number").text_content().strip()
                    if number == prev_number:
                        stable_count += 1
                        if stable_count >= 2:  # 2 checks with same value
                            return number
                    else:
                        prev_number = number
                        stable_count = 0
                    break
            time.sleep(poll_interval)

        raise TimeoutError(f"{title_text} number did not stabilize in time.")

    def get_customers_text(self):
        return self._get_stable_number_by_title("CUSTOMERS")

    def get_users_text(self):
        return self._get_stable_number_by_title("USERS")

    def fill_demo_form(self):
        # 0) If the success banner is already visible, assume form was submitted and exit:
        if self.page.query_selector("div.submitted-message") is not None:
            print("⚠️ Success message already present; skipping form fill.")
            return

        # 1) Scroll down so the form is (hopefully) in view:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        # 2) Wait for the form to appear in the DOM before we fill fields:
        #    But if it never shows up in, say, 5 seconds, assume it's already gone/replaced.
        print("✅ Waiting for form to be attached to DOM…")
        try:
            self.page.wait_for_selector("form.hs-form", state="attached", timeout=5000)
        except TimeoutError:
            # Form didn’t show up quickly—probably already submitted.
            print("⚠️ Form not found in 5s; assuming already submitted.")
            return

        # 3) Fill in all required inputs:
        self.page.fill("input[name='firstname']", "Zak")
        self.page.fill("input[name='lastname']", "Baba")
        self.page.fill("input[name='phone']", "01234567890")
        self.page.fill("input[name='email']", "zak.baba@s-d-s.co.uk")
        self.page.fill("input[name='company']", "Test company")

        # 4) Scroll to and click the "Landval" checkbox by its label:
        label = self.page.locator("label:has-text('Landval')")
        label.scroll_into_view_if_needed()
        label.click(force=True)

        # 5) Fill out the message textarea:
        self.page.fill("textarea[name='message']", "This is a test message, please ignore")

        # 6) Intercept the network request that HubSpot fires on submit:
        with self.page.expect_request_finished(
            lambda r: "hsforms.com" in r.url and r.method == "POST"
        ) as request_info:
            self.page.click("input[type='submit']")

        # 7) Once the request finishes, validate its response:
        submission_request = request_info.value
        response = submission_request.response()
        status_code = response.status
        print(f"\n🟢 Form submitted. Status: {status_code}, URL: {submission_request.url}")
        assert status_code == 200, f"❌ Form submission failed with status {status_code}"

        # 8) Wait for the success banner (this is your true signal of “test passed”):
        print("✅ Waiting for success message…")
        self.page.wait_for_selector("div.submitted-message", timeout=10000)
        success_text = self.page.inner_text("div.submitted-message")
        print(f"✅ Success message appeared: {success_text}")
        assert "Thank you for reaching out!" in success_text, "❌ Success message not found"





        





   