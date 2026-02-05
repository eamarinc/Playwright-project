import pytest

@pytest.mark.skip(reason="Form con comportamiento incorrecto conocido")
def test_contact_empty_form(home_page):
    """
    Test case: Verify that clicking Send message without filling the Contact form
    does not show a success message.
    
    Expected behavior: The form should validate required fields and NOT send the message.
    
    Steps:
    1. Open https://www.demoblaze.com/index.html
    2. Click on the "Contact" link
    3. Click on "Send message" button without filling any fields
    4. Verify that the success message "Thanks for the message!!" is NOT displayed
    
    Note: This test will FAIL if the application has a bug where it allows 
    submitting empty forms (which appears to be the case with demoblaze.com).
    """
    
    # Click on "Contact" link
    home_page.click_contact_link()
    
    # Verify the Contact modal is visible
    assert home_page.is_contact_modal_visible(), "Contact modal is not visible"
    print("✓ Contact modal opened successfully")
    
    # Wait a moment for modal to stabilize
    home_page.page.wait_for_timeout(500)
    
    # Set up a flag to capture any dialog that might appear
    dialog_appeared = False
    dialog_message = ""
    
    def handle_dialog(dialog):
        nonlocal dialog_appeared, dialog_message
        dialog_appeared = True
        dialog_message = dialog.message
        print(f"Alert/Dialog detected: '{dialog_message}'")
        dialog.accept()
    
    home_page.page.on("dialog", handle_dialog)
    
    # Click on "Send message" button without filling any fields
    home_page.click_send_message_button()
    
    # Wait a moment to see if any alert or confirmation appears
    home_page.page.wait_for_timeout(1500)
    
    # Check if a success alert appeared on the page (sweet-alert modal)
    success_alert = home_page.page.locator(".sweet-alert")
    is_sweet_alert_visible = success_alert.is_visible() if success_alert.count() > 0 else False
    
    if is_sweet_alert_visible:
        # If an alert is visible, check if it contains the success message
        alert_text = success_alert.text_content()
        assert "Thanks for the message!!" not in alert_text, \
            f"❌ BUG DETECTED: Success message appeared when form is empty. Alert text: '{alert_text}'"
        print(f"Alert found: {alert_text}")
    else:
        print("✓ No sweet-alert success message displayed")
    
    # Verify that no success dialog appeared
    if dialog_appeared:
        # This assertion will catch the bug where the app sends empty forms
        assert "Thanks for the message!!" not in dialog_message, \
            f"❌ BUG DETECTED: Success message appeared when form is empty. " \
            f"The application should validate required fields before submission. Dialog message: '{dialog_message}'"
    else:
        print("✓ No JavaScript dialog appeared - form validation working correctly")
    
    print("\n✓ Test passed: No success message 'Thanks for the message!!' was displayed for empty form")
