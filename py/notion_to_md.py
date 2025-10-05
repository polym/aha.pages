import os

import click
import yaml
from notion_client import Client
from notion2md.exporter.block import MarkdownExporter

from util import download_file


def extract_notion_metadata(meta, output_path):
     """Extract data from Notion meta for template rendering"""
     props = meta.get("properties", {})
     # Extract title
     title = ""
     if "Name" in props and props["Name"].get("title"):
         title = props["Name"]["title"][0]["plain_text"]

     tags = [t["name"] for t in props.get("tags", {}).get("multi_select", [])]
     categories = [c["name"] for c in props.get("categories", {}).get("multi_select", [])]
     
     # FIXME: authors not working?
     # print(props.get("authors", {}))
     # authors = [p["name"] for p in props.get("authors", {}).get("people", [])]

     cover_image = ""
     if cover := meta.get("cover"):
        if cover["type"] in ("file", "external"):
            cover_image = "cover.jpg"
            download_file(cover[cover["type"]]["url"], os.path.join(output_path, cover_image))
     
     return {
         "title": title,
         "draft": props.get("draft", {}).get("checkbox", False),
         "cover": {
             "image": cover_image
         },
         "tags": tags,
         # "categories": categories,
         "date": meta.get("created_time", ""),
         "lastmod": meta.get("last_edited_time", ""),
     }

def build_md_frontmatter(client, page_id, output_path):
    page = client.pages.retrieve(page_id)
    meta = extract_notion_metadata(page, output_path)
    frontmatter = "---\n"
    frontmatter += yaml.dump(meta, stream=None, allow_unicode=True)
    frontmatter += "\n---\n\n"
    return frontmatter

@click.command()
@click.option("--database_id", default=None, help="Notion database ID to export all pages from.")
@click.option("--page_id", default=None, help="Notion page ID to export a single page.")
@click.option("--post_path", default="", help="Output path for exported markdown files.")
def run(database_id, page_id, post_path):
    client = Client(auth=os.environ["NOTION_TOKEN"])
    page_ids = []
    if database_id:
        page_ids = [ r["id"]for r in client.databases.query(database_id)["results"] if r["object"] == "page"]
    if page_id:
        page_ids.append(page_id)
    for page_id in page_ids:
        output_path = os.path.join(post_path, page_id)
        md_path = os.path.join(output_path, "index.md")

        exporter = MarkdownExporter(
            block_id=page_id,
            output_path=output_path,
            # NOTE: must use "index" instead of "index.md"
            output_filename="index",
            download=True,
            unzipped=True,
        )
        exporter.export()

        # add frontmatter to the top of the md file
        frontmatter = build_md_frontmatter(client, page_id, output_path)
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(frontmatter + content)

        print(f"Exported page {page_id} to {output_path}")

if __name__ == "__main__":
    run()