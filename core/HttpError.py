# -*- encoding: utf-8 -*-

class HttpError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message    
    pass

