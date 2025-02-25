import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load data
faculty_df = pd.read_excel("SNA\Mini Proj\Faculty.xlsx")
citation_df = pd.read_excel("SNA\Mini Proj\Citation.xlsx")

# Get all faculty IDs
all_ids = set(faculty_df["Faculty_ID"])

# Create a directed graph
G = nx.DiGraph()

# Add nodes (all professors)
for _, row in faculty_df.iterrows():
    G.add_node(row["Faculty_ID"], name=row["Name"], affiliation=row["Affiliation"])

# Add edges (citations)
for _, row in citation_df.iterrows():
    if row["Source_Faculty_ID"] in all_ids:
        G.add_edge(row["Source_Faculty_ID"], row["Other_Faculty_Name"], weight=row["No_Citations"])

# Fix the issue: Only assign colors to valid faculty members
node_colors = []
for node in G.nodes():
    faculty_info = faculty_df[faculty_df["Faculty_ID"] == node]
    if not faculty_info.empty:
        affiliation = faculty_info["Affiliation"].values[0]
        node_colors.append("blue" if affiliation.startswith("NIT") else "red")
    else:
        node_colors.append("gray")  # Default color for unknown nodes

# Draw graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color="gray", node_size=2000, font_size=8)
plt.title("Combined Citation Network (IIT + NIT)")
plt.savefig("Combined Citation Network (IIT + NIT)")
plt.show()