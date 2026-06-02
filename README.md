# PyDep

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) [![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/infinition)

![IMG_0847](https://github.com/infinition/PyDep/assets/37984399/0663c495-29c1-417b-92fe-175e79a0efe0)

PyDep analyzes and visualizes dependencies within a Python codebase. It recursively scans a directory for Python files, extracts imports and external file interactions (such as JSON and CSV read/write operations), and maps them in an interactive dependency graph.

![PyDep Dependency Graph Example](https://github.com/infinition/PyDep/assets/37984399/46574c69-b0f9-4204-b43e-b9c6e57ee367)

## Features

- **Recursive Analysis**: Scans directories for `.py` source files, with support for ignoring custom paths (e.g. tests, build artifacts).
- **Dependency Detection**: Extracts import statements as well as data file interactions (CSV and JSON files).
- **Interactive Graphing**: Uses Plotly and NetworkX to generate a zoomable, interactive network graph in the browser.
- **Custom Layout**: Optimizes node spacing for clarity in large codebases.

## Installation

Install dependencies using pip:
```bash
pip install networkx plotly numpy
```

Clone the repository:
```bash
git clone https://github.com/infinition/PyDep.git
cd PyDep
```

## Usage

Run the script:
```bash
python PyDep.py
```

Provide the paths when prompted:
1. Enter the target project directory.
2. Choose whether to exclude specific subdirectories (e.g. `tests`, `.venv`).
3. The interactive visualization will open automatically in your default web browser.

### Example

Running the analysis:
```
Enter the path to the Python project directory: /home/user/projects
Do you want to ignore any directories? (Y/N): Y
Enter the directories to ignore, separated by commas: tests, docs
```

## Script Details

- `find_python_files(directory, ignore_dirs=None)`: Recursively locates Python source files while skipping ignored paths.
- `extract_imports(file_path)`: Parses a Python file to locate imports and file read/writes.
- `build_dependency_graph(directory, ignore_dirs)`: Compiles the list of dependencies into a mapping.
- `generate_graph(dependencies)`: Creates a NetworkX graph structure.
- `custom_layout(graph, iterations=500, k=0.5)`: Positions nodes using a custom force-directed spring layout.
- `draw_graph(graph)`: Builds and displays the interactive Plotly HTML chart.

## Star History

<a href="https://www.star-history.com/?repos=infinition%2FPyDep&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=infinition/PyDep&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=infinition/PyDep&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=infinition/PyDep&type=date&legend=top-left" />
 </picture>
</a>

## License

MIT. See [LICENSE](LICENSE).
