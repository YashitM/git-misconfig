import requests

file_name = input("Please Enter the filename (relative path): ")

urls = open(file_name, "r").readlines()

for url in urls:
    new_url = url.rstrip('\n') + ".git/"
    check_request = requests.get(new_url)
    if check_request.status_code == 200:
        print("[+] Git Misconfiguration Found in: " + new_url)
        