<div align="center">

# 🦀 OpenClaw 节点管理器

**轻量级、零依赖的 AI API 节点管理工具，专为 OpenClaw 设计**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://python.org)
[![零依赖](https://img.shields.io/badge/后端-零依赖-success)](server.py)
[![欢迎PR](https://img.shields.io/badge/PRs-欢迎-brightgreen.svg)](CONTRIBUTING.md)

[English](README.md) · [快速开始](#-快速开始) · [API接口](#-api-接口) · [贡献指南](CONTRIBUTING.md)

</div>

---

## ✨ 项目介绍

OpenClaw 节点管理器是一个 **精美的 AI API 节点管理 Web UI**，帮助您在一个地方统一管理所有 AI 模型提供商（OpenAI、Claude、DeepSeek、Gemini、OpenRouter、通义千问、Kimi 等）。

支持可视化状态测试、多配置文件切换、节点增删改查，后端零依赖，开箱即用。

### 🎯 核心特性

| 特性 | 说明 |
|------|------|
| 🚀 **后端零依赖** | 纯 Python 标准库实现，无需任何 `pip install` |
| 🎨 **高颜值深色界面** | 玻璃拟态设计，流畅微动画，专业级视觉效果 |
| 🔀 **多配置文件管理** | 新建、重命名、复制、导入、导出配置文件 |
| ⚡ **并发 API 测试** | 并发测试所有节点，实时显示连通状态 |
| 📦 **单文件前端** | 整个 UI 就是一个 `index.html`，可离线使用 |
| 🌐 **兼容所有 OpenAI 接口** | 适配任何兼容 OpenAI 格式的 API 端点 |
| 💾 **导入/导出** | 支持 JSON 文件拖拽导入或粘贴文本导入 |
| ⭐ **主模型设置** | 为 OpenClaw Agents 设置默认使用的模型 |

---

## 🚀 快速开始

### 方式 A：单文件模式（无需构建）

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/openclaw-node-manager.git
cd openclaw-node-manager

# 启动服务（Python 3.x，零依赖！）
python server.py

# 打开浏览器访问
# → http://127.0.0.1:5000
```

### 方式 B：开发模式（热更新）

```bash
# 终端 1 — 后端
python server.py

# 终端 2 — 前端开发服务器
cd manager-ui
npm install    # 首次运行
npm run dev    # → http://localhost:5173
```

### 方式 C：生产构建

```bash
cd manager-ui && npm run build
cd ..
python server.py   # 自动服务 dist/ 目录
# → http://127.0.0.1:5000
```

---

## 📁 目录结构

```
openclaw-node-manager/
├── server.py              # 后端 API 服务（纯 Python 标准库）
├── index.html             # 完整前端（单文件，使用 CDN React）
├── configs/
│   └── example_config.json   # 配置模板，填入您的 API Key 使用
└── manager-ui/            # （可选）Vite + React 开发源码
    ├── src/
    │   └── App.jsx
    └── package.json
```

---

## ⚙️ 配置说明

复制示例配置并填入您的 API 密钥：

```bash
cp configs/example_config.json configs/我的配置.json
# 编辑 configs/我的配置.json，填入真实的 API Key
```

### 配置文件格式

```json
{
  "models": {
    "providers": {
      "节点名称": {
        "baseUrl": "https://api.example.com/v1",
        "apiKey": "sk-您的API密钥",
        "api": "openai-completions",
        "models": [
          {
            "id": "模型ID",
            "name": "显示名称",
            "reasoning": false,
            "input": ["text", "image"],
            "contextWindow": 128000,
            "maxTokens": 4096
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": { "primary": "节点名称/模型ID" }
    }
  }
}
```

### 已测试的 AI 服务商

| 服务商 | Base URL |
|--------|----------|
| OpenAI | `https://api.openai.com/v1` |
| Anthropic (Claude) | `https://api.anthropic.com/v1` |
| DeepSeek | `https://api.deepseek.com/v1` |
| OpenRouter | `https://openrouter.ai/api/v1` |
| 阿里云通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 月之暗面 Kimi | `https://api.moonshot.cn/v1` |
| 智谱 GLM | `https://open.bigmodel.cn/api/paas/v4` |
| NVIDIA NIM | `https://integrate.api.nvidia.com/v1` |
| Google AI Studio | `https://generativelanguage.googleapis.com/v1beta/openai` |

---

## 🔌 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/config/list` | GET | 列出所有配置文件 |
| `/api/config?config=<名称>` | GET | 读取完整配置 |
| `/api/config?config=<名称>` | POST | 保存完整配置 |
| `/api/config?config=<名称>` | DELETE | 删除配置文件 |
| `/api/providers?config=<名称>` | GET | 获取节点列表 |
| `/api/providers/<节点名>?config=<名称>` | POST | 新增/更新节点 |
| `/api/providers/<节点名>?config=<名称>` | DELETE | 删除节点 |
| `/api/test?config=<名称>` | POST | 并发测试所有节点 |
| `/api/test/<节点名>` | POST | 测试单个节点 |

---

## 🛠️ 环境要求

| 层级 | 要求 |
|------|------|
| 后端 | Python 3.6+（仅标准库，无需 pip） |
| 前端（CDN 模式） | 任意现代浏览器 |
| 前端（开发模式） | Node.js 16+ 及 npm |

---

## 🤝 贡献指南

欢迎提交 PR！请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/新特性`)
3. 提交更改 (`git commit -m 'feat: 添加新特性'`)
4. 推送到分支 (`git push origin feature/新特性`)
5. 提交 Pull Request

---

## 📝 开源协议

本项目遵循 [MIT License](LICENSE) 开源协议。

---

<div align="center">

用 ❤️ 为 OpenClaw 用户打造 · [反馈问题](../../issues) · [功能建议](../../issues)

</div>
