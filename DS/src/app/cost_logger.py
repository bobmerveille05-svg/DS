"""Token and cost tracking for LLM operations."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class CostEntry:
    """A single cost/token record."""
    timestamp: str
    agent: str
    model: str
    tokens_used: int
    cost_usd: float
    task_id: str = ""
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.metadata is None:
            data['metadata'] = {}
        return data


class CostLogger:
    """Logs and aggregates token/cost metrics."""
    
    def __init__(self, log_file: Path = None):
        self.log_file = log_file or Path("cost_log.jsonl")
        self.entries: List[CostEntry] = []
    
    def log_cost(self, agent: str, model: str, tokens_used: int, 
                 cost_usd: float, task_id: str = "", metadata: Dict = None) -> None:
        """Record a cost entry."""
        entry = CostEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            agent=agent,
            model=model,
            tokens_used=tokens_used,
            cost_usd=cost_usd,
            task_id=task_id,
            metadata=metadata or {}
        )
        self.entries.append(entry)
        
        # Append to file
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry.to_dict()) + "\n")
    
    def get_summary(self, agent: str = None) -> Dict[str, Any]:
        """Get cost summary, optionally filtered by agent."""
        filtered = self.entries
        if agent:
            filtered = [e for e in self.entries if e.agent == agent]
        
        total_tokens = sum(e.tokens_used for e in filtered)
        total_cost = sum(e.cost_usd for e in filtered)
        
        return {
            "count": len(filtered),
            "total_tokens": total_tokens,
            "total_cost_usd": total_cost,
            "avg_cost_per_token": total_cost / total_tokens if total_tokens > 0 else 0
        }
