#!/usr/bin/python3

import requests
import argparse

def setup_parser():
	parser = argparse.ArgumentParser(description='Git Misconfiguration Checker')
	parser.add_argument('-f', '--file', type=str, help="File Location", required=True)
	parser.add_argument('-t', '--threads', type=int, help="Threads to Spawn", required=False)
	args = parser.parse_args()

	file_location = args.file
	num_threads = 5 # Default number of threads

	if args.threads:
		num_threads = args.threads

	return file_location, num_threads

def validate_url(url):
	valid_protocols = ['http', 'https']
	protocol_check_bool = False

	if url[len(url) - 1] != '/':
		url += '/'

	for protocol in valid_protocols:
		if protocol in url:
			protocol_check_bool = True

	if not protocol_check_bool:
		url = "http://" + url

	return url

def main():
	file_location, num_threads = setup_parser()
	urls = open(file_location, "r").readlines()

	misconfigured_urls = list()

	for url in urls:
		filtered_url = validate_url(url.rstrip('\n'))
		new_url = filtered_url.rstrip('\n') + ".git/"

		try:
			check_request = requests.get(new_url, timeout=5)
			if check_request.status_code == 200:
				print("[+] Git Misconfiguration Found in: " + new_url)
				misconfigured_urls.append(new_url)
		except requests.exceptions.Timeout:
			continue

	print("[x] Scan Complete. Found " + str(len(misconfigured_urls)) + " Misconfigured URLs from " + str(len(urls)) + " total URLs.")

if __name__ == '__main__':
	main()