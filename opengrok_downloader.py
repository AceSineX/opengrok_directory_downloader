import requests
import argparse
import os
from requests.auth import HTTPBasicAuth
import getpass

def download_directory(url, path="", auth=None):
    r = requests.get(url, allow_redirects=True, auth=auth)

    # Check if "tbody" exists in the response
    if "tbody" not in r.text:
        print(f"Error: The URL {url} does not contain the expected 'tbody' structure. Response text: {r.text}")
        return

    try:
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
                    subdirectory_path = os.path.join(path, filename)
                    if os.path.exists(subdirectory_path):
                        if not args.quiet:
                            print(subdirectory_path + " : EXISTS!")
                    else:
                        os.makedirs(subdirectory_path)
                        if not args.quiet:
                            print(subdirectory_path + " : CREATED!")

                    download_directory(link, subdirectory_path, auth)

            # It is a file
            else:
                final_dl_link = url.replace("xref", "raw") + filename
                if not args.quiet:
                    print("Downloading : " + final_dl_link)

                r1 = requests.get(final_dl_link, allow_redirects=True, auth=auth)
                with open(os.path.join(path, filename), 'wb') as f:
                    f.write(r1.content)
    except IndexError as e:
        print(f"Error processing the URL {url}: {e}")
        return


parser = argparse.ArgumentParser(description='Simple OpenGrok directory downloader')
parser.add_argument("opengrok_url", help="The URL of the OpenGrok directory to download from")
parser.add_argument("-u", "--username", help="Username for authentication (optional)")

# Define a "quiet" flag
parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output (quiet mode)")
# Define recursive flag
parser.add_argument("-r", "--recursive", action="store_true", help="Recursively download all subdirectories")

args = parser.parse_args()

if not args.opengrok_url:
    print("Usage: python3 grok_downloader.py [url]")
    sys.exit(1)

url = args.opengrok_url

if not url.endswith("/"):
    url = url + "/"

# Handle authentication
auth = None
if args.username:
    password = getpass.getpass(prompt="Enter password: ")
    auth = HTTPBasicAuth(args.username, password)

download_directory(url, auth=auth)
