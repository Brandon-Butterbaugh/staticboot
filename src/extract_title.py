



def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            temp = line[2:]
            temp = temp.strip()
            return temp
    raise ValueError("No h1 header found")