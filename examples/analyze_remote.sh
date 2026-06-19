# Analyze a remote git repository directly from its URL — no manual clone
# needed. Goose Finder (via PyDriller) handles the cloning internally.

# This example uses the `requests` library as a demo target because it is
# a well-known, pure-Python project with a rich commit history that produces
# interesting Goose Finder output.

# Usage:
#   bash examples/analyze_remote.sh

# Replace REPO_URL with any public Python repository you want to audit.


set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOOSE="$SCRIPT_DIR/../goose.py"

# Edit this URL
REPO_URL="https://github.com/psf/requests"

echo "🪿 Running Goose Finder on remote repository: $REPO_URL"
echo "⏳ PyDriller will clone the repo temporarily — this may take a moment..."
python "$GOOSE" "$REPO_URL"
