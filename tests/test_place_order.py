from config.config import TEST_USER
from datetime import datetime
import re

def test_place_order_modal(home_page):
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
    print(f"Product in cart: {cart_product_name}")

    # Verify product price in cart matches the product page price
    cart_product_price = cart_product_row.locator("td").nth(2).text_content()
    assert price_value in cart_product_price, f"Price mismatch: expected '{price_value}' in cart, got '{cart_product_price}'"
    
    # Get all products in the cart and sum their prices
    all_cart_rows = home_page.page.locator("#tbodyid tr")
    total_rows = all_cart_rows.count()
    print(f"\nTotal products in cart: {total_rows}")
    
    # Calculate the sum of all product prices
    calculated_total = 0.0
    
    for i in range(total_rows):
        row = all_cart_rows.nth(i)
        product_name = row.locator("td").nth(1).text_content()
        product_price_text = row.locator("td").nth(2).text_content()
        
        # Extract numeric value from price
        price_match = re.search(r'\d+\.?\d*', product_price_text.strip())
        if price_match:
            price = float(price_match.group())
            calculated_total += price
            print(f"  Product {i+1}: {product_name.strip()} - Price: {price}")
    
    print(f"\nCalculated total (sum of all prices): {calculated_total}")
    
    # Get the total from the cart page
    cart_total = home_page.get_cart_total()
    print(f"Cart total displayed: {cart_total}")
    assert cart_total > 0, "Cart total is not valid"
    
    # Verify that calculated total matches displayed cart total
    assert calculated_total == cart_total, \
        f"Calculated total ({calculated_total}) does not match displayed cart total ({cart_total})"
    print(f"✓ Price calculation verified: Sum of prices ({calculated_total}) = Cart total ({cart_total})")
    
    # Click on "Place Order" button
    home_page.click_place_order_button()
    
    # Wait for modal to be visible
    home_page.page.wait_for_timeout(500)
    
    # Verify that the "Place order" modal is displayed
    place_order_modal = home_page.get_place_order_modal()
    assert place_order_modal.is_visible(), "Place order modal is not visible"
    
    # Verify modal title
    modal_title = home_page.get_place_order_modal_title()
    assert "Place order" in modal_title, f"Expected 'Place order' in modal title, got '{modal_title}'"
    print(f"Modal title: {modal_title}")
    
    # Verify modal is displayed and has form fields
    name_field = home_page.get_place_order_name_field()
    assert name_field.is_visible(), "Name field is not visible in Place order modal"
    
    country_field = home_page.get_place_order_country_field()
    assert country_field.is_visible(), "Country field is not visible in Place order modal"
    
    city_field = home_page.get_place_order_city_field()
    assert city_field.is_visible(), "City field is not visible in Place order modal"
    
    # Get the total from the Place Order modal
    modal_total = home_page.get_place_order_modal_total()
    print(f"Modal total: {modal_total}")
    assert modal_total > 0, "Modal total is not valid"
    
    # Verify that cart total matches modal total
    assert cart_total == modal_total, f"Total amounts don't match: Cart total '{cart_total}' != Modal total '{modal_total}'"
    print(f"Total verification passed: Cart ({cart_total}) = Modal ({modal_total})")
    
    # Fill the Place Order form with payment information
    print("\nFilling payment information...")
    home_page.fill_place_order_form(
        name="Pedro Pérez",
        country="Chile",
        city="Santiago",
        credit_card="987654321",
        month="01",
        year="2027"
    )
    print("Payment information filled successfully")
    
    # Click the Purchase button
    home_page.click_purchase_button()
    
    # Wait for confirmation modal to appear
    home_page.page.wait_for_timeout(500)
    
    # Verify the confirmation modal is displayed
    confirmation_modal = home_page.page.locator(".sweet-alert")
    assert confirmation_modal.is_visible(), "Confirmation modal is not visible"
    
    # Verify the confirmation message
    confirmation_title = home_page.page.locator(".sweet-alert h2").text_content()
    assert "Thank you for your purchase!" in confirmation_title, \
        f"Expected 'Thank you for your purchase!' in confirmation, got '{confirmation_title}'"
    print(f"\n✓ Confirmation message: {confirmation_title}")
    
    # Get the purchase details text
    confirmation_text = home_page.page.locator(".sweet-alert .lead").text_content()
    print(f"Purchase details: {confirmation_text}")
    
    # Extract and verify the date from the confirmation
    
    date_match = re.search(r'Date:\s*(\d{1,2}/\d{1,2}/\d{4})', confirmation_text)
    if date_match:
        purchase_date_str = date_match.group(1)
        print(f"Purchase date found: {purchase_date_str}")
        
        # Get current date
        current_date = datetime.now()
        current_date_str = current_date.strftime("%-d/%-m/%Y")  # Format: D/M/YYYY without leading zeros
        
        # Also try with leading zeros in case the format varies
        current_date_str_with_zeros = current_date.strftime("%d/%m/%Y")  # Format: DD/MM/YYYY
        
        # Verify the date matches current date (try both formats)
        assert purchase_date_str == current_date_str or purchase_date_str == current_date_str_with_zeros, \
            f"Purchase date '{purchase_date_str}' does not match current date '{current_date_str}' or '{current_date_str_with_zeros}'"
        print(f"✓ Date verification passed: Purchase date ({purchase_date_str}) matches current date ({current_date_str})")
    else:
        print("Warning: Date not found in confirmation text")
    
    print("\n✓ Purchase completed successfully!")
    
    # Click the "OK" button in the confirmation modal
    ok_button = home_page.page.locator(".sweet-alert button.confirm")
    ok_button.click()
    print("✓ Clicked OK button")
    
    # Wait for modal to close
    home_page.page.wait_for_timeout(500)
    
    # Verify the confirmation modal is no longer visible
    assert not confirmation_modal.is_visible(), "Confirmation modal is still visible after clicking OK"
    print("✓ Confirmation modal closed")
    
    # Verify that the Place Order modal is also closed
    assert not place_order_modal.is_visible(), "Place Order modal is still visible after clicking OK"
    print("✓ Place Order modal closed")
    
    # Verify that we are redirected to the home page
    assert "index.html" in home_page.page.url or home_page.page.url.endswith("/"), \
        f"Not redirected to home page. Current URL: {home_page.page.url}"
    print(f"✓ Redirected to home page: {home_page.page.url}")
    
    print("\n✓ Test completed: All modals closed and returned to home page!")

