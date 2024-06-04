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
