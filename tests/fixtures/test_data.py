"""
Test Data Management
測試資料管理

QA Mindset: Centralize all test data in one place.
Benefits:
- Single source of truth for test data
- Easy to update when credentials change
- Reusable across all tests
- Clear documentation of test accounts

QA思維：將所有測試資料集中在一個地方。
好處：
- 測試資料的單一真實來源
- 憑證變更時易於更新
- 在所有測試中可重用
- 清晰的測試帳號文件
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class UserCredentials:
    """User credentials data class / 使用者憑證資料類別"""
    username: str
    password: str
    description: str = ""


@dataclass
class CheckoutInfo:
    """Checkout information data class / 結帳資訊資料類別"""
    first_name: str
    last_name: str
    postal_code: str


# User Credentials / 使用者憑證
# QA Mindset: Define all test users in one place.
# Makes it easy to see what accounts are available.
# QA思維：在一個地方定義所有測試使用者。
# 使查看可用帳號變得容易。

STANDARD_USER = UserCredentials(
    username="standard_user",
    password="secret_sauce",
    description="Standard user for positive test scenarios"
)

LOCKED_USER = UserCredentials(
    username="locked_out_user",
    password="secret_sauce",
    description="Locked account for negative testing"
)

PROBLEM_USER = UserCredentials(
    username="problem_user",
    password="secret_sauce",
    description="User with display issues"
)

PERFORMANCE_GLITCH_USER = UserCredentials(
    username="performance_glitch_user",
    password="secret_sauce",
    description="User with slow response times"
)

INVALID_USER = UserCredentials(
    username="invalid_user",
    password="wrong_password",
    description="Invalid credentials for negative testing"
)


# Checkout Information / 結帳資訊
# QA Mindset: Multiple data sets for different test scenarios.
# Prevents data conflicts when running tests multiple times.
# QA思維：不同測試場景的多個資料集。
# 多次執行測試時防止資料衝突。

CHECKOUT_DATA_SET_1 = CheckoutInfo(
    first_name="John",
    last_name="Doe",
    postal_code="12345"
)

CHECKOUT_DATA_SET_2 = CheckoutInfo(
    first_name="Jane",
    last_name="Smith",
    postal_code="54321"
)

CHECKOUT_DATA_SET_3 = CheckoutInfo(
    first_name="Test",
    last_name="User",
    postal_code="99999"
)

CHECKOUT_DATA_SPECIAL_CHARS = CheckoutInfo(
    first_name="John-O'Brien",
    last_name="Doe-Smith",
    postal_code="12345-6789"
)


# Expected Error Messages / 預期錯誤訊息
# QA Mindset: Centralize expected error messages.
# Makes it easy to update when error messages change.
# QA思維：集中預期錯誤訊息。
# 錯誤訊息變更時易於更新。

ERROR_MESSAGES = {
    "invalid_credentials": "Epic sadface: Username and password do not match any user in this service",
    "locked_account": "Epic sadface: Sorry, this user has been locked out",
    "username_required": "Epic sadface: Username is required",
    "password_required": "Epic sadface: Password is required",
    "first_name_required": "Error: First Name is required",
    "last_name_required": "Error: Last Name is required",
    "postal_code_required": "Error: Postal Code is required"
}


# Expected Page Content / 預期頁面內容
# QA Mindset: Define expected text for assertions.
# Makes tests more maintainable.
# QA思維：定義用於斷言的預期文字。
# 使測試更具可維護性。

EXPECTED_TEXT = {
    "order_complete_header": "Thank you for your order!",
    "order_complete_message": "Your order has been dispatched",
    "add_to_cart": "Add to cart",
    "remove": "Remove"
}
