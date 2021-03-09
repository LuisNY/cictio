#!/usr/bin/python3

import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../'))

from http_server.server import getServer

from ORM.base import createAll


if __name__ == "__main__":

    createAll()
    server = getServer()
    
    try :
        server.serve_forever()
    except :
        pass

    server.server_close()
    print("Server stopped")
