import customtkinter as ctk
from tkinter import filedialog
from CTkListbox import *
from CTkPDFViewer import *
from db import Database
from PIL import Image, ImageTk
import tkinter as tk
import ttkvideos as ttkv
from pygame import mixer

# Initialize the custom tkinter module

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

# Initialize the database
db = Database()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Media Library")
        self.geometry(f"{1100}x{700}")
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=340, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nswe")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.search_label = ctk.CTkLabel(self.sidebar_frame, text="Search Media")
        self.search_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20,10))
        self.media_type_label = ctk.CTkLabel(self.sidebar_frame, text="Media Type:")
        self.media_type_label.grid(row=1, column=0, padx=20, pady=20)
        self.media_type_entry = ctk.CTkOptionMenu(self.sidebar_frame, values=["Articles", "Images", "Videos", "Audio"])
        self.media_type_entry.grid(row=1, column=1, padx=20, pady=20)
        self.country_label = ctk.CTkLabel(self.sidebar_frame, text="Country:")
        self.country_label.grid(row=2, column=0, padx=20, pady=20)
        self.country_entry = ctk.CTkEntry(self.sidebar_frame)
        self.country_entry.grid(row=2, column=1, padx=20, pady=20)
        self.title_label = ctk.CTkLabel(self.sidebar_frame, text="Title:")
        self.title_label.grid(row=3, column=0, padx=20, pady=20)
        self.title_entry = ctk.CTkEntry(self.sidebar_frame)
        self.title_entry.grid(row=3, column=1, padx=20, pady=20)
        self.year_label = ctk.CTkLabel(self.sidebar_frame, text="Year:")
        self.year_label.grid(row=4, column=0, padx=20, pady=20)
        self.year_entry = ctk.CTkEntry(self.sidebar_frame)
        self.year_entry.grid(row=4, column=1, padx=20, pady=20)
        self.search_button = ctk.CTkButton(self.sidebar_frame, text="Search", command=self.fetch_media)
        self.search_button.grid(row=5, column=0, columnspan=2, padx=20, pady=30)

        self.middle_frame = ctk.CTkFrame(self, corner_radius=0, width=500)
        self.middle_frame.grid(row=0, column=1, rowspan=3, sticky="nswe")
        self.listbox = CTkListbox(self.middle_frame)
        self.listbox.pack(fill=ctk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.display_media)

        self.right_frame = ctk.CTkFrame(self, corner_radius=0, width=340)
        self.right_frame.grid(row=0, column=2, rowspan=5, sticky="nswe")
        self.upload_button = ctk.CTkButton(self.right_frame, text="Upload Media", command=self.upload_media)
        self.upload_button.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        

    def fetch_media(self):
        media_type = self.media_type_entry.get()
        country = self.country_entry.get()
        title = self.title_entry.get()
        year = self.year_entry.get()
        searchlist = []
        if media_type:
            searchlist.append(media_type)
        if country:
            searchlist.append(f"country = '{country}'")
        if title:
            searchlist.append(f"title LIKE '%{title}%'")
        if year:
            searchlist.append(f"date LIKE '%{year}%'")
        results = db.fetch(searchlist)
        # print(results)
        
        # Clear the listbox before inserting new items
        self.listbox.delete(0, ctk.END)
        
        for result in results:
            self.listbox.insert(ctk.END, result[5])

    def display_media(self, event):
        selected_index = self.listbox.curselection()
        if not selected_index:
            return

        selected_item = self.listbox.get(selected_index)
        # print(selected_item)
        path = str(selected_item[40:])
        media_type, country, metadata = path.split("/")
        title, creator, month, day, year = metadata.split("-")
        date = f"{month}/{day}/{year.split('.')[0]}"

        self.listbox.pack_forget()

        # # Add a return button
        return_button = ctk.CTkButton(self.middle_frame, text="Return", command=self.return_to_list)
        return_button.pack(anchor="nw", padx=10, pady=10)

        # # Display the media (simplified)
        media_label = ctk.CTkLabel(self.middle_frame, text=f"Title: {title}\nCreator: {creator}\nDate: {date}\n")
        media_label.pack(padx=20, pady=5)
        # # You can add code to display the actual media content (e.g., image, video player, etc.) based on media_type
        if media_type.lower() == "articles":
            self.display_text(selected_item)
        if media_type.lower() == "images":
            self.display_image(selected_item)
        # if media_type.lower() == "videos":
        #     self.display_video(selected_item)
        if media_type.lower() == "audio":
            self.display_audio(selected_item)

    def display_text(self, file_path):
        pdf_viewer = CTkPDFViewer(self.middle_frame, file_path)
        pdf_viewer.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

    def display_image(self, file_path):
        image = Image.open(file_path)
        image = image.resize((500, 500), Image.Resampling.LANCZOS)
        
        # Convert the PIL image to a CTkImage
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(500, 500))
        
        # Create a label to hold the image without any text
        image_label = ctk.CTkLabel(self.middle_frame, image=ctk_image, text="")
        image_label.pack(fill=ctk.BOTH, expand=True, padx=20)


    # Not working
    # def display_video(self, file_path):
    #     video_label = ctk.CTkLabel(self.middle_frame, text="")
    #     video_label.pack(fill=ctk.BOTH, expand=True, padx=20)
    #     player = ttkv.Ttkvideos(file_path, video_label, loop=1)
    #     player.play()

    #     # Add a return button to go back to the list
    #     return_button = ctk.CTkButton(self.middle_frame, text="Return", command=self.return_to_list)
    #     return_button.pack(anchor="nw", padx=10, pady=10)

    def display_audio(self, file_path):
        mixer.init()
        mixer.music.load(file_path)
        mixer.music.play()

        #create slider for audio duration
        audio_slider = ctk.CTkSlider(self.middle_frame, from_=0, to=100, orient="horizontal", length=500)
        audio_slider.pack(pady=20)
        audio_slider.set(50)

        #create play and pause buttons
        play_button = ctk.CTkButton(self.middle_frame, text="Play", command=lambda: mixer.music.unpause())
        play_button.pack(pady=20)
        pause_button = ctk.CTkButton(self.middle_frame, text="Pause", command=lambda: mixer.music.pause())

        # Add a return button to go back to the list
        return_button = ctk.CTkButton(self.middle_frame, text="Return", command=self.return_to_list)
        return_button.pack(anchor="nw", padx=10, pady=10)


    def return_to_list(self):
        for widget in self.middle_frame.winfo_children():
            widget.destroy()
        self.listbox = CTkListbox(self.middle_frame)
        self.listbox.pack(fill=ctk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.display_media)


    def upload_media(self):
        file_path = filedialog.askopenfilename()
        path = str(file_path[40:])
        media_type, country, metadata = path.split("/")
        title, creator, month, day, year = metadata.split("-")
        date = f"{month}/{day}/{year.split('.')[0]}"
        db.insert(media_type.lower(), country, title, creator, date, file_path)
            

if __name__ == "__main__":
    app = App()
    app.mainloop()
    