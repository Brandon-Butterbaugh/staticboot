import re

from textnode import TextNode, TextType



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delimiters = {"**": TextType.BOLD,
                  "`": TextType.CODE,
                  "_": TextType.ITALIC
                  }
    if old_nodes is None:
        raise ValueError("invalid: No nodes given")
    if delimiter not in delimiters:
        raise ValueError("invalid Markdown syntax")
    if delimiters[delimiter] is not text_type:
        raise ValueError("invalid: delimiter and text_type do not match")
    
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes = []
        split_text = node.text.split(delimiter)
        if len(split_text)%2 == 0:
            raise ValueError("invalid markdown: formatted section not closed")
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i%2 == 0:
                split_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_text[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    if old_nodes is None:
        raise ValueError("invalid: No nodes given")
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        old_text = node.text
        image = extract_markdown_images(node.text)
        if len(image) == 0:
            new_nodes.append(node)
            continue
        for i in image:
            split_text = old_text.split(f"![{i[0]}]({i[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(i[0], TextType.IMAGES, i[1]))
            old_text = split_text[1]
        if old_text != "":
            new_nodes.append(TextNode(old_text, TextType.TEXT))
    return new_nodes
       


def split_nodes_link(old_nodes):
    if old_nodes is None:
        raise ValueError("invalid: No nodes given")
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        old_text = node.text
        link = extract_markdown_links(node.text)
        if len(link) == 0:
            new_nodes.append(node)
            continue
        for l in link:
            split_text = old_text.split(f"[{l[0]}]({l[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(l[0], TextType.LINKS, l[1]))
            old_text = split_text[1]
        if old_text != "":
            new_nodes.append(TextNode(old_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    starter_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([starter_node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes