import json
import asyncio
import logging

import websockets


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Listen to port 8080 on all interfaces
HOST = "0.0.0.0"
BACKEND_PORT = 1233
CLIENT_PORT = 1234

clients = set()
backend = None


async def publish(msg):
    for c in clients:
        logger.info("SENDING MESSAGE TO: {}:{}".format(
            c.remote_address[0], c.remote_address[1]))
        await c.send(msg)


async def backend_handler(websocket, path):
    try:
        logger.info("incoming CONNECTION: {}:{}".format(
            websocket.remote_address[0], websocket.remote_address[1]))
        global backend
        if backend:
            # TODO multiple backends
            # Allow only one for now
            return
        backend = websocket
        # TODO publish connection to clients
        while True:
            message = await backend.recv()
            logger.debug("received msg from backend: {}".format(message))
            try:
                await publish(message)
            except Exception as e:
                logger.error(e)
    except websockets.exceptions.ConnectionClosed:
        logger.info("CONNECTION CLOSED: {}:{}".format(
            websocket.remote_address[0], websocket.remote_address[1]))
    finally:
        backend = None
        # TODO publish disconnection to clients


async def client_handler(websocket, path):
    try:
        logger.info("incoming CONNECTION: {}:{}".format(
            websocket.remote_address[0], websocket.remote_address[1]))
        clients.add(websocket)
        while True:
            request = await websocket.recv()
            data = json.loads(request)
            try:
                if not backend:
                    # TODO
                    continue
                await backend.send(request)
                response = await backend.recv()
                if data["action"] != "get":
                    await publish(json.dumps(response))
                else:
                    await websocket.send(json.dumps(response))
            except Exception as e:
                logger.error(e)
                await websocket.send(json.dumps(e.json()))
    except websockets.exceptions.ConnectionClosed:
        logger.info("CONNECTION CLOSED: {}:{}".format(
            websocket.remote_address[0], websocket.remote_address[1]))
    finally:
        clients.remove(websocket)


start_backend_server = websockets.serve(backend_handler, HOST, BACKEND_PORT)
start_client_server = websockets.serve(client_handler, HOST, CLIENT_PORT)

asyncio.get_event_loop().run_until_complete(start_backend_server)
asyncio.get_event_loop().run_until_complete(start_client_server)
asyncio.get_event_loop().run_forever()
