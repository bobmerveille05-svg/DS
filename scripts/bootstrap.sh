#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Bootstrapping Spec-Atlas project..."

check_dependency() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "❌ $1 not found. Install: $2"
        exit 1
    fi
    echo "✅ $1"
}

echo "📋 Checking dependencies..."
check_dependency "git" "https://git-scm.com"
check_dependency "uv" "https://docs.astral.sh/uv"
check_dependency "python3" "https://python.org"

echo ""
echo "📦 Installing specify-cli..."
uv tool install specify-cli \
    --from git+https://github.com/github/spec-kit.git \
    --force

echo ""
echo "⚙️  Configuring VS Code settings..."
mkdir -p .vscode

cat > .vscode/settings.json << 'SETTINGS_EOF'
{
    "chat.customAgentInSubagent.enabled": true,
    "github.copilot.chat.responsesApiReasoningEffort": "high",
    "chat.agent.maxRequests": 100
}
SETTINGS_EOF

cat > .vscode/extensions.json << 'EXTENSIONS_EOF'
{
    "recommendations": [
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "ms-python.python"
    ]
}
EXTENSIONS_EOF

echo ""
echo "🌿 Setting up git..."
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "chore: initial spec-atlas template setup"
fi

cat > AGENTS.md << 'AGENTS_EOF'
# Agent Configuration

## Plan Directory
.specify/specs

## Constitution
.specify/memory/constitution.md

## Atlas Phases Directory
.specify/specs
AGENTS_EOF

echo ""
echo "✅ Bootstrap complete!"
echo ""
echo "Next steps:"
echo "  1. Open VS Code: code ."
echo "  2. Run: specify init . --here --ai copilot"
echo "  3. Start with: /speckit.constitution"
