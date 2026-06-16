# CI/CD 错误修复 - libwebkit2gtk 包名更新

## 问题描述

GitHub Actions 在 Ubuntu 24.04 上运行时报错：
```
E: Unable to locate package libwebkit2gtk-4.0-dev
Error: Process completed with exit code 100
```

## 原因

Ubuntu 24.04 LTS 将 WebKit GTK 包名从 `libwebkit2gtk-4.0-dev` 更新为 `libwebkit2gtk-4.1-dev`。

## 解决方案

使用回退机制，先尝试新版本包名，如果失败则使用旧版本：

```yaml
- name: Install system dependencies
  run: |
    sudo apt-get update
    # Ubuntu 24.04+ uses libwebkit2gtk-4.1-dev instead of 4.0
    sudo apt-get install -y libgtk-3-dev libwebkit2gtk-4.1-dev ... || \
    sudo apt-get install -y libgtk-3-dev libwebkit2gtk-4.0-dev ...
```

## 修复的文件

- `.github/workflows/ci-cd.yml`
  - `test-rust` 任务
  - `build-release` 任务

## 兼容性

✅ Ubuntu 24.04 (使用 libwebkit2gtk-4.1-dev)  
✅ Ubuntu 22.04 (使用 libwebkit2gtk-4.0-dev)  
✅ Ubuntu 20.04 (使用 libwebkit2gtk-4.0-dev)

## 测试

提交后，GitHub Actions 应该能在 ubuntu-latest (24.04) 上成功运行。

---

**修复日期**: 2026-06-16  
**影响版本**: v2.0.1+
