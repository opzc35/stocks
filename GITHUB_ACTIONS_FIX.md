# GitHub Actions 配置指南

## 问题修复

### 1. ❌ Test Rust/Tauri 失败

**原因**: 项目没有 `src-tauri` 目录，但 CI 尝试构建 Tauri

**解决方案**: 
- 添加了目录存在检查
- 如果没有 Tauri，跳过测试
- 不会导致 CI 失败

### 2. ❌ Build Docker Image 需要凭证

**原因**: Docker Hub 登录需要 `DOCKER_USERNAME` 和 `DOCKER_PASSWORD`，但未配置

**解决方案**:
- 添加凭证检查
- 如果没有凭证，只构建不推送
- 给出友好提示信息

---

## 当前 CI/CD 流程

### 工作流程

```
推送代码到 main/develop
    ↓
并行执行3个测试作业:
    ├─ Test Python Backend
    ├─ Test Frontend
    └─ Test Rust/Tauri (如果存在)
    ↓
测试通过后 (仅 main 分支):
    ├─ Build Release (多平台)
    └─ Build Docker Image
```

### 测试作业

#### 1. Test Python Backend
- ✅ Python 3.12
- ✅ 安装依赖
- ✅ Flake8 代码检查
- ✅ Pytest 测试

#### 2. Test Frontend
- ✅ Node.js 20
- ✅ 安装依赖
- ✅ TypeScript 类型检查
- ✅ 构建测试

#### 3. Test Rust/Tauri
- ✅ 检查 src-tauri 是否存在
- ✅ 如果存在，运行 Rust 测试
- ✅ 如果不存在，跳过

#### 4. Build Release (main 分支)
- ✅ Ubuntu/macOS/Windows
- ✅ 构建 Tauri 应用
- ✅ 上传构建产物

#### 5. Build Docker Image (main 分支)
- ✅ 检查 Docker 凭证
- ✅ 有凭证: 构建并推送
- ✅ 无凭证: 只构建不推送

---

## 配置 GitHub Secrets

### Docker Hub 推送（可选）

如果你想自动推送 Docker 镜像到 Docker Hub:

1. **创建 Docker Hub 账号**
   - 访问 https://hub.docker.com/
   - 注册账号

2. **获取 Access Token**
   - 登录 Docker Hub
   - Account Settings → Security → New Access Token
   - 复制 Token

3. **添加 GitHub Secrets**
   - 打开你的 GitHub 仓库
   - Settings → Secrets and variables → Actions
   - 点击 "New repository secret"
   - 添加两个 secrets:
     ```
     DOCKER_USERNAME: your-docker-username
     DOCKER_PASSWORD: your-docker-access-token
     ```

4. **完成**
   - 下次推送到 main 分支时，会自动推送镜像

---

## 修复后的行为

### ✅ Test Rust/Tauri

**之前**:
```
❌ Process completed with exit code 100
   (找不到 src-tauri 目录)
```

**现在**:
```
✅ Skipping Rust tests - no src-tauri directory found
   (优雅地跳过，不影响 CI)
```

### ✅ Build Docker Image

**之前**:
```
❌ Username and password required
   (必须配置 Docker 凭证)
```

**现在**:
```
⚠️ Docker image built locally (no credentials configured)
   To enable Docker Hub push, add DOCKER_USERNAME and DOCKER_PASSWORD secrets
   (构建成功，给出配置提示)
```

---

## 本地测试

### 测试 Python 后端

```bash
cd python-engine
pip install -r requirements.txt
pip install flake8 pytest pytest-asyncio

# 代码检查
flake8 . --count --select=E9,F63,F7,F82

# 运行测试
pytest
```

### 测试前端

```bash
npm ci
npx tsc --noEmit
npm run build
```

### 测试 Docker 构建

```bash
cd python-engine
docker build -t stocks-trading:local .
```

---

## 跳过 CI（如果需要）

在提交信息中添加 `[skip ci]`:

```bash
git commit -m "Update docs [skip ci]"
```

---

## CI 状态徽章

添加到 README.md:

```markdown
![CI/CD](https://github.com/your-username/stocks/workflows/CI%2FCD%20Pipeline/badge.svg)
```

---

## 故障排除

### 问题: CI 仍然失败

**检查列表**:
1. ✅ 确认 `.github/workflows/ci-cd.yml` 已更新
2. ✅ 推送更改到 GitHub
3. ✅ 查看 Actions 标签页的详细日志

### 问题: Docker 推送失败

**可能原因**:
1. Secrets 未配置或配置错误
2. Docker Hub 账号问题
3. Access Token 权限不足

**解决方案**:
1. 检查 Secrets 名称是否正确
2. 重新生成 Access Token
3. 确认 Token 有写入权限

### 问题: Tauri 构建失败

**可能原因**:
1. 系统依赖未安装
2. Rust 工具链问题
3. Node.js 版本不匹配

**解决方案**:
1. 检查 workflow 中的依赖安装
2. 更新 Rust 工具链版本
3. 确认 Node.js 版本为 20

---

## 高级配置

### 添加代码覆盖率

```yaml
- name: Test with coverage
  run: |
    pip install pytest-cov
    pytest --cov=. --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

### 添加性能测试

```yaml
- name: Performance test
  run: npm run test:perf
```

### 添加 E2E 测试

```yaml
- name: E2E tests
  run: |
    npm run build
    npm run test:e2e
```

---

## 自定义触发条件

### 仅在特定路径变化时触发

```yaml
on:
  push:
    branches: [ main ]
    paths:
      - 'src/**'
      - 'package.json'
```

### 定时运行

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # 每天午夜
```

### 手动触发

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'
```

---

## 总结

✅ **修复完成**:
- Rust/Tauri 测试不再失败
- Docker 构建不再需要强制凭证
- 添加友好的错误提示

✅ **当前状态**:
- Python 测试正常运行
- 前端构建正常运行
- Rust 测试优雅跳过（如果不存在）
- Docker 构建可选推送

✅ **下一步**:
- （可选）配置 Docker Hub secrets
- （可选）添加 Tauri 支持
- 继续开发，CI 会自动运行

---

**更新日期**: 2026-06-16  
**版本**: v2.0.1  
**修复内容**: GitHub Actions 错误修复
