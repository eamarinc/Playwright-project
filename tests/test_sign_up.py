def test_sign_up(home_page, test_user_credentials):

        # Generate a unique username
        username = test_user_credentials["username"]
        password = test_user_credentials["password"]

        # Perform sign up
        home_page.sign_up(username, password)

        # Wait for the dialog
        dialog = home_page.page.wait_for_event('dialog')
        dialog_message = dialog.message
        dialog.accept()

        # Verify the dialog message
        assert dialog_message == "Sign up successful.", f"Expected 'Sign up successful.', got '{dialog_message}'"

        # Verify the modal is closed and back to home
        # Check that the carousel is visible
        assert home_page.carousel_inner.is_visible(), "Not back to home page, carousel not visible"
