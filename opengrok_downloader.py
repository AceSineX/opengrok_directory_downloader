import requests
import argparse
import os

def download_directory(url, path=""):
    r = requests.get(url, allow_redirects=True)
    wanted = r.text.split("tbody")[1].split("tbody")[0]
    size = len(r.text.split("tbody")[1].split("tbody")[0].split("<tr><td><p class=\"")) - 1

    for i in range(1, size):
        filename = wanted.split("></td><td><a href=\"")[i].split("\"")[0]
        link = url + filename
        
        # It is a directory
        if link.endswith("/"):
            if args.recursive:
                if not args.quiet:
                    print("Subdirectory : " + link)
                if os.path.exists(filename):
                    if not args.quiet:
                        print(filename + " : EXISTS!")
                else:
                    os.makedirs(filename)
                    if not args.quiet:
                        print(filename + " : CREATED!")

                download_directory(link, filename)

        # It is a file
        else:
            final_dl_link = url.replace("xref", "raw") + filename
            if not args.quiet:
                print("Downloading : " + final_dl_link)

            r1 = requests.get(final_dl_link, allow_redirects=True)
            with open(path + filename, 'wb') as f:
                f.write(r1.content)


parser = argparse.ArgumentParser(description='Simple OpenGrok directory downloader')
parser.add_argument("opengrok_url", help="The URL of the OpenGrok directory to download from")

# Define a "quiet" flag
parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output (quiet mode)")
# Define recursive flag
parser.add_argument("-r", "--recursive", action="store_true", help="Recursively download all subdirectories")

args = parser.parse_args()

if not args.opengrok_url:
    print("Usage: python3 grok_downloader.py [url]")
    url = args.opengrok_urlddq
    sys.exit(1)

url = args.opengrok_url

if not url.endswith("/"):
    url = url + "/"

download_directory(url)
