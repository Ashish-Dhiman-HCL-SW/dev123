import requests
import re

# List of (package, version) pairs from your corrected list
packages = [
    ("anyio", "4.12.0"),
    ("arrow", "1.4.0"),
    ("asttokens", "3.0.1"),
    ("async_lru", "2.0.5"),
    ("attrs", "25.4.0"),
    ("babel", "2.17.0"),
    ("beautifulsoup4", "4.14.3"),
    ("bleach", "6.3.0"),
    ("certifi", "2025.11.12"),
    ("cffi", "2.0.0"),
    ("charset-normalizer", "3.4.4"),
    ("colorama", "0.4.6"),
    ("contourpy", "1.3.3"),
    ("cycler", "0.12.1"),
    ("debugpy", "1.8.19"),
    ("decorator", "5.2.1"),
    ("defusedxml", "0.7.1"),
    ("fastjsonschema", "2.21.2"),
    ("fonttools", "4.61.1"),
    ("fqdn", "1.5.1"),
    ("h11", "0.16.0"),
    ("httpcore", "1.0.9"),
    ("httpx", "0.28.1"),
    ("idna", "3.11"),
    ("ipykernel", "7.1.0"),
    ("ipython", "9.8.0"),
    ("ipywidgets", "8.1.8"),
    ("jedi", "0.19.2"),
    ("jinja2", "3.1.6"),
    ("joblib", "1.5.3"),
    ("json5", "0.12.1"),
    ("jsonpointer", "3.0.0"),
    ("jsonschema", "4.25.1"),
    # … add the rest from your list …
]

def sanitize_name(name):
    """PyPI JSON API wants normalized names (replace '_' with '-') if needed."""
    return name.replace("_", "-")

def get_wheel_urls(package, version):
    url = f"https://pypi.org/pypi/{sanitize_name(package)}/{version}/json"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    urls = []
    for file in data.get("urls", []):
        fname = file.get("filename", "")
        # pick wheel files only
        if fname.endswith(".whl"):
            urls.append(file.get("url"))
    return urls

with open("download_commands.sh", "w") as out:
    out.write("#!/bin/bash\n\n")
    for pkg, ver in packages:
        try:
            wheel_urls = get_wheel_urls(pkg, ver)
            if not wheel_urls:
                print(f"No wheels found for {pkg}=={ver}")
                continue

            for url in wheel_urls:
                filename = url.split("/")[-1]
                cmd = f"curl -L -o {filename} {url}"
                out.write(cmd + "\n")
                print(f"Added curl for {pkg}: {filename}")
        except Exception as e:
            print(f"Error for {pkg}=={ver}: {e}")

print("\nDone! See download_commands.sh for all curl commands.")
