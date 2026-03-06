"""
Checkout Page Object Model
結帳頁面物件模型

QA Mindset: Encapsulates checkout process across multiple steps.
This page handles:
- Checkout step one: Customer information form
- Checkout step two: Order summary review
- Checkout complete: Order confirmation

QA思維：封裝跨多個步驟的結帳流程。
此頁面處理：
- 結帳步驟一：客戶資訊表單
- 結帳步驟二：訂單摘要審查
- 結帳完成：訂單確認
"""

from playwright.sync_api import Page
from tests.pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Checkout Page Object / 結帳頁面物件"""
    
    # Step One Selectors / 步驟一選擇器
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    CANCEL_BUTTON = "[data-test='cancel']"
    ERROR_MESSAGE = "[data-test='error']"
    
    # Step Two Selectors / 步驟二選擇器
    SUMMARY_INFO = ".summary_info"
    ITEM_TOTAL = ".summary_subtotal_label"
    TAX = ".summary_tax_label"
    TOTAL = ".summary_total_label"
    FINISH_BUTTON = "[data-test='finish']"
    
    # Complete Page Selectors / 完成頁面選擇器
    COMPLETE_HEADER = "[data-test='complete-header']"
    COMPLETE_TEXT = "[data-test='complete-text']"
    BACK_HOME_BUTTON = "[data-test='back-to-products']"
    
    def __init__(self, page: Page):
        """Initialize Checkout Page / 初始化結帳頁面"""
        super().__init__(page)
    
    # Step One Methods / 步驟一方法
    def enter_first_name(self, first_name: str) -> None:
        """Enter first name / 輸入名字"""
        self.fill(self.FIRST_NAME_INPUT, first_name)
    
    def enter_last_name(self, last_name: str) -> None:
        """Enter last name / 輸入姓氏"""
        self.fill(self.LAST_NAME_INPUT, last_name)
    
    def enter_postal_code(self, postal_code: str) -> None:
        """Enter postal code / 輸入郵遞區號"""
        self.fill(self.POSTAL_CODE_INPUT, postal_code)
    
    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """
        Fill all checkout information / 填寫所有結帳資訊
        
        QA Mindset: High-level method for complete form filling.
        Most tests will use this method.
        
        QA思維：完整表單填寫的高層級方法。
        大多數測試將使用此方法。
        """
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
    
    def click_continue(self) -> None:
        """
        Click continue button / 點擊繼續按鈕
        
        QA Mindset: Navigate to step two.
        Waits for navigation to complete.
        Use this for positive tests when form is valid.
        
        QA思維：導航到步驟二。
        等待導航完成。
        當表單有效時，在正向測試中使用此方法。
        """
        self.click(self.CONTINUE_BUTTON)
        self.wait_for_url("**/checkout-step-two.html")
    
    def click_continue_no_wait(self) -> None:
        """
        Click continue button without waiting for navigation / 點擊繼續按鈕但不等待導航
        
        QA Mindset: For negative tests where form validation may fail.
        Page should not navigate if validation fails.
        Use this when testing form validation errors.
        
        QA思維：用於表單驗證可能失敗的負向測試。
        如果驗證失敗，頁面不應該導航。
        在測試表單驗證錯誤時使用此方法。
        """
        self.click(self.CONTINUE_BUTTON)
        # Don't wait for navigation - validation may prevent it / 不等待導航 - 驗證可能阻止它
    
    def click_cancel(self) -> None:
        """
        Click cancel button / 點擊取消按鈕
        
        QA Mindset: Cancel checkout and return to cart.
        Useful for negative testing.
        
        QA思維：取消結帳並返回購物車。
        對負向測試有用。
        """
        self.click(self.CANCEL_BUTTON)
        self.wait_for_url("**/cart.html")
    
    def get_error_message(self) -> str:
        """
        Get error message text / 獲取錯誤訊息文字
        
        QA Mindset: Extract error for validation testing.
        Returns empty string if no error.
        
        QA思維：提取錯誤用於驗證測試。
        如果沒有錯誤則返回空字串。
        """
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed / 檢查是否顯示錯誤訊息"""
        return self.is_visible(self.ERROR_MESSAGE)
    
    # Step Two Methods / 步驟二方法
    def get_item_total(self) -> str:
        """
        Get item total from summary / 從摘要獲取商品總計
        
        QA Mindset: Extract total for calculation verification.
        Verifies pricing calculations are correct.
        
        QA思維：提取總計用於計算驗證。
        驗證定價計算是否正確。
        """
        return self.get_text(self.ITEM_TOTAL)
    
    def get_tax(self) -> str:
        """Get tax amount / 獲取稅額"""
        return self.get_text(self.TAX)
    
    def get_total(self) -> str:
        """Get total amount / 獲取總金額"""
        return self.get_text(self.TOTAL)
    
    def click_finish(self) -> None:
        """
        Click finish button / 點擊完成按鈕
        
        QA Mindset: Complete checkout process.
        Critical action - must work correctly.
        
        QA思維：完成結帳流程。
        關鍵操作 - 必須正確運作。
        """
        self.click(self.FINISH_BUTTON)
        self.wait_for_url("**/checkout-complete.html")
    
    # Complete Page Methods / 完成頁面方法
    def get_complete_header(self) -> str:
        """
        Get completion header text / 獲取完成標題文字
        
        QA Mindset: Verify order completion message.
        Critical for user feedback verification.
        
        QA思維：驗證訂單完成訊息。
        對使用者回饋驗證至關重要。
        """
        return self.get_text(self.COMPLETE_HEADER)
    
    def get_complete_text(self) -> str:
        """Get completion message text / 獲取完成訊息文字"""
        return self.get_text(self.COMPLETE_TEXT)
    
    def click_back_home(self) -> None:
        """
        Click back home button / 點擊返回首頁按鈕
        
        QA Mindset: Return to products page.
        Completes the checkout flow.
        
        QA思維：返回商品頁面。
        完成結帳流程。
        """
        self.click(self.BACK_HOME_BUTTON)
        self.wait_for_url("**/inventory.html")
    
    def verify_complete_page(self) -> bool:
        """
        Verify complete page is displayed / 驗證完成頁面已顯示
        
        QA Mindset: Page load verification.
        Ensures order completion page loaded correctly.
        
        QA思維：頁面載入驗證。
        確保訂單完成頁面正確載入。
        """
        return (
            self.is_visible(self.COMPLETE_HEADER) and
            self.is_visible(self.COMPLETE_TEXT) and
            self.is_visible(self.BACK_HOME_BUTTON)
        )
