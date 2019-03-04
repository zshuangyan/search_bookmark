import tornado.web
import tornado.ioloop
import logging.config
from tornado_logging import LOGGING
from search_handler import SearchHandler

logging.config.dictConfig(LOGGING)

app = tornado.web.Application([
    ('/search', SearchHandler),
])

server = tornado.web.HTTPServer(app)
server.listen(8888)
tornado.ioloop.IOLoop.current().start()