# models/model_dispatcher.py

def call_model(model_config: dict, prompt: str) -> dict:

    provider = model_config["provider"]

    if provider == "openai":
        from models.openai_adapter import call_openai
        return call_openai(model_config, prompt)

    elif provider == "gemini":
        from models.gemini_adapter import call_gemini
        return call_gemini(model_config, prompt)

    elif provider == "claude":
        from models.claude_adapter import call_claude
        return call_claude(model_config, prompt)

    elif provider == "perplexity":
        from models.perplexity_adapter import call_perplexity
        return call_perplexity(model_config, prompt)

    else:
        raise ValueError(f"Unsupported provider: {provider}")