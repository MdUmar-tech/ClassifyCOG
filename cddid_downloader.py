import os
import wget

# Define the URLs for the files you want to download
cddid_tbl_ftp_url = "https://ftp.ncbi.nih.gov/pub/mmdb/cdd/cddid.tbl.gz"
cog_le_ftp_url = "https://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/Cog_LE.tar.gz"
cog_fun_ftp_url = "https://ftp.ncbi.nih.gov/pub/COG/COG2020/data/fun-20.tab"
cog_def_ftp_url = "https://ftp.ncbi.nih.gov/pub/COG/COG2020/data/cog-20.def.tab"

# Define the folder where you want to save the downloaded files
data_folder = os.getcwd() + '/data'

# Create the data folder if it doesn't exist
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Download the files
cddid_tbl_file = wget.download(cddid_tbl_ftp_url, data_folder)
cog_le_file = wget.download(cog_le_ftp_url, data_folder)
cog_fun_file = wget.download(cog_fun_ftp_url, data_folder)
cog_def_file = wget.download(cog_def_ftp_url, data_folder)

# Print the paths of the downloaded files
print("Downloaded files:")
print(cddid_tbl_file)
print(cog_le_file)
print(cog_fun_file)
print(cog_def_file)
