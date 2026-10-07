import time
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

@pytest.fixture(scope="module")
def driver():
    """Create and configure a Chrome WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    yield driver
    
    driver.quit()


class TestShoppingScenarios:
    """Test suite covering the day 3 shopping scenario test cases (TC01 to TC10)."""

    def test_tc01_open_website(self, driver):
        """TC01: Open the online shopping website."""
        driver.get("https://vinothqaacademy.com/")
        # Expected Result: Shopping website opens successfully
        assert driver.title != ""

    def test_tc02_alert_accept(self, driver):
        """TC02: Customer clicks Delete/Remove Product and confirmation popup appears."""
        # Inject an alert to simulate clicking a delete button
        driver.execute_script("window.confirm('Are you sure you want to remove this product?');")
        
        # Expected Result: Product deletion is confirmed (accept alert)
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert.accept()

    def test_tc03_alert_dismiss(self, driver):
        """TC03: Customer clicks Delete/Remove Product but chooses Cancel."""
        driver.execute_script("window.confirm('Are you sure you want to remove this product?');")
        
        # Expected Result: Product remains in the cart (dismiss alert)
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert.dismiss()

    def test_tc04_prompt_send_keys(self, driver):
        """TC04: Customer enters a name/coupon/customer information in a prompt popup."""
        driver.execute_script("window.prompt('Enter your coupon code:');")
        
        # Expected Result: Entered information is submitted successfully (send keys to prompt)
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert.send_keys("DISCOUNT2026")
        alert.accept()

    def test_tc05_mouse_hover(self, driver):
        """TC05: Customer moves the mouse over the Products/Category menu."""
        # Inject a dummy menu element to hover over
        driver.execute_script("""
            var menu = document.createElement('div');
            menu.id = 'category-menu';
            menu.innerHTML = 'Products/Category';
            menu.style.padding = '20px';
            menu.style.backgroundColor = 'yellow';
            document.body.insertBefore(menu, document.body.firstChild);
        """)
        
        # Expected Result: Product categories/submenu are displayed (Mouse hover)
        menu_element = driver.find_element(By.ID, "category-menu")
        actions = ActionChains(driver)
        actions.move_to_element(menu_element).perform()

    def test_tc06_double_click(self, driver):
        """TC06: Customer double-clicks a product."""
        driver.execute_script("""
            var product = document.createElement('button');
            product.id = 'product-item';
            product.innerHTML = 'Double click me';
            product.ondblclick = function() { this.innerHTML = 'Double clicked!'; };
            document.body.insertBefore(product, document.body.firstChild);
        """)
        
        # Expected Result: Product details page opens (Double Click)
        product_element = driver.find_element(By.ID, "product-item")
        actions = ActionChains(driver)
        actions.double_click(product_element).perform()
        
        # Verify the double click worked
        assert product_element.text == 'Double clicked!'

    def test_tc07_drag_and_drop(self, driver):
        """TC07: Customer drags a product/item into a shopping cart area."""
        driver.execute_script("""
            var item = document.createElement('div');
            item.id = 'draggable-item';
            item.style.width = '50px'; item.style.height = '50px'; item.style.background = 'red';
            item.draggable = true;
            document.body.insertBefore(item, document.body.firstChild);
            
            var cart = document.createElement('div');
            cart.id = 'shopping-cart';
            cart.style.width = '100px'; cart.style.height = '100px'; cart.style.background = 'blue';
            document.body.insertBefore(cart, document.body.firstChild);
        """)
        
        # Expected Result: Product is moved to the cart (Drag & Drop)
        source = driver.find_element(By.ID, "draggable-item")
        target = driver.find_element(By.ID, "shopping-cart")
        actions = ActionChains(driver)
        actions.drag_and_drop(source, target).perform()

    def test_tc08_explicit_wait(self, driver):
        """TC08: Customer searches for a product and waits for the product results to load."""
        driver.execute_script("""
            setTimeout(function() {
                var result = document.createElement('div');
                result.id = 'search-result';
                result.innerHTML = 'Product Found';
                document.body.insertBefore(result, document.body.firstChild);
            }, 2000);
        """)
        
        # Expected Result: Product is displayed successfully (Explicit Wait)
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-result"))
        )
        assert result.is_displayed()

    def test_tc09_clickable_wait(self, driver):
        """TC09: Customer completes checkout and waits until the Place Order button becomes clickable."""
        driver.execute_script("""
            var btn = document.createElement('button');
            btn.id = 'place-order';
            btn.innerHTML = 'Place Order';
            btn.disabled = true;
            btn.style.position = 'fixed';
            btn.style.top = '0px';
            btn.style.left = '0px';
            btn.style.zIndex = '999999';
            document.body.insertBefore(btn, document.body.firstChild);
            
            setTimeout(function() {
                btn.disabled = false;
            }, 2000);
        """)
        
        # Expected Result: Order is submitted successfully (Clickable Wait)
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "place-order"))
        )
        assert btn.is_enabled()
        btn.click()

    def test_tc10_alert_wait(self, driver):
        """TC10: Customer completes the purchase and waits for the order confirmation popup."""
        driver.execute_script("""
            setTimeout(function() {
                alert('Order Confirmation: Success!');
            }, 2000);
        """)
        
        # Expected Result: Confirmation alert is handled successfully (Alert Wait)
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        assert 'Success' in alert.text
        alert.accept()


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])