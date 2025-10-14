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