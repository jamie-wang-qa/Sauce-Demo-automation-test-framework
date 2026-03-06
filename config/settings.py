"""
Configuration Settings
設定檔

QA Mindset: Centralize all configuration in one place.
This makes it easy to:
- Switch between environments (dev, staging, prod)
- Update URLs without searching through code
- Manage timeouts and retry logic
- Control test execution behavior

QA思維：將所有設定集中在一個地方。
這樣可以：
- 輕鬆在環境間切換（開發、測試、生產）
- 更新URL而無需搜尋代碼
- 管理超時和重試邏輯
- 控制測試執行行為
"""

# Base URL / 基礎URL
BASE_URL = "https://www.saucedemo.com/"

# Timeouts (in milliseconds) / 超時設定（毫秒）
DEFAULT_TIMEOUT = 30000  # 30 seconds / 30秒
NAVIGATION_TIMEOUT = 60000  # 60 seconds / 60秒
ELEMENT_TIMEOUT = 10000  # 10 seconds / 10秒

# Browser Configuration / 瀏覽器設定
BROWSER = "chromium"  # Options: chromium, firefox, webkit
HEADLESS = True  # Set to False for debugging / 設為False用於除錯
SLOW_MO = 0  # Slow down operations by X ms (useful for debugging) / 減慢操作X毫秒（用於除錯）

# Screenshot Configuration / 螢幕截圖設定
SCREENSHOT_ON_FAILURE = True
SCREENSHOT_DIR = "reports/screenshots"

# Test Data / 測試資料
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"
LOCKED_USERNAME = "locked_out_user"
INVALID_USERNAME = "invalid_user"
INVALID_PASSWORD = "wrong_password"
