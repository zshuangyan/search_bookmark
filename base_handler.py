from tornado.web import RequestHandler
import json
import logging

class BaseHandler(RequestHandler):
    def prepare(self):
        try:
            logging.info("enter prepare")
            self.data = json.loads(self.request.body.decode("utf-8"))
        except json.decoder.JSONDecodeError as e:
            self.write_error(400, exc_info=e)

    def write_error(self, status_code, **kwargs):
        self.write({"error_code": status_code, "error_msg": kwargs.get("exc_info", "")})
        self.finish()