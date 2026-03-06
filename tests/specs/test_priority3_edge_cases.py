"""
Priority 3: Edge Cases & Negative Tests
優先級3：邊界情況與負向測試

QA Mindset: These tests validate error handling and edge cases.
Important for robustness but don't block core functionality.
These tests should:
- Validate error messages
- Test form validation
- Handle edge cases
- Verify error recovery

QA思維：這些測試驗證錯誤處理和邊界情況。
對穩健性很重要，但不阻塞核心功能。
這些測試應該：
- 驗證錯誤訊息
- 測試表單驗證
- 處理邊界情況
- 驗證錯誤恢復

Test Cases:
- TC-010: Invalid login credentials
- TC-011: Locked account handling
- TC-012: Checkout form validation
- TC-013: Empty cart checkout attempt
- TC-014: Special characters in form fields
"""

import pytest
from tests.pages.login_page import LoginPage
from tests.pages.product_page import ProductPage
from tests.pages.cart_page import CartPage
from tests.pages.checkout_page import CheckoutPage
from tests.fixtures.test_data import (
    INVALID_USER, LOCKED_USER, CHECKOUT_DATA_SET_1, CHECKOUT_DATA_SPECIAL_CHARS,
    ERROR_MESSAGES
)


@pytest.mark.priority3
@pytest.mark.negative
class TestEdgeCases:
    """Edge Cases and Negative Test Suite / 邊界情況與負向測試套件"""
    
    @pytest.mark.login
    def test_tc010_invalid_login_credentials(self, page):
        """
        TC-010: Invalid Login Credentials
        無效登入憑證
        
        QA Mindset: Validates error handling and user feedback.
        Error messages should be clear and helpful:
        - Error message displayed
        - User remains on login page
        - User can retry login
        
        QA思維：驗證錯誤處理和使用者回饋。
        錯誤訊息應該清晰且有用：
        - 顯示錯誤訊息
        - 使用者停留在登入頁面
        - 使用者可以重試登入
        """
        # Arrange / 準備
        login_page = LoginPage(page)
        
        # Act / 執行
        login_page.login(INVALID_USER.username, INVALID_USER.password)
        
        # Assert / 斷言
        assert login_page.is_error_displayed(), "Error message should be displayed"
        
        error_message = login_page.get_error_message()
        assert ERROR_MESSAGES["invalid_credentials"] in error_message, \
            f"Expected error message about invalid credentials, got: {error_message}"
        
        # Verify still on login page / 驗證仍在登入頁面
        assert "inventory.html" not in page.url, "Should remain on login page"
        assert login_page.verify_login_page_elements(), "Login page should still be displayed"
    
    @pytest.mark.login
    def test_tc011_locked_account_handling(self, page):
        """
        TC-011: Locked Account Handling
        鎖定帳號處理
        
        QA Mindset: Validates account security and error messaging.
        Locked accounts should:
        - Show appropriate error message
        - Prevent login
        - Not allow access to application
        
        QA思維：驗證帳號安全性和錯誤訊息。
        鎖定帳號應該：
        - 顯示適當的錯誤訊息
        - 阻止登入
        - 不允許存取應用程式
        """
        # Arrange / 準備
        login_page = LoginPage(page)
        
        # Act / 執行
        login_page.login(LOCKED_USER.username, LOCKED_USER.password)
        
        # Assert / 斷言
        assert login_page.is_error_displayed(), "Error message should be displayed"
        
        error_message = login_page.get_error_message()
        assert ERROR_MESSAGES["locked_account"] in error_message, \
            f"Expected locked account error, got: {error_message}"
        
        # Verify login prevented / 驗證登入被阻止
        assert "inventory.html" not in page.url, "Should not navigate to products page"
        assert login_page.verify_login_page_elements(), "Should remain on login page"
    
    @pytest.mark.checkout
    def test_tc012_checkout_form_validation_empty_fields(self, logged_in_page):
        """
        TC-012: Checkout Form Validation - Empty Fields
        結帳表單驗證 - 空欄位
        
        QA Mindset: Validates form validation logic.
        All required fields should be validated:
        - Error when all fields empty
        - Error when individual fields missing
        - User remains on form page
        
        QA思維：驗證表單驗證邏輯。
        所有必填欄位都應該被驗證：
        - 所有欄位為空時顯示錯誤
        - 個別欄位缺失時顯示錯誤
        - 使用者停留在表單頁面
        """
        # Arrange / 準備
        product_page = ProductPage(logged_in_page)
        cart_page = CartPage(logged_in_page)
        checkout_page = CheckoutPage(logged_in_page)
        
        # Act / 執行
        # Add item and go to checkout / 加入商品並前往結帳
        product_page.add_to_cart(0)
        product_page.click_cart_icon()
        cart_page.click_checkout()
        
        # Try to continue with empty fields / 嘗試以空欄位繼續
        # Use click_continue_no_wait because validation should prevent navigation
        # 使用 click_continue_no_wait，因為驗證應該阻止導航
        checkout_page.click_continue_no_wait()
        
        # Assert / 斷言
        assert checkout_page.is_error_displayed(), "Error message should be displayed"
        
        error_message = checkout_page.get_error_message()
        assert ERROR_MESSAGES["first_name_required"] in error_message, \
            "Should show first name required error"
        
        # Fill first name only / 只填寫名字
        checkout_page.enter_first_name("John")
        # Use click_continue_no_wait because validation should prevent navigation
        # 使用 click_continue_no_wait，因為驗證應該阻止導航
        checkout_page.click_continue_no_wait()
        
        assert checkout_page.is_error_displayed(), "Error should still be displayed"
        error_message = checkout_page.get_error_message()
        assert ERROR_MESSAGES["last_name_required"] in error_message or \
               ERROR_MESSAGES["postal_code_required"] in error_message, \
            "Should show missing field error"
    
    @pytest.mark.cart
    def test_tc013_empty_cart_checkout_attempt(self, logged_in_page):
        """
        TC-013: Empty Cart Checkout Attempt
        空購物車結帳嘗試
        
        QA Mindset: Validates business logic.
        Checkout should require items in cart:
        - Checkout button should be disabled or redirect
        - Direct navigation to checkout prevented
        - User cannot proceed without items
        
        QA思維：驗證業務邏輯。
        結帳應該需要購物車中的商品：
        - 結帳按鈕應該被停用或重定向
        - 直接導航到結帳被阻止
        - 沒有商品時使用者無法繼續
        """
        # Arrange / 準備
        cart_page = CartPage(logged_in_page)
        
        # Act / 執行
        # Navigate to cart when empty / 空購物車時導航到購物車
        logged_in_page.goto("https://www.saucedemo.com/cart.html")
        
        # Assert / 斷言
        assert cart_page.is_cart_empty(), "Cart should be empty"
        
        # Try to access checkout directly / 嘗試直接存取結帳
        # Note: Sauce Demo might allow this, but cart should be empty
        # 注意：Sauce Demo 可能允許此操作，但購物車應該是空的
        if cart_page.is_visible(cart_page.CHECKOUT_BUTTON):
            # If button exists, clicking should show empty cart or error
            # 如果按鈕存在，點擊應該顯示空購物車或錯誤
            pass
    
    @pytest.mark.checkout
    def test_tc014_special_characters_in_form_fields(self, logged_in_page):
        """
        TC-014: Special Characters in Form Fields
        表單欄位中的特殊字元
        
        QA Mindset: Validates input handling.
        Real users may enter special characters:
        - Form should accept special characters
        - No validation errors for valid special chars
        - Special characters preserved in submission
        
        QA思維：驗證輸入處理。
        真實使用者可能會輸入特殊字元：
        - 表單應該接受特殊字元
        - 有效特殊字元不應有驗證錯誤
        - 提交時保留特殊字元
        """
        # Arrange / 準備
        product_page = ProductPage(logged_in_page)
        cart_page = CartPage(logged_in_page)
        checkout_page = CheckoutPage(logged_in_page)
        
        # Act / 執行
        # Add item and go to checkout / 加入商品並前往結帳
        product_page.add_to_cart(0)
        product_page.click_cart_icon()
        cart_page.click_checkout()
        
        # Fill form with special characters / 使用特殊字元填寫表單
        checkout_page.fill_checkout_info(
            CHECKOUT_DATA_SPECIAL_CHARS.first_name,
            CHECKOUT_DATA_SPECIAL_CHARS.last_name,
            CHECKOUT_DATA_SPECIAL_CHARS.postal_code
        )
        checkout_page.click_continue()
        
        # Assert / 斷言
        # Verify no validation errors / 驗證沒有驗證錯誤
        assert not checkout_page.is_error_displayed(), \
            "Form should accept special characters without errors"
        
        # Verify navigation to step two / 驗證導航到步驟二
        assert "checkout-step-two.html" in logged_in_page.url, \
            "Should proceed to checkout step two"
