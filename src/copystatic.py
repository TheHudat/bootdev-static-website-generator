import os
import shutil

from markdown_to_html import markdown_to_html_node
from block_markdown import extract_title

def copy_dir_content(target_dir, destination_dir):
    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)
    
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        destination_path = os.path.join(destination_dir, item)
        print(f" * {item_path} -> {destination_path}")
        if os.path.isfile(item_path):
            shutil.copy(item_path, destination_dir)
        else:
            copy_dir_content(item_path, destination_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, 'r') as file:
            md_content = file.read()
        print(f"File content {from_path} successfully saved to a variable...")
    except FileNotFoundError:
        print(f"Error: The file '{from_path}' was not found.")
    except Exception as e:
        print(f"An error occurred reading file {from_path}: {e}")

    try:
        with open(template_path, 'r') as file:
            template_content = file.read()
        print(f"File content {template_path} successfully saved to a variable...")
    except FileNotFoundError:
        print(f"Error: The file '{template_path}' was not found.")
    except Exception as e:
        print(f"An error occurred reading file {template_path}: {e}")

    html_node = markdown_to_html_node(md_content)
    page_title = extract_title(md_content)
    html_file = html_node.to_html()    

    template_content = template_content.replace("{{ Title }}", page_title)
    template_content = template_content.replace("{{ Content }}", html_file)

    dest_dirs = os.path.dirname(dest_path)
    if not os.path.exists(dest_dirs):
        os.makedirs(dest_dirs)
    
    try:
        with open(dest_path, 'w') as file:
            file.write(template_content)
    except Exception as e:
        print(f"An error occurred writing html file: {e}")
    
    print("Page generation complete...")