# Automated r/place

This script will automate the placement of tiles on r/place every 5 minutes according to some template image that you provide.

## Instructions

### 1. Clone the repo

To begin, clone the repository to your machine.

### 2. Include an image

Next, you must include in the script's directory a template image with the EXACT dimensions you want and RBG values that are used in r/place. RGB values can be found at the bottom of this readme.

### 3. Get an API key

After you've provide an image, you must authorize a new app if you don't have an API key already.

To do this visit `https://www.reddit.com/prefs/apps` and click on the "Create App" button.

Then, fill out the form:

1. Name it whatever you want
2. Select `script` as the type.
3. Provide any bogus redirect uri. Ex: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`.
4. Press `create app`.

Now you should have a client id and a secret key. The client key is the string under the name of the app, while the secret can be found in the `secret` field.

### 4. Populate `config.json`

With this information in hand, you must now populate the fields in `config.json` in the script directory. These fields include:

- `image_name`: The file name of the image you provided.
- `client_id`: The client id of the app you created.
- `secret`: The secret of the app you created.
- `start_x`: The x coordinate on the r/place canvas where you want to locate the left top corner of your template image.
- `start_y`: The y coordinate on the r/place canvas where you want to locate the left top corner of your template image.
- `canvas`: The canvas id of the r/place canvas you want to place the template image on. The canvas is broken into quadrants, with each quandrant having its own canvas id. The top left quadrant's id is 0, the top right is 1, the bottom left is 2, and the bottom right is 3.
- `username`: Your reddit username.
- `password`: Your reddit password.

Several of these fields contain sensitive information, so if you not using your own machine to run the script you should put these values in environment variables instead. This will require changing the script slightly. The reason the script needs the username and password is so it can place tiles on your behalf.

### 5. Run the script

Finally you are ready to run the script. To do this, run the following command:

```bash
py place.py
```

If you want verbose output, you can pass in a debug flag like so:

```bash
py place.py --degub
```

Now you should be automatically placing tiles on r/place!

## Notes

### Coordinate sytem

r/place uses a coordinate system that is familiar to anyone who has worked with computer graphics before but not intuitive to everyone else. Basically, the y axis is flipped, so the top left corner of the canvas is at (0,0) and the bottom right corner is at (width, height), meaning larger y coordinates are closer to the bottom of the canvas than smaller ones.

Since I have not adjusted for this in the script, this means that your image will be drawn upside down. To have it displayed right-side up, you must flip the y axis of your image before you start running the script. This should be easy to accomplish in any image editor. Importantly, you must reflect the image and not simply rotate it 180 degrees if your image is not symmetrical about the y axis.

Additionally, r/place is broken up into several canvases. The x and y coordinates you provide the script are relative to the canvas being drawn to, meaning if you want to place your drawing on the second canvas (the top right quadrant), you will use local coordinates instead of global coordinates. So, coordinate x = 1 is actually in the middle of r/place, but that the start of the second canvas.

### RGB values

As mentioned at the beginning of the readme, here are the RGB color codes corresponding to the colors used in r/place. If you want a transparent pixel, simply use in your template image any color not included here.

| color | rgb |
| --- | --- |
| dark red | (190, 0, 57) |
| red | (255, 69, 0) |
| orange | (255, 168, 0) |
| yellow | (255, 214, 53) |
| dark green | (0, 163, 104) |
| green | (0, 204, 120) |
| light green | (126, 237, 86) |
| dark teal | (0, 117, 111) |
| teal | (0, 158, 170) |
| dark blue | (36, 80, 164) |
| blue | (54, 144, 234) |
| light blue | (81, 233, 244) |
| indigo | (73, 58, 193) |
| periwinkle | (106, 92, 255) |
| dark purple | (129, 30, 159) |
| purple | (180, 74, 192) |
| pink | (255, 56, 129) |
| light pink | (255, 153, 170) |
| dark brown | (109, 72, 47) |
| brown | (156, 105, 38) |
| black | (0, 0, 0) |
| gray | (137, 141, 144) |
| light gray | (212, 215, 217) |
| white | (255, 255, 255) |