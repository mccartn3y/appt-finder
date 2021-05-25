import sys
import pickle
from getpass import getpass
import mechanize
from bs4 import BeautifulSoupimport sys
import pickle
from getpass import getpass
import mechanize
from bs4 import BeautifulSoup

br = mechanize.Browser()
br.set_handle_robots(False)
resp = br.open("https://sirfy.de/sirfy-de-corona-impfung-muenchen/#termin")
soup = BeautifulSoup(resp, 'html.parser')
print(soup.prettify())