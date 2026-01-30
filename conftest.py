import pytest
import time
from playwright.sync_api import sync_playwright
from pages.home_page import HomePage

@pytest.fixture(scope="function")
def home_page():
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch(channel="chrome", headless=False)
        except Exception:
            browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        home_page_instance = HomePage(page)
        home_page_instance.goto()
        yield home_page_instance
        browser.close()


@pytest.fixture(scope="session")
def test_user_credentials():
    username = "Test123" + str(int(time.time()))
    password = "1234567"
    return {"username": username, "password": password}