# instagram-to-website
The scripts in this project convert Instagram html archive into simple website.

The python scripts were written by ChatGPT 4.0.

The resulting website has a thumbnail landing page (index.html). Each thumbnail is from instagram post that links to a page with the full size images and the post description. [Example is here.](https://www.johndogfood.com/john/insta/index.html)

## Prerequisites
- The scripts were written for Python 3 on Mac OS.
- The following libraries are required:

  ```
  import os
  import sys
  from PIL import Image
  import subprocess
  import argparse
  from bs4 import BeautifulSoup
  from collections import defaultdict
  import re
  ```

## Web hosting folder structure

The structure consists of the following files and directories:
```
/css
  style.css
/images
  /posts
     /<folder-id> 
       imageid.jpg
       imageid_th.jpg
     /<folder-id>
      ...
/insta
  index.html
  /posts
    post_0.html
    post_1.html
    ...
```
  The script assumes you have the `/css` and `/images` directories already in place.

## Step 1: Archive your Instagram account
do stuff
# Step 2: Run create-tn.py to create thumbnails from images
do stuff
# Step 3: Run create-tn-mp4.py to create thumbnails from videos
do stuff
# Step 4: Run insta2html.py to create website files
do stuff
# Step 5: Fit n finish
do stuff
