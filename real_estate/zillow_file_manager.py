#!/home/bill/local_projects/.venv/local_projects/bin/python3

import os
import sys
import shutil
from bs4 import BeautifulSoup
import re

def extract_address(html_content):
    """
    Extracts the address text from a div with a class name containing "AddressWrapper".

    Args:
        html_content (str): The raw HTML content of the Zillow page.

    Returns:
        str: The extracted address text, or None if the element is not found.
    """
    try:
        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(html_content, 'lxml')

        # Use re.compile to find a class attribute that contains the substring "AddressWrapper"
        address_div = soup.find('div', class_=re.compile("AddressWrapper"))

        # Check if the element was found and return its text content
        if address_div:
            return address_div.get_text(strip=True)
        else:
            return None
    except Exception as e:
        print(f"An error occurred while parsing the address: {e}")
        return None


def sanitize_filename(address):
    """
    Strips illegal characters and replaces spaces with underscores
    to make a valid Linux filename.

    Args:
        address (str): The string to sanitize.

    Returns:
        str: The sanitized string.
    """
    if not address:
        return ""

    # Replace all non-breaking spaces (\xa0) and other whitespace with a single underscore.
    # This also handles standard spaces, tabs, and newlines.
    sanitized_address = re.sub(r'\s+', '_', address).strip('_')

    # Define a list of characters that are generally illegal in Linux filenames
    # include the comma as well
    illegal_chars = r'[,<>:"/\\|?*\'`]'
    # Remove all other illegal characters
    sanitized_address = re.sub(illegal_chars, '', sanitized_address)
    
    return sanitized_address


def rename_files_in_dir(directory):
    """
    Reads all files in a directory, extracts an address from the content,
    and renames the files with the sanitized address.

    Args:
        directory (str): The path to the directory containing the files.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory not found at {directory}")
        return

    print(f"Processing files in directory: {directory}")

    # Walk through the directory to find all files
    for root, _, files in os.walk(directory):
        for filename in files:
            full_path = os.path.join(root, filename)
            # Skip files that already have an extension (already processed)
            if has_extension(full_path):
                continue
            try:
                # Read the file content
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract and sanitize the address
                address = extract_address(content)
                sanitized_name = sanitize_filename(address)

                # Check if a valid address was found
                if sanitized_name:
                    new_filename = f"{sanitized_name}.zlw"
                    new_full_path = os.path.join(root, new_filename)
                    
                    # # Ensure the new filename doesn't already exist
                    # if os.path.exists(new_full_path):
                    #     print(f"Warning: File {new_filename} already exists. Skipping {filename}.")
                    #     continue

                    # Rename the file
                    os.rename(full_path, new_full_path)
                    print(f"Renamed '{filename}' to '{new_filename}'")
                else:
                    print(f"Could not find a valid address in '{filename}'. Skipping rename.")
            
            except UnicodeDecodeError:
                print(f"Skipping '{filename}' due to a UnicodeDecodeError. Please ensure file is UTF-8 encoded.")
            except Exception as e:
                print(f"An unexpected error occurred with file '{filename}': {e}")


def has_extension(filename):
    """
    Checks if a filename has an extension.
    """
    return os.path.splitext(filename)[1] != ''

def property_address_from_filename(filename):
    """
    Extracts the property address from a given filename by removing the extension
    and replacing underscores with spaces.

    Args:
        filename (str): The filename to process.

    Returns:
        str: The extracted property address.
    """
    # Remove the file extension
    base_name = os.path.splitext(os.path.basename(filename))[0]
    # Replace underscores with spaces
    address = base_name.replace('_', ' ')
    return address


def save_file_lines(lines, output_filename):
    """
    Saves a list of lines to a specified output file.

    Args:
        lines (list): List of strings to write to the file.
        output_filename (str): The name of the output file.
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')
        print(f"Saved output to {output_filename}")
    except IOError as e:
        print(f"Error writing to file {output_filename}: {e}")

        

if __name__ == "__main__":
    # If the user provides a directory, use it. 
    # Otherwise, use the page_scrapes under current directory.
    if len(sys.argv) > 1:
        dir_to_process = sys.argv[1]
    else:
        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dir_to_process = os.path.join(script_dir, 'page_scrapes')

    rename_files_in_dir(dir_to_process)
