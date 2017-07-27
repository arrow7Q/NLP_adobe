let $ = global.$
let handlers = require('./ui/handlers')


function initHandlers(){
  $.each(handlers.click, (index, handler) =>{
    console.log(index)
    $(handler.selector).click(handler.callback)
  });
}

module.exports = initHandlers
