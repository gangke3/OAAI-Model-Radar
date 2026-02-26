# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-02-26

### 🎉 Initial Release

#### Added
- **Multi-profile configuration management** — Create, rename, copy, delete, import and export config profiles
- **Concurrent API node testing** — Test all providers simultaneously with real-time status indicators
- **Per-node status display** — Color-coded success/error badges with expandable error details
- **Primary model configuration** — Set and persist the default model for OpenClaw agents
- **Import / Export** — Import via JSON file or paste; export current config to file
- **Add node via form or JSON** — Flexible node addition with form UI or raw JSON code input
- **Copy node JSON** — One-click copy of any node's JSON configuration
- **Unsaved changes prompt** — Warns before switching profiles or closing with unsaved changes
- **Zero-dependency Python backend** — `server.py` uses only Python standard library (no pip needed)
- **Single-file frontend** — `index.html` uses CDN-loaded React, works without any Node.js build step
- **Premium dark glassmorphism UI** — HSL color system, micro-animations, responsive layout
- **Persistent config selection** — Remembers last selected profile via `localStorage`

#### Supported Providers
- OpenAI (GPT-4o, GPT-4o-mini, o1, o3)
- Anthropic (Claude 3.5 Sonnet, Claude 3 Haiku)
- DeepSeek (DeepSeek-V3, DeepSeek-R1)
- OpenRouter (aggregator, 200+ models)
- Alibaba Cloud Qwen (通义千问)
- Moonshot Kimi (月之暗面)
- ZhipuAI GLM (智谱)
- NVIDIA NIM
- Google AI Studio (Gemini)
- Any OpenAI-compatible API endpoint
