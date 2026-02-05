
def test_place_order_with_empty_cart(home_page):
    """
    Test that verifies the Place Order modal should NOT appear 
    when trying to place an order with an empty cart.
    
    Steps:
    1. Open https://www.demoblaze.com/index.html
    2. Click on "Cart" menu
    3. Verify there are no products in the cart, if there are, delete them
    4. Click on "Place Order" button
    5. Assert that the modal does NOT appear (expected behavior)
    
    Expected: The modal should not appear or should show a validation message
    when the cart is empty.
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
    
    # Wait a moment for modal to potentially appear
    home_page.page.wait_for_timeout(500)
    
    # Step 5: Verify that the modal SHOULD NOT appear with empty cart
    modal_visible = home_page.is_place_order_modal_visible()
    
    # Assert that the modal should NOT be visible when cart is empty
    assert not modal_visible, "Place Order modal should NOT appear when cart is empty"
    
    print("✓ Place Order modal correctly NOT displayed with empty cart")
    print("\n✓ Test completed: Validated that modal does not appear with empty cart")
