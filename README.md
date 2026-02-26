<div align="center">

# 🦀 OpenClaw Node Manager

**A lightweight, zero-dependency AI API node manager for OpenClaw**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://python.org)
[![Zero Dependencies](https://img.shields.io/badge/Backend-Zero%20Dependencies-success)](server.py)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[中文文档](README.zh.md) · [Quick Start](#-quick-start) · [API Reference](#-api-reference) · [Contributing](CONTRIBUTING.md)

</div>

---

## ✨ What is OpenClaw Node Manager?

OpenClaw Node Manager is a **beautiful, production-ready web UI** for managing your OpenClaw API configurations. It lets you organize multiple AI model providers (OpenAI, Claude, DeepSeek, Gemini, OpenRouter, etc.) in one place — with visual status testing, multi-profile support, and zero server-side dependencies.

### 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 🚀 **Zero Backend Dependencies** | Server written in pure Python stdlib — no `pip install` ever needed |
| 🎨 **Premium Dark UI** | Glassmorphism design with smooth micro-animations |
| 🔀 **Multi-Profile Management** | Create, rename, copy, import & export configuration profiles |
| ⚡ **Concurrent API Testing** | Test all nodes simultaneously with real-time status indicators |
| 📦 **Single-File Frontend** | Entire UI is one `index.html` — works offline or as a static site |
| 🌐 **OpenAI-Compatible** | Works with any OpenAI-compatible API endpoint |
| 💾 **Import / Export** | Drag & drop JSON or paste to import; one-click export |
| ⭐ **Primary Model** | Set and track which model is your default for OpenClaw agents |

---

## 🚀 Quick Start

### Option A: One-File Mode (No Build Needed)

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/openclaw-node-manager.git
cd openclaw-node-manager

# Start the server (Python 3.x, zero dependencies!)
python server.py

# Open your browser
# → http://127.0.0.1:5000
```

### Option B: Development Mode (With Hot Reload)

```bash
# Terminal 1 — Backend
python server.py

# Terminal 2 — Frontend dev server
cd manager-ui
npm install    # first time only
npm run dev    # → http://localhost:5173
```

### Option C: Production Build

```bash
cd manager-ui && npm run build
cd ..
python server.py   # serves built frontend from dist/
# → http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
openclaw-node-manager/
├── server.py              # Backend API server (Python stdlib only)
├── index.html             # Complete frontend (single file, CDN React)
├── configs/
│   └── example_config.json   # Template — copy & fill in your API keys
└── manager-ui/            # (Optional) Vite + React source for development
    ├── src/
    │   └── App.jsx
    └── package.json
```

---

## ⚙️ Configuration

Copy the example configuration and fill in your API keys:

```bash
cp configs/example_config.json configs/my_config.json
# Edit my_config.json with your API keys
```

### Configuration Schema

```json
{
  "models": {
    "providers": {
      "ProviderName": {
        "baseUrl": "https://api.example.com/v1",
        "apiKey": "sk-YOUR_API_KEY",
        "api": "openai-completions",
        "models": [
          {
            "id": "model-id",
            "name": "Display Name",
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
      "model": { "primary": "ProviderName/model-id" }
    }
  }
}
```

### Supported Providers

Any OpenAI-compatible API works. Here are some tested providers:

| Provider | Base URL |
|----------|----------|
| OpenAI | `https://api.openai.com/v1` |
| Anthropic (Claude) | `https://api.anthropic.com/v1` |
| DeepSeek | `https://api.deepseek.com/v1` |
| OpenRouter | `https://openrouter.ai/api/v1` |
| Alibaba Cloud (Qwen) | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Moonshot (Kimi) | `https://api.moonshot.cn/v1` |
| ZhipuAI (GLM) | `https://open.bigmodel.cn/api/paas/v4` |
| NVIDIA NIM | `https://integrate.api.nvidia.com/v1` |
| Google AI Studio | `https://generativelanguage.googleapis.com/v1beta/openai` |

---

## 🔌 API Reference

The backend exposes a simple REST API:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/config/list` | GET | List all configuration profiles |
| `/api/config?config=<name>` | GET | Read a full configuration |
| `/api/config?config=<name>` | POST | Save a full configuration |
| `/api/config?config=<name>` | DELETE | Delete a configuration profile |
| `/api/providers?config=<name>` | GET | Get providers list only |
| `/api/providers/<name>?config=<name>` | POST | Add / update a single provider |
| `/api/providers/<name>?config=<name>` | DELETE | Remove a single provider |
| `/api/test?config=<name>` | POST | Concurrently test all providers |
| `/api/test/<name>` | POST | Test a single provider |

---

## 🛠️ Requirements

| Layer | Requirement |
|-------|-------------|
| Backend | Python 3.6+ (standard library only, no pip needed) |
| Frontend (CDN mode) | Any modern browser |
| Frontend (Dev mode) | Node.js 16+ & npm |

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ for OpenClaw users · [Report Bug](../../issues) · [Request Feature](../../issues)

</div>
