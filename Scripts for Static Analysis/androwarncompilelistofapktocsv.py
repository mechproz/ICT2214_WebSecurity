import csv
import os
import sys
sys.path.append('C:/Users/JiaJin/androwarn')  # Adjust based on your folder path, required to pull github's androwarn directory
from androguard.misc import AnalyzeAPK
from warn.analysis.analysis import perform_analysis

# Configuration
apk_directory = 'C:/Users/JiaJin/remaining/samsung/remainingfiles/4'        #please put this according to your file directory base on the list of apk files you want to analyze 
output_csv_file = 'C:/Users/JiaJin/remaining/samsung/samsung_full_analysis_results_4_test.csv' #put output csv file to slowly analyze and see what data to visualize and narrow down
MAX_CELL_LENGTH = 5000  #certain header rows have more than maximum character found from androwarn, and csv cannot store more 32,767 characters per cell, to quicken the process of analyzing due to many apk files

def truncate_data(data, max_length=MAX_CELL_LENGTH):
    """Truncate data if it exceeds max_length, appending '...' to indicate truncation."""
    return data[:max_length - 3] + '...' if len(data) > max_length else data

def analyze_apk(apk_path):
    """Analyze a single APK and return its analysis results."""
    print(f"Analyzing {apk_path}...")
    a, d, x = AnalyzeAPK(apk_path)
    analysis_results = perform_analysis(apk_path, a, d, x, False)

    # Initialize row data with file name
    row_data = {'file_name': os.path.basename(apk_path)}

    # Process analysis results and permissions together
    for category in analysis_results:
        if 'androidmanifest.xml' in category:
            for item in category['androidmanifest.xml']:
                if item[0] == 'permissions':
                    row_data['permissions'] = truncate_data("; ".join(item[1]))
        elif 'analysis_results' in category:
            for item in category['analysis_results']:
                row_data[item[0]] = truncate_data("; ".join(item[1])) if item[1] else "Not Found"
    
    print(f"Analysis complete for {os.path.basename(apk_path)}. Details captured.")
    return row_data

def main():
    # Prepare for collecting all unique headings
    all_headings = {'file_name', 'permissions'}

    # Initialize a list to collect all row data
    all_row_data = []

    # Process each APK file
    for apk_file in os.listdir(apk_directory):
        if apk_file.endswith(".apk"):
            apk_path = os.path.join(apk_directory, apk_file)
            row_data = analyze_apk(apk_path)
            all_row_data.append(row_data)
            # Update headings with keys from this APK's row data
            all_headings.update(row_data.keys())

    # Convert set to list and sort to maintain consistency, except 'file_name' at start
    all_headings = sorted(all_headings - {'file_name', 'permissions'})
    all_headings = ['file_name', 'permissions'] + all_headings

    # Write to CSV
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=all_headings)
        writer.writeheader()
        writer.writerows(all_row_data)

if __name__ == "__main__":
    main()
