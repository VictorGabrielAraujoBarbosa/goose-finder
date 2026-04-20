# 🪿 Goose Finder

"Peace was never an option."

Goose Finder is a CLI tool designed to hunt for "Annoyances" (code smells) in your Python repositories by analyzing the Git history. It identifies developers who increase code complexity and size (**Gooses**) and those who clean up the mess (**Janitors**).

## 🚀 Features

- **Complexity Tracking**: Uses cyclomatic complexity to detect when code becomes harder to maintain.
- **Size Analysis**: Tracks Logical Lines of Code (LLOC) to identify bloat.
 
- **Visual Reports**: 
  - **Top Battlegrounds**: Identifies the most problematic files based on chaos density.
  - **Top Annoyances**: Highlights the worst commits that introduced complexity or size.
  - **Hall of Fame**: A leaderboard for the "Master Goose" (most chaos) and "Master Janitor" (most cleanup).

## 🛠️ Installation

You will need Python installed, along with the following dependencies:

```bash
pip install pydriller radon
```

## 📖 Usage

Run the tool by providing the path to a local repository or a Git URL:

```bash
python goose_finder.py <path_to_repo_or_url> [options]
```

### Arguments

| Argument | Description |
| :--- | :--- |
| `<path_to_repo_or_url>` | The local path or Git URL of the repository to investigate. |

### Options

| Option | Description |
| :--- | :--- |
| `-h, --help` | Shows help and a "honk" for you. |
| `-v, --version` | Shows the current version of the tool. |

## 📊 Example Output

The tool generates a summary report including:
- **Top 5 Battlegrounds**: Files with the highest chaos density.
- **Top 5 Annoyances**: The most disruptive commits.
- **Hall of Fame**: The reigning "Master Goose" and "Master Janitor".

---
*Developed to prove that peace was never an option in code review.*
