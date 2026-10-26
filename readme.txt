Requirements:
Python3
Pillow library
argparse
BeautifulSoup (pip3 install beautifulsoup4)


python3 -m pip install --upgrade pillow


1. Export instagram as html, specify high quality photos
2.  Run thumbnail on media/posts folder in the instagram archive

python3 create-tn.py /instagram-archive/media/posts

This creates a thumbnail for each image in the folders under posts. The file name of each thumbnail image is the same as the orignial, but appended with "_tn"

3. Run convert script.
python3 script.py /path/to/post.html /path/to/output_directory

First argument is insta post.html
Second path is where script will create a directory. This directory should be a peer of the images directory (the images directory should contain the post directory from step two) The directory that this script creates will contain a homepage and a directory of webpages. 


<img src="../images/posts/202409/460530363_2139065896489199_377951156901332989_n_18059431918689017.jpg" class="carousel-img">


python3 /Users/john/insta-export/insta2html.py /Users/john/Dropbox/Apps/Meta/meta-2025-Feb-05-13-20-33/instagram-cyclingspokane-2025-02-05-sF2jTJee/your_instagram_activity/content/posts_1.html /Users/john/jdf/john



python3 /Users/john/insta-export/create-tn.py /Users/john/jdf/john/images/posts