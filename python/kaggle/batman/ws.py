#!/usr/bin/python
import websocket

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://coinsecure.in/websocket",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.run_forever()
    ws.send('{"method": "ticker"}')