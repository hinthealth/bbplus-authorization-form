"""Main application for BlueButton+ Patient Authorization form."""

from frontend import handlers
import webapp2


routes = (
    ('/api/add_direct_address/?', handlers.AddDirectAddressHandler),
    ('/api/remove_direct_address/?', handlers.RemoveDirectAddressHandler),
    ('/api/update_frequency/?', handlers.UpdateFrequencyHandler),
    ('/?', handlers.MainHandler),
)
application = webapp2.WSGIApplication(routes)
