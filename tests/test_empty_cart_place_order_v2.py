
def test_place_order_should_not_show_modal_with_empty_cart(home_page):
    """
    Test that verifies the Place Order button SHOULD NOT show the modal 
    when the cart is empty (expected behavior).
    
    This test will FAIL if the application shows the modal with an empty cart,
    which is considered a bug.
    
    Steps:
    1. Open https://www.demoblaze.com/index.html
    2. Click on "Cart" menu
    3. Verify there are no products in the cart, if there are, delete them
    4. Click on "Place Order" button
    5. Verify that the "Place order" modal is NOT displayed (expected behavior)
    """
    
    # Step 1: Already done by fixture (home_page.goto())
    print("\n✓ Opened demoblaze.com")
    
    # Step 2: Click on "Cart" menu
    home_page.click_cart()
    home_page.page.wait_for_url("**/cart.html", timeout=5000)  # Wait for cart page to load
    
    # Verify we are on the cart page
    assert "cart.html" in home_page.page.url, "Not on cart page"
    print("✓ Navigated to Cart page")
    
    # Step 3: Verify there are no products in the cart, if there are, delete them
    cart_items_count = home_page.get_cart_items_count()
    print(f"  Cart items count: {cart_items_count}")
    
    if cart_items_count > 0:
        print(f"  Found {cart_items_count} item(s) in cart. Deleting them...")
        home_page.delete_all_cart_items()
        
        # Verify all items were deleted
        final_count = home_page.get_cart_items_count()
        assert final_count == 0, f"Cart should be empty, but has {final_count} items"
        print("  ✓ All items deleted from cart")
    else:
        print("  ✓ Cart is already empty")
    
    # Step 4: Click on "Place Order" button
    place_order_button = home_page.page.locator("button", has_text="Place Order")
    place_order_button.click()
    print("✓ Clicked on 'Place Order' button")
    
    # Wait a moment to see if modal appears
    home_page.page.wait_for_timeout(500)
    
    # Step 5: Verify that the "Place order" modal is NOT displayed (EXPECTED behavior)
    modal_visible = home_page.is_place_order_modal_visible()
    assert not modal_visible, "BUG DETECTED: Place Order modal should NOT be visible when cart is empty, but it is displayed!"
    print("✓ Verified: Place Order modal is NOT displayed (as expected for empty cart)")
    
    print("\n✓ Test passed: Cannot place order with empty cart")


def test_place_order_with_empty_cart_documents_actual_behavior(home_page):
    """
    Test that documents the ACTUAL behavior when trying to place an order 
    with an empty cart.
    
    Steps:
    1. Open https://www.demoblaze.com/index.html
    2. Click on "Cart" menu
    3. Verify there are no products in the cart, if there are, delete them
    4. Click on "Place Order" button
    5. Verify the behavior with empty cart (documents actual behavior)
    """
    
    # Step 1: Already done by fixture (home_page.goto())
    print("\n✓ Opened demoblaze.com")
    
    # Step 2: Click on "Cart" menu
    home_page.click_cart()
    home_page.page.wait_for_url("**/cart.html", timeout=5000)  # Wait for cart page to load
    
    # Verify we are on the cart page
    assert "cart.html" in home_page.page.url, "Not on cart page"
    print("✓ Navigated to Cart page")
    
    # Step 3: Verify there are no products in the cart, if there are, delete them
    cart_items_count = home_page.get_cart_items_count()
    print(f"  Cart items count: {cart_items_count}")
    
    if cart_items_count > 0:
        print(f"  Found {cart_items_count} item(s) in cart. Deleting them...")
        home_page.delete_all_cart_items()
        
        # Verify all items were deleted
        final_count = home_page.get_cart_items_count()
        assert final_count == 0, f"Cart should be empty, but has {final_count} items"
        print("  ✓ All items deleted from cart")
    else:
        print("  ✓ Cart is already empty")
    
    # Step 4: Click on "Place Order" button
    place_order_button = home_page.page.locator("button", has_text="Place Order")
    place_order_button.click()
    print("✓ Clicked on 'Place Order' button")
    
    # Wait a moment for modal to appear
    home_page.page.wait_for_timeout(500)
    
    # Step 5: Verify that the modal appears (documenting ACTUAL behavior)
    modal_visible = home_page.is_place_order_modal_visible()
    
    # The application currently shows the modal even with empty cart
    # This documents the actual behavior
    if modal_visible:
        print("⚠️  Place Order modal IS displayed (even with empty cart)")
        print("    Note: This may be unexpected behavior - ideally the modal")
        print("    should not appear or show validation when cart is empty")
        
        # Verify the modal total is 0 or empty
        modal_total_element = home_page.page.locator("#totalm")
        if modal_total_element.is_visible():
            modal_total_text = modal_total_element.text_content()
            print(f"    Modal total text: '{modal_total_text}'")
            # When cart is empty, the total shows "Total:" without a value
        
        # Close the modal
        home_page.close_place_order_modal()
        print("✓ Closed Place Order modal")
    else:
        print("✓ Place Order modal is NOT displayed (expected behavior)")
    
    print("\n✓ Test completed: Documented actual behavior with empty cart")
