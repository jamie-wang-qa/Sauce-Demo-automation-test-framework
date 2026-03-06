"""
Login Page Object Model
登入頁面物件模型

QA Mindset: Encapsulates all login page interactions.
Benefits:
- Single source of truth for selectors
- Reusable login methods
- Easy to update when UI changes
- Tests read like user stories: login_page.login(username, password)

QA思維：封裝所有登入頁面互動。
好處：
- 選擇器的單一真實來源
- 可重用的登入方法
- UI變更時易於更新
- 測試讀起來像使用者故事：login_page.login(username, password)
"""

from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage
from config.settings import BASE_URL


class LoginPage(BasePage):
    """Login Page Object / 登入頁面物件"""
    
    # Page Selectors / 頁面選擇器
    # QA Mindset: Centralize selectors at class level.
    # If selector changes, update in one place only.
    # QA思維：在類別層級集中選擇器。
    # 如果選擇器變更，只需在一個地方更新。
    
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    
    def __init__(self, page: Page):
        """
        Initialize Login Page / 初始化登入頁面
        
        QA Mindset: Call parent constructor to set up base functionality.
        Then navigate to login page.
        
        QA思維：調用父類別構造函數以設置基礎功能。
        然後導航到登入頁面。
        """
        super().__init__(page)
        self.navigate(BASE_URL)
    
    def enter_username(self, username: str) -> None:
        """
        Enter username / 輸入使用者名稱
        
        QA Mindset: Encapsulate interaction with username field.
        If field changes, only update this method.
        
        QA思維：封裝與使用者名稱欄位的互動。
        如果欄位變更，只需更新此方法。
        """
        self.fill(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str) -> None:
        """
        Enter password / 輸入密碼
        
        QA Mindset: Separate method for password entry.
        Makes test code more readable.
        
        QA思維：密碼輸入的獨立方法。
        使測試代碼更具可讀性。
        """
        self.fill(self.PASSWORD_INPUT, password)
    
    def click_login(self) -> None:
        """
        Click login button / 點擊登入按鈕
        
        QA Mindset: Separate action method.
        Allows tests to verify button state before clicking.
        
        QA思維：獨立的操作方法。
        允許測試在點擊前驗證按鈕狀態。
        """
        self.click(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str) -> None:
        """
        Complete login flow / 完成登入流程
        
        QA Mindset: High-level method that combines all login steps.
        Most tests will use this method.
        For detailed testing, use individual methods.
        
        QA思維：結合所有登入步驟的高層級方法。
        大多數測試將使用此方法。
        對於詳細測試，使用個別方法。
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def get_error_message(self) -> str:
        """
        Get error message text / 獲取錯誤訊息文字
        
        QA Mindset: Extract error message for assertions.
        Returns empty string if no error (safer than None).
        
        QA思維：提取錯誤訊息用於斷言。
        如果沒有錯誤則返回空字串（比 None 更安全）。
        """
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def is_error_displayed(self) -> bool:
        """
        Check if error message is displayed / 檢查是否顯示錯誤訊息
        
        QA Mindset: Boolean check for error state.
        Useful for negative test assertions.
        
        QA思維：錯誤狀態的布林檢查。
        對負向測試斷言有用。
        """
        return self.is_visible(self.ERROR_MESSAGE)
    
    def verify_login_page_elements(self) -> bool:
        """
        Verify all login page elements are visible / 驗證所有登入頁面元素可見
        
        QA Mindset: Page load verification.
        Ensures page loaded correctly before interaction.
        
        QA思維：頁面載入驗證。
        確保互動前頁面正確載入。
        """
        return (
            self.is_visible(self.USERNAME_INPUT) and
            self.is_visible(self.PASSWORD_INPUT) and
            self.is_visible(self.LOGIN_BUTTON)
        )
    
    def wait_for_products_page(self) -> None:
        """
        Wait for navigation to products page / 等待導航到商品頁面
        
        QA Mindset: Explicit wait for page transition.
        Prevents race conditions in tests.
        
        QA思維：明確等待頁面轉換。
        防止測試中的競爭條件。
        """
        self.wait_for_url("**/inventory.html")
