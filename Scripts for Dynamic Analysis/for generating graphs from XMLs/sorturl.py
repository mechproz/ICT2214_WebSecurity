import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import urlparse

def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def combine_urls_by_domain(urls):
    combined_urls = {}
    for url, count in urls.items():
        domain = extract_domain(url)
        if domain in combined_urls:
            combined_urls[domain] += count
        else:
            combined_urls[domain] = count
    return combined_urls

def main():
    # Read the CSV file into a DataFrame
    df = pd.read_csv('urls.csv')

    # Group URLs by domain
    combined_urls = combine_urls_by_domain(dict(zip(df['URL'], df['Count'])))

    # Create a new DataFrame from combined URLs
    combined_df = pd.DataFrame({'Domain': list(combined_urls.keys()), 'Count': list(combined_urls.values())})

    # Sort DataFrame by Count in descending order
    combined_df = combined_df.sort_values(by='Count', ascending=True)

    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv('combined_urls_by_domain.csv', index=False)


    # Plotting
    plt.figure(figsize=(10, 6))
    plt.barh(combined_df['Domain'], combined_df['Count'], color='skyblue')
    plt.xlabel('Count')
    plt.ylabel('Domain')
    plt.title('URL Counts by Domain')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
