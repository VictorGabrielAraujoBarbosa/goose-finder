# Displays the Goose Finder help message and version information.
# Run this first to get familiar with the available options.

# Usage:
#   bash examples/show_help.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOOSE="$SCRIPT_DIR/../goose.py"

echo "════════════════════════════════════════"
echo "  goose.py --help"
echo "════════════════════════════════════════"
python "$GOOSE" --help

echo ""
echo "════════════════════════════════════════"
echo "  goose.py --version"
echo "════════════════════════════════════════"
python "$GOOSE" --version
