const PythonBridge = require('./python_bridge');

module.exports = (text, callback) => {
  let pythonBridge = new PythonBridge()
  pythonBridge.run('processors/query_processor.py', text, callback)
}
