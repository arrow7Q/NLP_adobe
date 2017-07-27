let processQueryHandler = require('./process_query_handler')
let processFeatureHandler = require('./process_feature_handler')
let answerHandler = require('./answer_handler')
let solrAddHandler = require('./solr_add_handler')
let sorlQueryHandler = require('./solr_query_handler')

let handlers = {
  click:[{
    selector:'#predict_answer',
    callback: answerHandler
  },
  {
    selector:'#demo_process_question',
    callback: processQueryHandler
  },
  {
  	selector:'#demo_process_features',
  	callback: processFeatureHandler
  },
  {
    selector:'#demo_solr_add',
    callback: solrAddHandler
  },
  {
    selector:'#demo_solr_search',
    callback: sorlQueryHandler
  },

  ]
}
module.exports = handlers
