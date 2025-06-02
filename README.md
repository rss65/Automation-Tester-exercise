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

---

## 🚀 Quick Start

### 1. **Install Dependencies**

```sh
pip install -r requirements.txt
playwright install
