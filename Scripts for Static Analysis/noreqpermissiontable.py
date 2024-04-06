import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

# Load the dataset
file_path = 'full_analysis_results.csv' #name according to the filepath of the androwarn analysis filepath csv 
data = pd.read_csv(file_path)

# Define headers to check for findings
headers_to_check = [
    'PIM_data_leakage', 'audio_video_eavesdropping', 'code_execution',
    'connection_interfaces_exfiltration', 'device_settings_harvesting',
    'location_lookup', 'suspicious_connection_establishment',
    'telephony_identifiers_leakage', 'telephony_services_abuse'
]

# Function to determine if permissions are empty and if there are findings in other headers
def has_findings_without_permissions(row):
    # Check if permissions are empty with the specific pattern
    if row['permissions'] == "Asked: []; Implied: []; Declared: []":
        # Check for findings in other headers
        for header in headers_to_check:
            if row[header] != 'Not Found':
                return True  # There are findings without permissions
    return False

# Apply the function to filter out rows where permissions are empty but other findings are present
filtered_data = data[data.apply(has_findings_without_permissions, axis=1)]

# Create a new dataframe to count findings for each APK file
apk_counts = filtered_data.groupby('file_name')[['PIM_data_leakage', 'device_settings_harvesting']].apply(lambda x: (x != 'Not Found').sum())

# Check if DataFrame is empty
if apk_counts.empty:
    print("No data to plot.")
else:
    # Create a figure and axis object
    fig, ax = plt.subplots(figsize=(15, 8))

    # Set axis position to center
    ax.set_position([0, 0, 1, 1])

    # Hide axes
    ax.axis('off')

    # Add table title header
    table_title = "Findings Count for Google Pixel"
    ax.text(0.4, 0.95, table_title, horizontalalignment='center', verticalalignment='center', fontsize=16, fontweight='bold', color='#3b5998')

    # Plot the table with specified cell alignment
    tbl = table(ax, apk_counts, loc='center', cellLoc='center')

    # Set the font size and cell colors
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1.5, 1.5)  # Increase the table scale

    # Center the table within the figure
    tbl.set_fontsize(12)
    tbl.scale(1.2, 1.2)  # Increase the table scale
    tbl.scale(1, 1.5)  # Adjust table scale vertically

    # Customize cell colors
    cell_colors = [['#f7f7f7'] * len(apk_counts.columns)] * len(apk_counts)
    tbl.auto_set_column_width(col=list(range(len(apk_counts.columns))))

    # Set cell alignment for the first two columns
    for i in range(len(apk_counts)):
        tbl.get_celld()[(i + 1, 0)].set_text_props(fontweight='bold', color='#3b5998')  # Row label properties
        tbl.get_celld()[(i + 1, 1)].set_text_props(fontweight='bold', color='#3b5998')  # Row label properties

    # Set column labels font weight
    tbl.get_celld()[(0, 0)].set_text_props(fontweight='bold')
    tbl.get_celld()[(0, 1)].set_text_props(fontweight='bold')

    # Add description below the table
    description_text = "1: Found\n0: Not Found"
    ax.text(0.4, 0.02, description_text, horizontalalignment='center', verticalalignment='center', fontsize=12, color='#3b5998')

    # Save the table as an image
    try:
        plt.savefig('table_image_google.png', bbox_inches='tight', pad_inches=0.05)
        print("Table image saved successfully.")
    except Exception as e:
        print(f"Error saving table image: {str(e)}")


