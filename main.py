import warnings
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os
import tkinter as tk
from tkinter import filedialog

# Filter UserWarning for ignore_ncx
warnings.filterwarnings("ignore", category=UserWarning, module='ebooklib.epub')
# Filter FutureWarning for XML searches
warnings.filterwarnings("ignore", category=FutureWarning, module='ebooklib.epub')

def select_epub_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select EPUB File",
        filetypes=[("EPUB files", "*.epub")]
    )
    root.destroy()  # Close the tkinter window
    return file_path

def epub_to_text(epub_path):
    book = epub.read_epub(epub_path)
    title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else "Unknown Book"
    output_dir = os.path.join('output', sanitize_filename(title))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    chapter_number = 1
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, 'html.parser')
            for br in soup.find_all("br"):
                br.replace_with("\n")
            for p in soup.find_all("p"):
                p.append("\n")
            text = soup.get_text()
            text = clean_text(text)
            # Skip chapters that contain only "cover", "Illustrations", or are empty
            if text.lower() in ["cover", "illustrations"] or not text:
                continue
            if text:
                filename = os.path.join(output_dir, f'{title} - Chapter {chapter_number}.txt')
                with open(filename, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)
                print(f'Chapter {chapter_number} saved to {filename}')
                chapter_number += 1

def clean_text(text):
    text = text.strip()
    if text.lower().startswith('index'):
        text = text[5:].lstrip(' ,.:\n')
    return text

def sanitize_filename(filename):
    invalid = '<>:"/\\|?*'
    for char in invalid:
        filename = filename.replace(char, '')
    return filename

def main():
    epub_path = select_epub_file()
    if epub_path:
        epub_to_text(epub_path)
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()
