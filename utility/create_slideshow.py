#!/usr/bin/env python3

import os
import argparse
import xml.etree.ElementTree as ET
import random

def create_gnome_wallpaper_xml(directory, output_filename, static_duration, transition_duration):
    """
    Creates an XML file for a Gnome dynamic wallpaper from image files in a directory, in a random order.
    """
    
    if not os.path.isdir(directory):
        print(f"Error: Directory not found at {directory}")
        return

    supported_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.svg')
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(supported_extensions)]

    if not files:
        print(f"No supported image files found in {directory}")
        return

    # Randomize the list of files
    random.shuffle(files)

    root = ET.Element("background")

    for i in range(len(files)):
        current_file = files[i]
        next_file = files[(i + 1) % len(files)]

        static = ET.SubElement(root, "static")
        ET.SubElement(static, "duration").text = str(static_duration)
        ET.SubElement(static, "file").text = current_file

        transition = ET.SubElement(root, "transition")
        ET.SubElement(transition, "duration").text = str(transition_duration)
        ET.SubElement(transition, "from").text = current_file
        ET.SubElement(transition, "to").text = next_file

    output_file = os.path.join(directory, output_filename)
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Successfully created XML file: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Gnome dynamic wallpaper XML file.")
    parser.add_argument("directory", help="The path to the directory containing wallpaper images.")
    parser.add_argument("-o", "--output", dest="output_filename", default="slideshow.xml",
                        help="The name of the output XML file. (default: slideshow.xml)")
    parser.add_argument("-s", "--static", dest="static_duration", type=float, default=720.0,
                        help="The duration in seconds each image is displayed. (default: 720)")
    parser.add_argument("-t", "--transition", dest="transition_duration", type=float, default=4.0,
                        help="The duration in seconds for the transition between images. (default: 4)")
    
    args = parser.parse_args()
    
    create_gnome_wallpaper_xml(args.directory, args.output_filename, args.static_duration, args.transition_duration)