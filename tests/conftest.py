"""
Pytest Configuration and Fixtures
Pytest 設定與 Fixtures

QA Mindset: Fixtures are reusable setup/teardown code.
They help us:
- Avoid code duplication
- Ensure consistent test environment
- Handle browser lifecycle
- Manage test data
- Clean up after tests

QA思維：Fixtures 是可重用的設置/清理代碼。
它們幫助我們：
- 避免代碼重複
- 確保一致的測試環境
- 處理瀏覽器生命週期
- 管理測試資料
- 測試後清理
"""

import pytest
from playwright.sync_api import Page, Browser, BrowserContext, sync_playwright
from config.settings import BASE_URL, HEADLESS, BROWSER, SLOW_MO, DEFAULT_TIMEOUT


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """
    Browser Launch Arguments
    瀏覽器啟動參數
    
    QA Mindset: Configure browser launch settings once for all tests.
    This ensures consistent browser behavior across all tests.
    
    QA思維：為所有測試配置瀏覽器啟動設定一次。
    這確保所有測試中瀏覽器行為一致。
    """
    return {
        "headless": HEADLESS,
        "slow_mo": SLOW_MO,
    }


@pytest.fixture(scope="session")
def browser_context_args():
    """
    Browser Context Arguments
    瀏覽器上下文參數
    
    QA Mindset: Set default viewport, timeouts, and other context settings.
    This ensures all pages start with the same configuration.
    
    QA思維：設定預設視窗大小、超時和其他上下文設定。
    這確保所有頁面以相同配置開始。
    """
    return {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,  # Useful for test environments / 對測試環境有用
    }


@pytest.fixture(scope="session")
def browser(browser_type_launch_args):
    """
    Browser Fixture - Creates browser instance for test session
    瀏覽器 Fixture - 為測試會話創建瀏覽器實例
    
    QA Mindset: Session scope means browser is created once and reused.
    This is more efficient than creating a new browser for each test.
    
    QA思維：Session scope 意味著瀏覽器創建一次並重用。
    這比為每個測試創建新瀏覽器更高效。
    """
    playwright = sync_playwright().start()
    
    # Launch browser based on BROWSER setting / 根據BROWSER設定啟動瀏覽器
    if BROWSER == "chromium":
        browser = playwright.chromium.launch(**browser_type_launch_args)
    elif BROWSER == "firefox":
        browser = playwright.firefox.launch(**browser_type_launch_args)
    elif BROWSER == "webkit":
        browser = playwright.webkit.launch(**browser_type_launch_args)
    else:
        browser = playwright.chromium.launch(**browser_type_launch_args)
    
    yield browser
    
    # Cleanup / 清理
    browser.close()
    playwright.stop()


@pytest.fixture(scope="function")
def page(browser: Browser, browser_context_args) -> Page:
    """
    Page Fixture - Creates a new page for each test
    頁面 Fixture - 為每個測試創建新頁面
    
    QA Mindset: 
    - Function scope: Each test gets a fresh page (test isolation)
    - Automatic cleanup: Page closes after test completes
    - Consistent setup: All tests start with same page configuration
    
    QA思維：
    - Function scope：每個測試獲得新頁面（測試隔離）
    - 自動清理：測試完成後頁面關閉
    - 一致設置：所有測試以相同頁面配置開始
    """
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    
    # Set default timeout / 設定預設超時
    page.set_default_timeout(DEFAULT_TIMEOUT)
    
    yield page
    
    # Cleanup / 清理
    page.close()
    context.close()


