import json
import math
import sys
import time
from io import BytesIO
from typing import Union

import requests
from PIL import Image

import quick_log
from quick_log import log

quick_log.debug = False

# Placeholders
access_token = ""
start_x = None
start_y = None
canvas = None
client_id = None
secret = None
template = None
config = None
username = None
password = None
width = None
height = None

# Mapping from RGB values to r/place color codes
rgb_to_code_map = {
    (190, 0, 57): 1,  # dark red
    (255, 69, 0): 2,  # red
    (255, 168, 0): 3,  # orange
    (255, 214, 53): 4,  # yellow
    (0, 163, 104): 6,  # dark green
    (0, 204, 120): 7,  # green
    (126, 237, 86): 8,  # light green
    (0, 117, 111): 9,  # dark teal
    (0, 158, 170): 10,  # teal
    (36, 80, 164): 12,  # dark blue
    (54, 144, 234): 13,  # blue
    (81, 233, 244): 14,  # light blue
    (73, 58, 193): 15,  # indigo
    (106, 92, 255): 16,  # periwinkle
    (129, 30, 159): 18,  # dark purple
    (180, 74, 192): 19,  # purple
    (255, 56, 129): 22,  # pink
    (255, 153, 170): 23,  # light pink
    (109, 72, 47): 24,  # dark brown
    (156, 105, 38): 25,  # brown
    (0, 0, 0): 27,  # black
    (137, 141, 144): 29,  # gray
    (212, 215, 217): 30,  # light gray
    (255, 255, 255): 31,  # white
}

# Mapping from r/place color codes to RGB values
code_to_rgb_map = {}
for k, v in rgb_to_code_map.items():
    code_to_rgb_map[v] = k

# Encode image pixels to r/place color codes
def load_template(file: str) -> list[list[int]]:
    img = Image.open(file).convert("RGB")
    data = img.getdata()
    w = img.width
    h = img.height

    count = 0
    new_img = []
    for i in range(h):
        line = []
        for j in range(w):
            idx = i * w + j
            count += 1
            if data[idx] in rgb_to_code_map.keys():
                line.append(rgb_to_code_map[data[idx]])
            else:
                line.append(-1)
        new_img.append(line)

    assert count == w * h
    return new_img


def refresh_token() -> str:
    log("Refreshing access token")

    client_auth = requests.auth.HTTPBasicAuth(client_id, secret)
    post_data = {"grant_type": "password", "username": username, "password": password}
    headers = {"User-Agent": f"ChangeMeClient/0.1 by {username}"}

    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=client_auth,
        data=post_data,
        headers=headers,
    )
    access_token = response.json()["access_token"]

    return access_token


def place_pixel(x: int, y: int, color: int, access_token: str, canvas: int) -> int:
    """Try to place a pixel and return the time at which we can place the next pixel."""

    log(f"Placing pixel at {x}, {y} with color {color}")
    url = "https://gql-realtime-2.reddit.com/query"
    headers = {
        "origin": "https://hot-potato.reddit.com",
        "referer": "https://hot-potato.reddit.com/",
        "apollographql-client-name": "mona-lisa",
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }
    payload = json.dumps(
        {
            "operationName": "setPixel",
            "query": "mutation setPixel($input: ActInput!) {\n  act(input: $input) {\n    data {\n      ... on BasicMessage {\n        id\n        data {\n          ... on GetUserCooldownResponseMessageData {\n            nextAvailablePixelTimestamp\n            __typename\n          }\n          ... on SetPixelResponseMessageData {\n            timestamp\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
            "variables": {
                "input": {
                    "actionName": "r/replace:set_pixel",
                    "PixelMessageData": {
                        "coordinate": {"x": x, "y": y},
                        "colorIndex": color,
                        "canvasIndex": canvas,
                    },
                }
            },
        }
    )

    response = requests.post(url, data=payload, headers=headers)
    json_data = response.json()

    success = json_data["data"] is not None
    if success:
        timestamp = math.floor(
            json_data["data"]["act"]["data"][0]["data"]["nextAvailablePixelTimestamp"]
        )
    else:
        timestamp = math.floor(
            json_data["errors"][0]["extensions"]["nextAvailablePixelTs"]
        )

    formatted_timestamp = timestamp / 1000  # Convert to seconds
    return formatted_timestamp


