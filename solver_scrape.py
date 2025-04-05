from typing import List
import requests
import time
from bs4 import BeautifulSoup, NavigableString
from selenium import webdriver
import re
import pickle

def remove_special_characters(input_string: str) -> str:
    # Replace anything that is not a letter, number, underscore, or space
    result = re.sub(r'[^\w\s-]', '', input_string)
    
    return result

def fetch_puzzle_names(url: str) -> List[str]:
    result = []
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all article titles based on the assumed structure
        puzzle_names = soup.find_all('span', class_='name')
        # Print all found article titles
        for name in puzzle_names:
            result.append(remove_special_characters(name.get_text()))
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
    return result

def fetch_solvers(url: str, driver) -> List[str]:
    names = []
    driver.get(url)
    time.sleep(5)

    try:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find all article titles based on the assumed structure
        p_tag = soup.find('p', class_='correct-submissions margin-top-20')
        names = list(p_tag.stripped_strings)
        # Check if the <p> tag was found
        if not p_tag:
            print("No solvers!")
    except AttributeError:
        print("Invalid puzzle URL.")
    
    return names

def main():
    PREFIX = "https://www.janestreet.com/puzzles"
    PAGES = 10

    # get all puzzle names
    first_page_url = PREFIX + "/archive/index.html"
    names = []
    for page_num in range(1, PAGES + 1):
        url = first_page_url
        if page_num > 1:
            url = PREFIX + f"/archive/page{page_num}/index.html"
        names = names + fetch_puzzle_names(url)
    names.pop(0)  # remove the most recent puzzle
    
    # create solution page urls
    solution_urls = []
    suffix = "-solution"
    for i in range(len(names)):
        subpage = '-'.join(names[i].split()).lower() + suffix
        solution_urls.append(PREFIX + f"/{subpage}")

    # get all solver names
    solvers_counts = {}
    solvers_puzzles = {}
    driver = webdriver.Chrome()
    for i, url in enumerate(solution_urls):
        print(url)
        solvers = fetch_solvers(url, driver)
        for solver in solvers:
            if solver not in solvers_counts:
                solvers_counts[solver] = 0
            solvers_counts[solver] += 1
            if solver not in solvers_puzzles:
                solvers_puzzles[solver] = []
            solvers_puzzles[solver].append(names[i])
    
    with open("solvers_counts.pkl", "wb") as fp:
        pickle.dump(solvers_counts, fp)
        print("solvers_counts stored to pkl file.")
    
    with open("solvers_puzzles.pkl", "wb") as fp:
        pickle.dump(solvers_puzzles, fp)
        print("solvers_puzzles stored to pkl file.")

if __name__ == "__main__":
    main()


    
