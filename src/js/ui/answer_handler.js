//const query_handler = require('./process_query_handler')
//const solr_query_handler = require('./solr_query_handler')
let ui_utils = require('./utils')
let $ = global.$
const queryTypeMap = {
  Information:"DEF",
  Process:"STP"
}


let answerProcessor = (docs, type) =>{
  let newDocs = []

// testing -utkarsh
  let isInArray = (arr, str) => {
      return arr.indexOf(str.toLowerCase()) > -1;
  }

  $.each(docs, (index, doc) =>{
    doc.scores = JSON.parse(doc.scores)
    //--->
    // if( isInArray(doc.object, text) )
    //   doc.scores[type]+= 5 
    // console.log(doc.scores[type])
    //--->

    doc.index = index
    newDocs.push(doc)
  })
  let compareFn = (doc1, doc2) => {
    if(doc1.scores && doc2.scores && doc1.scores[type] !== undefined && doc2.scores[type] !== undefined){
      if(doc1.scores[type] !== doc2.scores[type]){
        return doc2.scores[type] - doc1.scores[type]
      }
      else{
        return doc1.index - doc2.index
      }
    }
    return 0
  }
  newDocs.sort(compareFn)
  return newDocs
}

//testing --utkarsh
// let boost = (docs, type, text ) =>{
//   let modDocs = []

// let isInArray = (arr, str) => {
//     return arr.indexOf(str.toLowerCase()) > -1;
// }

//   $.each(docs, (index, doc) =>{
//     doc.scores = JSON.parse(doc.scores)
//     if( isInArray(doc.object, text) )
//       doc.scores[type]+= 5 
//     console.log(doc.scores[type])
//   })
// }



let onSolrQueryResult = (res, type) =>{
  if(res && res.numFound >0){
    //let docs = res.docs.splice(0, 5)
    //console.log(text)  //for testting

    //let temp = boost(res.docs, type, text)
    let top_docs = answerProcessor(res.docs, type)
    top_docs = top_docs.splice(0, 5)
    let answerHtml = ui_utils.getTableHtml(top_docs, type)

    //let answerHtml =   setscore(docs)
    if(top_docs.length > 0 &&  top_docs[0]["text"]){
        $('.first-answer').show()
        $('#first_answer').html(top_docs[0]["text"][0])

        $('.predicted-answer').show()
        $('#processed_answer').html(answerHtml)
      }
  }
}

let onQueryResult = (res) =>{
  //let q_text = $('#q_text').val()
  console.log(res)  // again testing


  let query_result = JSON.parse(res)
  let query_param = {}
  //var q_type = queryTypeMap[query_result.qtype]
  let q_features = query_result.features || []
  let q_text = q_features.join(' ')
  let query_string = `q=${q_text}`
  console.log(query_result.qtype)
  if(query_result.qtype){
    //query_param.type = queryTypeMap[query_result.qtype]
    query_param.type = query_result.qtype

    query_string += `&type=${query_param.type}`

    //onSolrQueryResult(q_text,q_type)
  }
  let successFn = (res) =>{
    onSolrQueryResult(res, query_param.type)
  }

  $.ajax({
    type: 'get',
    url: "solr/search",
    data: query_string,
    success: successFn
  });

}

//get the queryprocessed from the python script
module.exports= () =>{
  let q_text = $('#q_text').val()
  $.ajax({
    type: 'get',
    url: "query",
    data:`q=${q_text}`,
    success: onQueryResult
  });
}