def get_canvas(canvas_index: int, access_token: str) -> list[tuple]:
    """Return flat list of RGB values for canvas png."""

    log("Getting canvas")
    url = "https://gql-realtime-2.reddit.com/query"
    headers = {
        "origin": "https://hot-potato.reddit.com",
        "referer": "https://hot-potato.reddit.com/",
        "apollographql-client-name": "mona-lisa",
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }
    payload = json.dumps(
        {
            "variables": {
                "input": {
                    "channel": {
                        "teamOwner": "AFD2022",
                        "category": "CANVAS",
                        "tag": str(canvas_index),
                    }
                }
            },
            "extensions": {},
            "operationName": "replace",
            "query": "subscription replace($input: SubscribeInput!) {\n  subscribe(input: $input) {\n    id\n    ... on BasicMessage {\n      data {\n        __typename\n        ... on FullFrameMessageData {\n          __typename\n          name\n          timestamp\n        }\n        ... on DiffFrameMessageData {\n          __typename\n          name\n          currentTimestamp\n          previousTimestamp\n        }\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        }
    )

    response = requests.post(url, data=payload, headers=headers)
    response.json()["data"]["subscribe"]["data"]["name"]
    img_url = response.json()["data"]["subscribe"]["data"]["name"]
    img = Image.open(BytesIO(requests.get(img_url).content))
    img = img.convert("RGB")
    return list(img.getdata())


def get_pixel(x: int, y: int, img: list[tuple]) -> tuple:
    log(f"Getting pixel at {x}, {y}")
    canvas_height = 1000
    idx = y * canvas_height + x
    return img[idx]


def scan_and_replace_pixels(
    x: int,
    y: int,
    width: int,
    height: int,
    canvas: int,
    access_token: str,
    template: list[list[int]],
) -> Union[int, bool]:
    log("Scanning and replacing pixels")

    img = get_canvas(canvas, access_token)
    for i in range(width):
        for j in range(height):
            img_x = x + i
            img_y = y + j
            pixel = get_pixel(img_x, img_y, img)

            template_pixel = template[i][j]
            if template_pixel == -1:  # Ignore this pixel
                continue
            elif pixel == code_to_rgb_map[template_pixel]:  # Pixel is already correct
                log(f"Pixel at {img_x}, {img_y} is already correct")
                continue
            else:  # Pixel is incorrect
                log(
                    f"Calling place pixel at {img_x}, {img_y} with color {template_pixel}"
                )
                timestamp = place_pixel(
                    img_x, img_y, template_pixel, access_token, canvas
                )
                return timestamp

    return False  # No pixels were replaced


def main():
    access_token = refresh_token()
    while True:
        try:
            result = scan_and_replace_pixels(
                start_x, start_y, width, height, canvas, access_token, template
            )
        except KeyError as e:
            if e.args[0] == "data":
                log("Bad token")
                access_token = refresh_token()
                continue
            else:
                raise e

        if result == False:  # No pixels were replaced
            log("Sleeping temporarily")
            time.sleep(10)
        else:
            log(
                f"Sleeping until we can place next pixel: {result - time.time()} seconds"
            )

            if result - time.time() > 5:
                time.sleep(result - time.time() + 3)
            else:
                time.sleep(10)


if __name__ == "__main__":

    with open("config.json") as f:
        config = json.load(f)

    start_x = int(config["start_x"])
    start_y = int(config["start_y"])
    canvas = int(config["canvas"])
    client_id = config["client_id"]
    secret = config["secret"]
    username = config["username"]
    password = config["password"]
    template = load_template("pixil-frame-0.png")
    width = len(template[0])
    height = len(template)

    for arg in sys.argv[1:]:
        if arg == "--debug" or arg == "-d":
            quick_log.debug = True
        elif arg == "--no-debug":
            quick_log.debug = False
        elif "=" in arg:  # Overriding config
            flag, val = arg.split("=")
            if flag == "--template":
                template = load_template(val)
            elif flag == "--start-x":
                start_x = int(val)
            elif flag == "--start-y":
                start_y = int(val)
            elif flag == "--canvas":
                canvas = int(val)

    print("Starting...\n  To stop, press Ctrl+C\n  To see script output, run with --debug or -d", flush=True)
    main()