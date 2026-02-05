from config.config import TEST_USER

def test_add_samsung_galaxy_s7_to_cart(home_page):
    # Login first
    home_page.login(TEST_USER["username"], TEST_USER["password"]) 

    # Click on "Phones" category
    home_page.click_phones_category()

    # Click on "Samsung galaxy s7" to view details
    home_page.select_product("Samsung galaxy s7")

    # Verify the product details correspond to "Samsung galaxy s7"
    product_name = home_page.get_product_name()
    assert product_name == "Samsung galaxy s7", f"Expected 'Samsung galaxy s7', got '{product_name}'"

    # Verify price is displayed and save it for later comparison
    product_price = home_page.get_product_price()
    assert "$" in product_price, f"Price not displayed correctly: '{product_price}'"
    
    # Extract the numeric price value
    price_value = product_price.split("*")[0].strip().replace("$", "").strip()

    # Click "Add to cart" button and handle dialog
    with home_page.page.expect_event("dialog") as dialog_info:
        home_page.add_product_to_cart()
    dialog = dialog_info.value
    
    # Verify the dialog message confirms product was added
    assert dialog.message == "Product added.", f"Expected 'Product added.', got '{dialog.message}'"
    dialog.accept()
    
    # Click on "Cart" menu
    home_page.click_cart()
    home_page.page.wait_for_url("**/cart.html", timeout=10000)

    # Verify we are on the cart page
    assert "cart.html" in home_page.page.url, "Not on cart page"
    
    # Wait for cart table body to be attached to DOM
    home_page.page.locator("#tbodyid").wait_for(state="attached", timeout=10000)
    
    # Wait for the specific product to appear in cart
    home_page.page.locator("#tbodyid tr").filter(has_text="Samsung galaxy s7").first.wait_for(state="visible", timeout=10000)

    # Verify the product is in the cart
    cart_product_row = home_page.page.locator("#tbodyid tr").filter(has_text="Samsung galaxy s7")
    assert cart_product_row.count() > 0, "Samsung galaxy s7 not found in cart"
    
    # Verify product name in cart
    cart_product_name = cart_product_row.locator("td").nth(1).text_content()
    assert "Samsung galaxy s7" in cart_product_name, f"Expected 'Samsung galaxy s7' in cart, got '{cart_product_name}'"
    print(cart_product_name)

    # Verify product price in cart matches the product page price
    cart_product_price = cart_product_row.locator("td").nth(2).text_content()
    assert price_value in cart_product_price, f"Price mismatch: expected '{price_value}' in cart, got '{cart_product_price}'"
    
    # Count total products in cart before deletion
    cart_rows_before = home_page.page.locator("#tbodyid tr")
    products_count_before = cart_rows_before.count()
    print(f"Products in cart before deletion: {products_count_before}")
    
    # Count how many instances of "Samsung galaxy s7" are in the cart
    samsung_s7_rows_before = home_page.page.locator("#tbodyid tr").filter(has_text="Samsung galaxy s7")
    samsung_s7_count_before = samsung_s7_rows_before.count()
    print(f"Samsung galaxy s7 instances before deletion: {samsung_s7_count_before}")
    
    # Click on "Delete" link to remove the specific product from cart
    # Use .first to delete the first occurrence if there are multiple
    first_row = cart_product_row.first
    delete_link = first_row.locator("a")
    delete_link.click()
    
    # Wait for the specific row to be removed from the DOM
    first_row.wait_for(state="detached", timeout=5000)
    
    # Wait for the page to update after deletion
    home_page.page.wait_for_timeout(500)
    
    # Verify the specific Samsung galaxy s7 instance was removed
    # Re-create the locator to get fresh count
    samsung_s7_rows_after = home_page.page.locator("#tbodyid tr").filter(has_text="Samsung galaxy s7")
    samsung_s7_count_after = samsung_s7_rows_after.count()
    
    # Since the application seems to remove all instances, we verify at least one was removed
    assert samsung_s7_count_after < samsung_s7_count_before, \
        f"Expected Samsung galaxy s7 count to decrease, but went from {samsung_s7_count_before} to {samsung_s7_count_after}"
    
    print(f"Samsung galaxy s7 instances after deletion: {samsung_s7_count_after}")
    
    # Verify total products in cart decreased
    # Note: The application may remove all instances of the same product, not just one
    cart_rows_after = home_page.page.locator("#tbodyid tr")
    products_count_after = cart_rows_after.count()
    print(f"Products in cart after deletion: {products_count_after}")
    
    assert products_count_after < products_count_before, \
        f"Expected total products to decrease, but went from {products_count_before} to {products_count_after}"
    
    print(f"Products in cart after deletion: {products_count_after}")
    print(f"Samsung galaxy s7 instances after deletion: {samsung_s7_count_after}")
    print("Product successfully removed from cart!")