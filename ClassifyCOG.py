import argparse
import os  # Added for directory creation

import pandas as pd

def parse_rps_blast_output(filepath):
    """
    Extract top hit blast results (no duplicated query info).
    """
    df = pd.read_csv(filepath, sep="\t", header=None)
    df.columns = ["qaccver", "saccver", "pident", "length", "mismatch", "gapopen", 
                  "qstart", "qend", "sstart", "send", "evalue", "bitscore"]
    return df.drop_duplicates(subset=['qaccver'], keep='first')

def read_cddid_file(filepath):
    """
    Extracts COG IDs and descriptions from a cddid.tbl file.
    """
    cog_description_dict = {}
    with open(filepath, "r") as file:
        for line in file:
            columns = line.strip().split("\t")
            if columns[1].startswith("COG"):
                cog_description_dict[columns[0]] = columns[1]
    return cog_description_dict

def cddid_to_COG(top_hit_df, cog_description_dict):
    """
    Updates the 'saccver' column in a DataFrame with COG IDs from a dictionary.

    Args:
        top_hit_df (pd.DataFrame): DataFrame containing 'saccver' column.
        cog_description_dict (dict): Dictionary mapping match numbers to COG IDs.

    Returns:
        pd.DataFrame: DataFrame with 'saccver' column updated with COG IDs.
    """
    # Create a copy of the DataFrame to avoid modifying the original DataFrame
    updated_df = top_hit_df.copy()

    # Iterate through the DataFrame and replace values in the 'saccver' column
    # Iterate through the DataFrame and add values to the 'COG' column
    for index, row in updated_df.iterrows():
        # Extract the match number from the 'saccver' column value
        match_number = row['saccver'].split(':')[1]
        # Check if the match number exists in cog_description_dict
        if match_number in cog_description_dict:
            # Add the corresponding COG ID to the new 'COG' column
            updated_df.at[index, 'COG'] = cog_description_dict[match_number]

    return updated_df

def assign_COG_function(cog_def_filepath, top_hit_df, cddid_table):
    """
    Reads a COG definition file, merges it with a top hit DataFrame,
    and returns the selected class column and the merged DataFrame.

    Args:
        cog_def_filepath (str): Path to the COG definition file (tab-delimited, no header).
        top_hit_df (pd.DataFrame): DataFrame containing qaccver and saccver columns.
        cddid_table (dict): Dictionary mapping match numbers to COG IDs.

    Returns:
        tuple: (pd.Series, pd.DataFrame)
            - selected_class (pd.Series): Series containing the 'Class' column from the merged DataFrame.
            - merged_df (pd.DataFrame): The merged DataFrame containing relevant columns.
    """

    # Read the COG definition file efficiently
    cog_def_df = pd.read_csv(cog_def_filepath, sep="\t", header=None, encoding='ISO-8859-1', 
                             names=["COG", "Class", "Gene_function", "Gene", "pathway", "unknown", "type"])

    # Select relevant columns for clarity and efficiency
    selected_top_hit_df = top_hit_df#[['qaccver', 'saccver', 'COG']]
    #selected_cog_def_df = cog_def_df[['COG', 'Class']]  # Only 'Class' required from COG definitions

    # Perform outer merge (left for all top hits, right for any matching COGs)
    merged_df = pd.merge(selected_top_hit_df, cog_def_df, on='COG')

    # Extract the selected class for convenience
    selected_class = merged_df['Class']

    return selected_class, merged_df


def classify(selected_class, fun_filepath):
    """
    Classifies functional descriptions based on COG annotations.

    Args:
        selected_class (pd.Series): Series containing selected class from merged DataFrame.
        fun_filepath (str): Path to the fun-20.tab file.

    Returns:
        pd.DataFrame: DataFrame with classified functional descriptions.
    """
    # Read the fun-20.tab file into a DataFrame
    fun_df = pd.read_csv(fun_filepath, sep="\t", header=None, names=["Class", "Functional_Category_Code", "Functional_Description"])
    fun_df = fun_df[["Class", "Functional_Description"]]
    
    #Splits characters of selected_class data frame in a list and inserts them into new rows in a DataFrame, for example KL which is K and L
    #so get each single class
    result = []
    for item in selected_class:
        if isinstance(item, str) and len(item) > 1:
            for char in item:
                result.append(char)
        else:
            result.append(item)

    # Convert the result into a DataFrame
    df_split_selected_class = pd.DataFrame({'col1': result})
    
    # Merge df_split_selected_class with fun_df based on 'Class'
    merged_df = pd.merge(df_split_selected_class, fun_df, left_on='col1', right_on='Class', how='outer')

    # Group by 'Class' and 'Functional_Description', count occurrences, rename, and reset index
    grouped_df = merged_df.groupby(['Class', 'Functional_Description']).size().to_frame(name='frequency').reset_index()

    return grouped_df

