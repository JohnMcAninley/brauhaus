import time
import json
import asyncio
import logging

import websockets


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

DEFAULT_RECONNECT = 5.0


class Client():

    def __init__(self, *args, **kwargs):
        self._uri = kwargs['uri']
        self._reconnect_time = kwargs.get('reconnect', DEFAULT_RECONNECT)
        self._client = None
        self._last_attempt_time = None

    def connect(self):
        if self._client and self._client.open:
            return True
        try:
            self._client = asyncio.get_event_loop().run_until_complete(
                websockets.connect(uri=self._uri)
            )
        except Exception as e:
            logger.error(e)
        self._last_attempt_time = time.time()
        return True if self._client else False

    def push(self, data):
        if not self._client or not self._client.open:
            if time.time() - self._last_attempt_time > self._reconnect_time:
                if not self.connect():
                    return False
            else:
                return False
        try:
            asyncio.get_event_loop().run_until_complete(
                self._client.send(json.dumps(data))
            )
            self._last_push_time = time.time()
        except websockets.exceptions.ConnectionClosed:
            logger.info("CONNECTION CLOSED: {}:{}".format(
                self._client.remote_address[0], self._client.remote_address[1]))

    def read(self):
        if not self._client:
            # reconnect
            return None
        if not self._client.messages:
            return None
        # TODO handle all or one at a time?
        try:
            msg_str = asyncio.get_event_loop().run_until_complete(
                self._client.recv()
            )
            msg = json.loads(msg_str)
        except Exception as e:
            logger.error(e)
            return None
        return msg
