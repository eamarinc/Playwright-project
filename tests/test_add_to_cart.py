import time
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
    
    # Wait a moment for the cart to update
    time.sleep(1)

    # Click on "Cart" menu
    home_page.click_cart()
    time.sleep(3)  # Wait for cart page to load

    # Verify we are on the cart page
    assert "cart.html" in home_page.page.url, "Not on cart page"

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
    delete_link = cart_product_row.first.locator("a")
    delete_link.click()
    
    # Wait for the product to be removed from the DOM
    time.sleep(2)
    
    # Verify the specific Samsung galaxy s7 instance was removed
    samsung_s7_rows_after = home_page.page.locator("#tbodyid tr").filter(has_text="Samsung galaxy s7")
    samsung_s7_count_after = samsung_s7_rows_after.count()
    assert samsung_s7_count_after == samsung_s7_count_before - 1, \
        f"Expected Samsung galaxy s7 count to decrease by 1, but went from {samsung_s7_count_before} to {samsung_s7_count_after}"
    
    # Verify total products in cart decreased by 1
    cart_rows_after = home_page.page.locator("#tbodyid tr")
    products_count_after = cart_rows_after.count()
    assert products_count_after == products_count_before - 1, \
        f"Expected total products to decrease by 1, but went from {products_count_before} to {products_count_after}"
    
    print(f"Products in cart after deletion: {products_count_after}")
    print(f"Samsung galaxy s7 instances after deletion: {samsung_s7_count_after}")
    print("Product successfully removed from cart!")