#!/usr/bin/python3

import requests
import argparse
import threading
from threading import Thread

global_url_counter = 0
misconfigured_urls = list()

def setup_parser():
	parser = argparse.ArgumentParser(description='A MultiThreaded Git Misconfiguration Checker')
	parser.add_argument('-f', '--file', type=str, help="File Location", required=True)
	args = parser.parse_args()

	file_location = args.file

	return file_location

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

def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filled_length = int(length * iteration // total)
	bar = fill * filled_length + '-' * (length - filled_length)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')

	if iteration == total: 
		print()

def send_request(url, result, counter, total_urls, lock):
	global global_url_counter

	filtered_url = validate_url(url.rstrip('\n'))
	new_url = filtered_url.rstrip('\n') + ".git/"

	try:
		check_request = requests.get(new_url, timeout=5)
		if check_request.status_code == 200:
			misconfigured_urls.append(new_url)
	except requests.exceptions.Timeout:
		pass

	lock.acquire()

	global_url_counter += 1
	print_progress_bar(global_url_counter, total_urls, prefix = 'Progress:', suffix = 'Complete', length = 50)
	
	lock.release()


def main():
	file_location = setup_parser()
	urls = open(file_location, "r").readlines()

	print_progress_bar(0, len(urls), prefix = 'Progress:', suffix = 'Complete', length = 50)

	threads = []

	for counter, url in enumerate(urls):
		process = Thread(target=send_request, args=[url, counter, counter, len(urls), threading.Lock()])
		process.start()
		threads.append(process)

	for process in threads:
		process.join()
		
	for misconfigured_url in misconfigured_urls:
		print("[+] " + misconfigured_url)

	print("[x] Scan Complete. Found " + str(len(misconfigured_urls)) + " Misconfigured URLs from " + str(len(urls)) + " total URLs.")


if __name__ == '__main__':
	main()
