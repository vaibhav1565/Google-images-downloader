import re


def decode_url(url):
    """Decode escape sequences in a URL."""
    # Replace Unicode escape sequences (e.g., \u003d -> =)
    url = re.sub(r'\\u([0-9a-fA-F]{4})',
                 lambda match: chr(int(match.group(1), 16)), url)
    # Replace other common escape sequences (e.g., \t, \n, etc.)
    url = url.replace(r'\t', '\t').replace(r'\n', '\n').replace(r'\r', '\r')
    url = url.replace(r'\"', '"').replace(r"\'", "'").replace(r'\\', '\\')
    return url


def extract_and_decode_urls(text):
    """Extract and decode all URLs in a given text."""
    # Regular expression to find URLs
    # Find all matches in the input text
    url_pattern = r'(https?://[^\s",]+?\.(?:jpg|jpeg|png|gif|bmp|webp|tiff))'
    urls = re.findall(url_pattern, text)
    # Decode escape sequences in each URL
    decoded_urls = [decode_url(url) for url in urls if not url.startswith('https://ssl.gstatic.com')]
    
    return decoded_urls


# Read the input text from a file
input_text = open('f.txt').read()
print("Done reading file")

# Extract and decode URLs
urls = extract_and_decode_urls(input_text)
# Print the result
print(urls)