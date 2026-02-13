"""Model provider routing interface."""

from typing import Protocol, Dict, Any
from enum import Enum


class ProviderType(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MOCK = "mock"  # For testing


class ProviderConfig:
    """Configuration for a model provider."""
    
    def __init__(self, provider_type: ProviderType, api_key: str = "", **kwargs):
        self.provider_type = provider_type
        self.api_key = api_key
        self.extra_config = kwargs


class ModelRouter:
    """Routes tasks to optimal LLM providers based on configuration."""
    
    def __init__(self):
        self.providers: Dict[str, ProviderConfig] = {}
        self.default_provider: str = "mock"
    
    def register_provider(self, name: str, config: ProviderConfig) -> None:
        """Register a model provider."""
        self.providers[name] = config
    
    def get_provider(self, provider_name: str = None) -> ProviderConfig:
        """Get provider config, defaulting to default provider."""
        if provider_name is None:
            provider_name = self.default_provider
        
        if provider_name not in self.providers:
            raise ValueError(f"Provider '{provider_name}' not registered")
        
        return self.providers[provider_name]
    
    def route_task(self, task_description: str, preferred_provider: str = None) -> str:
        """Route a task to a provider and return provider name."""
        provider = self.get_provider(preferred_provider)
        return provider.provider_type.value
