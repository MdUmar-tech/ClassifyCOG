import pandas as pd

# Load the cddid.tbl file
cddid_df = pd.read_csv('cddid.tbl', sep='\t', header=None, encoding='utf-8', encoding_errors='ignore')
cddid_df.columns = ['ID', 'COG', 'Gene', 'Description', 'Length']

# Print the full cddid DataFrame
print("Full cddid_df:")
print(cddid_df.head())

# Load the cog-20.def.tab file
cog_def_df = pd.read_csv('cog-20.def.tab', sep='\t', header=None, encoding='utf-8', encoding_errors='ignore')
cog_def_df.columns = ['COG', 'Function', 'Description', 'Gene', 'Pathway', 'Unknown', 'PDB']

# Extract the COG IDs that start with 'COG' from cddid_df
cddid_filtered = cddid_df[cddid_df['COG'].str.startswith('COG')]

# Extract COG IDs from both dataframes
cddid_cogs = set(cddid_filtered['COG'])
cog_def_cogs = set(cog_def_df['COG'])

# Find COG IDs in cddid.tbl that are not in cog-20.def.tab
missing_cogs = cddid_cogs - cog_def_cogs

# Filter cddid_df to show only rows with missing COGs
missing_cogs_df = cddid_df[cddid_df['COG'].isin(missing_cogs)]

# Print the DataFrame with missing COG IDs
print("\nRows in cddid_df with COG IDs not in cog-20.def.tab:")
print(missing_cogs_df)
