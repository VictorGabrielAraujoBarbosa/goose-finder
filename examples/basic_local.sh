# The simplest way to use Goose Finder: analyze the git repository located
# in the current working directory.

# Usage:
#   cd /path/to/your/repo
#   bash examples/basic_local.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOOSE="$SCRIPT_DIR/../goose.py"

echo "🪿 Running Goose Finder on the current directory..."
python "$GOOSE" .
