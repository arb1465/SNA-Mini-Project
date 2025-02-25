import pandas as pd
import time
from scholarly import scholarly

# Load faculty data
faculty_df = pd.read_excel("SNA\Mini Proj\Faculty.xlsx")

# Prepare list to store citation data
citation_data = []

# Iterate through faculty members
for index, row in faculty_df.iterrows():
    faculty_name = row["Name"]
    affiliation = row["Affiliation"]

    print(f"Fetching Google Scholar profile for: {faculty_name} ({affiliation})")

    try:
        # Search for faculty profile
        search_query = scholarly.search_author(f"{faculty_name} {affiliation}")
        author = next(search_query, None)  # Get first match
        if author is None:
            print(f"No profile found for {faculty_name}")
            continue

        # Fetch full profile details
        author = scholarly.fill(author)
        

        # Get the first co-author (if available)
        coauthor_name = author["coauthors"][0]["name"] if "coauthors" in author and author["coauthors"] else "No Co-Author Found"

        # Get publications
        for pub in author.get("publications", [])[:10]:  # Fetch top 10 publications
            title = pub["bib"].get("title", "Unknown Title")
            num_citations = pub.get("num_citations", 0)

            # Store in citation_data list
            citation_data.append({
                "Source_Faculty_ID": row["Faculty_ID"],
                "Source_Faculty_Name": author["name"],
                "Paper_Title": title,
                "Co_Author": coauthor_name,
                "No_Citations": num_citations
            })

        # Wait to avoid getting blocked by Google Scholar
        time.sleep(5)

    except Exception as e:
        print(f"Error fetching data for {faculty_name}: {e}")

# Convert to DataFrame
citation_df = pd.DataFrame(citation_data)

# Save to Excel
citation_df.to_excel("facultyCitations.xlsx", index=False)

print("Citation data has been saved to facultyCitations.xlsx")