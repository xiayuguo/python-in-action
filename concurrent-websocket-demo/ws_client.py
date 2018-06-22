import time
import json
import string
import random
import websocket

from concurrent.futures import ThreadPoolExecutor, as_completed


def gen_name(size=6, chars=string.ascii_letters + string.digits):
    """生成名字(从A-Za-z,1-9共62字符中随机出字符拼接出字符串)"""
    return ''.join(random.choice(chars) for _ in range(size))


def on_message(ws, message):
    print(f"server: {message}")
    response = json.loads(message)
    now = time.time() * 1000
    total_cost = now - response["op_time"]
    res_cost = now - response["res_time"]
    print(f"total_cost is {total_cost}, res_cost is {res_cost}")


def on_error(ws, error):
    print(f"ERROR: {error}")


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    name = gen_name()
    ws.send(json.dumps(dict(name=name, op_time=int(time.time() * 1000))))


def ws_cli():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:18889/websocket",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


def main(num=100):
    with ThreadPoolExecutor(max_workers=num) as executor:
        future_task = dict((executor.submit(ws_cli), i)
                             for i in range(num))

        for future in as_completed(future_task):
            i = future_task[future]
            if future.exception() is not None:
                print(f'{i} generated an exception: {future.exception()}')
            else:
                print(f'{i} is finish')


if __name__ == "__main__":
    main()


