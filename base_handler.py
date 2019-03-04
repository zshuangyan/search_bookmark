from tornado.web import RequestHandler
from tornado.escape import json_decode
import json

class BaseHandler(RequestHandler):
    def prepare(self):
        if self.request.body:
            try:
                self.data = json_decode(self.request.body)
            except TypeError or json.JSONDecodeError as e:
                self.write_error(400, error_msg=e)

    def write_error(self, status_code, **kwargs):
        """
        Override RequestHandler.write_error to produce a custom error response.

        For more information, refers to
        https://www.tornadoweb.org/en/stable/guide/structure.html?highlight=write_error
        """
        self.write({"error_code": status_code, "error_msg": kwargs.get("error_msg", "")})
        self.finish()
