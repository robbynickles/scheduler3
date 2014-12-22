import threading
PORTNO = 10552

class FunctionThread (threading.Thread):
    """
    Thread that runs a function.
    """
    def __init__(self, f )
        threading.Thread.__init__(self)
    def run(self):
        f()
