# Analyze a local git repository at a specific path.
# Edit the REPO_PATH variable below to point to the repository you want to
# investigate.

# Usage:
#   bash examples/analyze_local_path.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOOSE="$SCRIPT_DIR/../goose.py"

# Edit this path 
REPO_PATH="/path/to/your/repo"

if [ ! -d "$REPO_PATH/.git" ]; then
  echo "❌ Error: '$REPO_PATH' is not a valid git repository."
  echo "   Please update REPO_PATH inside this script."
  exit 1
fi

echo "🪿 Running Goose Finder on: $REPO_PATH"
python "$GOOSE" "$REPO_PATH"
