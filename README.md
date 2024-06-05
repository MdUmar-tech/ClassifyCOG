COG Classification Script
This script is designed to classify protein sequences based on Cluster of Orthologous Groups (COG) identifiers. It utilizes the results obtained from an RPSBLAST search against the COG database to assign COG categories to the input protein sequences.

RPSBLAST
RPSBLAST is a variant of the PSI-BLAST algorithm designed specifically for searching a protein sequence database with a protein profile. It is used in this script to search for matches against the COG database.

To use RPSBLAST, you need to have it installed on your system. You can install it manually or through Conda. Detailed instructions for installation can be found here.

To perform an RPSBLAST search, you can use a command similar to the following:


rpsblast -query protein.faa -db Cog_LE/cog -out rpsblast_output.out -evalue 0.01 -outfmt 6

This command searches the protein sequences in the file protein.faa against the COG database (Cog_LE/cog) and saves the results in rpsblast_output.out in tabular format (-outfmt 6) with an E-value threshold of 0.01.

Required Files
Before running the script, you need to download the necessary files from the NCBI FTP server:

cddid.tbl: Conserved Domain Database (CDD) identifier file.
Cog_LE.tar.gz: COG database files.
fun-20.tab: Functional category descriptions.
cog-20.def.tab: COG definitions.
rpsblast_output.out: RPSBLAST output file obtained by searching protein sequences against the COG database.
You can download these files from here.

Alternatively, you can use the cddid_downloader.py script provided in this repository to download the cddid.tbl file.

Usage
To classify protein sequences using this script, you can use the following command:


python ClassifyCOG.py -r rpsblast_output.out -c cddid.tbl -f fun-20.tab -d cog-20.def.tab -o results
Replace rpsblast_output.out, cddid.tbl, fun-20.tab, and cog-20.def.tab with the paths to the respective files downloaded earlier. The -o option specifies the directory where the results will be saved.

Note
This script relies on the results obtained from RPSBLAST against the COG database. Make sure to perform the RPSBLAST search before running the classification script.

For any issues or questions, please feel free to contact maintainer_name.



################################################### Note on COG Function Assignment ######################################################

Issue Description
We identified an issue where certain COG IDs present in the cddid.tbl file are not found in the cog-20.def.tab file. This discrepancy can result in missing functional annotations when merging these datasets.

Code Update
To address this issue, we have updated the ClassifyCOG.py script to ensure that all COG IDs from the top hits are retained in the merged DataFrame, even if they lack corresponding entries in the cog-20.def.tab file. This change is reflected in the assign_COG_function function.

Updated Code Snippet
In the ClassifyCOG.py script, the merge operation has been modified as follows:

python
Copy code
# Perform outer merge (left for all top hits, right for any matching COGs)
merged_df = pd.merge(selected_top_hit_df, cog_def_df, on='COG', how='left')
This change ensures that all top hits are included in the merged DataFrame (merged_df), with missing COG functions represented as NaN.

Handling Missing COG Functions
After making this update, you may notice that the merged_df.csv file contains empty 'Class' columns for some entries. If you encounter this situation and need to assign functions to these COG IDs, you can trace the same COG IDs in the cddid.tbl file.

Steps to Trace Missing COG Functions
Open the cddid.tbl file and locate the COG ID of interest.
Note the corresponding gene or functional description provided in the cddid.tbl file.
Use this information to manually update or annotate the missing COG function in your analysis.
Example
If you find an entry in merged_df.csv with an empty 'Class' column:

Locate the COG ID in the cddid.tbl file.
Refer to the Description column in cddid.tbl to find the relevant functional annotation.
By following these steps, you can ensure that all COG IDs have appropriate functional annotations, even if they were initially missing from the cog-20.def.tab file.


