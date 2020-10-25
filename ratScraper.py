import requests
from bs4 import BeautifulSoup

# Set read_from_file to true to parse a
# cached page instead of fetching a new copy.
read_from_file = True

# Set split_cue_words to comma separate cue words
split_cue_words = True

if read_from_file:
    page = open("cached_page.html", "r")
    soup = BeautifulSoup(page, 'html.parser')
else:
    page = requests.get("https://www.remote-associates-test.com")
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Save a copy of the page locally
    saved_page = open("cached_page.html", "w")
    saved_page.write(page.text)
    saved_page.close()

results = open("results.csv", "w")
words = ''
answer = ''
difficulty = ''
error_count = 0

for tr in soup.find_all('tr'):
    try:
        words = tr.find('a').contents[0]
    except:
        error_count += 1
        continue
    try:
        answer = tr.find_all('span')[0].contents[0]
    except:
        error_count += 1
        continue
    try:
        difficulty = tr.find_all('span')[1].contents[0]
    except:
        # Some questions don't have difficulties. Assume medium.
        difficulty = "Medium"
        
    if split_cue_words:
        words = words.replace(" / ", ", ")
    results.write("{},{},{}\n".format(words, answer, difficulty))
    
results.close()

# Page's table header looks like a question, so it looks like an error,
# so expected value of error_count is 1.
if error_count > 1:
    print("Error: {} questions not saved".format(error_count))
