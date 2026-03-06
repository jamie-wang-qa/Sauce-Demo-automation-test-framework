"""
Product Page Object Model
商品頁面物件模型

QA Mindset: Encapsulates product browsing and cart operations.
This page handles:
- Product listing
- Adding items to cart
- Sorting products
- Navigation to cart

QA思維：封裝商品瀏覽和購物車操作。
此頁面處理：
- 商品列表
- 將商品加入購物車
- 商品排序
- 導航到購物車
"""

from playwright.sync_api import Page
from tests.pages.base_page import BasePage


class ProductPage(BasePage):
    """Product Page Object / 商品頁面物件"""
    
    # Page Selectors / 頁面選擇器
    PRODUCT_CONTAINER = ".inventory_list"
    PRODUCT_ITEM = ".inventory_item"
    PRODUCT_NAME = ".inventory_item_name"
    PRODUCT_PRICE = ".inventory_item_price"
    ADD_TO_CART_BUTTON = "button.btn_inventory"
    REMOVE_BUTTON = "button.btn_inventory"
    CART_ICON = "#shopping_cart_container"
    CART_BADGE = ".shopping_cart_badge"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    MENU_BUTTON = "#react-burger-menu-btn"
    
    def __init__(self, page: Page):
        """Initialize Product Page / 初始化商品頁面"""
        super().__init__(page)
    
    def get_product_count(self) -> int:
        """
        Get number of products displayed / 獲取顯示的商品數量
        
        QA Mindset: Count products for assertions.
        Useful for verifying product list loaded correctly.
        
        QA思維：計算商品數量用於斷言。
        對驗證商品列表正確載入有用。
        """
        return self.page.locator(self.PRODUCT_ITEM).count()
    
    def get_product_name(self, index: int = 0) -> str:
        """
        Get product name by index / 按索引獲取商品名稱
        
        QA Mindset: Extract product name for verification.
        Index-based access for predictable test data.
        
        QA思維：提取商品名稱用於驗證。
        基於索引的存取以獲得可預測的測試資料。
        """
        return self.page.locator(self.PRODUCT_NAME).nth(index).inner_text()
    
    def get_product_price(self, index: int = 0) -> str:
        """
        Get product price by index / 按索引獲取商品價格
        
        QA Mindset: Extract price for calculation verification.
        Returns formatted price string.
        
        QA思維：提取價格用於計算驗證。
        返回格式化的價格字串。
        """
        return self.page.locator(self.PRODUCT_PRICE).nth(index).inner_text()
    
    def add_to_cart(self, index: int = 0) -> None:
        """
        Add product to cart by index / 按索引將商品加入購物車
        
        QA Mindset: Encapsulate add to cart action.
        Index allows selecting specific product.
        
        QA思維：封裝加入購物車操作。
        索引允許選擇特定商品。
        """
        add_button = self.page.locator(self.ADD_TO_CART_BUTTON).nth(index)
        add_button.click()
    
    def remove_from_cart(self, index: int = 0) -> None:
        """
        Remove product from cart by index / 按索引從購物車移除商品
        
        QA Mindset: Encapsulate remove action.
        Button text changes from "Add to cart" to "Remove" after adding.
        
        QA思維：封裝移除操作。
        加入後按鈕文字從「加入購物車」變為「移除」。
        """
        remove_button = self.page.locator(self.REMOVE_BUTTON).nth(index)
        remove_button.click()
    
    def get_cart_badge_count(self) -> int:
        """
        Get cart badge count / 獲取購物車徽章數量
        
        QA Mindset: Extract cart count for verification.
        Returns 0 if badge not visible (empty cart).
        
        QA思維：提取購物車數量用於驗證。
        如果徽章不可見則返回0（空購物車）。
        """
        if self.is_visible(self.CART_BADGE):
            count_text = self.get_text(self.CART_BADGE)
            return int(count_text) if count_text.isdigit() else 0
        return 0
    
    def click_cart_icon(self) -> None:
        """
        Click cart icon to navigate to cart / 點擊購物車圖示導航到購物車
        
        QA Mindset: Navigation action.
        Waits for navigation to complete.
        
        QA思維：導航操作。
        等待導航完成。
        """
        self.click(self.CART_ICON)
        self.wait_for_url("**/cart.html")
    
    def select_sort_option(self, option: str) -> None:
        """
        Select sort option / 選擇排序選項
        
        QA Mindset: Encapsulate sorting interaction.
        Options: "az", "za", "lohi", "hilo"
        
        QA思維：封裝排序互動。
        選項："az", "za", "lohi", "hilo"
        """
        self.page.select_option(self.SORT_DROPDOWN, option)
        # Wait for products to reorder / 等待商品重新排序
        self.page.wait_for_timeout(500)  # Small delay for UI update / 小延遲以更新UI
    
    def verify_products_displayed(self) -> bool:
        """
        Verify products are displayed / 驗證商品已顯示
        
        QA Mindset: Page load verification.
        Ensures products loaded before interaction.
        
        QA思維：頁面載入驗證。
        確保互動前商品已載入。
        """
        return self.is_visible(self.PRODUCT_CONTAINER) and self.get_product_count() > 0
    
    def get_button_text(self, index: int = 0) -> str:
        """
        Get button text (Add to cart / Remove) / 獲取按鈕文字（加入購物車/移除）
        
        QA Mindset: Verify button state.
        Button text indicates if item is in cart.
        
        QA思維：驗證按鈕狀態。
        按鈕文字指示商品是否在購物車中。
        """
        return self.page.locator(self.ADD_TO_CART_BUTTON).nth(index).inner_text()
