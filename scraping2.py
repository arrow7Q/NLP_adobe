import xml.etree.ElementTree as ET

tree=ET.parse('books.xml')
root=tree.getroot()

print root.tag
print root.attrib

for child in root:
    print child.tag
        

