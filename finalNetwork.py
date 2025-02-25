import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import time
from scholarly import scholarly

# Load faculty data
faculty_df = pd.read_excel("SNA/Mini-Proj/Faculty.xlsx")

# Initialize Graph
G = nx.DiGraph()

# Dictionary to store faculty affiliation
faculty_affiliation = {row["Faculty_ID"]: row["Affiliation"] for _, row in faculty_df.iterrows()}

# Process each faculty member
citation_data = []

for index, row in faculty_df.iterrows():
    faculty_id = row["Faculty_ID"]
    faculty_name = row["Name"]
    affiliation = row["Affiliation"]

    print(f"Fetching Google Scholar profile for: {faculty_name} ({affiliation})")

    try:
        # Search Google Scholar
        search_query = scholarly.search_author(f"{faculty_name} {affiliation}")
        author = next(search_query, None)

        if author:
            author = scholarly.fill(author)
            G.add_node(faculty_id, label=faculty_name, affiliation=affiliation)

            # Fetch top 5 collaborators from co-authors
            for coauthor in author.get("coauthors", [])[:5]:
                coauthor_name = coauthor["name"]

                # Check if co-author is in our faculty list
                match = faculty_df[faculty_df["Name"] == coauthor_name]
                if not match.empty:
                    coauthor_id = match.iloc[0]["Faculty_ID"]
                    G.add_edge(faculty_id, coauthor_id)  # Faculty to Faculty link
                else:
                    coauthor_id = coauthor_name
                    G.add_node(coauthor_id, label=coauthor_name, affiliation="Other")
                    G.add_edge(faculty_id, coauthor_id)  # Faculty to external author link

                # Store in citation data
                citation_data.append({
                    "Source_Faculty_ID": faculty_id,
                    "Target_Faculty_ID": coauthor_id,
                    "CoAuthor_Name": coauthor_name
                })

            time.sleep(3)  # To avoid getting blocked

    except Exception as e:
        print(f"Error fetching data for {faculty_name}: {e}")

# Save citation network to Excel
citation_df = pd.DataFrame(citation_data)
citation_df.to_excel("faculty_citation_network.xlsx", index=False)

# 1. Degree Centrality (Direct Connections)
degree_centrality = nx.degree_centrality(G)

# 2. Betweenness Centrality (Bridges Between Groups)
betweenness_centrality = nx.betweenness_centrality(G)

# 3. Closeness Centrality (Efficiency in Reaching Others)
closeness_centrality = nx.closeness_centrality(G)

# 4. Eigenvector Centrality (Influence Based on Neighbors)
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)

# 5. Graph Density (Overall Connectivity Level)
graph_density = nx.density(G)

# 6. Average Clustering Coefficient (Tendency to Form Clusters)
try:
    clustering_coefficient = nx.average_clustering(G.to_undirected())  # Convert to undirected for calculation
except:
    clustering_coefficient = "Not available (due to directed nature)"


# Store Measures in a DataFrame
centrality_measures = pd.DataFrame({
    "Faculty_ID": list(G.nodes()),
    "Degree Centrality": [degree_centrality.get(n, 0) for n in G.nodes()],
    "Betweenness Centrality": [betweenness_centrality.get(n, 0) for n in G.nodes()],
    "Closeness Centrality": [closeness_centrality.get(n, 0) for n in G.nodes()],
    "Eigenvector Centrality": [eigenvector_centrality.get(n, 0) for n in G.nodes()],
})

# Save to Excel
centrality_measures.to_excel("faculty_centrality_measures.xlsx", index=False)

# Print Overall Network Statistics
print("\n### Network Statistics ###\n\n")
print(f"Graph Density: {graph_density}")
print(f"Average Clustering Coefficient: {clustering_coefficient}\n")
print("Top 5 Influential Nodes (Degree Centrality):\n")
print(f"Degree Centrality: {degree_centrality}")


# Visualization
plt.figure(figsize=(10, 8))

# Set node colors
node_colors = []
for node in G.nodes():
    if node in faculty_affiliation:
        node_colors.append("red" if faculty_affiliation[node].startswith("IIT") else "blue")
    else:
        node_colors.append("gray")

# Draw graph
pos = nx.spring_layout(G, seed=42)  # Layout
nx.draw(G, pos, with_labels=True, node_size=500, node_color=node_colors, edge_color="black", font_size=8)
plt.savefig('Final Citation Network')
plt.show()