"""
Cart Page Object Model
購物車頁面物件模型

QA Mindset: Encapsulates shopping cart operations.
This page handles:
- Viewing cart items
- Removing items
- Navigating to checkout
- Continuing shopping

QA思維：封裝購物車操作。
此頁面處理：
- 查看購物車商品
- 移除商品
- 導航到結帳
- 繼續購物
"""

from playwright.sync_api import Page
from tests.pages.base_page import BasePage


class CartPage(BasePage):
    """Cart Page Object / 購物車頁面物件"""
    
    # Page Selectors / 頁面選擇器
    CART_LIST = ".cart_list"
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    REMOVE_BUTTON = "button.cart_button"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    CART_BADGE = ".shopping_cart_badge"
    
    def __init__(self, page: Page):
        """Initialize Cart Page / 初始化購物車頁面"""
        super().__init__(page)
    
    def get_item_count(self) -> int:
        """
        Get number of items in cart / 獲取購物車中的商品數量
        
        QA Mindset: Count items for verification.
        Useful for assertions after add/remove operations.
        
        QA思維：計算商品數量用於驗證。
        對添加/移除操作後的斷言有用。
        """
        return self.page.locator(self.CART_ITEM).count()
    
    def get_item_name(self, index: int = 0) -> str:
        """
        Get item name by index / 按索引獲取商品名稱
        
        QA Mindset: Extract item name for verification.
        Verifies correct items in cart.
        
        QA思維：提取商品名稱用於驗證。
        驗證購物車中的正確商品。
        """
        return self.page.locator(self.ITEM_NAME).nth(index).inner_text()
    
    def get_item_price(self, index: int = 0) -> str:
        """
        Get item price by index / 按索引獲取商品價格
        
        QA Mindset: Extract price for calculation verification.
        Verifies pricing accuracy.
        
        QA思維：提取價格用於計算驗證。
        驗證定價準確性。
        """
        return self.page.locator(self.ITEM_PRICE).nth(index).inner_text()
    
    def remove_item(self, index: int = 0) -> None:
        """
        Remove item from cart by index / 按索引從購物車移除商品
        
        QA Mindset: Encapsulate remove action.
        Waits for UI update after removal.
        
        QA思維：封裝移除操作。
        移除後等待UI更新。
        """
        self.page.locator(self.REMOVE_BUTTON).nth(index).click()
        # Wait for item to be removed / 等待商品被移除
        self.page.wait_for_timeout(500)
    
    def click_continue_shopping(self) -> None:
        """
        Click continue shopping button / 點擊繼續購物按鈕
        
        QA Mindset: Navigation action.
        Returns to products page.
        
        QA思維：導航操作。
        返回商品頁面。
        """
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        self.wait_for_url("**/inventory.html")
    
    def click_checkout(self) -> None:
        """
        Click checkout button / 點擊結帳按鈕
        
        QA Mindset: Navigation to checkout flow.
        Critical action - must work correctly.
        
        QA思維：導航到結帳流程。
        關鍵操作 - 必須正確運作。
        """
        self.click(self.CHECKOUT_BUTTON)
        self.wait_for_url("**/checkout-step-one.html")
    
    def verify_cart_items_displayed(self) -> bool:
        """
        Verify cart items are displayed / 驗證購物車商品已顯示
        
        QA Mindset: Page load verification.
        Ensures cart loaded correctly.
        
        QA思維：頁面載入驗證。
        確保購物車正確載入。
        """
        return self.is_visible(self.CART_LIST)
    
    def is_cart_empty(self) -> bool:
        """
        Check if cart is empty / 檢查購物車是否為空
        
        QA Mindset: State verification.
        Useful for edge case testing.
        
        QA思維：狀態驗證。
        對邊界情況測試有用。
        """
        return self.get_item_count() == 0
    
    def get_cart_badge_count(self) -> int:
        """
        Get cart badge count from header / 從標題獲取購物車徽章數量
        
        QA Mindset: Verify badge updates after cart changes.
        Badge should reflect current cart count.
        
        QA思維：驗證購物車變更後徽章更新。
        徽章應反映當前購物車數量。
        """
        if self.is_visible(self.CART_BADGE):
            count_text = self.get_text(self.CART_BADGE)
            return int(count_text) if count_text.isdigit() else 0
        return 0
