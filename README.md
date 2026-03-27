# Sauce Demo E2E Test Automation / Sauce Demo E2E 測試自動化

## Project Overview / 專案概述

This project contains end-to-end (E2E) test automation for [Sauce Demo](https://www.saucedemo.com/), a standard e-commerce demo application used for testing purposes.

本專案包含針對 [Sauce Demo](https://www.saucedemo.com/) 的端對端（E2E）測試自動化，這是一個用於測試目的的標準電商演示應用程式。

## Project Structure / 專案結構

```
saurcedemo/
├── README.md                 # Project overview and setup instructions / 專案概述與設定說明
├── docs/                     # Documentation directory / 文件目錄
│   ├── ARCHITECTURE.md       # Project architecture and design / 專案架構與設計
│   ├── TEST_STRATEGY.md      # Testing strategy and approach / 測試策略與方法
│   ├── TEST_PLAN.md          # Detailed test plan and scope / 詳細測試計劃與範圍
│   ├── TEST_CASES.md         # Test case documentation / 測試案例文件
│   ├── TEST_DATA.md          # Test data and user credentials / 測試資料與使用者憑證
│   ├── SETUP.md              # Setup and installation guide / 設置與安裝指南
│   ├── QA_WORKFLOW.md        # QA workflow after test execution / 測試執行後的QA工作流程
│   └── GIT_SETUP.md          # Git setup and GitHub guide / Git設置與GitHub指南
├── tests/                    # Test scripts directory / 測試腳本目錄
│   ├── pages/                # Page Object Model (POM) classes / 頁面物件模型類別
│   ├── fixtures/             # Test fixtures and utilities / 測試固定裝置與工具
│   └── specs/                # Test specifications / 測試規格
├── config/                   # Configuration files / 設定檔
└── reports/                  # Test execution reports / 測試執行報告
```

## Technology Stack / 技術棧

- **Playwright**: Browser automation framework / 瀏覽器自動化框架
- **TypeScript/JavaScript**: Programming language / 程式語言
- **Page Object Model (POM)**: Design pattern for maintainable tests / 可維護測試的設計模式

## Getting Started / 快速開始

### Prerequisites / 前置需求

- Node.js (v18 or higher) / Node.js（v18 或更高版本）
- npm or yarn

### Installation / 安裝

```bash
npm install
```

### Running Tests / 執行測試

```bash
# Run all tests / 執行所有測試
npm test

# Run tests in headed mode / 以有頭模式執行測試
npm run test:headed

# Run specific test suite / 執行特定測試套件
npm run test:login
```

## Test Coverage / 測試覆蓋範圍

- ✅ User authentication flows / 使用者認證流程
- ✅ Product browsing and sorting / 商品瀏覽與排序
- ✅ Shopping cart management / 購物車管理
- ✅ Checkout process / 結帳流程
- ✅ Error handling and validation / 錯誤處理與驗證
- ✅ Cross-browser compatibility / 跨瀏覽器相容性

## Documentation / 文件

所有說明文件都在 `docs/` 資料夾中：

- [Architecture](./docs/ARCHITECTURE.md) - Project architecture and design / 專案架構與設計
- [Test Strategy](./docs/TEST_STRATEGY.md) - Understanding the QA approach / 了解QA方法
- [Test Plan](./docs/TEST_PLAN.md) - Detailed test planning / 詳細測試計劃
- [Test Cases](./docs/TEST_CASES.md) - Individual test case specifications / 個別測試案例規格
- [Test Data](./docs/TEST_DATA.md) - Test credentials and data / 測試憑證與資料
- [Setup Guide](./docs/SETUP.md) - Setup and installation instructions / 設置與安裝說明
- [QA Workflow](./docs/QA_WORKFLOW.md) - QA workflow after test execution / 測試執行後的QA工作流程

## Contributing / 貢獻

When adding new tests, please follow the established patterns and update relevant documentation.

新增測試時，請遵循既定的模式並更新相關文件。
