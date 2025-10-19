import os
from markdown_blocks import markdown_to_html_node
from extract_title import extract_title



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

#   read markdown file at from_path and store it
    try:
        with open(from_path, 'r', encoding="utf-8") as file:
            from_read = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file '{from_path}' was not found.")     
    except Exception as e:
        raise ValueError(f"An error occurred while reading the file: {e}")

#   read template file at template_path and store it    
    try:
        with open(template_path, 'r', encoding="utf-8") as file:
            template_read = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file '{template_path}' was not found.")     
    except Exception as e:
        raise ValueError(f"An error occurred while reading the file: {e}")
    
#   convert markdown to html string with markdown_to_html_node and .to_html

    from_node = markdown_to_html_node(from_read)
    from_html = from_node.to_html()
    from_title = extract_title(from_read)

#   replace {{ Title }} and {{ Content }} placeholders in the template

    template_read = template_read.replace("{{ Title }}", from_title)
    template_read = template_read.replace("{{ Content }}", from_html)

#   write full html page to file at dest_path. create if don't exist

    dest = os.path.dirname(dest_path)
    if dest and not os.path.exists(dest):
        os.makedirs(dest, exist_ok=True)
    try:
        with open(dest_path, 'w', encoding="utf-8") as file:
            file.write(template_read)
    except IOError as e:
        print(f"Error writing HTML page to {dest_path}: {e}")
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
#   make list of whats in directory
    entries = os.listdir(dir_path_content)

#   iterate over list
    for entry in entries:

#   get full paths for content and destination
        full_path = os.path.join(dir_path_content, entry)
        dest = os.path.join(dest_dir_path, entry)

#   check if path is a file and if not call again on the new directory
        if not os.path.isfile(full_path):
            generate_pages_recursive(full_path, template_path, dest)

#   if check confirms its a file, generate the page
        else:
            generate_page(
                os.path.join(dir_path_content, "index.md"),
                template_path,
                os.path.join(dest_dir_path, "index.html")
                    )