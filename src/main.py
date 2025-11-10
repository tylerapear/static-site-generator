import os, shutil

from pathlib import Path
from textnode import TextNode, TextType
from mdparsing import markdown_to_html_node

def main():
    deep_copy_directory("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    
    
def deep_copy_directory(source_path, dest_path):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)
    for item in os.listdir(source_path):
        if os.path.isfile(f"{source_path}/{item}"):
            shutil.copy(f"{source_path}/{item}", dest_path)
        else:
            deep_copy_directory(f"{source_path}/{item}", f"{dest_path}/{item}")
            
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[0] == "#" and line[1] != "#":
            return line[1:].strip()
    raise Exception("File does not contain a header line")

def generate_page(from_path, template_path, dest_path):
    print(f"\n\033[33mGenerating page from {from_path} to {dest_path} using {template_path}\033[0m\n")
    from_content = ""
    with open(from_path) as file:
        from_content = file.read()
    template_content = ""
    with open(template_path) as file:
        template_content = file.read()
    html_text = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)
    template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_text)
    path = Path(dest_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(template_content)
    
    
        

if __name__ == "__main__":
    main()