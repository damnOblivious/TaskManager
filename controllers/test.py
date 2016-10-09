def hello():
    import cgi
    x=request.env.http_accept_language
    y=request.args
    z=request.vars
    redirect(URL('index',))
def index():
    x=request.args
    return x
