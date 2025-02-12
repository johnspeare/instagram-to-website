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
- Export as HTML
- Choose Large photos
## Step 2: Run create-tn.py to create thumbnails from images

Point the script at the `/media/posts` directory of the instagram archive, for example: 
```
python3 create-tn.py /instagram-archive/media/posts
```
The script will create a thumbnail for each image in the directories under `/media/posts`. The file name of each thumbnail image is the same as the orignial, but appended with `_tn`.
## Step 3: Copy the /posts directory into your /images directory
From here out, work from your development website environment.

Copy the `/media/posts` directory with all instagram images (and the new corresponding thumbnails) to your `/website-root/images` directory.

It should have this structure:

```
/images
  /posts
     /<folder-id> 
       imageid.jpg
       imageid_th.jpg
     /<folder-id>
      ...
```

## Step 4: Run create-tn-mp4.py to create thumbnails from videos

Point the script at the `website-root/images/posts` directory, for example: 
```
python3 create-tn-mp4.py /website/images/posts
```
The script will create a thumbnail for each mp4 in the directories under `/images/posts`. The file name of each thumbnail image is the same as the orignial, but appended with `_tn.jpg`.

## Step 5: Run insta2html.py to create website files
This script does all the heavy lifting -- it does the following:
- Parses the instagram archive content posts file (`Apps/Meta/meta-<date>/instagram-<username>-<datecode>/your_instagram_activity/content/posts_1.html`)
- Extracts image link reference, date, and description from each post
- Creates the `\insta` directory and puts the following directories files in it:
  - `index.html`: A table of thumbnails. Each thumbnail maps to a post page
  - `/posts`: A directory of web pages (post_0.html, post_1.html...). Each web page maps to an original post.


The script takes two arguments: the path to the instagram source content post1.html file, and the output directory, which should be your website root. For example:
`python3 insta2html.py /Apps/Meta/meta-2025-Feb-05-13-20-33/instagram-cyclingspokane-2025-02-05-sF2jTJee/your_instagram_activity/content/posts_1.html /website`

There are a few tweaks you can make easily by inspecting the script:

- Font is a google web script
- Yearly links  on each section don't include 2024 or 2023. You can find that logic in the script and tweak or remove that.
- Output directory name is `insta` -- you can change that. It's referenced in a couple places.
- Baseline HTML for index.html and post_n.html pages is tweakable.


## Step 6: Fit n finish
Result is pretty ugly. The resulting site assumes there's a `\css\style.css` file for pretty making.
