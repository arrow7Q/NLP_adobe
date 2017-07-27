
const PythonBridge = require('./python_bridge');
let solr_add_processor = require('./solr/add')
let solrAdder = (data)=>{
  docs = JSON.parse(data)
  docs.forEach((doc) =>{
    doc.id = doc["@id"]
    solr_add_processor(doc)
    console.log(`doc=${doc}`)
  })
}

module.exports = () => {
  let pythonBridge = new PythonBridge()
  pythonBridge.run('processors/ruleprocessor.py', "", solrAdder)
}
