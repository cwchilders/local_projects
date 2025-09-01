#!/usr/bin/env python3

import parse_zillow_page as page
import zillow_file_manager as file_manager

scrapes_dir = '/home/bill/local_projects/real_estate/page_scrapes'
output_folder = '/home/bill/Personal/Real Estate/parsed_favorites'

def main():

    file_manager.rename_files_in_dir(scrapes_dir)
    page.format_scrape(scrapes_dir, output_folder)
    
if __name__ == "__main__":
    main()

