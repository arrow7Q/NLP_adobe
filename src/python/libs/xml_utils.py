def textify(node):
    s=[]
    if node.text:
        s.append(node.text)
    for child in node.getchildren():
        s.extend(textify(child))
    if node.tail:
        s.append(node.tail)
    return s