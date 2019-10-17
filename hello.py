# coding=utf8
import socket
import urllib.parse as parse

url = parse.urlparse('http://www.google.com/')
print(url.netloc)
print(url.port)
