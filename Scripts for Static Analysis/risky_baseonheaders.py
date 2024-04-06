import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'samsung_full_analysis_results_1.csv' #name according to the csv file path of your compile apk files analysis from androwarn 
data = pd.read_csv(file_path)

# Define the headers indicating potential privacy or security risks and their corresponding risk scores
risky_headers = {
    'PIM_data_leakage': 5,
    'audio_video_eavesdropping': 4,
    'code_execution': 4,
    'connection_interfaces_exfiltration': 3,
    'device_settings_harvesting': 3,
    'location_lookup': 2,
    'suspicious_connection_establishment': 2,
    'telephony_identifiers_leakage': 3,
    'telephony_services_abuse': 2
}

# Function to apply the risk score for found risks
def apply_risk_scores(row):
    risk_score = 0
    for header in risky_headers:
        if row[header] != 'Not Found':
            risk_score += risky_headers[header]
    return risk_score

# Calculate the risk score for each APK file
data['risk_score'] = data.apply(apply_risk_scores, axis=1)

# Filter APK files that have any findings related to risky activities
risky_apks = data[data['risk_score'] > 0]

# Sort APK files by risk score in descending order
risky_apks_sorted = risky_apks.sort_values(by='risk_score', ascending=False)

# Select the top N risky APK files to display
top_n = 10  # Choose the number of top APK files to display
top_risky_apks = risky_apks_sorted.head(top_n)

# Plotting the bar chart for risky APK files only
plt.figure(figsize=(10, 6))
# Ensure file names are strings
top_risky_apks['file_name'] = top_risky_apks['file_name'].astype(str)
# Plot the bar chart
bars = plt.barh(top_risky_apks['file_name'], top_risky_apks['risk_score'], color='red')
plt.xlabel('Risk Score')
plt.ylabel('APK File')
plt.title(f'Top {top_n} Riskiest APK Files')
plt.gca().invert_yaxis()  # Invert y-axis to display highest risk at the top
plt.grid(axis='x')  # Add gridlines for better readability

# Adjust left margin to make room for longer y-axis label
plt.subplots_adjust(left=0.4)

plt.show()
