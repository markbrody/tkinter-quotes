#!/usr/bin/env python3

import json
import random
import tkinter as tk
from tkinter.font import Font
import requests

class Gui(tk.Tk):
    """
    Main GUI designed for 1920x1080. Adjust "wraplength" and "padx" values as 
    necessary.
    """
    def __init__(self, *args, **kwargs):

        self.PADDING_X = 360

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("{0}x{1}+0+0".format(width, height))
        self.title("Quote of the Day")
        self.overrideredirect(1)

        self.quote = tk.StringVar()
        self.author = tk.StringVar()

        quote_frame = tk.Frame(bg="#dcdcda")
        quote_frame.pack(fill=tk.X)

        quote_args = {
            "bg": "#dcdcda",
            "wraplength": width - self.PADDING_X * 2,
            "justify": "left",
            "textvariable": self.quote,
        }
        quote_font = Font(family="Open Sans", size=48, slant="italic")
        quote_label = tk.Label(quote_frame, **quote_args)
        quote_label.configure(font=quote_font)
        quote_label.grid(padx=(self.PADDING_X, 0), pady=(50, 0))

        author_frame = tk.Frame(bg="#dcdcda")
        author_frame.pack(fill=tk.BOTH, expand=True)

        author_args = {
            "bg": "#dcdcda",
            "textvariable": self.author,
        }
        author_font = Font(family="Open Sans", size=32)
        author_label = tk.Label(author_frame, **author_args)
        author_label.configure(font=author_font)
        author_label.grid(padx=(self.PADDING_X, 0), pady=(50, 0))

        footer_frame = tk.Frame(bg="#dcdcda")
        footer_frame.pack(fill=tk.BOTH)

        quit_args = {
            "command": self.quit,
            "text": "Quit",
            "bg": "#ffffff",
            "borderwidth": 0,
        }
        quit_button = tk.Button(footer_frame, **quit_args)
        quit_button.pack(side=tk.RIGHT, padx=(2,15), pady=15)

        update_args = {
            "command": self.update,
            "text": "Update",
            "bg": "#ffffff",
            "borderwidth": 0
        }
        update_button = tk.Button(footer_frame, **update_args)
        update_button.pack(side=tk.RIGHT, pady=15)

        self.update()

    def update(self):
        """ Update labels """
        try:
            request = self.request()
            quote = request['contents']['quotes'][0]
            self.quote.set(quote['quote'])
            self.author.set(f"- {quote['author']}")
        except:
            pass

    def request(self):
        """ Query TheySaidSo API """
        categories = ["inspire", "management", "sports", "life", "funny",
                      "love", "art", "students", ]
        category = random.choice(categories)
        url = f"http://quotes.rest/qod.json?category={category}"
        response = requests.request("GET", url)
        print(response.text)
        return json.loads(response.text)

def main():
    """ Run main GUI """
    gui = Gui()
    gui.mainloop()

if __name__ == "__main__":
    main()
