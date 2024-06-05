COG Classification Script

This script is designed to classify protein sequences based on Cluster of Orthologous Groups (COG) identifiers. It utilizes the results obtained from an RPSBLAST search against the COG database to assign COG categories to the input protein sequences.

RPSBLAST

RPSBLAST is a variant of the PSI-BLAST algorithm designed specifically for searching a protein sequence database with a protein profile. It is used in this script to search for matches against the COG database.

To use RPSBLAST, you need to have it installed on your system. You can install it manually or through Conda. Detailed instructions for installation can be found here.

To perform an RPSBLAST search, you can use a command similar to the following:


rpsblast -query protein.faa -db Cog_LE/cog -out rpsblast_output.out -evalue 0.01 -outfmt 6

This command searches the protein sequences in the file protein.faa against the COG database (Cog_LE/cog) and saves the results in rpsblast_output.out in tabular format (-outfmt 6) with an E-value threshold of 0.01.

Required Files: 

Before running the script, you need to download the necessary files from the NCBI FTP server:

#https://ftp.ncbi.nih.gov/pub/mmdb/cdd/

#https://www.ncbi.nlm.nih.gov/Structure/cdd/cdd.shtml

#https://www.ncbi.nlm.nih.gov/research/cog-project/

#https://ftp.ncbi.nlm.nih.gov/pub/COG/COG2020/data/

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

For any issues or questions, please feel free to contact arc.umar@gmail.com.


#  Note on COG Function Assignment  Issue #################################################

We identified an issue where certain COG IDs present in the cddid.tbl file are not found in the cog-20.def.tab file. This discrepancy can result in missing functional annotations when merging these datasets.


To address this, you can modify the ClassifyCOG.py script to retain all COG IDs from the top hits, even if they lack corresponding entries in cog-20.def.tab. Simply change the merge operation to a left join:

update code 
# Modify this line in ClassifyCOG.py (line 77-78):
merged_df = pd.merge(selected_top_hit_df, cog_def_df, on='COG')
# Replace with:
merged_df = pd.merge(selected_top_hit_df, cog_def_df, on='COG', how='left')

After this change, some entries in merged_df.csv may have empty 'Class' columns. If you encounter this, manually annotate missing COG functions using the cddid.tbl file:

Locate the COG ID in cddid.tbl.
Refer to the Description column in cddid.tbl for the functional annotation.
By following these steps, you ensure comprehensive functional annotations in your analysis, even for COG IDs missing from cog-20.def.tab.

Also all mising COG can also be track using missing_COG.py (missiing COG description in cog-20.def.tab, it use two file cddid.tbl and cog-20.def.tab)
