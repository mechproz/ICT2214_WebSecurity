import csv
import xml.etree.ElementTree as ET

# Path to the XML file
xml_file = '1334_200324_capturenolocation.xml'


# Parse XML
tree = ET.parse(xml_file)
root = tree.getroot()

# Extract URLs and count occurrences
url_counts = {}
for url in root.findall('.//url'):
    url_text = url.text
    if url_text in url_counts:
        url_counts[url_text] += 1
    else:
        url_counts[url_text] = 1

# Write URLs and counts to CSV
csv_file = 'urls.csv'
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['URL', 'Count'])

    for url, count in url_counts.items():
        writer.writerow([url, count])

print("URLs extracted and their counts saved to", csv_file)