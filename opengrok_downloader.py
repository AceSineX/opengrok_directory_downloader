import requests
import argparse

parser = argparse.ArgumentParser(description='Simple OpenGrok directory downloader')
parser.add_argument("opengrok_url", help="The URL of the OpenGrok directory to download from")

# Define a "quiet" flag
parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output (quiet mode)")

args = parser.parse_args()

if not args.opengrok_url:
    print("Usage: python3 grok_downloader.py [url]")
    url = args.opengrok_urlddq
    sys.exit(1)

url = args.opengrok_url + "/"

r = requests.get(url, allow_redirects=True)

wanted = r.text.split("tbody")[1].split("tbody")[0]
a = wanted.split("<tr><td><p class=\"p\"/></td><td><a href=")[1].split("\"")[1]

size = len(r.text.split("tbody")[1].split("tbody")[0].split("<tr><td><p class=\"p\"/></td><td><a href="))

for i in range(1, size):
    filename = wanted.split("<tr><td><p class=\"p\"/></td><td><a href=")[i].split("\"")[1]
    final_dl_link = url.replace("xref", "raw") + filename

    if not args.quiet:
        print("Downloading : " + final_dl_link)

    r1 = requests.get(final_dl_link, allow_redirects=True)
    with open(filename, 'wb') as f:
            f.write(r1.content)
