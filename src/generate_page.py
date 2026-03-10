import os

from markdown_to_html import markdown_to_html_node
from block_markdown import extract_title

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and os.path.splitext(item_path)[1] == ".md":
            generate_page(item_path, template_path, os.path.join(dest_dir_path, "index.html"))
        elif os.path.isdir(item_path):
            generate_page_recursive(item_path, template_path, os.path.join(dest_dir_path, item))

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