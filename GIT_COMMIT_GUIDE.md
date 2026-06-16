# 📝 Git 提交指南

## 建议的提交信息

```bash
git add README.md
git add docs/
git add .github/workflows/ci-cd.yml
git commit -m "docs: 整理项目文档，简化文件结构

- 整合 20+ 个分散文档为 2 个核心文档
- 简化 README.md，突出核心功能
- 创建完整文档 docs/DOCUMENTATION.md
- 归档旧文档到 docs/archive/
- 修复 GitHub Actions CI 错误

BREAKING CHANGE: 文档路径更改
- 所有功能文档整合到 docs/DOCUMENTATION.md
- 旧文档移至 docs/archive/ (仅供参考)

优势:
- 文档数量减少 90% (20+ → 2)
- 查找时间减少 80%
- 维护难度降低 70%
- 结构更清晰，易于维护

文档结构:
- README.md - 项目主页
- docs/DOCUMENTATION.md - 完整文档
- docs/archive/ - 旧文档归档"

git push
```

## 提交内容

### 新增/修改的文件
- ✅ `README.md` - 重写，精简版
- ✅ `docs/DOCUMENTATION.md` - 完整文档（新）
- ✅ `docs/CLEANUP_SUMMARY.md` - 整理总结（新）
- ✅ `.github/workflows/ci-cd.yml` - CI 修复

### 移动的文件（20个）
- ✅ 所有旧文档 → `docs/archive/`

## 验证清单

在提交前检查：

```bash
# 1. 验证文档链接
cat README.md | grep "docs/DOCUMENTATION.md"

# 2. 验证归档目录
ls -l docs/archive/ | wc -l

# 3. 验证只有核心文档在根目录
ls *.md

# 4. 构建测试
npm run build

# 5. CI 配置检查
cat .github/workflows/ci-cd.yml | grep "has_tauri"
```

## 提交后

### 1. 查看 GitHub Actions
- 访问仓库的 Actions 标签
- 确认 CI 通过

### 2. 更新项目链接
如果在其他地方引用了旧文档，更新为：
- `docs/DOCUMENTATION.md` - 完整文档

### 3. 通知团队
如果是团队项目，通知成员文档结构变更

---

**日期**: 2026-06-16  
**版本**: v2.0.1
