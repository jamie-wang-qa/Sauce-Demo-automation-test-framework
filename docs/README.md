# Documentation Directory / 文件目錄

## Purpose / 目的

This directory contains all project documentation and guides. All `.md` files (except root `README.md`) are stored here for better organization.

此目錄包含所有專案文件和指南。所有 `.md` 檔案（除了根目錄的 `README.md`）都存放在這裡以便更好地組織。

## File Structure / 檔案結構

### Core Documentation / 核心文件

- **ARCHITECTURE.md** - Project architecture, design patterns, and technical decisions
  - 專案架構、設計模式和技術決策

- **TEST_STRATEGY.md** - Testing strategy, approach, and QA mindset
  - 測試策略、方法和 QA 思維

- **TEST_PLAN.md** - Detailed test plan, scope, and execution schedule
  - 詳細測試計劃、範圍和執行時間表

- **TEST_CASES.md** - Individual test case specifications with steps and expected results
  - 個別測試案例規格，包含步驟和預期結果

- **TEST_DATA.md** - Test data, user credentials, and data management strategy
  - 測試資料、使用者憑證和資料管理策略

### Setup & Guides / 設置與指南

- **SETUP.md** - Environment setup, installation, and getting started guide
  - 環境設置、安裝和快速開始指南

- **QA_WORKFLOW.md** - Complete QA workflow after test execution
  - 測試執行後的完整 QA 工作流程

- **GIT_SETUP.md** - Git repository setup and GitHub push guide
  - Git 儲存庫設置和 GitHub 推送指南

## Adding New Documentation / 添加新文件

When creating new documentation files:

創建新文件時：

1. **Place in this directory** - All `.md` files (except root `README.md`) go here
   - 放在此目錄中 - 所有 `.md` 檔案（除了根目錄的 `README.md`）都放在這裡

2. **Update this README** - Add your new file to the list above
   - 更新此 README - 將新檔案添加到上面的列表中

3. **Update root README.md** - Add link to your new documentation in the Documentation section
   - 更新根目錄的 README.md - 在文件部分添加新文件的連結

4. **Follow naming convention** - Use UPPER_SNAKE_CASE.md for consistency
   - 遵循命名約定 - 使用 UPPER_SNAKE_CASE.md 以保持一致性

## File Organization / 檔案組織

### By Category / 按類別

- **Architecture & Design** - ARCHITECTURE.md
- **Testing Strategy** - TEST_STRATEGY.md, TEST_PLAN.md, TEST_CASES.md, TEST_DATA.md
- **Setup & Guides** - SETUP.md, QA_WORKFLOW.md, GIT_SETUP.md

### By Audience / 按受眾

- **Developers** - ARCHITECTURE.md, SETUP.md
- **QA Engineers** - TEST_STRATEGY.md, TEST_PLAN.md, TEST_CASES.md, TEST_DATA.md, QA_WORKFLOW.md
- **All Team Members** - GIT_SETUP.md

## Best Practices / 最佳實踐

1. **Keep files focused** - Each file should have a clear, single purpose
   - 保持檔案專注 - 每個檔案應該有明確的單一目的

2. **Update regularly** - Keep documentation in sync with code changes
   - 定期更新 - 保持文件與程式碼變更同步

3. **Use clear structure** - Follow existing file structure patterns
   - 使用清晰的結構 - 遵循現有的檔案結構模式

4. **Include examples** - Provide code examples and use cases
   - 包含範例 - 提供程式碼範例和使用案例

5. **Bilingual support** - Maintain both English and Chinese versions where applicable
   - 雙語支援 - 在適用的地方保持英文和中文版本

## Notes / 備註

- All files in this directory are excluded from Git (via `.gitignore`)
  - 此目錄中的所有檔案都從 Git 中排除（通過 `.gitignore`）

- Root `README.md` is kept in the project root for GitHub visibility
  - 根目錄的 `README.md` 保留在專案根目錄以便在 GitHub 上可見

- Future documentation should follow the same structure and patterns
  - 未來的文件應該遵循相同的結構和模式
