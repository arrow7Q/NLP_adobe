import xml.etree.ElementTree as ET



path='dita/frm_getstarted_gs.xml'


tree=ET.parse(path)
root=tree.getroot()
    
print root.tag
print root.attrib

for child in root:
  for i in child.iter('p'):
    print i.text
  print '\n'


    
        
