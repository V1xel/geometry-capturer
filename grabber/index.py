import mss
import mss.tools
import time
import pygetwindow as gw

# Find the window by window title
window = gw.getWindowsWithTitle(
    "Star Wars: Knights of the Old Republic II: The Sith Lords"
)[0]

# Set up MSS and capture loop
with mss.mss() as sct:
    sct_img = sct.grab(
        {
            "top": window.top + 35,
            "left": window.left + 10,
            "width": window.width - 20,
            "height": window.height - 45,
        }
    )
    mss.tools.to_png(sct_img.rgb, sct_img.size, output="screenshot.png")

    # Wait a bit before capturing the next frame
    time.sleep(0.1)
