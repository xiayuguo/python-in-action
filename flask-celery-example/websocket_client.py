# -*- coding: utf-8 -*-

import json
import logging
from websocket import create_connection

log = logging.getLogger(__name__)


def ws_client(message, ip='127.0.0.1', port=12345, timeout=2):
    result = False
    try:
        if isinstance(message, dict):
            message = json.dumps(message)

        ws = create_connection("ws://%s:%s/websocket" % (ip, port), timeout)

        ws.send(message)
        ws.close()
        result = True
        log.debug('send websocket OK: %s' % message)
    except Exception, err:
        log.exception("exception![%s]" % str(err))
        # ws.close()
        result = False
    return result
