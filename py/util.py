import httpx

def download_file(url, dest_path):
    """Download a file from a URL to a local destination path."""
    with httpx.stream("GET", url) as response:
        response.raise_for_status()
        with open(dest_path, "wb") as file:
            for chunk in response.iter_bytes():
                file.write(chunk)