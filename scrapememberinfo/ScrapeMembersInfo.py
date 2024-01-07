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
import tkinter as tk
from tkinter import filedialog


options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)

def contains_chinese(text):
    # Regular expression that matches any Chinese character
    chinese_char_regex = r'[\u4e00-\u9fff]'
    return re.search(chinese_char_regex, text) is not None

# def contains_malay_word(text):
#     # Path to your Excel file
#     malay_file = 'C:\\Users\\nic35\\FYP\\CommonMalayWords.xlsx'

#     # Read the Excel file
#     df = pd.read_excel(malay_file)

#     # Assuming the words are in a column named 'Word'
#     malay_words = set(word.lower() for word in df['Words'].tolist())

#     # Split the text into individual words
#     text_words = set(word.lower() for word in re.findall(r'\b\w+\b', text))

#     # Check for an exact match in the text words
#     return any(word in text_words for word in malay_words)

# def check_malay_name(text):
#     # Path to your Excel file
#     malay_file = 'C:\\Users\\nic35\\FYP\\MalayNames.xlsx'

#     # Read the Excel file
#     df = pd.read_excel(malay_file)

#     # Assuming the words are in a column named 'Word'
#     malay_words = df['Name'].tolist()
#     text_lower = text.lower()
#     for word in malay_words:
#         if word.lower() in text_lower:
#             return True
#     return False

def detect_language(text):
    try:
        # First, check if the text contains any Chinese characters
        if contains_chinese(text):
            return 'zh-cn'  # Return 'zh-cn' if Chinese characters are found

        # If no Chinese characters are found, use langdetect
        return detect(text)
    except:
        return "Error in language detection"

def get_information(wait):
    try:
        # Wait for the <ul> element to be present
        ul_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.xeuugli.x1r8uery.x1iyjqo2.xs83m0k.xsyo7zv.x16hj40l.x10b6aqq.x1yrsyyn")))

        # # Loop through each element (li) in the ul
        # for li_element in ul_element.find_elements(By.XPATH, "./*"):
            # try:
                # # Find the second div element within the li
                # second_div = li_element.find_elements(By.CLASS_NAME, "x9f619.x1n2onr6.x1ja2u2z.x78zum5.x2lah0s.x1nhvcw1.x1qjc9v5.xozqiw3.x1q0g3np.xexx8yu.xykv574.xbmpl8g.x4cne27.xifccgj")[1]  # Second element

                # # Extract text from the span within the second div
                # span_text = second_div.find_element(By.CLASS_NAME, "x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u.x1yc453h").text

                # print(span_text)
            # except IndexError:
                # print("Second div not found in this element")
            # except Exception as e:
                # print("Error in processing element:", e)

    except Exception as e:
        print("Error during scraping:", e)

def scroll_page(browser, interval=3):
    for _ in range(3):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    time.sleep(interval)

def check_file_exist(folder_path):
    folder_path = folder_path + "\\output.csv"
    try:
        # Check if the file already exists
        if os.path.exists(folder_path):
            # Read the existing data
            df = pd.read_csv(folder_path, encoding='utf-8')
        else:
            # Create a new DataFrame if file does not exist
            df = pd.DataFrame(columns=["name", "profile_id", "state", "city"])
        
        # data["name"] = name
        # data["profile_id"] = profileid
        return df
    except Exception as e:
        print("Error in checking file:", e)

# def get_info(te3, name, profileid, index):
#     try:
          
#         data = {"name": name, "profile_id": profileid, "state": None, "city": None}
        
#         try:
#             # Check if the file already exists
#             if os.path.exists(new_file_name):
#                 # Read the existing data
#                 df = pd.read_csv(new_file_name, encoding='utf-8')
#             else:
#                 # Create a new DataFrame if file does not exist
#                 df = pd.DataFrame(columns=["name", "profile_id", "State", "City", "Work As", "Graduated From", "Single/Married", "Went To", "College", "Relationship", "Marriage"])
            
#             data["name"] = profileid
#             data["profile_id"] = name

#             return df
#         except Exception as e:
#             print("Error in checking file:", e)
        
#         # try:
#             # for elem in te3:
#                 # print(te3)
#                 # if elem:
#                     # text = elem.get_text()
#                     # print(text)
#                     # if "Lives in" in text:
#                         # state = text.split("Lives in")[-1].strip()
                        
#                         # #if pd.isna(df.at[index, "State"]):
#                         # # Extract and assign the state information
#                         # data["state"] = state
#                     # if "From" in text:
#                         # #pd.isna(df.at[index, "City"]):
#                         # # Extract and assign the city information
#                         # city = text.split("From")[-1].strip()
#                         # #df.at[len(df) - 1, "City"] = city
#                         # data["city"] = city
#         # except Exception as e:
#             # print("Error in extracting info: ", e)
         
