import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load data
faculty_df = pd.read_excel("SNA\Mini Proj\Faculty.xlsx")
citation_df = pd.read_excel("SNA\Mini Proj\Citation.xlsx")

# Filter for IIT professors
iit_faculty = faculty_df[faculty_df["Affiliation"].str.contains("IIT", na=False)]
iit_ids = set(iit_faculty["Faculty_ID"])

# Create a directed graph
G = nx.DiGraph()

# Add nodes (professors)
for _, row in iit_faculty.iterrows():
    G.add_node(row["Faculty_ID"], name=row["Name"])

# Add edges (citations)
for _, row in citation_df.iterrows():
    if row["Source_Faculty_ID"] in iit_ids:
        G.add_edge(row["Source_Faculty_ID"], row["Other_Faculty_Name"], weight=row["No_Citations"])

# Draw graph
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="lightcoral", edge_color="gray", node_size=2000, font_size=8)
plt.title("Citation Network (IIT Professors)")
plt.savefig("Citation Network (IIT Professors)")
plt.show()