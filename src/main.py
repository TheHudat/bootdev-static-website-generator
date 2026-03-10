import os
import shutil

from copystatic import copy_dir_content
from generate_page import generate_page_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
dir_path_blog = dir_path_content + "/blog"
template_path = "./template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print("Copying static files to public directory...")
    copy_dir_content(dir_path_static, dir_path_public)

    print("Generating website...")
    generate_page_recursive(
        dir_path_content, 
        template_path, 
        dir_path_public,
    )

main()