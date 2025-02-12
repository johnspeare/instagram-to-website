import argparse
from bs4 import BeautifulSoup
import os
from collections import defaultdict
import re

def extract_posts(html_file):
    """Extracts Instagram posts from the archive HTML."""
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    posts = []

    for post_div in soup.find_all("div", class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder"):
        # Extract description
        description_div = post_div.find("div", class_="_3-95 _2pim _a6-h _a6-i")
        description = description_div.get_text(strip=True) if description_div else ""

        # Extract media files (JPG or MP4)
        media_divs = post_div.find_all("a", target="_blank")
        media_files = [media["href"].replace("media/posts/", "../../images/posts/") for media in media_divs if "href" in media.attrs]

        # Extract date
        date_div = post_div.find("div", class_="_3-94 _a6-o")
        date = date_div.get_text(strip=True) if date_div else ""

        # Extract proper 4-digit year
        year_match = re.search(r'\b(20\d{2})\b', date)
        year = year_match.group(1) if year_match else "Unknown"

        posts.append({"description": description, "media": media_files, "date": date, "year": year})

    return posts

def generate_post_page(post, index, output_folder):
    """Creates an individual post HTML page with a carousel."""
    posts_folder = os.path.join(output_folder, "insta", "posts")
    os.makedirs(posts_folder, exist_ok=True)

    post_filename = f"post_{index}.html"
    post_filepath = os.path.join(posts_folder, post_filename)

    carousel_media = "".join(
        f'<div class="carousel-item">' +
        (f'<img src="{media}" class="page-image">' if media.lower().endswith(".jpg")
         else f'<video class="page-video" autoplay loop muted playsinline><source src="{media}" type="video/mp4"></video>') +
        '</div>'
        for media in post["media"]
    )

    post_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
        <link rel="stylesheet" href="../../css/style.css">
        <script defer src="../script.js"></script>
    </head>
    <body>
        <div class="container">
            <a href="../index.html">Cycling Spokane Instagram Home</a>
            <h2>{post["date"]}</h2>
            <p>{post["description"]}</p>
            <div class="carousel">{carousel_media}</div>
        </div>
    </body>
    </html>
    """

    with open(post_filepath, "w", encoding="utf-8") as file:
        file.write(post_html)

    return post_filename

def generate_homepage(posts, output_folder):
    """Creates the homepage linking to all posts with thumbnails in a table."""
    insta_folder = os.path.join(output_folder, "insta")
    os.makedirs(insta_folder, exist_ok=True)

    # Organize posts by extracted year
    posts_by_year = defaultdict(list)
    for post in posts:
        posts_by_year[post["year"].strip()].append(post)

    # Generate bookmarks at the top of the homepage
    year_links = "".join(f'<a href="#{year}" class="year-link">{year}</a> ' for year in sorted(posts_by_year.keys(), reverse=True))

    table_rows = ""
    for year in sorted(posts_by_year.keys(), reverse=True):
        first_post = True
        for i in range(0, len(posts_by_year[year]), 3):
            row_cells = "".join(
                f'<td class="tg-0lax" style="text-align:center;"><a href="posts/post_{posts.index(posts_by_year[year][j])}.html">' +
                (f'<img src="../images/posts/{posts_by_year[year][j]["media"][0].split("/")[-2]}/{posts_by_year[year][j]["media"][0].split("/")[-1].replace(".jpg", "_tn.jpg").replace(".mp4", "_tn.jpg")}" class="thumbnail-img">') +
                f'</a><br>{posts_by_year[year][j]["date"]}</td>'
                for j in range(i, min(i + 3, len(posts_by_year[year]))) if posts_by_year[year][j]["media"]
            )
            if first_post:
                table_rows += f'<tr><td colspan="3"><h3 id="{year}">{year}</h3></td></tr>'
                if year not in ["2024", "2023"]:
                    table_rows += f'<tr><td colspan="3" style="text-align:right;"><a href="#top">Back to top</a></td></tr>'
                first_post = False
            table_rows += f'<tr>{row_cells}</tr>'

    homepage_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
        <link rel="stylesheet" href="../css/style.css">
        <style>
            .year-links {{ text-align: center; margin-bottom: 20px; }}
            .year-link {{ margin: 0 10px; text-decoration: none; font-size: 18px; }}
            .year-link:hover {{ text-decoration: underline; }}
            .thumbnail-img {{ display: block; margin: 0 auto; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Cycling Spokane Instagram Archive</h2>
            <div class="year-links">{year_links}</div>
            <div class="table-container">
                <table class="tg">
                    <tbody>{table_rows}</tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """

    with open(os.path.join(insta_folder, "index.html"), "w", encoding="utf-8") as file:
        file.write(homepage_html)

def main():
    parser = argparse.ArgumentParser(description="Convert Instagram archive HTML to static website.")
    parser.add_argument("input_html", help="Path to the Instagram archive HTML file")
    parser.add_argument("output_folder", help="Path to the output directory for the website")
    args = parser.parse_args()

    os.makedirs(args.output_folder, exist_ok=True)
    posts = extract_posts(args.input_html)

    for index, post in enumerate(posts):
        generate_post_page(post, index, args.output_folder)
    generate_homepage(posts, args.output_folder)

    print(f"Website generation complete! Files are in {args.output_folder}/insta")

if __name__ == "__main__":
    main()