def main(args):
    # Step 1: Read the BLAST output file
    top_hit_df = parse_rps_blast_output(args.blast_output_filepath)
    
    # Step 2: Read the COG description file
    cddid_table = read_cddid_file(args.cddid_filepath)
    
    cog_def_filepath = args.cog_def_filepath
    
    fun_filepath = args.fun_filepath  # Corrected variable name

    # Step 3: Update COG IDs in top hit DataFrame
    updated_top_hit_df = cddid_to_COG(top_hit_df, cddid_table)

    # Step 4: Assign COG function to top hit DataFrame
    selected_class, merged_df = assign_COG_function(cog_def_filepath, updated_top_hit_df, cddid_table)

    merged_df = merged_df[['qaccver', 'saccver', 'pident', 'evalue', 'COG', 'Class', 'Gene_function', 'Gene']]
    #print(merged_df)

    # Compute COG statistics
    cog_stats = merged_df[['COG', 'Gene_function']].value_counts().reset_index(name='frequency')
    print(cog_stats)
    
    # Create results directory if it doesn't exist
    os.makedirs(args.results_directory, exist_ok=True)

    # Save COG 
    merged_df.to_csv(os.path.join(args.results_directory, "classifier_result.tsv"), sep='\t', index=False)
    
    # Save COG statistics
    cog_stats.to_csv(os.path.join(args.results_directory, "cog_stats.txt"), sep='\t', index=False)
    
    grouped_df = classify(selected_class, fun_filepath)
    Total = grouped_df['frequency'].sum()
    print(Total)
    print(grouped_df)
    # Save functional category statistics
    grouped_df.to_csv(os.path.join(args.results_directory, "func_stats.txt"), sep='\t', index=False)
    
    # Calculate overall assignment statistics
    total_query_proteins = len(merged_df)  # Total query proteins categorized into COGs
    Total_COG_cdd_in_database = len(cddid_table)
    total_cogs_cdd_used = top_hit_df['saccver'].nunique()  # Total COGs used for the query proteins
    total_assigned_functional_categories = grouped_df['frequency'].sum()  # Total number of assigned functional categories
    total_functional_categories = len(grouped_df)  # Total functional categories used for the query proteins

    # Print overall assignment statistics
    print("Overall assignment statistics:")
    print(f"~ Total query proteins categorized into COGs: {total_query_proteins}")
    print(f"~ Total COGs used for the query proteins [of {Total_COG_cdd_in_database} overall]: {total_cogs_cdd_used}")
    print(f"~ Total number of assigned functional categories: {total_assigned_functional_categories}")
    print(f"~ Total functional categories used for the query proteins [of {total_functional_categories} overall]: {total_functional_categories}")
    print(f"Classification completed. Results saved to {args.results_directory}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="COG Classification Script")
    parser.add_argument("-r", "--blast_output_filepath", type=str, required=True, help="Path to the rpsblast result file")
    parser.add_argument("-c", "--cddid_filepath", type=str, required=True, help="Path to the cddid.tbl file")
    parser.add_argument("-f", "--fun_filepath", type=str, required=True, help="Path to the fun-20.tab file")
    parser.add_argument("-d", "--cog_def_filepath", type=str, required=True, help="Path to the cog-20.def.tab file")
    parser.add_argument("-o", "--results_directory", type=str, required=True, help="Directory containing result files")
    
    args = parser.parse_args()
    main(args)

#usage 
#python ClassifyCOG.py -r path_to_blast_output -c path_to_/cddid.tbl -f path_to_/fun-20.tab -d path_to_/cog-20.def.tab -o path_to_results_directory