#         new_df = pd.DataFrame([data])
        
#         # Append the new data to the DataFrame
#         df = pd.concat([df, new_df], ignore_index=True)
        
#         # Write the updated DataFrame back to the Excel file
#         df.to_csv(new_file_name, index=False)
#     except Exception as e:
#         print("Error during scraping:", e)
    
# def append_new_column_into_excel():
#     df = pd.read_csv(excel_file)

#     # Flag to check if any new column is added
#     new_column_added = False

#     # Check if new columns exist; if not, add them
#     for column in ["State", "City", "Work As", "Graduated From", "Single/Married", "Went To", "College", "Relationship", "Marriage", "Preferred Language"]:
#         if column not in df.columns:
#             df[column] = None
#             new_column_added = True  # Set flag as new column is added

#     # Save the DataFrame back to the CSV file only if a new column was added
#     if new_column_added:
#         df.to_csv(excel_file, index=False)
#         print("Updated DataFrame saved to CSV.")
#     else:
#         print("No new column was added.")

def scrape_website(email, password, folder_path, folder_path1):

    ul_element_found = False

    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.set_page_load_timeout(600)
    browser.get("https://www.facebook.com/")

    browser.find_element(By.ID, "email").send_keys(email)
    browser.find_element(By.ID, "pass").send_keys(password)
    browser.find_element(By.ID, "pass").send_keys(Keys.RETURN)
    
    wait = WebDriverWait(webdriver, 10)  # Timeout of 10 seconds
    
    
    df = check_file_exist(folder_path)

    data_file_read_profile = pd.read_csv(folder_path1, encoding='utf-8')

    for index, row in data_file_read_profile.iterrows():

        if stop_scraping:
            break

        data = {"name": row["Profile ID"], 
                "profile_id": row["Name"], 
                "state": None, 
                "city": None, 
                "WorksAs": None, 
                "WentTo": None, 
                "Hobbies": [], 
                "College": None,
                "Relationship": None,
                "Marriage": None,
                "Preferred Language": None}
        placeholder = row["Name"]
        url = f"https://www.facebook.com/profile.php?id={placeholder}"
        
        # if (check_malay_name(row["Profile ID"])):
        #     data["Preferred Language"] = "ms"
            
        #url = "https://www.facebook.com/sammy.loong.56/?show_switched_toast=0&show_invite_to_follow=0&show_switched_tooltip=0&show_podcast_settings=0&show_community_review_changes=0&show_community_rollback=0&show_follower_visibility_disclosure=0"
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        browser.get(url)
        
        try:
            elements = soup.find_all('div', class_="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w xeuugli x1r8uery x1iyjqo2 xs83m0k xsyo7zv x16hj40l x10b6aqq x1yrsyyn")
            #hobbies_parent = soup.find_all('div', class_="x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x1qjc9v5 xozqiw3 x1q0g3np x1pi30zi x1swvt13 xyamay9 xykv574 xbmpl8g x4cne27 xifccgj")
            newsfeed = soup.find_all(attrs={"data-pagelet": "ProfileTimeline"})
            i = 0
            if newsfeed:
                for item in newsfeed:
                    # Scroll down three times
                    scroll_page(browser, 3)
                    elements_with_class = item.find_all(class_="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")
                    print("elements_with_class: ", len(elements_with_class))
                    

                    # Iterate through each found element and process it
                    for element in elements_with_class:
                        if element:
                            text = element.get_text(strip=True)
                            print(text)
                            print(detect_language(text))
                            if (detect_language(text) == "zh-cn"):
                                data["Preferred Language"] = "zh-cn"
                                break
                            else:
                                data["Preferred Language"] = "en"
                        else:
                            print("Element not found.")
                    
                    i = 0
                        # Do something with each element, e.g., print it or extract text
                        # print(element) 
                
                # news = newsfeed.find_all('div', "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
                # print(news)
            for element in elements:
                ul_element = element.find('ul')
                if ul_element:
                    ul_element_found = True
                    div_elements = ul_element.find_all('div')
                    for div in div_elements:
                        spans = div.find_all('span')

                        
                        for span in spans:
                            span_text = span.get_text()
                            if span_text in data.values():
                                
                                break
                            if "Lives in" in span_text:
                                data["state"] = span_text.split("Lives in")[-1].strip()
                            elif "From" in span_text:
                                data["city"] = span_text.split("From")[-1].strip()
                            elif "Works at" in span_text:
                                data["WorksAs"] = span_text.split("Works at")[-1].strip()
                            elif "Went to" in span_text:
                                data["WentTo"] = span_text.split("Went to")[-1].strip()
                            elif "Studies at" in span_text:
                                data["College"] = span_text.split("Studies at")[-1].strip()
                            elif "In a relationship with" in span_text:
                                data["Relationship"] = span_text.split("In a relationship with")[-1].strip()
                            elif "Single" in span_text or "Married" in span_text:
                                data["Marriage"] = span_text
                            
                            break
                    
                    

                    # for div in div_elements:
                        # if div:
                            # intro = div.find('div', class_="x2b8uid x80vd3b x1q0q8m5 xso031l x1l90r2v")
                            # print(div)
                            # #Within each div, find the nested element with the specific class
                            # #te3 = div.find_all('div', class_="xu06os2 x1ok221b")
                            # te3 = div.find('div', class_="xu06os2 x1ok221b")
                            # print(te)
                            # get_info(te3, row['Name'], row['Profile ID'], index)
                                    
                            # if intro:
                                # intro1 = intro.find('span')
                                # if intro1:
                                    # print("Intro: " + intro.get_text())
                            # # target_element1 = div.find('div', class_="x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1nhvcw1 x1qjc9v5 xozqiw3 x1q0g3np xexx8yu xykv574 xbmpl8g x4cne27 xifccgj")
                            # # target_element = div.find('div', class_="x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1nhvcw1 x1qjc9v5 xozqiw3 x1q0g3np xyamay9 xykv574 xbmpl8g x4cne27 xifccgj")
                            # # print(target_element1);
                            # # if target_element or target_element1:
                                # # print("target element found")
                                # # te = div.find('div', class_="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w xeuugli x1r8uery x1iyjqo2 xs83m0k xamitd3 xsyo7zv x16hj40l x10b6aqq x1yrsyyn")
                                # # if te:
                                    # # print("te")
                                    # # te2 = div.find('div', class_="x78zum5 xdt5ytf xz62fqu x16ldp7u")
                                    # # if te2:
                                        # # print("te2")
                                        # # te3 = div.find('div', class_="xu06os2 x1ok221b")
                                        # # if te3:
                                        
                                            # # Find the span element with the specific class within the div
                                            # # span_element = soup.find('span', class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
                                            # # print(span_element);
                                            # # if span_element:
                                                # # print(span_element.get_text())
                                            # # else:
                                                # # print("Span element not found.")
                            
                        # else: 
                            # print("No div found")
                else: 
                    print("No ul element found")

            # if hobbies_parent:
            #     hobbies = hobbies_parent.find_all('div', class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xzsf02u")
            #     for text in hobbies:
            #         data["Hobbies"].append = text
        

        except Exception as e:
            print("Error during scraping:", e)
        
        if ul_element_found:
            ul_element_found = False
            new_df = pd.DataFrame([data])

            # Append the new data to the DataFrame
            df = pd.concat([df, new_df], ignore_index=True)

            num_rows = len(df)

            print("Before: ", num_rows)

            # Write the updated DataFrame back to the Excel file
            df.to_csv(folder_path+"\\output.csv", index=False)

            print("After: ", num_rows)
        
        time.sleep(1)
        gc.collect()

