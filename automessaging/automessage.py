import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import threading
import csv
import re
import pdb
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
import os
from langdetect import detect
import gc
import pyautogui
import requests
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tkinter import ttk, filedialog, messagebox


def create_labeled_input(tab, label_text):
    """Helper function to create a labeled input field in a given tab."""
    label = ttk.Label(tab, text=label_text)
    label.pack(padx=10, pady=(10, 0))  # Extra padding on top
    entry = ttk.Entry(tab)
    entry.pack(padx=10, pady=(0, 10))  # Extra padding on bottom
    return entry

def create_labeled_scrolled_text(tab, label_text):
    """Helper function to create a labeled ScrolledText widget in a given tab."""
    label = ttk.Label(tab, text=label_text)
    label.pack(padx=10, pady=(10, 0))  # Extra padding on top
    scrolled_text = ScrolledText(tab, wrap=tk.WORD, height=5)
    scrolled_text.pack(padx=10, pady=(0, 10))  # Extra padding on bottom
    return scrolled_text

def submit_data(email_entry, password_entry, scrolled_texts_tab2, scrolled_texts_tab3, folder_path):
    # Retrieve data from inputs
    email = email_entry.get()
    password = password_entry.get()
    texts_tab2 = [text.get("1.0", tk.END).strip() for text in scrolled_texts_tab2]
    texts_tab3 = [text.get("1.0", tk.END).strip() for text in scrolled_texts_tab3]

    # Call the function with the retrieved data
    process_data(email, password, texts_tab2, texts_tab3, folder_path)

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Update a label or variable with the file path
        selected_file_label.config(text=file_path)
    else:
        messagebox.showinfo("Information", "No file selected")

def process_data(email, password, texts_tab2, texts_tab3, folder_path):
    
    ul_element_found = False
    gc.collect()
    browser = webdriver.Chrome()
    browser.set_page_load_timeout(600)
    browser.get("https://www.messenger.com")
    print("Waiting...")
    time.sleep(5)
    print("Waited finished")
    browser.find_element(By.ID, "email").send_keys(email)
    browser.find_element(By.ID, "pass").send_keys(password)
    browser.find_element(By.ID, "pass").send_keys(Keys.RETURN)

    data_file_read_profile = pd.read_excel(folder_path)

    for index, row in data_file_read_profile.iterrows():
        icebreaker = row["IceBreaker"]
        placeholder = row["profile_id"]
        language_prefence = row["Preferred Language"]

        random_number = random.randint(600, 900)

        url = f"https://www.messenger.com/t/{placeholder}"
        browser.set_page_load_timeout(random_number)
        browser.get(url)

        element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.x78zum5.x1iyjqo2.x1gja9t.x16n37ib.x1xmf6yo.x1e56ztr.xeuugli.x1n2onr6'))
        )
        element_child = element.find_element(By.CSS_SELECTOR, '.xat24cr.xdj266r')

        # element = browser.find_element(By.CSS_SELECTOR, '.x78zum5.x1iyjqo2.x1gja9t.x16n37ib.x1xmf6yo.x1e56ztr.xeuugli.x1n2onr6')
        # element_child = element.find_element(By.CSS_SELECTOR, '.xat24cr.xdj266r')
        if (language_prefence == "en"):
            message = icebreaker + "\n" + random.choice(texts_tab2)
        
        
        elif(language_prefence == "zh-cn"):
            message = icebreaker + "\n" + random.choice(texts_tab3)
           

        for char in message:
            if char == "\n":
                # Perform Shift+Enter for newline
                ActionChains(browser).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
            else:
                element_child.send_keys(char)
            time.sleep(0.04)  # Delay of 0.1 seconds between each character

        element_child.send_keys(Keys.RETURN)
        time.sleep(random_number)
        gc.collect()

    print("Email:", email)
    print("Password:", password)
    print("Texts from Tab 2:", texts_tab2)
    print("Texts from Tab 3:", texts_tab3)

# Create the main window
root = tk.Tk()
root.title("Tabbed Interface with Labeled Inputs")

# Create the Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both', padx=10, pady=10)

# First tab with Email and Password input fields
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Tab 1')
email_entry = create_labeled_input(tab1, "Email")
password_entry = create_labeled_input(tab1, "Password")

select_file_button = ttk.Button(tab1, text="Select File", command=select_file)
select_file_button.pack(pady=10)

selected_file_label = ttk.Label(tab1, text="No file selected")
selected_file_label.pack(pady=10)

# Second tab with three labeled long text inputs
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='English')
scrolled_text_v1_tab2 = create_labeled_scrolled_text(tab2, "Version 1")
scrolled_text_v2_tab2 = create_labeled_scrolled_text(tab2, "Version 2")
scrolled_text_v3_tab2 = create_labeled_scrolled_text(tab2, "Version 3")
scrolled_texts_tab2 = []
scrolled_texts_tab2.append(scrolled_text_v1_tab2)
scrolled_texts_tab2.append(scrolled_text_v2_tab2)
scrolled_texts_tab2.append(scrolled_text_v3_tab2)
# Third tab with three labeled long text inputs
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text='Chinese')
scrolled_text_v1_tab3 = create_labeled_scrolled_text(tab3, "Version 1")
scrolled_text_v2_tab3 = create_labeled_scrolled_text(tab3, "Version 2")
scrolled_text_v3_tab3 = create_labeled_scrolled_text(tab3, "Version 3")
scrolled_texts_tab3 = []
scrolled_texts_tab3.append(scrolled_text_v1_tab3)
scrolled_texts_tab3.append(scrolled_text_v2_tab3)
scrolled_texts_tab3.append(scrolled_text_v3_tab3)

submit_button = ttk.Button(root, text="Submit", command=lambda: submit_data(email_entry, password_entry, scrolled_texts_tab2, scrolled_texts_tab3, selected_file_label.cget("text")))
submit_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
