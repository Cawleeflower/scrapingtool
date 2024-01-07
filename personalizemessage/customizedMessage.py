import pandas as pd
import tkinter as tk
from tkinter import filedialog
import gc

new_df = pd.DataFrame()

# Read the Excel file
def get_data(row):
        data = {
            'name': row['name'],
            'profile_id': row['profile_id'],
            'state': row['state'],
            'city': row['city'],
            'WorksAs': row['WorksAs'],
            'WentTo': row['WentTo'],
            'Hobbies': row['Hobbies'],
            'College': row['College'],
            'Relationship': row['Relationship'],
            'Marriage': row['Marriage'],
            'Preferred Language': row['Preferred Language'],
            'IceBreaker': None
        }
        # Append the dictionary to the list
        
        return data
# Function to create a customized message
def check_row_data_exist(row):

    data = {"name": True, 
                "profile_id": True, 
                "state": None, 
                "city": None, 
                "WorksAs": None, 
                "WentTo": None, 
                "Hobbies": [], 
                "College": None,
                "Relationship": None,
                "Marriage": None,
                "Preferred Language": None}

    has_state = pd.notna(row['state'])
    has_city = pd.notna(row['city'])
    has_works_as = pd.notna(row['WorksAs'])
    has_went_to = pd.notna(row['WentTo'])
    has_hobbies = pd.notna(row['Hobbies'])
    has_college = pd.notna(row['College'])
    has_relationship = pd.notna(row['Relationship'])
    has_marriage = pd.notna(row['Marriage'])
    has_preferred_language = pd.notna(row['Preferred Language'])

    data["state"] = has_state
    data["city"] = has_city
    data["WorksAs"] = has_works_as
    data["WentTo"] = has_went_to
    data["College"] = has_college
    data["Relationship"] = has_relationship
    data["Marriage"] = has_marriage
    data["Preferred Language"] = has_preferred_language

    return data

def generate_messages(of, tf):
    tf = tf + "\\icebreaker.xlsx"
    df = pd.read_csv(of)
    
    new_df = pd.DataFrame()

    for index, row in df.iterrows():
        data_exist = check_row_data_exist(row)
        data = get_data(row)

        icebreaker = ""
        name = data["name"]
        city = data["city"]
        state = data["state"]
        WorksAs = data["WorksAs"]
        WentTo = data["WentTo"]
        College = data["College"]
        Relationship = data["Relationship"]
        Marriage = data["Marriage"]
        if data["Preferred Language"] == "zh-cn":
            
            if data["city"] == "Kuantan" or data["city"] == "Pahang":

                icebreaker = f"你好邻居！成为{city}的一部分感觉真好吧？祝你有一个充满我们周围所有当地乐趣的一天。"
                
            elif data_exist["city"]:
                
                icebreaker = f"你好{name}！愿你的每一天都充满阳光和灵感。"

            elif data_exist["state"]:
                icebreaker = f"你好{name}！愿你的每一天都充满阳光和灵感。"
            
            elif data_exist["Relationship"]:
                icebreaker = f"嘿{name}，希望您能与您的特别之人一起享受生活中这美好章节的每一刻。"
                
            elif data_exist["Marriage"] and Marriage == "Married":
                icebreaker = f"嘿{name}，愿你的婚姻生活充满爱与欢笑，每一天都像故事书中的美好篇章。"
            elif data_exist["WorksAs"]:
                icebreaker = f"你好{name}，我注意到您在{WorksAs}工作。能遇到来自如此受尊敬的组织的人总是很有趣。"
            else:
                icebreaker = f"你好{name}！愿你的每一天都充满阳光和灵感。"
        elif data["Preferred Language"] == "en":
            if data["city"] == "Kuantan" or data["city"] == "Pahang":

                icebreaker = f"Hello from across {city}! Always a pleasure to greet someone from our community."
                
            elif data_exist["city"]:
                
                icebreaker = f"Hi {name}, reaching out to you in {city}. May your experiences today be as diverse and rich as your city's culture."
            
            elif data_exist["state"]:
                icebreaker = f"Hi {name}, reaching out to you in {state}. May your experiences today be as diverse and rich as your city's culture."
            
            elif data_exist["Relationship"]:
                icebreaker = f"Hey {name}, hope you're enjoying every moment of this amazing chapter in your life with your special someone."
            
            elif data_exist["Marriage"] and Marriage == "Married":
                icebreaker = f"Hi {name}, wishing you both a life filled with love, understanding, and countless cherished moments together."
            elif data_exist["WorksAs"]:
                icebreaker = f"Hello {name}, I noticed you're with {WorksAs}. It's always intriguing to meet someone from such a well-regarded organization"
            else:
                icebreaker = f"Good day {name}! Thrilled to connect with you. Wishing you a journey filled with happiness and exciting discoveries."
        data["IceBreaker"] = icebreaker
        # Check if 'df' exists and is a DataFrame
        is_null_df_null = new_df is None
        if is_null_df_null:
            new_df = pd.DataFrame([data])
        if 'df' in locals() or 'df' in globals():
            if isinstance(new_df, pd.DataFrame):
                # Create a new DataFrame from the data
                newnew_df = pd.DataFrame([data]) 
                # num_rows = df.shape[0]
                # print(newnew_df.head(5))
                # print("Number of records:", num_rows)
                # print("---")
                # print(newnew_df.head(5))
                # print("Number of records:", num_rows)
                # Append new data to existing 'df'
                new_df = pd.concat([new_df, newnew_df], ignore_index=True)
        
        print(new_df.head(5))

        #replace new_file_name with original_file to replace    
        new_df.to_excel(tf, index=False)

print(f'Data written')


def open_folder_dialog():
    folder_path = filedialog.askopenfilename()  # Opens the folder dialog
    if folder_path:
        folder_path_label.config(text=folder_path)  # Displays the selected folder path

def open_folder_dialog1():
    folder_path1 = filedialog.askdirectory()  # Opens the folder dialog
    if folder_path1:
        folder_path_label1.config(text=folder_path1)  # Displays the selected folder path

class MyGui:
    def __init__(self, root):
        self.root = root

        # Button to open the folder dialog
        open_folder_button = tk.Button(root, text="Locate your output.csv", command=open_folder_dialog)
        open_folder_button.pack()

        # Label to display the selected folder path
        global folder_path_label
        folder_path_label = tk.Label(root, text="No folder selected")
        folder_path_label.pack()

        # Button to open the folder dialog
        open_folder_button = tk.Button(root, text="Locate your folder path to output your file", command=open_folder_dialog1)
        open_folder_button.pack()

        # Label to display the selected folder path
        global folder_path_label1
        folder_path_label1 = tk.Label(root, text="No folder selected")
        folder_path_label1.pack()

        # Create a submit button
        submit_button = tk.Button(root, text="Run Program", command=lambda: generate_messages(folder_path_label.cget("text"), folder_path_label1.cget("text")))
        submit_button.pack()

root = tk.Tk()
my_gui = MyGui(root)
root.title("Scrape Members Info")
root.mainloop()