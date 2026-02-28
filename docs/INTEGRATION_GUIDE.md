# 🔌 OAAI Model-Radar Integration Guide

OAAI Model-Radar is not just a concurrent latency testing radar; it naturally acts as your reliable **Local Configuration Gateway**. You can seamlessly integrate it into complex Agent frameworks (like OpenClaw, LangChain, or Autogen) to route AI requests appropriately.

## 🌟 Scenario 1: Seamless Integration with OpenClaw Engine
The OpenClaw engine requests a standard combination of `baseUrl` and `apiKey` to start acting intelligently. Instead of hardcoding these, you can dynamically select the best responding node from OAAI Model-Radar.

**Workflow Pipeline:**
1. Open the OAAI Model-Radar dashboard, click **"Test All"**, and evaluate which endpoint responds fastest.
2. Select it and set it as the **Primary Model**.
3. OAAI Model-Radar strictly persists this config into your `configs/` folder (e.g., `configs/default.json`).
4. Read this JSON configuration inside your main Python orchestrator script:

```python
import json

def get_best_llm_config(config_name="default"):
    # Read the optimal node persisted by OAAI Model-Radar
    config_path = f'path/to/oaai-model-radar/configs/{config_name}.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Locate the first configured provider
    provider_key = list(data['providers'].keys())[0]
    provider_info = data['providers'][provider_key]
    
    return {
        "base_url": provider_info['baseUrl'],
        "api_key": provider_info['apiKey'],
        "model_name": provider_info['primaryModel']
    }

# Inject the best config into your framework safely!
best_config = get_best_llm_config()
openclaw.init(
    baseUrl=best_config['base_url'], 
    apiKey=best_config['api_key'], 
    model=best_config['model_name']
)
```

## 🌟 Scenario 2: Connecting to the Shell as Environment Variables
If you run a heavy Docker-centric environment, you don't even need to use Python to read it. Use a tiny shell hack to convert your radar's result directly into an `.env` file!

```bash
# Extract value using jq
BEST_API_KEY=$(jq -r '.providers.OpenAI.apiKey' configs/default.json)
BEST_BASE_URL=$(jq -r '.providers.OpenAI.baseUrl' configs/default.json)

# Inject to docker
docker run -e OPENAI_API_KEY=$BEST_API_KEY -e OPENAI_BASE_URL=$BEST_BASE_URL my_agent_image
```

Enjoy treating OAAI Model-Radar as your centralized nerve center, while preserving 100% of your anonymity!
