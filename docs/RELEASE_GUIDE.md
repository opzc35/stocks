# Release 工作流说明

## 📦 发布内容

当你推送一个版本标签时（如 `v2.0.2`），会自动构建并发布以下内容：

### 1. ✅ Web 应用（默认）
**始终构建**

输出文件：
- `stocks-web-2.0.2.tar.gz` - Linux/Mac 用户
- `stocks-web-2.0.2.zip` - Windows 用户

包含内容：
- 构建好的 HTML/CSS/JS 文件
- 可部署到任何 Web 服务器

使用方式：
```bash
# 解压
tar -xzf stocks-web-2.0.2.tar.gz
# 或
unzip stocks-web-2.0.2.zip

# 部署到 Web 服务器
nginx -s reload
# 或使用任何静态文件服务器
```

### 2. 🖥️ 桌面应用（可选）
**仅当存在 `src-tauri` 目录时构建**

当前状态：⏭️ **跳过**（项目没有 src-tauri）

如果将来添加 Tauri：
- `stocks-trading_2.0.2_amd64.deb` - Ubuntu/Debian
- `stocks-trading-2.0.2.dmg` - macOS
- `stocks-trading-2.0.2.msi` - Windows

### 3. 🐳 Docker 镜像（可选）
**仅当配置了 Docker Hub 凭证时推送**

镜像标签：
- `username/stocks-trading:latest`
- `username/stocks-trading:2.0.2`

使用方式：
```bash
docker pull username/stocks-trading:latest
docker run -p 8000:8000 username/stocks-trading:latest
```

---

## 🚀 如何发布版本

### 方式 1: 创建标签（推荐）

```bash
# 1. 确保所有更改已提交
git add .
git commit -m "feat: 完成 v2.0.2"

# 2. 创建标签
git tag v2.0.2

# 3. 推送标签
git push origin v2.0.2

# 4. 自动触发 Release workflow
# 查看: https://github.com/your-repo/actions
```

### 方式 2: GitHub UI 创建 Release

1. 访问 `https://github.com/your-repo/releases/new`
2. 选择或创建新标签
3. 填写 Release 标题和描述
4. 点击 "Publish release"

### 方式 3: 手动触发

1. 访问 `https://github.com/your-repo/actions/workflows/release.yml`
2. 点击 "Run workflow"
3. 选择分支和输入标签

---

## 📊 构建时间

| 任务 | 时间 | 说明 |
|------|------|------|
| Create Release | ~30s | 创建 GitHub Release |
| Build Web | ~2m | 构建 Web 应用 |
| Build Tauri | ~8m | 构建桌面应用（如果有） |
| Publish Docker | ~5m | 发布 Docker 镜像（如果配置） |

**总时间**:
- 仅 Web: ~2-3 分钟
- Web + Docker: ~7-8 分钟
- 全部（Web + Tauri + Docker）: ~15 分钟

---

## 🎯 推荐的发布流程

### 当前项目（Web 为主）

```bash
# 1. 完成开发和测试
npm run build  # 本地测试

# 2. 更新版本号（可选）
# 编辑 package.json 中的 version

# 3. 提交更改
git add .
git commit -m "chore: bump version to 2.0.2"

# 4. 创建并推送标签
git tag v2.0.2
git push origin v2.0.2

# 5. 查看构建
# GitHub Actions → Release workflow
```

### 发布后

Release 页面会包含：
- 📝 Release 说明
- 📦 `stocks-web-2.0.2.tar.gz` (下载)
- 📦 `stocks-web-2.0.2.zip` (下载)
- 🐳 Docker 镜像链接（如果推送了）

---

## 🔧 配置选项

### 启用 Docker 推送

在 GitHub 仓库设置中添加 Secrets:
- `DOCKER_USERNAME` - Docker Hub 用户名
- `DOCKER_PASSWORD` - Docker Hub Token

### 启用 Tauri 构建

1. 初始化 Tauri:
   ```bash
   npm create tauri-app
   # 选择集成到现有项目
   ```

2. 添加应用图标:
   ```
   src-tauri/icons/
   ├── icon.png (512x512, 方形)
   ├── 32x32.png
   ├── 128x128.png
   └── icon.ico (Windows)
   ```

3. 下次推送标签时会自动构建桌面应用

---

## 📥 用户如何使用发布

### Web 部署

```bash
# 1. 下载 release
wget https://github.com/your-repo/releases/download/v2.0.2/stocks-web-2.0.2.tar.gz

# 2. 解压
tar -xzf stocks-web-2.0.2.tar.gz

# 3. 部署
# Nginx
sudo cp -r dist/* /var/www/html/

# 或使用 serve
npx serve dist
```

### Docker 部署

```bash
# 拉取镜像
docker pull username/stocks-trading:2.0.2

# 运行容器
docker run -d \
  -p 8000:8000 \
  --name stocks-api \
  username/stocks-trading:2.0.2
```

### 桌面应用（将来）

**Windows**:
1. 下载 `.msi` 文件
2. 双击安装

**macOS**:
1. 下载 `.dmg` 文件
2. 拖拽到 Applications

**Linux**:
```bash
# Debian/Ubuntu
sudo dpkg -i stocks-trading_2.0.2_amd64.deb

# 或 AppImage
chmod +x stocks-trading_2.0.2_amd64.AppImage
./stocks-trading_2.0.2_amd64.AppImage
```

---

## 🔍 故障排除

### Release 创建成功但没有附件

**可能原因**:
- `npm run build` 失败
- `dist/` 目录为空
- Upload asset 步骤失败

**解决方案**:
1. 查看 Actions 日志
2. 本地测试 `npm run build`
3. 确认 `dist/` 目录存在

### Tauri 构建失败

**可能原因**:
- 缺少应用图标
- 缺少 Cargo.toml
- 系统依赖未安装

**解决方案**:
- 当前已自动跳过（if: hashFiles）
- 添加 src-tauri 后会自动启用

### Docker 推送失败

**可能原因**:
- 未配置 Docker Hub 凭证
- Token 权限不足

**解决方案**:
- 当前已自动跳过（if: vars.DOCKER_USERNAME）
- 配置 Secrets 后会自动启用

---

## 📝 版本号规范

推荐使用语义化版本（SemVer）:

- `v1.0.0` - 主版本（重大更改）
- `v1.1.0` - 次版本（新功能）
- `v1.1.1` - 补丁版本（Bug 修复）

示例：
```bash
# 修复 bug
git tag v2.0.3

# 添加新功能
git tag v2.1.0

# 重大更新
git tag v3.0.0
```

---

## 🎉 总结

**当前配置**:
- ✅ Web 应用自动构建和发布
- ⏭️ Tauri 桌面应用自动跳过（无 src-tauri）
- ⏭️ Docker 镜像自动跳过（无凭证）

**推荐使用**:
- Web 应用发布 → 适合部署到服务器
- 用户访问 Web 界面使用

**将来扩展**:
- 配置 Docker Hub → 支持容器化部署
- 添加 Tauri → 支持桌面应用

---

**版本**: v2.0.2  
**更新**: 2026-06-16
