from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid Markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        extracted_text_value = extract_markdown_images(old_node.text)
        if extracted_text_value == []:
            new_nodes.append(old_node)
            continue

        for tup in extracted_text_value:
            image_markdown = f'![{tup[0]}]({tup[1]})'
            split_result = old_node.text.split(image_markdown, 1)
            if split_result[0] != '':
                new_nodes.append(TextNode(split_result[0], text_type_text))
            new_nodes.append(TextNode(tup[0], text_type_image, tup[1]))
            old_node.text = split_result[1]

        if old_node.text != '':
            new_nodes.append(TextNode(old_node.text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        extracted_text_value = extract_markdown_links(old_node.text)
        if extracted_text_value == []:
            new_nodes.append(old_node)
            continue

        for tup in extracted_text_value:
            link_markdown = f'[{tup[0]}]({tup[1]})'
            split_result = old_node.text.split(link_markdown, 1)
            if split_result[0] != '':
                new_nodes.append(TextNode(split_result[0], text_type_text))

            new_nodes.append(TextNode(tup[0], text_type_link, tup[1]))
            old_node.text = split_result[1]

        if old_node.text != '':
            new_nodes.append(TextNode(old_node.text, text_type_text))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, '**', text_type_bold)
    nodes = split_nodes_delimiter(nodes, '*', text_type_italic)
    nodes = split_nodes_delimiter(nodes, '`', text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