def run_program(link, email, folder_path, file_to_iterate):
    # Here you can add the code to run your program with these inputs
    global stop_scraping
    stop_scraping = False
    scraping_thread = threading.Thread(target=scrape_website, args=(link, email, folder_path, file_to_iterate))
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
        open_folder_button = tk.Button(root, text="Locate your result.csv", command=open_folder_dialog)
        open_folder_button.pack()

        # Label to display the selected folder path
        global folder_path_label
        folder_path_label = tk.Label(root, text="No folder selected")
        folder_path_label.pack()

        # Button to open the folder dialog
        open_folder_button = tk.Button(root, text="Select folder for file output", command=open_folder_dialog1)
        open_folder_button.pack()

        # Label to display the selected folder path
        global folder_path_label1
        folder_path_label1 = tk.Label(root, text="No folder selected")
        folder_path_label1.pack()

        # Create a submit button
        submit_button = tk.Button(root, text="Run Program", command=lambda: run_program(email_entry.get(), password_entry.get(), folder_path_label1.cget("text"), folder_path_label.cget("text")))
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
    folder_path = filedialog.askopenfilename()  # Opens the folder dialog
    if folder_path:
        folder_path_label.config(text=folder_path)  # Displays the selected folder path

def open_folder_dialog1():
    folder_path = filedialog.askdirectory()  # Opens the folder dialog
    if folder_path:
        folder_path_label1.config(text=folder_path)  # Displays the selected folder path

def on_stop():
    global stop_scraping
    stop_scraping = True
    

# Start the GUI event loop
root = tk.Tk()
my_gui = MyGui(root)
root.title("Scrape Members Info")
root.mainloop()
