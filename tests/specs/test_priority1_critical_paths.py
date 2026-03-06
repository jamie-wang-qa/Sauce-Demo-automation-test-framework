"""
Priority 1: Critical Path Tests
優先級1：關鍵路徑測試

QA Mindset: These tests validate core business functionality.
If these fail, the application is unusable.
These tests should:
- Run first (smoke tests)
- Always pass
- Be fast (< 30 seconds each)
- Cover the minimum viable user journey

QA思維：這些測試驗證核心業務功能。
如果這些失敗，應用程式將無法使用。
這些測試應該：
- 首先運行（冒煙測試）
- 始終通過
- 快速（每個 < 30秒）
- 涵蓋最小可行的使用者旅程

Test Cases:
- TC-001: Standard user login flow
- TC-002: Add single item to cart and checkout
- TC-003: Complete checkout with valid information
- TC-004: Verify order completion message
"""

import pytest
from tests.pages.login_page import LoginPage
from tests.pages.product_page import ProductPage
from tests.pages.cart_page import CartPage
from tests.pages.checkout_page import CheckoutPage
from tests.fixtures.test_data import STANDARD_USER, CHECKOUT_DATA_SET_1, EXPECTED_TEXT


@pytest.mark.priority1
@pytest.mark.smoke
@pytest.mark.login
class TestCriticalPaths:
    """
    Critical Path Test Suite
    關鍵路徑測試套件
    
    QA Mindset: Group related tests in a class.
    Makes test organization clearer.
    Shared setup/teardown can be added at class level.
    
    QA思維：將相關測試分組在類別中。
    使測試組織更清晰。
    可以在類別層級添加共享設置/清理。
    """
    
    @pytest.mark.login
    def test_tc001_standard_user_login_flow(self, page):
        """
        TC-001: Standard User Login Flow
        標準使用者登入流程
        
        QA Mindset: This is the most critical test.
        If login fails, nothing else can be tested.
        Test should verify:
        - Login page loads correctly
        - Valid credentials work
        - Navigation to products page succeeds
        
        QA思維：這是最關鍵的測試。
        如果登入失敗，其他都無法測試。
        測試應驗證：
        - 登入頁面正確載入
        - 有效憑證有效
        - 導航到商品頁面成功
        """
        # Arrange / 準備
        login_page = LoginPage(page)
        
        # Act / 執行
        # Verify login page elements are visible / 驗證登入頁面元素可見
        assert login_page.verify_login_page_elements(), "Login page elements should be visible"
        
        # Perform login / 執行登入
        login_page.login(STANDARD_USER.username, STANDARD_USER.password)
        
        # Assert / 斷言
        # Verify navigation to products page / 驗證導航到商品頁面
        login_page.wait_for_products_page()
        assert "inventory.html" in page.url, "Should navigate to products page after login"
        
        # Verify no error messages / 驗證沒有錯誤訊息
        assert not login_page.is_error_displayed(), "No error message should be displayed"
    
    @pytest.mark.cart
    def test_tc002_add_single_item_to_cart(self, logged_in_page):
        """
        TC-002: Add Single Item to Cart and Navigate to Cart
        將單一商品加入購物車並導航到購物車
        
        QA Mindset: Validates core cart functionality.
        Critical state changes to verify:
        - Button text changes (Add to cart → Remove)
        - Cart badge updates
        - Navigation to cart works
        
        QA思維：驗證核心購物車功能。
        要驗證的關鍵狀態變化：
        - 按鈕文字變化（加入購物車 → 移除）
        - 購物車徽章更新
        - 導航到購物車有效
        """
        # Arrange / 準備
        product_page = ProductPage(logged_in_page)
        cart_page = CartPage(logged_in_page)
        
        # Act / 執行
        # Verify products are displayed / 驗證商品已顯示
        assert product_page.verify_products_displayed(), "Products should be displayed"
        
        # Add first product to cart / 將第一個商品加入購物車
        initial_button_text = product_page.get_button_text(0)
        product_page.add_to_cart(0)
        
        # Assert / 斷言
        # Verify button text changed / 驗證按鈕文字已變更
        updated_button_text = product_page.get_button_text(0)
        assert updated_button_text != initial_button_text, "Button text should change after adding to cart"
        assert EXPECTED_TEXT["remove"] in updated_button_text, "Button should show 'Remove'"
        
        # Verify cart badge shows 1 / 驗證購物車徽章顯示1
        assert product_page.get_cart_badge_count() == 1, "Cart badge should show 1 item"
        
        # Navigate to cart / 導航到購物車
        product_page.click_cart_icon()
        
        # Verify cart page / 驗證購物車頁面
        assert cart_page.verify_cart_items_displayed(), "Cart items should be displayed"
        assert cart_page.get_item_count() == 1, "Cart should contain 1 item"
    
    @pytest.mark.checkout
    def test_tc003_complete_checkout_with_valid_info(self, logged_in_page):
        """
        TC-003: Complete Checkout with Valid Information
        使用有效資訊完成結帳
        
        QA Mindset: Validates entire purchase flow.
        Critical validations:
        - Form accepts valid input
        - Navigation between steps works
        - Price calculations are correct
        - Order completion succeeds
        
        QA思維：驗證整個購買流程。
        關鍵驗證：
        - 表單接受有效輸入
        - 步驟間導航有效
        - 價格計算正確
        - 訂單完成成功
        """
        # Arrange / 準備
        product_page = ProductPage(logged_in_page)
        cart_page = CartPage(logged_in_page)
        checkout_page = CheckoutPage(logged_in_page)
        
        # Act / 執行
        # Add item to cart / 將商品加入購物車
        product_page.add_to_cart(0)
        product_page.click_cart_icon()
        
        # Start checkout / 開始結帳
        cart_page.click_checkout()
        
        # Fill checkout information / 填寫結帳資訊
        checkout_page.fill_checkout_info(
            CHECKOUT_DATA_SET_1.first_name,
            CHECKOUT_DATA_SET_1.last_name,
            CHECKOUT_DATA_SET_1.postal_code
        )
        checkout_page.click_continue()
        
        # Assert / 斷言
        # Verify step two page / 驗證步驟二頁面
        assert "checkout-step-two.html" in logged_in_page.url, "Should navigate to checkout step two"
        
        # Verify order summary is displayed / 驗證訂單摘要已顯示
        item_total = checkout_page.get_item_total()
        tax = checkout_page.get_tax()
        total = checkout_page.get_total()
        
        assert item_total, "Item total should be displayed"
        assert tax, "Tax should be displayed"
        assert total, "Total should be displayed"
        
        # Complete checkout / 完成結帳
        checkout_page.click_finish()
        
        # Verify completion page / 驗證完成頁面
        assert "checkout-complete.html" in logged_in_page.url, "Should navigate to completion page"
        assert checkout_page.verify_complete_page(), "Complete page should be displayed"
    
    @pytest.mark.checkout
    def test_tc004_verify_order_completion_message(self, logged_in_page):
        """
        TC-004: Verify Order Completion Message
        驗證訂單完成訊息
        
        QA Mindset: Validates user feedback after purchase.
        Critical for user experience:
        - Success message is clear
        - Navigation back works
        - User remains logged in
        
        QA思維：驗證購買後的使用者回饋。
        對使用者體驗至關重要：
        - 成功訊息清晰
        - 返回導航有效
        - 使用者保持登入狀態
        """
        # Arrange / 準備
        product_page = ProductPage(logged_in_page)
        cart_page = CartPage(logged_in_page)
        checkout_page = CheckoutPage(logged_in_page)
        
        # Act / 執行
        # Complete checkout flow / 完成結帳流程
        product_page.add_to_cart(0)
        product_page.click_cart_icon()
        cart_page.click_checkout()
        checkout_page.fill_checkout_info(
            CHECKOUT_DATA_SET_1.first_name,
            CHECKOUT_DATA_SET_1.last_name,
            CHECKOUT_DATA_SET_1.postal_code
        )
        checkout_page.click_continue()
        checkout_page.click_finish()
        
        # Assert / 斷言
        # Verify completion message / 驗證完成訊息
        complete_header = checkout_page.get_complete_header()
        assert complete_header == EXPECTED_TEXT["order_complete_header"], \
            f"Expected '{EXPECTED_TEXT['order_complete_header']}', got '{complete_header}'"
        
        # Verify completion text / 驗證完成文字
        complete_text = checkout_page.get_complete_text()
        assert EXPECTED_TEXT["order_complete_message"] in complete_text, \
            "Completion message should indicate order dispatched"
        
        # Verify back home button / 驗證返回首頁按鈕
        checkout_page.click_back_home()
        assert "inventory.html" in logged_in_page.url, "Should navigate back to products page"
        
        # Verify user still logged in / 驗證使用者仍登入
        assert product_page.verify_products_displayed(), "User should remain logged in"
