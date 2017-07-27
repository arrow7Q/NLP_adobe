from xml_utils import textify
from nltk import sent_tokenize

class StepsProcessor:
    def __init__(self,node):
        self.xmlNode = node
    
    def readSteps(self,stepsNode):
        steps = []
        for node in stepsNode:
            if(node.text and node.text != ""):
                steps.append(node.text)
        return steps

    def getSteps(self):
        steps = []
        # if node.text:
        #     steps.append(node.text)
        # for child in node.getchildren():
        #     steps.extend(getSteps(child))
        # if node.tail:
        #     steps.append(node.tail)
        # return steps




        #steps.append(self.xmlNode.text)
        for node in self.xmlNode:
            if(node.tag == "steps"):
                steps = textify(node)
        #print steps
        return steps

    def getStepsHTML(self):
        steps = self.getSteps()
        steps = " ".join(steps).replace('\n','').strip()
        steps = sent_tokenize(steps)
        stepsHTML = ""
        for step in steps:
            stepsHTML+= "<li> " + step + " </li>"

        stepsHTML = "<ul>" + stepsHTML + "</ul>"
        return stepsHTML
