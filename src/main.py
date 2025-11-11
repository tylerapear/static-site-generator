import os, shutil, sys

from pathlib import Path
from textnode import TextNode, TextType
from mdparsing import markdown_to_html_node

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    print("\n\033[33mDeleting public directory...\033[0m\n")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    deep_copy_directory(dir_path_static, dir_path_public)
    generate_all_pages_in_dir(basepath, dir_path_content, template_path, dir_path_public)
    
def deep_copy_directory(source_path, dest_path):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)
    for item in os.listdir(source_path):
        item_source_path = os.path.join(source_path, item)
        item_dest_path = os.path.join(dest_path, item)
        if os.path.isfile(item_source_path):
            shutil.copy(item_source_path, dest_path)
        else:
            deep_copy_directory(item_source_path, item_dest_path)
            
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[0] == "#" and line[1] != "#":
            return line[1:].strip()
    raise Exception("File does not contain a header line")

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"\n\033[33mGenerating page from {from_path} to {dest_path} using {template_path}\033[0m\n")
    from_content = ""
    with open(from_path) as file:
        from_content = file.read()
    template_content = ""
    with open(template_path) as file:
        template_content = file.read()
    html_text = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)
    template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_text).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    path = Path(dest_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(template_content)
    
def generate_all_pages_in_dir(basepath, from_path, template_path, dest_path):
    contents = os.listdir(from_path)
    for item in contents:
        item_from_path = os.path.join(from_path, item)
        item_dest_path = os.path.join(dest_path, item)
        if os.path.isfile(item_from_path):
            item_dest_path = Path(item_dest_path).with_suffix(".html")
            generate_page(basepath, item_from_path, template_path, item_dest_path)
        else:
            generate_all_pages_in_dir(basepath, item_from_path, template_path, item_dest_path)
        

if __name__ == "__main__":
    main()