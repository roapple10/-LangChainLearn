# LangChainLearnBook CH1 專案簡介

歡迎閱讀本專案！本章整理自 [書籍作者的 GitHub](https://github.com/iangithub/LangChainLearnBook)，主要說明如何安裝與使用 Poetry 來管理 Python 專案依賴。

---

## Poetry 介紹

Poetry 是一個現代化的 Python 專案和依賴管理工具，更詳細介紹與官方安裝指引請參考：[Poetry 官方文件](https://python-poetry.org/docs/#installing-with-the-official-installer)

---

## 安裝 Poetry

### 官方安裝指令

#### Windows (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

詳細圖文教學：[Windows 安裝Poetry 教學](https://realnewbie.com/coding/python/windows-install-poetry/)

#### Mac (Terminal)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 其他安裝方式

#### 透過 Homebrew 安裝（僅 Mac）

```bash
brew install poetry
```

#### 透過 pipx 安裝

**Windows (PowerShell):**
```powershell
# 安裝 pipx
pip install pipx

# 使用 pipx 安裝 poetry
pipx install poetry
```

**Mac (Terminal):**
```bash
# 安裝 pipx
pip3 install pipx

# 使用 pipx 安裝 poetry
pipx install poetry
```

### 驗證安裝

安裝完成後，請執行以下命令確認安裝成功：

**Windows (PowerShell) / Mac (Terminal):**
```bash
poetry --version
```

如顯示poetry : 無法辨識 'poetry' 詞彙是否為 Cmdlet、函數、指令檔或可執行程式的名稱。請檢查名稱拼字是否正確，如果包含  路徑的話，請確認路徑是否正確，然後再試一次。 
請執行以下指令 

```bash
$base = python -m site --user-base
$poetryPath = Join-Path $base "Scripts"
if (Test-Path (Join-Path $poetryPath "poetry.exe")) {
    $env:Path += ";$poetryPath"
    [Environment]::SetEnvironmentVariable("Path", $env:Path, "User")
    Write-Host "`n✅ Poetry path added:`n$poetryPath`n"
    poetry --version
} else {
    Write-Host "`n⚠️ 未找到 poetry.exe，請確認是否已安裝 Poetry。"
}
```


如安裝過程遇到問題，請參考以上文件或官方 FAQ。

---

## 使用 Poetry 管理專案

### 安裝專案依賴

在專案目錄下執行以下命令來安裝所有依賴：

**Windows (PowerShell) / Mac (Terminal):**
```bash
poetry install
```

---

### 啟動虛擬環境（Poetry 2.0+）

**重要提示：** 從 Poetry 2.0.0 開始，`poetry shell` 命令不再預設可用。請使用以下新方法：

#### 方法 1：使用 `env activate` 命令（官方推薦）

**步驟 1：** 執行以下命令查看啟動環境的指令：

**Windows (PowerShell) / Mac (Terminal):**
```bash
poetry env activate
```

該命令會顯示啟動虛擬環境所需的完整路徑。

**步驟 2：** 複製並執行上面顯示的啟動命令來真正啟動虛擬環境：

**Windows (PowerShell):**
```powershell
# 範例路徑（請使用步驟 1 顯示的實際路徑）
C:\Users\YourUsername\Documents\Lanchain\LangChainLearnBook\CH1\ch1\.venv\Scripts\Activate.ps1
```

**Mac (Terminal):**
```bash
# 範例路徑（請使用步驟 1 顯示的實際路徑）
source /Users/ray-mac/Documents/Lanchain/LangChainLearnBook/CH1/ch1/.venv/bin/activate
```

**確認是否啟動成功：** 如果成功啟動，您的終端機提示符會變成：

**Windows (PowerShell):**
```powershell
(.venv) PS C:\Users\YourUsername\Documents\Lanchain\LangChainLearnBook\CH1\ch1>
```

**Mac (Terminal):**
```bash
(.venv) ray-mac@GuandeMacBook-Air ch1 %
```

注意開頭會多出 `(.venv)` 前綴，表示您已進入虛擬環境。

---

#### 方法 2：直接執行命令（推薦用於日常開發）

不需要啟動虛擬環境，直接使用 `poetry run` 執行 Python 腳本：

**Windows (PowerShell):**
```powershell
poetry run python ch1/01_dotenv.py
```

**Mac (Terminal):**
```bash
poetry run python ch1/01_dotenv.py
```

---

#### 方法 3：安裝 shell 插件（如需要傳統的 shell 命令）

如果您偏好使用 `poetry shell` 命令，可以安裝插件：

**Windows (PowerShell) / Mac (Terminal):**
```bash
poetry self add poetry-plugin-shell
```

安裝後即可使用：

**Windows (PowerShell) / Mac (Terminal):**
```bash
poetry shell
```

---

### 退出虛擬環境

如果使用了方法 1 或方法 3 啟動虛擬環境，可以執行：

**Windows (PowerShell) / Mac (Terminal):**
```bash
deactivate
```

---

## 常用 Poetry 命令速查表

| 功能 | Windows (PowerShell) | Mac (Terminal) |
|------|---------------------|----------------|
| 安裝依賴 | `poetry install` | `poetry install` |
| 新增套件 | `poetry add package-name` | `poetry add package-name` |
| 移除套件 | `poetry remove package-name` | `poetry remove package-name` |
| 執行腳本 | `poetry run python script.py` | `poetry run python script.py` |
| 查看環境資訊 | `poetry env info` | `poetry env info` |
| 列出已安裝套件 | `poetry show` | `poetry show` |
| 更新套件 | `poetry update` | `poetry update` |
| 查看版本 | `poetry --version` | `poetry --version` |

---

## 參考資源

- [Poetry 官方文件 - 管理環境](https://python-poetry.org/docs/managing-environments/#activating-the-environment)
- [Poetry 2.0 更新說明](https://python-poetry.org/docs/)
- [Poetry 基本用法](https://python-poetry.org/docs/basic-usage/)

