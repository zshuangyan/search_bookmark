from base_handler import BaseHandler
from utils.validate import json_validate
from searcher.search import search
import json

SEARCH_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "num": {
            "type": "number"
        }
    }
}


class SearchHandler(BaseHandler):
    @json_validate(SEARCH_SCHEMA)
    def post(self):
        result = search(**self.data)
        self.write({"error_code": 200,
                    "data": str(result),
                    "error_msg": "query succeed"})
