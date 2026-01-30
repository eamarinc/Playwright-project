from playwright.sync_api import Page
from config.config import BASE_URL

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.carousel_inner = page.locator('.carousel-inner')
        self.sign_up_link = page.locator("#signin2")
        self.sign_up_modal = page.locator("#signInModal")
        self.username_field = page.locator("#sign-username")
        self.password_field = page.locator("#sign-password")
        self.sign_up_button = page.locator("#signInModal .btn-primary")
        self.login_link = page.locator("#login2")
        self.login_modal = page.locator("#logInModal")
        self.login_username_field = page.locator("#loginusername")
        self.login_password_field = page.locator("#loginpassword")
        self.login_button = page.locator("#logInModal button", has_text="Log in")
        self.welcome_message = page.locator("#nameofuser")
        self.logout_link = page.locator("nav").locator("text=Log out")
        self.phones_link = page.locator("a", has_text="Phones")
        self.cart_link = page.locator("#cartur")
        self.add_to_cart_button = page.locator("a", has_text="Add to cart")
        self.place_order_button = page.locator("button", has_text="Place Order")
        self.place_order_modal = page.locator("#orderModal")
        self.place_order_modal_title = page.locator("#orderModalLabel")
        self.place_order_name_field = page.locator("#name")
        self.place_order_country_field = page.locator("#country")
        self.place_order_city_field = page.locator("#city")
        self.place_order_credit_card_field = page.locator("#card")
        self.place_order_month_field = page.locator("#month")
        self.place_order_year_field = page.locator("#year")
        self.place_order_purchase_button = page.locator("#orderModal button", has_text="Purchase")
        self.place_order_close_button = page.locator("#orderModal button", has_text="Close")
 
    def goto(self):
        self.page.goto(BASE_URL, wait_until="load")
 
    def is_carousel_changing(self, wait_time: int = 10000) -> bool:
        """
        Verifies if the carousel is changing by checking if the active item changes after a wait time.
        """
        # Get the initial active carousel item
        initial_active = self.carousel_inner.locator('.active').first
        initial_html = initial_active.inner_html()
 
        # Wait for the carousel to potentially change
        self.page.wait_for_timeout(wait_time)
 
        # Get the new active carousel item
        new_active = self.carousel_inner.locator('.active').first
        new_html = new_active.inner_html()
 
        # Return True if the active item has changed
        return initial_html != new_html

    def sign_up(self, username: str, password: str):
        self.sign_up_link.click()
        self.sign_up_modal.wait_for(state="visible")
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.sign_up_button.click()

    def open_login_modal(self):
        self.login_link.click()
        self.login_modal.wait_for(state="visible")

    def login(self, username: str, password: str):
        self.login_link.click()
        self.login_modal.wait_for(state="visible")
        self.login_username_field.fill(username)
        self.login_password_field.fill(password)
        self.login_button.click()
        # Wait for modal to close
        self.login_modal.wait_for(state="hidden")
        # Wait for login to complete
        self.page.wait_for_timeout(2000)

    def logout(self):
        self.logout_link.click()
        # Wait for logout to complete
        self.page.wait_for_timeout(2000)

    def click_phones_category(self):
        self.phones_link.click()
        self.page.wait_for_timeout(1000)

    def select_product(self, product_name: str):
        self.page.locator("a", has_text=product_name).click()
        self.page.wait_for_load_state("load")

    def get_product_name(self) -> str:
        locator = self.page.locator(".name")
        locator.wait_for(state="visible")
        content = locator.text_content()
        return content.strip() if content else ""

    def get_product_price(self) -> str:
        locator = self.page.locator(".price-container")
        locator.wait_for(state="visible")
        content = locator.text_content()
        return content.strip() if content else ""

    def add_product_to_cart(self):
        self.add_to_cart_button.click()

    def click_cart(self):
        self.cart_link.click()
        self.page.wait_for_load_state("load")

    def click_place_order_button(self):
        self.place_order_button.click()
        self.place_order_modal.wait_for(state="visible")

    def get_place_order_modal(self):
        return self.place_order_modal

    def get_place_order_modal_title(self) -> str:
        content = self.place_order_modal_title.text_content()
        return content.strip() if content else ""

    def get_place_order_name_field(self):
        return self.place_order_name_field

    def get_place_order_country_field(self):
        return self.place_order_country_field

    def get_place_order_city_field(self):
        return self.place_order_city_field

    def fill_place_order_form(self, name: str, country: str, city: str, 
                              credit_card: str, month: str, year: str):
        self.place_order_name_field.fill(name)
        self.place_order_country_field.fill(country)
        self.place_order_city_field.fill(city)
        self.place_order_credit_card_field.fill(credit_card)
        self.place_order_month_field.fill(month)
        self.place_order_year_field.fill(year)

    def click_purchase_button(self):
        self.place_order_purchase_button.click()

    def close_place_order_modal(self):
        self.place_order_close_button.click()
        self.place_order_modal.wait_for(state="hidden")

    def get_cart_total(self) -> float:
        total_element = self.page.locator("#totalp")
        total_element.wait_for(state="visible")
        content = total_element.text_content()
        if content:
            # Extract only numeric characters and dots
            import re
            numeric_match = re.search(r'\d+\.?\d*', content.strip())
            if numeric_match:
                try:
                    return float(numeric_match.group())
                except ValueError:
                    return 0.0
        return 0.0

    def get_place_order_modal_total(self) -> float:
        total_element = self.page.locator("#totalm")
        total_element.wait_for(state="visible", timeout=5000)
        content = total_element.text_content()
        if content:
            # Extract only numeric characters and dots using regex
            import re
            numeric_match = re.search(r'\d+\.?\d*', content.strip())
            if numeric_match:
                try:
                    return float(numeric_match.group())
                except ValueError:
                    return 0.0
        return 0.0

    def get_cart_items_count(self) -> int:
        """Returns the number of items in the cart."""
        cart_rows = self.page.locator("#tbodyid tr")
        return cart_rows.count()

    def delete_all_cart_items(self):
        """Deletes all items from the cart by clicking the delete link for each item."""
        import time
        while self.get_cart_items_count() > 0:
            # Find the first delete link and click it
            delete_link = self.page.locator("#tbodyid tr a").first
            delete_link.click()
            # Wait for the item to be removed
            time.sleep(1)

    def is_place_order_modal_visible(self) -> bool:
        """Checks if the Place Order modal is visible."""
        try:
            return self.place_order_modal.is_visible()
        except:
            return False