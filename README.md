# SDS Automation QA Assessment

## Overview

This repository contains an end-to-end functional test suite for [Shelton Development Services (SDS)](https://s-d-s.co.uk/), built as part of an interview assessment.  
It demonstrates robust automation principles, modern Python tooling, and a focus on maintainability, scalability, and clear reporting.

---

## 📋 What’s Covered

- **Customer/User Stats**: Automated validation of SDS’s live customer and user counts.
- **Demo Request Form**: Positive and negative scenarios for the "Book a demo" form on the Landval product page, including data-driven negative tests (e.g., invalid phone, missing fields) and API response validation.
- **Cross-Browser and Mobile**: Tests can run on Chromium, Firefox, WebKit, and mobile emulation.
- **Video and Reporting**: Each test run records video and generates detailed Allure + HTML reports.
- **Parallel Execution**: All tests can be executed in parallel for speed.
- **CI/CD Integration**: The tests are run automatically on all browsers on github push requests using github actions.

---

## 🚀 Quick Start

### 1. **Install Dependencies**

```sh
pip install -r requirements.txt
playwright install
```
🧑‍💻 Running the Test Suite
2. Test Execution Examples
All commands below assume you are in the project root.

Desktop Browsers
Browser	Command Example
Chromium	pytest ```sh--browser=chromium --alluredir=reports/allure-results/chromium-desktop```
Firefox	pytest ```sh--browser=firefox --alluredir=reports/allure-results/firefox-desktop```
WebKit	pytest ```sh--browser=webkit --alluredir=reports/allure-results/webkit-desktop```

Mobile Emulation (Chromium Only)
To run with mobile emulation (e.g., iPhone 12):

```sh
pytest --browser=chromium --mobile --alluredir=reports/allure-results/chromium-mobile
```
Parallel Execution
To speed things up, you can run tests in parallel (e.g., 4 workers):

```sh
pytest -n 4 --browser=chromium --alluredir=reports/allure-results/chromium-desktop
```
Note: The -n 4 flag requires pytest-xdist (included in requirements).

3. Generating Allure Reports
After your test run completes, generate and view a beautiful Allure report:
```sh
allure generate reports/allure-results/chromium-desktop -o reports/allure-report/chromium-desktop --clean
allure open reports/allure-report/chromium-desktop
```
Replace chromium-desktop with the desired output folder (e.g., firefox-desktop or chromium-mobile).

4. Additional Tips
Test Videos:
Each test automatically records a video, saved in /test-videos/ and named after the test for easy debugging.

Environment Requirements:

Python 3.8+

Playwright browsers installed (playwright install)

Allure CLI installed 
