import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define categories dictionary
categories = {
    'INFORMATION STORAGE AND PROCESSING': ['J', 'A', 'K', 'L', 'B'],
    'CELLULAR PROCESSES AND SIGNALING': ['D', 'Y', 'V', 'T', 'M', 'N', 'Z', 'W', 'U', 'O'],
    'METABOLISM': ['C', 'G', 'E', 'F', 'H', 'I', 'P', 'Q'],
    'POORLY CHARACTERIZED': ['R', 'S', 'X']
}

# Read the data from the file
MCCB_246 = pd.read_csv("results/func_stats.txt", header=None, delimiter="\t")
MCCB_246.drop(index=MCCB_246.index[0], axis=0, inplace=True)

# Rename the columns
MCCB_246.columns = ["FunctionClass", "Description", "Frequency"]

# Convert 'Frequency' column to numeric
MCCB_246["Frequency"] = pd.to_numeric(MCCB_246["Frequency"])

# Customize color palette
palette = sns.color_palette("husl", n_colors=len(MCCB_246["FunctionClass"].unique()))

# Plot the data with customized palette and width/dodge
plt.figure(figsize=(14, 8))
sns.barplot(data=MCCB_246, x="FunctionClass", y="Frequency", palette=palette)
plt.xlabel("COG categories")
plt.ylabel("Frequency")
plt.title("COG Function Classification")

# Create custom legend handles and labels with categories followed by subcategories
custom_legend_handles = []
custom_legend_labels = []
for category, subcategories in categories.items():
    # Add a custom legend handle and label for the current category
    custom_legend_handles.append(plt.Line2D([0], [0], color='gray', linestyle='-', linewidth=2))
    custom_legend_labels.append(category)
    
    # Add original legend handles and labels for subcategories of the current category
    for subcategory in subcategories:
        if subcategory in MCCB_246["FunctionClass"].values:
            index = MCCB_246[MCCB_246["FunctionClass"] == subcategory].index[0]
            label = f"{subcategory}: {MCCB_246.at[index, 'Description']}"
            custom_legend_handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=palette[index % len(palette)], markersize=10))
            custom_legend_labels.append(label)

# Create the custom legend with increased size
plt.legend(custom_legend_handles, custom_legend_labels, bbox_to_anchor=(1, 0.5), loc='center left', title="MMCC100 Function class", prop={'size': 11})  # Increased size here

# Adjust the layout
plt.tight_layout(pad=2)
plt.savefig("plot.png", dpi=300)

plt.show()
