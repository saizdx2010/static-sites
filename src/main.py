import os
import shutil
from pathlib import Path


from block_converter import (markdown_to_html_node)


static_path = './static'
public_path = './public'
content_path = "./content"
template_path = "./template.html"


def main():
    copy_static(static_path, public_path)
    # generate_page(
    #     os.path.join(content_path, 'index.md'),
    #     template_path,
    #     os.path.join(public_path, 'index.html'),
    # )
    generate_page_recursive(
        os.path.join(content_path),
        template_path,
        os.path.join(public_path),
    )


def copy_static(src, dest):
    if os.path.exists(src):
        static_items = os.listdir(src)
        if os.path.exists(dest):
            shutil.rmtree(dest)
            os.mkdir(dest)
            for item in static_items:
                full_path = os.path.join(src, item)
                if os.path.isfile(full_path):
                    shutil.copy(full_path, dest)
                if os.path.isdir(full_path):
                    if os.path.exists(dest):
                        new_dir_path = os.path.join(dest, item)
                        os.mkdir(new_dir_path)
                        copy_static(full_path, new_dir_path)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)


def generate_page_recursive(from_path, template_path, dest_path):
    list_of_content_dir = os.listdir(from_path)
    for item in list_of_content_dir:
        item_full_path = os.path.join(from_path, item)
        dest_full_path = os.path.join(dest_path, item)
        if os.path.isfile(item_full_path):
            dest_full_path = Path(dest_full_path).with_suffix(".html")
            generate_page(item_full_path, template_path, dest_full_path)
        else:
            generate_page_recursive(item_full_path, template_path, dest_full_path)


def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {
          dest_path} using {template_path}')

    with open(from_path, 'r') as from_file, open(template_path, 'r') as template_file:

        from_file = from_file.read()
        template_file = template_file.read()

        converted_from_file = markdown_to_html_node(from_file)

        from_file_html = converted_from_file.to_html()

        title = extract_title(from_file)

        converted_template_file = template_file.replace('{{ Title }}', title)

        converted_template_file = converted_template_file.replace(
            '{{ Content }}', from_file_html)

        dest_dir = os.path.dirname(dest_path)

        if os.path.exists(dest_dir):
            pass

        else:
            os.makedirs(dest_dir)

        with open(dest_path, 'w') as dest_file:
            dest_file.write(converted_template_file)


main()
