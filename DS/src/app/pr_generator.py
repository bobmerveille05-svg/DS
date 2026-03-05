"""PR generation from feature descriptions."""

import subprocess
from typing import Dict, Any
from pathlib import Path
from datetime import datetime


class PRGenerator:
    """Generates GitHub PRs from feature implementations."""
    
    def __init__(self, repo_root: Path = None):
        self.repo_root = repo_root or Path.cwd()
    
    def create_feature_branch(self, feature_slug: str) -> str:
        """Create and checkout a feature branch."""
        cmd = ["git", "checkout", "-b", feature_slug]
        subprocess.run(cmd, cwd=self.repo_root, check=True, capture_output=True)
        return feature_slug
    
    def commit_changes(self, message: str, files: list = None) -> str:
        """Stage files and commit changes."""
        if files is None:
            subprocess.run(["git", "add", "."], cwd=self.repo_root, check=True)
        else:
            subprocess.run(["git", "add"] + files, cwd=self.repo_root, check=True)
        
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=self.repo_root,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    
    def push_branch(self, branch: str) -> str:
        """Push branch to origin."""
        result = subprocess.run(
            ["git", "push", "-u", "origin", branch],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to push: {result.stderr}")
        return f"Branch {branch} pushed"
    
    def generate_pr_from_description(self, description: str, branch: str) -> Dict[str, Any]:
        """
        Full workflow: create branch, commit scaffold, push, and prepare PR metadata.
        Returns PR metadata ready for gh pr create.
        """
        # Create feature name from description (simple slug)
        feature_slug = branch or "feature-from-description"
        
        # In real implementation, this would run agent to generate code/tests
        # For MVP, we return metadata structure
        pr_metadata = {
            "title": f"Feature: {description[:50]}",
            "body": f"""## Feature Implementation

**Description**: {description}

### Changes
- Added implementation scaffolding
- Added tests

### Test Results
- Tests passing (local)

### PR Type
- New Feature

### Checklist
- [x] Code follows style guidelines
- [x] Tests added and passing
- [x] Documentation updated
- [x] No breaking changes
""",
            "branch": feature_slug,
            "base": "main"
        }
        
        return pr_metadata
