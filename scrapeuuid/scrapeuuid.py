from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import threading
import csv
import re
import pdb
import gc
import tkinter as tk
from tkinter import filedialog

stop_scraping = False

def check_class_existence(html, class_name):
    soup = BeautifulSoup(html, 'html.parser')
    return bool(soup.find_all(class_=class_name))

def get_hrefs_and_texts(soup, class_name):
    elements = soup.find_all('span', class_=class_name)
    hrefs_texts = []
    seen_hrefs = set()  # Set to track seen hrefs

    for elem in elements:
        a_tag = elem.find('a')
        if a_tag and a_tag.has_attr('href'):
            href = a_tag['href']
            if href not in seen_hrefs:  # Check if the href is unique
                seen_hrefs.add(href)  # Add the href to the set
                text = a_tag.get_text()
                aria_label = a_tag.get('aria-label', '')
                # Extract numbers from the text
                numbers = re.findall(r'\d+', text)
                numbers1 = re.findall(r'\d+', href)
                number_part = numbers1[1] if numbers else None
                
                hrefs_texts.append((aria_label, numbers1[1]))

    return hrefs_texts

def scroll_page(browser):
    global stop_scraping
    interval=3
    while not stop_scraping:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(interval)

scroll_started_event = threading.Event()

def scrape_website(url, email, password, file_directory):
    try:
        gc.collect()
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        browser.get("https://www.facebook.com/")
        time.sleep(5)

        if not check_class_existence(browser.page_source, "fbIndex"):
            return "Facebook login page not loaded properly."

        browser.find_element(By.ID, "email").send_keys(email)
        browser.find_element(By.ID, "pass").send_keys(password)
        browser.find_element(By.ID, "pass").send_keys(Keys.RETURN)
        time.sleep(5)

        browser.get(url)
        time.sleep(5)

        # Start scrolling thread
        global stop_scraping
        stop_scraping = False
        while not stop_scraping:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("Scrolling...")
            time.sleep(3)  # Simulating a time-consuming task
        print("Stopped scraping.")
        # Extract data
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        hrefs = get_hrefs_and_texts(soup, "xt0psk2")
        # Open or create a CSV file to append data
        try:
            with open(file_directory+"\\result.csv", 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
            
                # Write headers if the file is newly created
                if file.tell() == 0:
                    writer.writerow(["Profile ID", "Name"])  # Column headers

                # Write data
                    for href_text in hrefs:    
                        print(href_text)
                        writer.writerow([href_text[0], href_text[1]])  # Ensure href_text elements are passed as a list
        except Exception as e:
            print(f"An error occurred while processing {href_text}: {e}")


        return hrefs

    except Exception as e:
        return f"An error occurred: {e}"

    finally:
        browser.quit()

def on_start(browser):
    global scroll_thread
    scroll_thread = threading.Thread(target=start_scraping, args=(browser,))
    scroll_thread.start()
    scroll_started_event.set()
    scroll_started_event.wait()

def start_scraping(browser):
    global stop_scraping
    stop_scraping = False
    while not stop_scraping:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Scrolling...")
        time.sleep(3)  # Simulating a time-consuming task
    print("Stopped scraping.")

def run_program(link, email, password, folder_path):
    # Here you can add the code to run your program with these inputs
    scraping_thread = threading.Thread(target=scrape_website, args=(link, email, password, folder_path))
    scraping_thread.start()

class MyGui:
    def __init__(self, root):
        self.root = root
        # Create the main window

        # Create and pack widgets for email input
        tk.Label(root, text="Email:").pack()
        email_entry = tk.Entry(root)
        email_entry.pack()

        # Create and pack widgets for password input
        tk.Label(root, text="Password:").pack()
        password_entry = tk.Entry(root, show="*")  # 'show="*"' to hide password
        password_entry.pack()

        # Button to open the folder dialog
        open_folder_button = tk.Button(root, text="Open Folder", command=open_folder_dialog)
        open_folder_button.pack()

        # Create and pack widgets for link input
        tk.Label(root, text="Link:").pack()
        link_entry = tk.Entry(root)
        link_entry.pack()

        # Label to display the selected folder path
        global folder_path_label
        folder_path_label = tk.Label(root, text="No folder selected")
        folder_path_label.pack()

        # Create a submit button
        submit_button = tk.Button(root, text="Run Program", command=lambda: run_program(link_entry.get(), email_entry.get(), password_entry.get(), folder_path_label.cget("text")))
        submit_button.pack()

        stop_button = tk.Button(root, text="Stop Scraping", command=on_stop)
        stop_button.pack()

    def start_thread(self):
        self.label.config(text="Thread Running...")
        worker = threading.Thread(target=self.long_running_task)
        worker.start()

    def long_running_task(self):
        # Simulating a long-running task
        time.sleep(5)
        self.update_gui()

    def update_gui(self):
        # Ensure GUI updates happen on the main thread
        if self.root:
            self.root.after(0, self.label.config, {"text": "Task Finished"})

def open_folder_dialog():
    folder_path = filedialog.askdirectory()  # Opens the folder dialog
    if folder_path:
        folder_path_label.config(text=folder_path)  # Displays the selected folder path

def on_stop():
    global stop_scraping
    stop_scraping = True
    

# Start the GUI event loop
root = tk.Tk()
my_gui = MyGui(root)
root.title("Scrape UUID")
root.mainloop()