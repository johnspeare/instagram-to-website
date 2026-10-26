import argparse
from bs4 import BeautifulSoup
import os

def extract_posts(html_file):
    """Extracts Instagram posts from the archive HTML."""
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    posts = []

    for post_div in soup.find_all("div", class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder"):
        # Extract description
        description_div = post_div.find("div", class_="_3-95 _2pim _a6-h _a6-i")
        description = description_div.get_text(strip=True) if description_div else ""

        # Extract images
        image_divs = post_div.find_all("a", target="_blank")
        images = [img["href"].replace("media/posts/", "../../images/posts/") for img in image_divs if "href" in img.attrs]

        # Extract date
        date_div = post_div.find("div", class_="_3-94 _a6-o")
        date = date_div.get_text(strip=True) if date_div else ""

        posts.append({"description": description, "images": images, "date": date})

    return posts

def generate_post_page(post, index, output_folder):
    """Creates an individual post HTML page with a carousel."""
    posts_folder = os.path.join(output_folder, "insta", "posts")
    os.makedirs(posts_folder, exist_ok=True)

    post_filename = f"post_{index}.html"
    post_filepath = os.path.join(posts_folder, post_filename)

    carousel_images = "".join(
        f'<div class="carousel-item"><img src="{img}" class="page-image"></div>'
        for img in post["images"]
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
            <div class="carousel">{carousel_images}</div>
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

    table_rows = ""
    for i in range(0, len(posts), 3):
        row_cells = "".join(
            f'<td class="tg-0lax"><a href="posts/post_{j}.html">'
            f'<img src="../images/posts/{posts[j]["images"][0].split("/")[-2]}/{posts[j]["images"][0].split("/")[-1].replace(".jpg", "_tn.jpg")}" class="thumbnail-img"></a>'
            f'<br>{posts[j]["date"]}</td>'
            for j in range(i, min(i + 3, len(posts))) if posts[j]["images"]
        )
        table_rows += f'<tr>{row_cells}</tr>'

    homepage_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
        <link rel="stylesheet" href="../css/style.css">
    </head>
    <body>
        <div class="container">

            <h2>Cycling Spokane Instagram Archive</h2>
            <div class="table-container">
                <table class="tg">
                    <tbody>
                        {table_rows}
                    </tbody>
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
