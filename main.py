import os
import threading
import tkinter as tk
from gtts import gTTS
from tkinter import ttk
import speech_recognition as sr
from playsound import playsound
from deep_translator import GoogleTranslator
from google.transliteration import transliterate_text

# Create an instance of Tkinter frame or window
win = tk.Tk()

# Set the geometry of tkinter frame
win.geometry("700x450")
win.title("Real-Time Voice🎙️ Translator🔊")

# Load icon if file exists
icon_path = "icon.png"
if os.path.exists(icon_path):
    icon = tk.PhotoImage(file=icon_path)
    win.iconphoto(False, icon)
else:
    print(f"Warning: '{icon_path}' not found, skipping icon setup.")

# Create labels and text boxes for recognized and translated text
input_label = tk.Label(win, text="Recognized Text ⮯")
input_label.pack()
input_text = tk.Text(win, height=5, width=50)
input_text.pack()

output_label = tk.Label(win, text="Translated Text ⮯")
output_label.pack()
output_text = tk.Text(win, height=5, width=50)
output_text.pack()

blank_space = tk.Label(win, text="")
blank_space.pack()

# Create a dictionary of language names and codes
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-CN",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "German": "de",
    "French": "fr",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Gujarati": "gu",
    "Punjabi": "pa"
}

language_names = list(language_codes.keys())

# Variables to store the selected language codes
selected_input_lang_code = "auto"  # Default: auto detect input language
selected_output_lang_code = "en"   # Default: English output language

# Create dropdown menus for the input and output languages
input_lang_label = tk.Label(win, text="Select Input Language:")
input_lang_label.pack()

input_lang = ttk.Combobox(win, values=language_names)
input_lang.pack()

output_lang_label = tk.Label(win, text="Select Output Language:")
output_lang_label.pack()

output_lang = ttk.Combobox(win, values=language_names)
output_lang.pack()

# Event bindings for input and output language dropdowns
def update_input_lang_code(event):
    global selected_input_lang_code
    selected_language_name = input_lang.get()
    selected_input_lang_code = language_codes.get(selected_language_name, "auto")

def update_output_lang_code(event):
    global selected_output_lang_code
    selected_language_name = output_lang.get()
    selected_output_lang_code = language_codes.get(selected_language_name, "en")

input_lang.bind("<<ComboboxSelected>>", update_input_lang_code)
output_lang.bind("<<ComboboxSelected>>", update_output_lang_code)

blank_space = tk.Label(win, text="")
blank_space.pack()

keep_running = False

# Function to handle the voice translation process
def update_translation():
    global keep_running

    if keep_running:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Speak Now!\n")
            audio = r.listen(source)

            try:
                speech_text = r.recognize_google(audio)
                input_text.insert(tk.END, f"{speech_text}\n")

                if speech_text.lower() in {'exit', 'stop'}:
                    keep_running = False
                    return

                transliterated_text = transliterate_text(speech_text, lang_code=selected_input_lang_code) if selected_input_lang_code not in ('auto', 'en') else speech_text

                # Translation using Google Translator
                translated_text = GoogleTranslator(source=selected_input_lang_code, target=selected_output_lang_code).translate(text=transliterated_text)

                # Speech generation and playback
                voice = gTTS(translated_text, lang=selected_output_lang_code)
                voice.save('voice.mp3')
                playsound('voice.mp3')
                os.remove('voice.mp3')

                output_text.insert(tk.END, translated_text + "\n")

            except sr.UnknownValueError:
                output_text.insert(tk.END, "Could not understand!\n")
            except sr.RequestError:
                output_text.insert(tk.END, "Could not request from Google!\n")

    win.after(100, update_translation)

# Start the translation process in a separate thread
def run_translator():
    global keep_running

    if not keep_running:
        keep_running = True
        translation_thread = threading.Thread(target=update_translation)
        translation_thread.start()

# Stop the execution of the translator
def kill_execution():
    global keep_running
    keep_running = False

# Open the "About" window
def open_about_page():
    about_window = tk.Toplevel()
    about_window.title("About")
    about_window.iconphoto(False, icon)

    github_link = ttk.Label(about_window, text="github.com/SamirPaulb/real-time-voice-translator", underline=True, foreground="blue", cursor="hand2")
    github_link.bind("<Button-1>", lambda e: open_webpage("https://github.com/SamirPaulb/real-time-voice-translator"))
    github_link.pack()

    about_text = tk.Text(about_window, height=10, width=50)
    about_text.insert("1.0", """
    A machine learning project that translates voice from one language to another in real time while preserving the tone and emotion of the speaker, and outputs the result in MP3 format. Choose input and output languages from the dropdown menu and start the translation!
    """)
    about_text.pack()

    close_button = tk.Button(about_window, text="Close", command=about_window.destroy)
    close_button.pack()

# Open a web page in the default browser
def open_webpage(url):
    import webbrowser
    webbrowser.open(url)

# Buttons for running the translator, stopping execution, and opening the About page
run_button = tk.Button(win, text="Start Translation", command=run_translator)
run_button.place(relx=0.25, rely=0.9, anchor="c")

kill_button = tk.Button(win, text="Kill Execution", command=kill_execution)
kill_button.place(relx=0.5, rely=0.9, anchor="c")

about_button = tk.Button(win, text="About this project", command=open_about_page)
about_button.place(relx=0.75, rely=0.9, anchor="c")

# Run the Tkinter event loop
win.mainloop()
