# CI/CD 配置指南

## GitHub Actions 工作流

项目配置了完整的CI/CD流程，包括：

### 1. 持续集成 (CI) - `ci-cd.yml`

**触发条件**：
- Push到 `main` 或 `develop` 分支
- Pull Request到 `main` 或 `develop` 分支

**工作流程**：

#### Python后端测试
- ✅ 安装Python 3.12
- ✅ 安装依赖包
- ✅ Flake8代码检查
- ✅ Pytest单元测试

#### 前端测试
- ✅ 安装Node.js 20
- ✅ 安装npm依赖
- ✅ TypeScript类型检查
- ✅ 构建前端应用

#### Rust/Tauri测试
- ✅ 安装Rust工具链
- ✅ Cargo代码检查
- ✅ Clippy静态分析
- ✅ 运行Rust测试

#### 发布构建 (仅main分支)
- ✅ 跨平台构建 (Ubuntu, macOS, Windows)
- ✅ 生成Tauri应用
- ✅ 上传构建产物

#### Docker镜像 (可选)
- ✅ 构建Docker镜像
- ✅ 推送到Docker Hub

### 2. 发布工作流 - `release.yml`

**触发条件**：
- 推送版本标签 (例如：`v1.0.0`)

**工作流程**：
- ✅ 创建GitHub Release
- ✅ 构建多平台Tauri应用
- ✅ 自动上传到Release
- ✅ 发布Docker镜像到Docker Hub

### 3. 依赖更新检查 - `dependencies.yml`

**触发条件**：
- 每周一早上8点自动运行
- 手动触发

**工作流程**：
- ✅ 检查Python依赖安全性 (pip-audit)
- ✅ 检查npm依赖安全性 (npm audit)
- ✅ 发现问题自动创建Issue

---

## 配置 Secrets

在GitHub仓库设置中需要配置以下Secrets：

### 必需的Secrets (用于Docker发布)：
```
DOCKER_USERNAME   - Docker Hub用户名
DOCKER_PASSWORD   - Docker Hub访问令牌
```

### 可选的Secrets：
```
ANTHROPIC_API_KEY - Claude AI API密钥 (用于AI功能)
```

**配置路径**：
Settings → Secrets and variables → Actions → New repository secret

---

## Docker部署

### 使用Docker Compose

1. **启动所有服务**：
```bash
docker-compose up -d
```

2. **查看日志**：
```bash
docker-compose logs -f
```

3. **停止服务**：
```bash
docker-compose down
```

### 使用Docker直接运行

1. **构建镜像**：
```bash
cd python-engine
docker build -t stocks-backend .
```

2. **运行容器**：
```bash
docker run -d -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_key \
  -v $(pwd)/data:/app/data \
  --name stocks-backend \
  stocks-backend
```

---

## 本地开发工作流

### 1. 开发前检查
```bash
# Python代码检查
cd python-engine
flake8 .

# TypeScript类型检查
npx tsc --noEmit

# Rust代码检查
cd src-tauri
cargo clippy
```

### 2. 运行测试
```bash
# Python测试
cd python-engine
pytest

# Rust测试
cd src-tauri
cargo test
```

### 3. 构建应用
```bash
# 前端构建
npm run build

# Tauri构建
npm run tauri:build
```

---

## 发布新版本

### 步骤：

1. **更新版本号**：
```bash
# 更新 package.json
# 更新 src-tauri/Cargo.toml
# 更新 src-tauri/tauri.conf.json
```

2. **提交更改**：
```bash
git add .
git commit -m "chore: bump version to v1.0.0"
```

3. **创建标签**：
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

4. **自动触发**：
- GitHub Actions自动运行
- 构建多平台应用
- 创建GitHub Release
- 发布Docker镜像

---

## CI/CD徽章

在README.md中添加徽章：

```markdown
![CI/CD](https://github.com/your-username/stocks/workflows/CI%2FCD%20Pipeline/badge.svg)
![Release](https://github.com/your-username/stocks/workflows/Release/badge.svg)
```

---

## 故障排查

### 构建失败

1. **检查日志**：
   - 访问 GitHub Actions 标签页
   - 点击失败的工作流
   - 查看详细日志

2. **常见问题**：
   - 依赖版本冲突：更新 `requirements.txt` 或 `package.json`
   - 系统依赖缺失：检查 Ubuntu安装步骤
   - 测试失败：修复代码后重新推送

### Docker构建失败

1. **本地测试**：
```bash
docker-compose build
docker-compose up
```

2. **检查Dockerfile**：
   - 确认基础镜像版本
   - 检查依赖安装命令
   - 验证文件路径

---

## 性能优化

### 缓存策略

CI/CD配置使用缓存加速构建：

- **Python**: `~/.cache/pip`
- **Node.js**: `~/.npm`
- **Rust**: `~/.cargo/` + `target/`
- **Docker**: GitHub Container Registry

### 并行化

- 三个测试作业并行运行
- 多平台构建并行执行
- 减少总构建时间

---

## 监控和通知

### GitHub Actions通知

GitHub会自动发送通知：
- ✅ 工作流完成
- ❌ 工作流失败
- 📋 依赖问题

### 自定义通知 (可选)

可以集成Slack、Discord等：

```yaml
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 安全最佳实践

1. **不要提交Secrets到代码**
2. **使用GitHub Secrets管理敏感信息**
3. **定期更新依赖**
4. **审查依赖更新工作流的Issue**
5. **使用最小权限原则**

---

## 文档更新日期

**版本**: 1.0.0  
**更新时间**: 2026-06-15

---

## 相关链接

- [GitHub Actions文档](https://docs.github.com/actions)
- [Tauri Actions](https://github.com/tauri-apps/tauri-action)
- [Docker Build Push](https://github.com/docker/build-push-action)
