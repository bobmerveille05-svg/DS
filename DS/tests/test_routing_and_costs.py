import tempfile
from pathlib import Path
from app.model_router import ModelRouter, ProviderConfig, ProviderType
from app.cost_logger import CostLogger


def test_model_router_register():
    """Test registering a provider."""
    router = ModelRouter()
    config = ProviderConfig(ProviderType.OPENAI, api_key="test-key")
    router.register_provider("openai", config)
    
    assert "openai" in router.providers
    assert router.get_provider("openai").provider_type == ProviderType.OPENAI


def test_model_router_default():
    """Test default provider routing."""
    router = ModelRouter()
    provider = router.get_provider()
    assert provider.provider_type == ProviderType.MOCK


def test_cost_logger_log():
    """Test logging a cost entry."""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / "costs.jsonl"
        logger = CostLogger(log_file=log_file)
        
        logger.log_cost("agent1", "gpt-4", 100, 0.05, task_id="task-1")
        
        assert len(logger.entries) == 1
        assert logger.entries[0].agent == "agent1"
        assert logger.entries[0].tokens_used == 100


def test_cost_logger_summary():
    """Test cost summary."""
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / "costs.jsonl"
        logger = CostLogger(log_file=log_file)
        
        logger.log_cost("agent1", "gpt-4", 100, 0.05)
        logger.log_cost("agent1", "gpt-4", 50, 0.025)
        
        summary = logger.get_summary("agent1")
        assert summary["count"] == 2
        assert summary["total_tokens"] == 150
        assert abs(summary["total_cost_usd"] - 0.075) < 1e-9  # Use approx comparison for floats