@pytest.fixture(scope="function")
def logged_in_page(page: Page):
    """
    Logged In Page Fixture - Pre-login for tests that need authentication
    已登入頁面 Fixture - 為需要認證的測試預先登入
    
    QA Mindset:
    - Reusable login: Avoid repeating login code in every test
    - Faster tests: Login once, use in multiple tests
    - Consistent state: All tests start from same logged-in state
    - Error handling: Verify login succeeded before proceeding
    
    QA思維：
    - 可重用登入：避免在每個測試中重複登入代碼
    - 更快測試：登入一次，在多個測試中使用
    - 一致狀態：所有測試從相同登入狀態開始
    - 錯誤處理：在繼續之前驗證登入成功
    """
    from config.settings import BASE_URL, VALID_USERNAME, VALID_PASSWORD
    
    # Navigate to login page / 導航到登入頁面
    page.goto(BASE_URL, wait_until="networkidle")
    
    # Verify login page loaded / 驗證登入頁面已載入
    page.wait_for_selector("#user-name", state="visible", timeout=10000)
    page.wait_for_selector("#password", state="visible", timeout=10000)
    page.wait_for_selector("#login-button", state="visible", timeout=10000)
    
    # Perform login / 執行登入
    page.fill("#user-name", VALID_USERNAME)
    page.fill("#password", VALID_PASSWORD)
    page.click("#login-button")
    
    # Wait for navigation to products page / 等待導航到商品頁面
    # Use explicit wait with timeout / 使用明確等待與超時
    try:
        # Wait for URL to contain inventory / 等待 URL 包含 inventory
        # Use a simple pattern that matches the actual URL format / 使用匹配實際 URL 格式的簡單模式
        # Wait with explicit timeout and check result / 使用明確超時等待並檢查結果
        try:
            page.wait_for_url("**/inventory.html", timeout=30000)
        except Exception as url_wait_error:
            # Check current URL when wait fails / 等待失敗時檢查當前 URL
            current_url_on_failure = page.url
            raise Exception(
                f"wait_for_url timed out or failed. "
                f"Current URL: {current_url_on_failure}, "
                f"Error: {str(url_wait_error)}"
            ) from url_wait_error
        
        # Immediately check URL after wait / 等待後立即檢查 URL
        current_url_after_wait = page.url
        if "inventory.html" not in current_url_after_wait:
            raise Exception(
                f"wait_for_url completed but URL is incorrect. "
                f"Expected: **/inventory.html, Got: {current_url_after_wait}"
            )
        
        # Wait for page to load completely / 等待頁面完全載入
        page.wait_for_load_state("networkidle", timeout=10000)
        
        # Verify URL changed / 驗證 URL 已變化
        current_url = page.url
        if "inventory.html" not in current_url:
            raise Exception(f"URL did not change to products page. Current URL: {current_url}")
            
    except Exception as e:
        # Check current URL / 檢查當前 URL
        current_url = page.url
        
        # Wait a bit for error message to appear / 等待錯誤訊息出現
        page.wait_for_timeout(2000)
        
        # Check if login failed / 檢查登入是否失敗
        error_selector = "[data-test='error']"
        error_text = ""
        try:
            if page.locator(error_selector).is_visible(timeout=2000):
                error_text = page.locator(error_selector).inner_text()
        except:
            pass
        
        # Build comprehensive error message / 建立全面的錯誤訊息
        error_msg = f"Login fixture failed!\n"
        error_msg += f"Username: {VALID_USERNAME}\n"
        error_msg += f"Password: {'*' * len(VALID_PASSWORD)}\n"
        error_msg += f"Expected URL: **/inventory.html\n"
        error_msg += f"Actual URL: {current_url}\n"
        error_msg += f"Page Title: {page.title()}\n"
        if error_text:
            error_msg += f"Login error message: {error_text}\n"
        error_msg += f"Original exception: {str(e)}\n"
        error_msg += f"\nTroubleshooting:\n"
        error_msg += f"- Check if credentials are correct\n"
        error_msg += f"- Check if website is accessible\n"
        error_msg += f"- Check network connectivity"
        
        raise Exception(error_msg) from e
    
    # Final verification / 最終驗證
    current_url = page.url
    if "inventory.html" not in current_url:
        # Get page title for debugging / 獲取頁面標題用於除錯
        page_title = page.title()
        raise Exception(
            f"Login fixture final verification failed!\n"
            f"Expected URL: **/inventory.html\n"
            f"Actual URL: {current_url}\n"
            f"Page Title: {page_title}\n"
            f"Username used: {VALID_USERNAME}"
        )
    
    # Verify products page elements are visible / 驗證商品頁面元素可見
    page.wait_for_selector(".inventory_list", state="visible", timeout=10000)
    
    # Verify menu button exists (needed for logout test) / 驗證選單按鈕存在（登出測試需要）
    page.wait_for_selector("#react-burger-menu-btn", state="visible", timeout=10000)
    
    yield page
    
    # Note: Page cleanup handled by page fixture / 注意：頁面清理由 page fixture 處理


