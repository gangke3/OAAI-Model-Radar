# OAAI Model-Radar 全网推广首发物料包

这些是我为你撰写的宣发软文和指南，您可以直接复制去各大社区发布！

## 第一波：国内社区“冷启动”软文

### 🎯 适用平台：V2EX / 掘金 / 知乎 / 开源中国
**标题建议：** 【造了个轮子】受够了臃肿的网关，我用 Python 标准库撸了一个零依赖、纯本地的大模型接口测速与管理器
**节点/标签建议：** `分享创造`, `Python`, `人工智能`, `AIGC`, `开源`

**正文内容：**
大家好！

在折腾各种大模型 API 和构建 Agent 的时候，我发现自己手里总是攒了一大堆 OpenAI 格式的 API 节点和 Key（比如各家大模型官方厂、个人部署的中转站、或者像 Ollama 跑的本地小模型等）。

为了管理它们并测算延迟哪家最快，市面上的方案两极分化极为严重：
1. **老牌 API 网关项目**：比如 OneAPI 等。功能确实强，但是环境太重了！你要建一个数据库、搞一堆依赖，有的甚至要 Redis 才能跑跑起来。
2. **在线的白嫖测速网站**：方便是方便，但谁敢把带有自己信用卡额度的 Key，轻易粘贴到一个不知名网站里呢？这种东西一旦后门抓取，那损失就大了。

为了完全解决这个痛点，我花了一点时间写了一个非常纯粹的小工具：「**OAAI Model-Radar**」。

它**没有**采用任何臃肿的框架，甚至做到了**零第三方依赖**（纯用 Python 基础标准库搭建），主打的就是极致的轻量、安全、纯本地化。

👉 **[项目地址 GitHub: 请替换为您的 GitHub Url]**
🌍 **[在线只读演示: https://oaai.xyz/model-radar/ ]**

#### 💡 这个雷达工具有什么特点？
- **⚡ 零依赖双击即用**：不用经历痛苦的 `pip install` 或者各种报错。只要有环境，点开就能跑！（同时也内置了纯净版极速 Docker-compose 一行启动方案给你）。前端应用了我手搓的原生玻璃拟态 (Glassmorphism) UI，支持暗色模式，颜值和手感都极度在线。
- **🚀 一键高并发快感**：把你有的 API 端点全堆进去，点一下“测试全部”，瞬间并发测试所有厂商和节点的连通性和实际延迟，谁快谁慢一秒见效！
- **🔐 真正的安全保险箱**：所有配置生成标准的物理本地 JSON 文件。连一个向上统计发送的字节都没有，完全不需要担心 API 层泄露！
- **📂 支持复杂环境热插拔**：你可以为自己不同的开发工程创建多套独立 Config 方便按需隔离（这对多项目共存非常有帮助）。

这虽然是个个人练手开源工具，但希望能在极简纯粹主义的道路上帮到同样折腾大模型的大家。如果大家体验后有什么改进建议，热烈欢迎直接给我提 Issue 或丢 PR。如果它帮你省下了折腾环境的时间，希望能点个 **Star⭐** 给我一点动力！感谢各位！

---

## 第二波：海外超级流量池同步引爆引流

### 🎯 适用平台：Reddit (`r/selfhosted`, `r/Python`, `r/LocalLLaMA`)
*发布建议规则：请在北美工作日的早晨（对应北京时间的晚上 9:00 - 11:30 之间发帖效果极佳）。*

**Title:** I built a zero-dependency, local-only LLM API manager & concurrent speed radar, because I don't trust cloud testers.

**Body:**
Hey folks! 

Like many of us diving deep into LLM ecosystems, I have an ever-growing collection of local models, custom endpoints, and various API keys spread across different projects. To manage them and benchmark latency, I found myself choosing between two unpleasant options: 

1. Implementing gigantic enterprise API Gateways (which require database databases, Go/Node deployments, huge dependencies).
2. Using random online speed-testing tools (which means pasting valid paid API keys onto third-party servers... big no.)

So, I scratched my own itch and built **OAAI Model-Radar**.

💻 **Link to GitHub Repo:** [Your GitHub Link]
🌐 **Live Preview (Read-only UI demo):** https://oaai.xyz/model-radar/

The most important feature for me: It uses **Zero Third-Party Dependencies**. I built the backend completely with Python's standard library to guarantee portability without environment hell.

**Core specs I focused on:**
- **Absolute Local Privacy**: Your keys never leave your device. All your configs are strictly stored in local `.json` files.
- **Concurrent Benchmarking**: Press one button and it pings all your endpoints concurrently to show accurate real-time latency across your matrix.
- **Zero Fiction Setup**: Run the `start.bat` or `start.sh` straight out of the box. Docker `compose` support is there too.
- **Gorgeous UI**: Built a custom dark mode UI featuring a glassmorphism style using plain HTML/JS/CSS without bloated frontend frameworks.

I am an independent dev and built this to keep things light and robust. I’d love to hear your honest feedback. Feel free to roast the code or suggest features! If this perfectly fits into your self-hosted LLM stack, a Star ⭐ would definitely make my day. Enjoy!

### 🎯 适用平台：Hacker News (Show HN 分类)
**Title:** Show HN: A zero-dependency local API manager & speed radar for LLMs in Python

**URL:** 填入你的 GitHub 仓库地址。
*(HackerNews 不需要你废话太多，极客们看到标题懂了就会点进去看你的 Readme 里的对比图，你的对比图现在已经足够惊艳了！)*

---

## 🚀 第三步：“傍大款”持续被动引流 (向 Awesome List 提交 PR)
请去 GitHub 核心搜索框内搜索这三个顶流榜单，Fork 它们，然后提交一句话的 Pull Request 将你的仓库地址加进去：
- [ ] `awesome-llm` 
- [ ] `awesome-ai-tools`
- [ ] `awesome-selfhosted` (由于我们有 Docker 功能和完美自建特性，这个榜极其合适)

**PR Description Sample:**
*"Proposing to add OAAI Model-Radar - a zero-dependency local LLM API config manager and concurrent speed testing tool, fitting great for users seeking lightweight privacy-first implementations."*
