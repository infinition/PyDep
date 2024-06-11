# PyDep

![IMG_0847](https://github.com/infinition/PyDep/assets/37984399/0663c495-29c1-417b-92fe-175e79a0efe0)


PyDep is a Python script designed to analyze and visualize the dependencies within a Python project. It recursively scans the specified directory for Python files, extracts import statements and file interactions (CSV and JSON), and generates an interactive dependency graph using NetworkX and Plotly.

![Capture d'écran 2024-06-10 153809](https://github.com/infinition/PyDep/assets/37984399/46574c69-b0f9-4204-b43e-b9c6e57ee367)

Features
Recursive Python File Search: Finds all Python files in a specified directory, with options to ignore certain subdirectories.
Dependency Extraction: Extracts import statements, CSV file interactions, and JSON file interactions from each Python file.
Interactive Visualization: Creates an interactive dependency graph using Plotly, displaying the relationships between modules, CSV files, and JSON files.
Customizable Layout: Applies a custom layout to the graph for better visualization of dependencies.
Installation
Ensure you have Python 3.x installed along with the required packages:


pip install networkx plotly numpy
Clone the repository or download the script directly:


git clone https://github.com/infinition/pydep.git
cd pydep
Usage
To run the script, follow these steps:

Navigate to the script directory:


cd path/to/pydep
Run the script:


python pydep.py
Provide the required input:
The script will prompt you to enter the path of the directory you wish to analyze and optionally any directories you want to ignore.

Example:


Enter the path to the Python project directory: /path/to/project
Do you want to ignore any directories? (Y/N): Y
Enter the directories to ignore, separated by commas: dir_to_ignore1, dir_to_ignore2
Output:
The script will generate and display an interactive dependency graph in your default web browser.

Example

# Run the script
python pydep.py

# Sample input prompts
Enter the path to the Python project directory: /home/user/projects
Do you want to ignore any directories? (Y/N): Y
Enter the directories to ignore, separated by commas: tests, docs

# Output
Dependency graph generated and displayed.
Script Details
find_python_files(directory, ignore_dirs=None)
This function recursively finds all Python files in a directory, excluding specified ignored directories.

Parameters:
directory (str): The root directory to explore.
ignore_dirs (list): List of directories to ignore.
Returns: A list of paths to Python files.
extract_imports(file_path)
This function extracts all import statements and file interactions (CSV and JSON) from a Python file.

Parameters: file_path (str): The path to the Python file.
Returns: A tuple containing lists of imports, CSV files, and JSON files.
build_dependency_graph(directory, ignore_dirs)
This function builds a dependency graph from Python files in a directory.

Parameters:
directory (str): The root directory to explore.
ignore_dirs (list): List of directories to ignore.
Returns: A dictionary representing the dependencies.
generate_graph(dependencies)
This function generates a NetworkX graph from dependencies.

Parameters: dependencies (dict): A dictionary of dependencies.
Returns: A NetworkX graph object.
custom_layout(graph, iterations=500, k=0.5)
This function applies a custom layout to the graph for better visualization.

Parameters:
graph (NetworkX graph): The graph to layout.
iterations (int): Number of iterations for the spring layout algorithm.
k (float): Optimal distance between nodes.
Returns: A dictionary of positions.
draw_graph(graph)
This function draws the graph using Plotly for interactive visualization.

Parameters: graph (NetworkX graph): The graph to draw.
Returns: None.
main()
The main function that orchestrates the workflow.

Parameters: None.
Returns: None.
License
This project is licensed under the MIT License. See the LICENSE file for details.
