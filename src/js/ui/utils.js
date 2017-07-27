module.exports = {
  getListHtml(docs){
    let text = ""
    $.each(docs, (index, doc) =>{
      let doctext = doc.text && doc.text[0]
      if(typeof(doctext) === 'string'){
        doctext = doctext.replace(/(\n)+/g, '<br />');
        text += `<li>${doctext}</li>`
      }
    })
    return (text.length === 0 )? text: `<ol>${text}</ol>`
  },
  getTableHtml(docs, type){
    let text = ""
    $.each(docs, (index, doc) =>{
      let doctext = doc.text && doc.text[0]
      if(typeof(doctext) === 'string'){
        doctext = doctext.replace(/(\n)+/g, '<br />');
        let score = (doc.scores && doc.scores[type])? doc.scores[type] : 0
        text += `<tr><td>${doctext}</td><td>${score}</td> </tr>`
      }
    })
    return (text.length === 0 )? text: `<table><tr><th>Result</th><th>Score</th></tr>${text}</ol>`
  }
}
