import argparse
from rdflib import Graph
import networkx as nx
import matplotlib.pyplot as plt
import re

def clean_uri(uri):
    """
    Clean and simplify URIs for better visualization
    """
    # Remove full URI prefix
    uri = re.sub(r'^<?(http://www\.wikidata\.org/entity/)?', '', str(uri))
    uri = re.sub(r'>?$', '', uri)
    # Replace underscores with spaces
    uri = uri.replace('_', ' ')
    # Remove problematic characters
    uri = re.sub(r'[^\w\s]', '', uri)
    return uri.strip()

def visualize_knowledge_graph(ttl_file, output_file=None):
    """
    Visualize a knowledge graph from a TTL file using NetworkX and Matplotlib.
    
    :param ttl_file: Path to the Turtle RDF file
    :param output_file: Optional path to save the visualization
    """
    # Load the RDF file
    g = Graph()
    
    # Read file contents and preprocess
    with open(ttl_file, 'r') as f:
        ttl_content = f.read()
    
    # Remove problematic lines with hex escape characters
    cleaned_content = re.sub(r'wd:20%', 'wd:twenty_percent', ttl_content)
    
    # Parse the cleaned content
    g.parse(data=cleaned_content, format="turtle")

    # Create a directed graph using NetworkX
    G = nx.DiGraph()

    # Add nodes and edges from the RDF graph
    for s, p, o in g:
        # Clean and simplify node names
        s_str = clean_uri(s)
        p_str = clean_uri(p)
        o_str = clean_uri(o)
        
        # Add nodes and edge
        G.add_edge(s_str, o_str, predicate=p_str)

    # Set up the plot
    plt.figure(figsize=(40, 40))
    
    # Use spring layout for node positioning
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    # Determine node colors based on type
    node_colors = []
    for node in G.nodes():
        if 'Person' in node:
            node_colors.append('lightblue')
        elif 'Date' in node or 'year' in node.lower():
            node_colors.append('lightgreen')
        elif 'GPE' in node or 'Location' in node:
            node_colors.append('salmon')
        elif 'ORG' in node:
            node_colors.append('lightpink')
        else:
            node_colors.append('lightgray')
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500, alpha=0.8)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=True, alpha=0.5)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=6, font_weight="bold")
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'predicate')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=4)
    
    plt.title("Knowledge Graph Visualization", fontsize=20)
    plt.axis('off')
    
    # Save or show the plot
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Graph visualization saved to {output_file}")
    else:
        plt.show()

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Visualize a Knowledge Graph from a TTL file')
    parser.add_argument('input_file', help='Path to the input TTL file')
    parser.add_argument('-o', '--output', help='Path to save the output visualization', default=None)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Generate output filename if not provided
    if not args.output:
        output_file = args.input_file.rsplit('.', 1)[0] + '_kg_visualization.png'
    else:
        output_file = args.output
    
    # Visualize the knowledge graph
    visualize_knowledge_graph(args.input_file, output_file)

if __name__ == "__main__":
    main()