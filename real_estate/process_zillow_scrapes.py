#!/usr/bin/env python3

import os
import parse_zillow_page as page
import zillow_file_manager as file_manager
import real_estate_config as config


scrapes_dir = config.scrapes_dir
images_dir = config.images_dir
output_folder = config.output_folder

def main():
    file_manager.rename_files_in_dir(scrapes_dir)
    page.format_scrape(scrapes_dir, output_folder)

    
if __name__ == "__main__":
    main()

