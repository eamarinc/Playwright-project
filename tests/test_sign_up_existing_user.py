from config.config import TEST_USER

def test_sign_up_existing_user(home_page):
    """Attempt to sign up with an existing user and verify the alert message.

    Steps:
    - Open Sign up modal (handled by `home_page.sign_up`)
    - Fill username and password
    - Click Sign up
    - Verify alert text is "This user already exist." and accept it
    - Verify the Sign up modal remains visible after dismissing the alert
    """
    username = TEST_USER["username"]
    password = TEST_USER["password"]

    # Use the page object to perform sign up (opens modal, fills fields, clicks button)
    home_page.sign_up(username, password)

    # Wait for and read the dialog that appears
    dialog = home_page.page.wait_for_event("dialog")
    msg = dialog.message
    dialog.accept()

    assert msg == "This user already exist.", f"Unexpected dialog message: {msg}"

    # After accepting the dialog, the Sign up modal should still be visible
    assert home_page.sign_up_modal.is_visible(), "Sign up modal should remain visible after dismissing alert"
