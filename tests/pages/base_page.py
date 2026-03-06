"""
Base Page Class
基礎頁面類別

QA Mindset: Base class contains common functionality shared by all pages.
This follows DRY (Don't Repeat Yourself) principle:
- Common methods (wait, click, fill) in one place
- Consistent error handling
- Reusable utilities

QA思維：基礎類別包含所有頁面共享的通用功能。
這遵循 DRY（不要重複自己）原則：
- 通用方法（等待、點擊、填寫）在一個地方
- 一致的錯誤處理
- 可重用的工具
"""

from playwright.sync_api import Page, expect
from typing import Optional


class BasePage:
    """Base class for all page objects / 所有頁面物件的基礎類別"""
    
    def __init__(self, page: Page):
        """
        Initialize base page / 初始化基礎頁面
        
        QA Mindset: All page objects need a Page instance.
        This is passed from the test via fixture.
        
        QA思維：所有頁面物件都需要一個 Page 實例。
        這通過 fixture 從測試傳遞。
        """
        self.page = page
    
    def navigate(self, url: str) -> None:
        """
        Navigate to a URL / 導航到URL
        
        QA Mindset: Centralized navigation with error handling.
        If navigation fails, we get clear error messages.
        
        QA思維：集中化導航與錯誤處理。
        如果導航失敗，我們會得到清晰的錯誤訊息。
        """
        self.page.goto(url, wait_until="networkidle")
    
    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Click an element / 點擊元素
        
        QA Mindset: Wrapper around page.click() with better error messages.
        If element not found, we get helpful error info.
        
        QA思維：page.click() 的包裝器，提供更好的錯誤訊息。
        如果找不到元素，我們會得到有用的錯誤資訊。
        """
        self.page.click(selector, timeout=timeout)
    
    def fill(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """
        Fill an input field / 填寫輸入欄位
        
        QA Mindset: Clear input before filling (more reliable).
        Some fields might have default values that need clearing.
        
        QA思維：填寫前清除輸入（更可靠）。
        某些欄位可能有需要清除的預設值。
        """
        self.page.fill(selector, value, timeout=timeout)
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get text content of an element / 獲取元素的文字內容
        
        QA Mindset: Extract text for assertions.
        Returns empty string if element not found (safer).
        
        QA思維：提取文字用於斷言。
        如果找不到元素則返回空字串（更安全）。
        """
        return self.page.locator(selector).inner_text(timeout=timeout)
    
    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Check if element is visible / 檢查元素是否可見
        
        QA Mindset: Visibility check before interaction.
        Prevents errors from interacting with hidden elements.
        
        QA思維：互動前檢查可見性。
        防止與隱藏元素互動時出錯。
        """
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout or 5000)
            return True
        except:
            return False
    
    def wait_for_url(self, url_pattern: str, timeout: Optional[int] = None) -> None:
        """
        Wait for URL to match pattern / 等待URL匹配模式
        
        QA Mindset: Ensure navigation completed before proceeding.
        Prevents race conditions in tests.
        
        QA思維：確保導航完成後再繼續。
        防止測試中的競爭條件。
        """
        self.page.wait_for_url(url_pattern, timeout=timeout)
    
    def get_title(self) -> str:
        """Get page title / 獲取頁面標題"""
        return self.page.title()
    
    def take_screenshot(self, filename: str) -> None:
        """
        Take screenshot / 截圖
        
        QA Mindset: Visual debugging tool.
        Screenshots help understand test failures.
        
        QA思維：視覺除錯工具。
        截圖幫助理解測試失敗。
        """
        self.page.screenshot(path=filename, full_page=True)
