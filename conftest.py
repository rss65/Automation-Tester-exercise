# conftest.py
import os
import shutil
import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Which Playwright browser to use: chromium, firefox, or webkit (default: chromium).",
    )
    parser.addoption(
        "--mobile",
        action="store_true",
        default=False,
        help="Run tests in mobile emulation (iPhone 12) if set; otherwise desktop.",
    )

@pytest.fixture(scope="session")
def pw():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    return pytestconfig.getoption("browser")

@pytest.fixture(scope="session")
def browser(pw, browser_name):
    return getattr(pw, browser_name).launch(headless=False)

@pytest.fixture(scope="function")
def context(request, browser, pw):
    mobile_flag = request.config.getoption("--mobile")
    test_videos_dir = os.path.join(os.getcwd(), "test-videos")
    os.makedirs(test_videos_dir, exist_ok=True)

    if mobile_flag:
        iphone_12 = pw.devices["iPhone 12"]
        browser_context = browser.new_context(
            **iphone_12,
            record_video_dir=test_videos_dir,
        )
    else:
        browser_context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/116.0.0.0 Safari/537.36"
            ),
            record_video_dir=test_videos_dir,
        )

    yield browser_context
    browser_context.close()

@pytest.fixture(scope="function")
def page(request, context):
    page = context.new_page()
    yield page
    try:
        page.close()
    except Exception:
        pass

    video = page.video
    if video:
        raw_path = video.path()
        if raw_path and os.path.exists(raw_path):
            test_name = request.node.name
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{test_name}_{ts}.webm"
            dst = os.path.join(os.getcwd(), "test-videos", new_filename)

            try:
                video.save_as(dst)
                print(f"📽️ Video for this test: {dst}")
            except Exception as e:
                print(f"⚠️ Could not save video {raw_path} → {dst}: {e}")
        else:
            print("⚠️ No raw video file was found at all.")
    else:
        print("⚠️ There was no video object associated with this page.")
