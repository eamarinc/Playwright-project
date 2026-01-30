import time
from config.config import TEST_USER

def test_login_modal(home_page):
    # Click the "Log in" menu in the header
    home_page.open_login_modal()

    # Verify that the Log in modal is displayed
    assert home_page.login_modal.is_visible(), "Log in modal is not displayed"

    # Verify modal title text
    title = home_page.login_modal.locator(".modal-title").text_content().strip()
    assert title == "Log in", f"Expected modal title 'Log in', got '{title}'"

    # Close the modal by clicking the Close button
    home_page.login_modal.locator("button", has_text="Close").click()


def test_login(home_page):

        # Perform login with existing user
        home_page.login(TEST_USER["username"], TEST_USER["password"])

        # Verify the modal is closed and back to home
        assert not home_page.login_modal.is_visible(), "Log in modal is still visible"
        assert home_page.carousel_inner.is_visible(), "Not back to home page, carousel not visible"

        # Verify "Welcome Edgartesting123" is displayed instead of "Log in"
        navbar_text = home_page.page.locator("nav").text_content()
        assert f"Welcome {TEST_USER['username']}" in navbar_text, f"Welcome message not found in navbar"

        # Wait one second and then log out
        time.sleep(1)
        home_page.logout()
        assert home_page.login_link.is_visible(), "Log in link not visible after logout"
