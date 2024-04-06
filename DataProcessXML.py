from bs4 import BeautifulSoup
import pandas as pd


# Read text data from file
with open('1334_200324_capturenolocation.xml', 'r') as file:
    text_data = file.read()

# Parse the XML content
soup = BeautifulSoup(text_data, 'xml')

# Initialize lists to store extracted data
matched_count = []
matched_texts = []
host_ips = []
urls = []
hosts = []
times = []
response_texts = []
request_texts = []

# Define the magic word for searching in text
magic_word = 'carrier'

# Find all items (assuming each item contains the fields we're interested in)
for item in soup.find_all('item'):
    # Attempt to find the magic word within each item
    if magic_word.lower() in item.get_text().lower():
        # Extract fields
        time = item.time.get_text() if item.find('time') else 'N/A'
        url = item.url.get_text() if item.find('url') else 'N/A'
        host = item.host.get_text() if item.find('host') else 'N/A'
        # For demonstration, assuming host IP is an attribute of the host tag
        host_ip = item.host['ip'] if item.find('host') and 'ip' in item.host.attrs else 'N/A'
        
        # Count instances of magic word
        count = item.get_text().lower().count(magic_word.lower())
        
        # Append to lists
        times.append(time)
        urls.append(url)
        hosts.append(host)
        host_ips.append(host_ip)
        matched_count.append(count)
        matched_texts.append(magic_word)  # Assuming we're just marking the presence of the magic word
        
        # Response text extraction would depend on the structure, showing a generic approach
        response_text = item.response.get_text() if item.find('response') else 'N/A'
        response_texts.append(response_text)

         # Response text extraction would depend on the structure, showing a generic approach
        request_text = item.request.get_text() if item.find('request') else 'N/A'
        request_texts.append(request_text)
# Convert extracted data into a pandas DataFrame
df = pd.DataFrame({
    'Time': times,
    'URL': urls,
    'Host': hosts,
    'Host IP': host_ips,
    'Matched String Count': matched_count,
    'Matched Texts': matched_texts,
    'Response Text': response_texts,
    'Request Text': request_texts
})


# Truncate cells in DataFrame to 5000 characters max
for col in df.columns:
    if df[col].dtype == 'object':  # Check if the column is of type 'object', which are usually strings
        df[col] = df[col].str[:5000]  # Truncate to 5000 characters

# Get the number of rows in the DataFrame
num_rows = len(df)
print(f"The DataFrame contains {num_rows} rows.")

# Export the DataFrame to a CSV file
csv_file_path = 'carrier.csv'
df.to_csv(csv_file_path, index=False)

csv_file_path
