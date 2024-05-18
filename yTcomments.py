from selenium import webdriver
from bs4 import BeautifulSoup
import time

def ScrapComment(url):
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    
    # Open the given URL in the browser
    driver.get(url)
    
    # Initialize previous height to 0
    prev_h = 0
    
    # Loop to scroll down the page incrementally
    while True:
        # Execute JavaScript to get the current height of the page
        height = driver.execute_script("""
            function getActualHeight() {
                return Math.max(
                    Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                    Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                    Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                );
            }
            return getActualHeight();
        """)
        
        # Scroll down by 200 pixels
        driver.execute_script(f"window.scrollTo({prev_h}, {prev_h + 200})")
        
        # Wait for the page to load new content (adjust this value based on your network speed)
        time.sleep(10)
        
        # Increment the previous height
        prev_h += 200
        
        # Break the loop if we've reached the bottom of the page
        if prev_h >= height:
            break
    
    # Create a BeautifulSoup object from the page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Close the browser
    driver.quit()
    
    # Select the video title element using CSS selector
    title_text_div = soup.select_one('#container h1')
    title = title_text_div and title_text_div.text
    
    # Select all comment text elements using CSS selector
    comment_div = soup.select("#content #content-text")
    
    # Extract text from each comment element and create a list of comments
    comment_list = [x.text for x in comment_div]
    
    # Print the video title and the list of comments
    print(title, comment_list)

if __name__ == "__main__":
    # List of YouTube video URLs to scrape comments from
    urls = [
        "https://www.youtube.com/watch?v=vn71-FA0qBA",
        "https://www.youtube.com/watch?v=cMJWC-csdK4",
    ]
    
    # Call the ScrapComment function with the first URL
    ScrapComment(urls[0])
