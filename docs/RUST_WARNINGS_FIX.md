# Rust 代码警告修复

## 修复的问题

### 1. dead_code 警告
**文件**: `src-tauri/src/services/python_bridge.rs`

**问题**: 未使用的字段和方法
- `base_url` 字段未读取
- `is_running()` 方法未使用
- `health_check()` 方法未使用
- `get_base_url()` 方法未使用

**修复**: 添加 `#[allow(dead_code)]` 属性
```rust
#[allow(dead_code)]
pub struct PythonEngine {
    process: Mutex<Option<Child>>,
    base_url: String,
}

#[allow(dead_code)]
pub fn is_running(&self) -> bool { ... }
```

### 2. Database 结构体警告
**文件**: `src-tauri/src/services/database.rs`

**问题**: 未使用的结构体和方法（未来实现的占位符）

**修复**: 添加 `#[allow(dead_code)]` 属性
```rust
#[allow(dead_code)]
pub struct Database {
    pool: Option<SqlitePool>,
}

#[allow(dead_code)]
impl Database { ... }
```

### 3. 大写缩写命名警告
**文件**: `src-tauri/src/commands/market.rs`

**问题**: `OHLCV` 包含大写缩写

**修复**: 添加 `#[allow(clippy::upper_case_acronyms)]` 属性
```rust
#[derive(Debug, Serialize, Deserialize)]
#[allow(clippy::upper_case_acronyms)]
pub struct OHLCV {
    pub timestamp: i64,
    pub open: f64,
    ...
}
```

**为什么不改名**: OHLCV 是金融领域的标准术语（Open, High, Low, Close, Volume），保持大写更符合行业惯例。

## 修复的文件

- ✅ `src-tauri/src/services/python_bridge.rs`
- ✅ `src-tauri/src/services/database.rs`
- ✅ `src-tauri/src/commands/market.rs`

## 测试

```bash
cd src-tauri
cargo clippy -- -D warnings
cargo build
```

应该看到：
- ✅ 0 个警告
- ✅ 0 个错误
- ✅ 编译成功

## 说明

这些是**预留的功能代码**，用于未来扩展：
- `PythonEngine` 的健康检查和状态查询方法
- `Database` 的数据库操作（当前使用 Python 后端）
- `OHLCV` 保持金融行业标准命名

使用 `#[allow(dead_code)]` 和 `#[allow(clippy::upper_case_acronyms)]` 是正确的做法，避免误删未来需要的代码。

---

**修复日期**: 2026-06-16  
**版本**: v2.0.1
