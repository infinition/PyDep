import os
import re
import networkx as nx
import plotly.graph_objects as go
import numpy as np

def find_python_files(directory, ignore_dirs=None):
    """Recursively find all Python files in a directory, excluding ignored directories."""
    python_files = []
    ignore_dirs = set(ignore_dirs) if ignore_dirs else set()
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in ignore_dirs]
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_imports(file_path):
    """Extract all imports and file interactions from a Python file."""
    imports = []
    csv_files = []
    json_files = []
    with open(file_path, 'r') as file:
        content = file.read()
        # Match different types of imports
        matches = re.findall(r'from\s+(\S+)\s+import\s+(\S+)', content)
        matches += re.findall(r'import\s+(\S+)', content)
        matches += re.findall(r'from\s+(\S+)\s+import\s+\(([^)]+)\)', content)
        matches += re.findall(r'from\s+(\S+)\s+import\s+([\w,\s]+)', content)
        
        for match in matches:
            if isinstance(match, tuple):
                imports.append(match)
            else:
                imports.append((match, ''))
        
        # Handle multiple imports from the same package
        imports_expanded = []
        for imp in imports:
            if ',' in imp[1]:
                parts = [part.strip() for part in imp[1].split(',')]
                for part in parts:
                    imports_expanded.append((imp[0], part))
            else:
                imports_expanded.append(imp)
        
        # Find CSV and JSON file interactions
        csv_matches = re.findall(r'[\'"]([\w/\\]+\.csv)[\'"]', content)
        json_matches = re.findall(r'[\'"]([\w/\\]+\.json)[\'"]', content)
        
        csv_files.extend(csv_matches)
        json_files.extend(json_matches)

    return imports_expanded, csv_files, json_files

def build_dependency_graph(directory, ignore_dirs):
    """Build a dependency graph from Python files in a directory."""
    python_files = find_python_files(directory, ignore_dirs)
    dependencies = {}

    for file_path in python_files:
        module_name = os.path.relpath(file_path, directory).replace(os.sep, '.').replace('.py', '')
        imports, csv_files, json_files = extract_imports(file_path)
        dependencies[module_name] = {
            'imports': [imp[0] for imp in imports if imp[0]],
            'csv_files': csv_files,
            'json_files': json_files
        }

    return dependencies

def generate_graph(dependencies):
    """Generate a NetworkX graph from dependencies."""
    graph = nx.DiGraph()

    for module, details in dependencies.items():
        graph.add_node(module, type='module')
        for dep in details['imports']:
            if dep in dependencies:
                graph.add_edge(module, dep, color='green', width=2)
        for csv_file in details['csv_files']:
            graph.add_node(csv_file, type='csv')
            graph.add_edge(module, csv_file, color='blue', width=1)
        for json_file in details['json_files']:
            graph.add_node(json_file, type='json')
            graph.add_edge(module, json_file, color='blue', width=1)

    return graph

def custom_layout(graph, iterations=500, k=0.5):
    pos = nx.spring_layout(graph, iterations=iterations, k=k)
    nodes = list(graph.nodes())
    sizes = np.array([10 + 10 * graph.degree(node) for node in nodes])
    min_dist = sizes / 2.0
    for _ in range(iterations):
        for i, n1 in enumerate(nodes):
            for j, n2 in enumerate(nodes):
                if i >= j:
                    continue
                dist = np.linalg.norm(pos[n1] - pos[n2])
                if dist < min_dist[i] + min_dist[j]:
                    direction = pos[n1] - pos[n2]
                    direction /= np.linalg.norm(direction)
                    displacement = (min_dist[i] + min_dist[j] - dist) / 2
                    pos[n1] += displacement * direction
                    pos[n2] -= displacement * direction
    return pos

def draw_graph(graph):
    """Draw the graph using Plotly for interactive visualization."""
    pos = custom_layout(graph, k=0.5, iterations=200)  # Adjusted spring_layout parameters
    edge_traces = []

    for edge in graph.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace = go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=edge[2]['width'], color=edge[2]['color']),
            hoverinfo='none',
            mode='lines')
        edge_traces.append(edge_trace)

    node_x = []
    node_y = []
    node_size = []
    node_color = []
    node_text = []

    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        # The size of the node is proportional to the number of dependencies (degree)
        node_size.append(10 + 10 * graph.degree(node))
        # Color nodes based on their type
        node_attr = graph.nodes[node]
        if node_attr['type'] == 'module':
            node_color.append('skyblue')
        elif node_attr['type'] == 'csv':
            node_color.append('green')
        elif node_attr['type'] == 'json':
            node_color.append('orange')
        else:
            node_color.append('grey')  # Default color for any other type

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=node_size,
            color=node_color,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    fig = go.Figure(data=edge_traces + [node_trace],
                    layout=go.Layout(
                        title='Python Project Dependencies',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Python project dependency graph",
                            showarrow=False,
                            xref="paper", yref="paper"
                        )],
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False),
                        dragmode='pan',  # Allows dragging with the middle mouse button
                        height=800  # Set a height for the figure
                    )
                    )
    fig.show()

def main():
    project_directory = os.path.abspath(input("Enter the path to the Python project directory: "))
    ignore_option = input("Do you want to ignore any directories? (Y/N): ").strip().upper()
    ignore_dirs = []
    if ignore_option == 'Y':
        ignore_dirs = input("Enter the directories to ignore, separated by commas: ").strip().split(',')

    ignore_dirs = [os.path.abspath(os.path.join(project_directory, d.strip())) for d in ignore_dirs]
    dependencies = build_dependency_graph(project_directory, ignore_dirs)
    graph = generate_graph(dependencies)
    draw_graph(graph)
    print("Dependency graph generated and displayed.")

if __name__ == '__main__':
    main()

# to add the .py extension to the files in the graph, add the following line to the node_text list comprehension:
# node_text.append(node + '.py')