@pytest.fixture(scope="function", autouse=True)
def setup_test_environment(request, page: Page):
    """
    Setup Test Environment - Runs before each test
    設置測試環境 - 每個測試前運行
    
    QA Mindset:
    - autouse=True: Automatically runs for every test
    - Pre-test setup: Clear cookies, set base URL, etc.
    - Post-test cleanup: Screenshot on failure, clear state
    - Skip cookie clearing for logged_in_page fixture: Don't clear cookies if test uses logged_in_page
    
    QA思維：
    - autouse=True：自動為每個測試運行
    - 測試前設置：清除 cookies、設定基礎 URL 等
    - 測試後清理：失敗時截圖、清除狀態
    - 為 logged_in_page fixture 跳過清除 cookies：如果測試使用 logged_in_page，不清除 cookies
    """
    # Pre-test setup / 測試前設置
    # Only clear cookies if test doesn't use logged_in_page fixture
    # 只有在測試不使用 logged_in_page fixture 時才清除 cookies
    # This prevents clearing cookies after login in logged_in_page fixture
    # 這防止在 logged_in_page fixture 登入後清除 cookies
    if "logged_in_page" not in request.fixturenames:
        page.context.clear_cookies()
    
    yield
    
    # Post-test cleanup / 測試後清理
    # Screenshot on failure is handled by pytest-html plugin
    # 失敗時的截圖由 pytest-html 插件處理


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots and logs on test failure
    在測試失敗時捕獲螢幕截圖和日誌的 Hook
    
    QA Mindset:
    - Visual debugging: Screenshots help debug failures
    - Automatic capture: No need to remember to add screenshots
    - Evidence: Screenshots serve as evidence of failures
    - Logging: Detailed logs help understand failure context
    
    QA思維：
    - 視覺除錯：截圖幫助除錯失敗
    - 自動捕獲：無需記住添加截圖
    - 證據：截圖作為失敗的證據
    - 日誌記錄：詳細日誌幫助理解失敗上下文
    """
    import os
    from datetime import datetime
    
    outcome = yield
    rep = outcome.get_result()
    
    # Take screenshot on failure / 失敗時截圖
    if rep.when == "call" and rep.failed:
        # Try to get page object from fixtures / 嘗試從 fixtures 獲取 page 物件
        page = None
        
        # Check for page fixture / 檢查 page fixture
        if "page" in item.fixturenames:
            page = item.funcargs.get("page")
        # Check for logged_in_page fixture / 檢查 logged_in_page fixture
        elif "logged_in_page" in item.fixturenames:
            page = item.funcargs.get("logged_in_page")
        
        if page:
            # Create screenshots directory if not exists / 如果不存在則創建截圖目錄
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            # Generate screenshot filename with timestamp / 生成帶時間戳的截圖檔名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_filename)
            
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                # Add screenshot path to report / 將截圖路徑添加到報告
                if hasattr(rep, "extra"):
                    rep.extra.append(("image", screenshot_path))
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")
        
        # Log failure details / 記錄失敗詳情
        log_dir = "reports/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_filename = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_path = os.path.join(log_dir, log_filename)
        
        try:
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(f"Test: {item.name}\n")
                f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Status: FAILED\n")
                f.write(f"\n--- Error Message ---\n")
                f.write(f"{str(rep.longrepr)}\n")
                f.write(f"\n--- Test Location ---\n")
                f.write(f"File: {item.fspath}\n")
                f.write(f"Line: {item.location[1]}\n")
                if page:
                    f.write(f"\n--- Page Info ---\n")
                    f.write(f"URL: {page.url}\n")
                    f.write(f"Title: {page.title()}\n")
        except Exception as e:
            print(f"Failed to write log file: {e}")
