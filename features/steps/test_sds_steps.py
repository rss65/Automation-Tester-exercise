# features/steps/test_sds_steps.py

from pytest_bdd import given, when, then, scenarios
import pytest

from pages.home_stats_page import HomeStatsPage
from pages.landval_demo_page import LandvalDemoPage

# Point this at your single feature file under “features/”
scenarios("../sds_site.feature")


@pytest.fixture
def stats_page(page):
    """
    Navigate to the SDS homepage and return a HomeStatsPage instance.
    """
    page.goto("https://s-d-s.co.uk/", wait_until="domcontentloaded", timeout=30000)
    return HomeStatsPage(page)


@pytest.fixture
def demo_page(page):
    """
    Return a LandvalDemoPage instance. We’ll navigate in the @when step.
    """
    return LandvalDemoPage(page)


#
# —————————————————————————————
# BDD Steps for “Customers” / “Users”
# —————————————————————————————
#
@given("I am on the SDS homepage")
def on_homepage(stats_page):
    # The stats_page fixture has already navigated to the homepage.
    pass


@then("I should see how many customers SDS have")
def verify_customers(stats_page):
    customers = stats_page.get_customers_text()
    print(f"🟢 Customers found: {customers}")
    # Allow commas, e.g. “1,234”
    assert customers.replace(",", "").isdigit()


@then("I should see how many users SDS have")
def verify_users(stats_page):
    users = stats_page.get_users_text()
    print(f"🟢 Users found: {users}")
    assert users.replace(",", "").isdigit()


#
# —————————————————————————————
# BDD Steps for “Request a Landval demo”
# —————————————————————————————
#
@given("I am a potential customer of SDS")
def on_contact_us(demo_page):
    # Nothing to do here yet; we’ll navigate in the @when step below
    pass


@when("I fill in the demo request form with valid data")
def fill_form_with_valid_data(demo_page):
    # 1) Navigate directly to the Landval “Book a demo” anchor on the SDS site
    demo_page.goto_contact_page()

    # 2) Build the hard‐coded “Zak Baba” payload
    payload = {
        "firstname": "Zak",
        "lastname":  "Baba",
        "phone":     "01234567890",
        "email":     "zak.baba@s-d-s.co.uk",
        "company":   "Test company",
        "enquiry":   "Landval",
        "message":   "This is a test message, please ignore",
        "expect_success": True
    }

    # 3) Fill and submit
    status_code, resp_message = demo_page.fill_demo_form_with_payload(payload)

    # 4) Assert successful submission
    assert status_code == 200, f"Expected 200 but got {status_code} / {resp_message}"
    assert "Thank you for reaching out" in resp_message, (
        f"Success banner not found; got: {resp_message}"
    )


@then("the form should be submitted successfully")
def verify_form_submitted():
    # All verification has already happened in the @when step,
    # so this step can just pass to satisfy pytest‐bdd.
    pass
