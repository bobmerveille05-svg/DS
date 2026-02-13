import tempfile
from pathlib import Path
from app.orchestrator import AgentOrchestrator
from app.pr_generator import PRGenerator


def test_agent_orchestrator_create_task():
    """Test creating an agent task."""
    orchestrator = AgentOrchestrator()
    task_id = orchestrator.create_task("planner", "Describe feature")
    
    assert task_id in orchestrator.tasks
    assert orchestrator.tasks[task_id].agent_type == "planner"
    assert orchestrator.tasks[task_id].status == "pending"


def test_agent_orchestrator_workflow():
    """Test full feature workflow."""
    orchestrator = AgentOrchestrator()
    result = orchestrator.run_feature_workflow("Add user authentication")
    
    assert result["status"] == "ready_for_pr"
    assert "plan_task" in result
    assert "code_task" in result
    assert "test_task" in result
    
    # Verify all tasks completed
    plan_task = orchestrator.tasks[result["plan_task"]]
    assert plan_task.status == "completed"
    assert len(plan_task.output) > 0


def test_pr_generator_metadata():
    """Test PR metadata generation."""
    gen = PRGenerator()
    metadata = gen.generate_pr_from_description(
        "Add login endpoint",
        "feature-login"
    )
    
    assert "title" in metadata
    assert "body" in metadata
    assert metadata["base"] == "main"
    assert "Add login endpoint" in metadata["title"]


def test_orchestrator_task_lifecycle():
    """Test task state transitions."""
    orchestrator = AgentOrchestrator()
    task_id = orchestrator.create_task("coder", "Implement feature")
    
    # Initial state
    task = orchestrator.tasks[task_id]
    assert task.status == "pending"
    
    # Start task
    orchestrator.start_task(task_id)
    assert task.status == "running"
    assert task.started_at
    
    # Complete task
    orchestrator.complete_task(task_id, "Feature implemented")
    assert task.status == "completed"
    assert task.output == "Feature implemented"
    assert task.completed_at
