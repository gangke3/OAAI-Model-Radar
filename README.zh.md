<div align="center">

# 🦀 OAAI Model-Radar

![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg)
![Docker Supported](https://img.shields.io/badge/Docker-Supported-2496ED?logo=docker&logoColor=white)
![Python 3.9+](https://img.shields.io/badge/Python-3.9+-yellow.svg)
[![OAAI.xyz](https://img.shields.io/badge/Website-OAAI.xyz-purple.svg)](https://oaai.xyz)
[![在线演示](https://img.shields.io/badge/🌐_在线演示-oaai.xyz%2Fmodel--radar-blue.svg)](https://oaai.xyz/model-radar/)

**告别繁重的网关，纯本地零依赖的 AI 模型 API 节点探测雷达与配置管理器** <br>
*由 OAAI.xyz 出品*

> 🌐 **[在线演示 → https://oaai.xyz/model-radar/](https://oaai.xyz/model-radar/)** &nbsp;*（只读预览，无需登录）*

</div>

---

## ✨ 界面预览 (Interface Preview)

<div align="center">
  <img src="assets/screenshot.png" alt="OAAI Model-Radar UI" width="800" style="border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);"/>
</div>

### 🚀 一键并发测试体验
感受“一键并发测试所有节点”的爽快感：
<div align="center">
  <img src="assets/demo.gif" alt="Concurrent Testing Demo" width="800" style="border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);"/>
</div>

## 🌟 核心特性 (Features)

- **⚡ 纯本地零依赖**：基于 Python 标准库构建，无需安装繁杂的第三方依赖。
- **🚀 优雅的并发测速**：一键并行测试多个 API 节点与模型，实时展现延迟与连通性。
- **🔐 数据纯本地安全**：所有配置和 API Key 均存储在本地文件中，绝不上传到任何云端。
- **📂 多配置无缝切换**：可为不同项目或应用创建相互独立的环境配置，切换游刃有余。
- **🐋 开箱即用的容器化**：提供轻量的 Docker 支持，服务端部署仅需一行命令，且自动持久化数据。

## 🚀 快速开始 (Quick Start)

### 方式 A：纯本地零依赖（桌面端推荐）

利用随附的一键启动脚本，你可以享受“双击即用”的极致体验。

**Windows OS:**
1. 双击运行目录下的 `start.bat`。
2. 脚本将自动启动服务，并在默认浏览器中唤起 `http://127.0.0.1:5000`。

**Mac / Linux OS:**
```bash
# 1. 赋予执行权限
chmod +x start.sh

# 2. 启动服务 (同时会自动为您打开浏览器)
./start.sh
```

### 方式 B：Docker 部署（服务器/运维端推荐）

让服务端运维人员享受开箱即用的乐趣，配置改动会在本地 `configs/` 目录持久化。

```bash
# 1. 确保已安装 Docker 和 Docker Compose
# 2. 在项目根目录执行：
docker-compose up -d

# 3. 访问 http://<您的服务器IP>:5000
```
要停止服务，只需运行 `docker-compose down`。

## ⚙️ 配置文件说明

`OAAI Model-Radar` 的各个配置文件统一存放于 `configs/` 目录中，支持热重载，您可以随时备份管理。配置文件的基本 JSON 结构如下：

```json
{
  "name": "My_First_Config",
  "providers": {
    "OpenAI": {
      "baseUrl": "https://api.openai.com/v1",
      "apiKey": "sk-xxx...",
      "models": [
        {
          "id": "gpt-4-turbo",
          "name": "GPT-4 Turbo"
        }
      ],
      "primaryModel": "gpt-4-turbo",
      "status": "available",
      "latency": 350,
      "lastTested": "2026-02-27T12:00:00.000Z"
    }
  }
}
```

## 📄 授权协议

本项目采用 [MIT License](LICENSE) 授权，随时欢迎你的 Star ⭐ 和 PR！

---
> Made with ❤️ by **[OAAI.xyz](https://oaai.xyz)**
