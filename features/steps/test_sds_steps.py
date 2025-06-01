from pytest_bdd import given, when, then, scenarios
import pytest
from pages.home_page import HomePage

scenarios('../sds_site.feature')

@pytest.fixture
def home_page(page):
    page.goto("https://s-d-s.co.uk/")
    return HomePage(page)

@pytest.fixture
def contact_us_page(page):
    page.goto("https://s-d-s.co.uk/products/landval-cloud/#footer-form")
    return HomePage(page)

@given("I am on the SDS homepage")
def on_homepage(home_page):  
    pass

@given("I am a potential customer of SDS")
def on_contact_us(contact_us_page):  
    pass

@then("I should see how many customers SDS have")
def verify_customers(home_page):
    customers = home_page.get_customers_text()
    print(f"\n🟢 Customers found: {customers}")
    assert customers.isdigit() or ',' in customers

@then("I should see how many users SDS have")
def verify_users(home_page):
    users = home_page.get_users_text()
    print(f"\n🟢 Users found: {users}")
    assert users.isdigit() or ',' in users

@when("I fill in the demo request form with valid data")
@then("the form should be submitted successfully")
def submit_demo_form(contact_us_page):  
    contact_us_page.fill_demo_form()
