import tkinter as tk
import ctypes
import re
import lexical_Analyzer  # importing scanner for token list

global row_num_widget, Editor, Terminal, Terminal_display

# Disable DPI awareness on Windows
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ctypes.windll.shcore.SetProcessDpiAwareness(True)

keyword = ["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", "extern",
           "float", "for", "goto", "if", "int", "long", "register", "return", "short", "signed", "sizeof", "static",
           "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while", "bool",
           "malloc", "calloc", "realloc", "free",
           "printf", "scanf", "fprintf", "fscanf", "fread", "fwrite", "fseek", "fputs", "fgets", "fopen", "fclose" , "rewind", "fgetc", "fgetw", "fputc", "fputs", "ftell"
           ]


def keyword_color(keyword, start, end):
    if keyword == "break" or keyword == "continue" or keyword == "return" or keyword == "goto":  # flow control keywords
        Editor.tag_add("yellow", start, end)
        Editor.tag_config("yellow", foreground="yellow")

    elif keyword == "int" or keyword == "float" or keyword == "double" or keyword == "char" or keyword == "bool" or keyword == "void" or keyword == "long":  # data types
        Editor.tag_add("red", start, end)
        Editor.tag_config("red", foreground="red")

    elif keyword == "while" or keyword == "for" or keyword == "do":  # loops keywords
        Editor.tag_add("pink", start, end)
        Editor.tag_config("pink", foreground="pink")

    elif keyword == "if" or keyword == "else" or keyword == "switch" or keyword == "case"  or keyword == "default":  # decision control keywords
        Editor.tag_add("blue", start, end)
        Editor.tag_config("blue", foreground="blue")

    elif keyword == "auto" or keyword == "register" or keyword == "static" or keyword == "extern" or keyword == "unsigned" or keyword == "signed" or keyword == "const":  # Storage Classes:
        Editor.tag_add("Dark Orange", start, end)
        Editor.tag_config("Dark Orange", foreground="Dark Orange")

    elif keyword == "calloc" or keyword == "malloc" or keyword == "realloc" or keyword == "free":  # Memory Management:
        Editor.tag_add("brown", start, end)
        Editor.tag_config("brown", foreground="brown")

    elif keyword == "enum" or keyword == "struct" or keyword == "volatile" or keyword == "union":  #
        Editor.tag_add("violet", start, end)
        Editor.tag_config("violet", foreground="violet")

    elif keyword == "printf" or keyword == "scanf" or keyword == "volatile" or keyword == "union":  #
        Editor.tag_add("light blue", start, end)
        Editor.tag_config("light blue", foreground="light blue")

    elif keyword == "fprintf" or keyword == "fscanf" or keyword == "fread" or keyword == "fwrite" or keyword == "fseek" or keyword == "fopen" or keyword == "fclose" or keyword == "fgets" or keyword == "fputs" or keyword == "rewind" or keyword == "fgetc" or keyword == "fgetw" or keyword == "fputc" or keyword == "fputs" or keyword == "ftell":  # File Handling
        Editor.tag_add("light blue", start, end)
        Editor.tag_config("light blue", foreground="light blue")


def run_code():
    Terminal_display.delete("1.0", "end")
    user_input = Editor.get("1.0", "end")
    tokens = lexical_Analyzer.scanner(user_input)
    i = 1
    for token in tokens:
        Terminal_display.insert(f"{i}.0", f"{token}\n")
        print(token)
        i += 1


def update_row_numbers(event=None):
    row_num_widget.config(state="normal")  # Enable the Text widget
    row_num_widget.delete("1.0", "end")  # Delete old roe detail information
    num_lines = Editor.index("end-1c").split(".")[0]  # Get the number of lines in the Editor section
    for line_num in range(1, int(num_lines) + 1):  # Insert row numbers into the row_num_widget
        row_num_widget.insert("end", str(line_num) + "\n")
    row_num_widget.config(state="disabled")  # Disable the Text widget


def colorize_text(event):
    add_space()
    global keyword
    # Remove existing tags
    tag_names = Editor.tag_names()
    for tag in tag_names:
        Editor.tag_remove(tag, "1.0", "end")

    text = Editor.get("1.0", "end-1c")  # Get the text from the Text widget

    # Find and colorize preprocessor directives
    for match in re.finditer(r'#(include|define|ifdef|ifndef|endif|if|else|elif)\b', text):
        start = match.start()
        end = match.end()
        Editor.tag_add("Dark Cyan", f"1.0+{start}c", f"1.0+{end}c")
        Editor.tag_config("Dark Cyan", foreground="Dark Cyan")

    # Find and keywords and reserved words
    for key in keyword:
        start = "1.0"
        key_length = len(key)
        while True:
            start = Editor.search(r"\y" + re.escape(key) + r"\y", start, stopindex="end", regexp=True)
            if not start:
                break
            section1 = start.split(".")[0]
            section2 = start.split(".")[1]
            dif = int(section2)  # covert the float section int an int
            dif = dif + key_length  # add the length of the keyword
            end = section1 + "." + f"{dif}"  # convert to string to get the endpoint index of keyword
            keyword_color(key, start, end)
            start = end

    # Find and colorize single line comments
    for match in re.finditer(r'(\/\/[^\n\r]*[\n\r])', text):
        start = match.start()
        end = match.end()
        tag_names = Editor.tag_names()
        for tag in tag_names:
            Editor.tag_remove(tag, f"1.0+{start}c", f"1.0+{end}c")
        Editor.tag_remove("all", f"1.0+{start}c", f"1.0+{end}c")
        Editor.tag_add("gray", f"1.0+{start}c", f"1.0+{end}c")
        Editor.tag_config("gray", foreground="gray")

    # Find and colorize Multi line comments
    for match in re.finditer(r'\/\*[\s\S]*?\*\/', text):
        start = match.start()
        end = match.end()
        tag_names = Editor.tag_names()
        for tag in tag_names:
            Editor.tag_remove(tag, f"1.0+{start}c", f"1.0+{end}c")
        Editor.tag_remove("all", f"1.0+{start}c", f"1.0+{end}c")
        Editor.tag_add("gray", f"1.0+{start}c", f"1.0+{end}c")
        Editor.tag_config("gray", foreground="gray")

    # Find and colorize strings
    for match in re.finditer(r'\"(\\.|[^"])*\"', text):
        start = match.start()
        end = match.end()
        tag_names = Editor.tag_names()
        for tag in tag_names:
            Editor.tag_remove(tag, f"1.0+{start}c", f"1.0+{end}c")
        Editor.tag_add("green", f"1.0+{start}c", f"1.0+{end}c")
        Editor.tag_config("green", foreground="green")


def add_space():  # to Insert a space at the beginning of each line
    current_line = Editor.index(tk.INSERT).split(".")[0]
    current_char = Editor.index(tk.INSERT).split(".")[1]
    if current_char == '0':
        Editor.insert(f"{current_line}.0", " ")


def main():
    global row_num_widget, Editor, Terminal, Terminal_display
    app = tk.Tk()
    # app.state("zoomed")
    app.config(bg='gray')
    app.minsize(1000, 900)

    container = tk.Frame(app, bg="#232B2B")
    container.place(x=0, y=0, relwidth=1, relheight=1)

    # ========================================================= Navigation Bar ========================
    nav_bar_bg = "#242124"
    nav_bar = tk.Frame(container, bg=nav_bar_bg)
    nav_bar.place(x=0, y=0, relwidth=1, height=35)

    nav_bar = tk.Button(nav_bar, bg=nav_bar_bg, text="Run", fg='white', borderwidth=0, border=0, activebackground=nav_bar_bg, activeforeground="green", command=run_code)
    nav_bar.place(x=0, y=0, relwidth=0.05, relheight=1)

    # ======================================================== Editor Section ============================

    Text_Frame = tk.Frame(container, border=0, bg=nav_bar_bg)
    Text_Frame.place(x=0, y=35, relwidth=1, relheight=0.75)

    Editor_color = "#343434"
    row_num_widget = tk.Text(Text_Frame, wrap="none", font=("Courier New", 12), width=4, padx=5, takefocus=0, border=0, background=Editor_color)
    row_num_widget.place(x=0, y=0, width=50, relheight=1)
    row_num_widget.config(state="disabled")

    Editor = tk.Text(Text_Frame, border=0, bg=Editor_color, font=("Courier New", 12), wrap="none", fg='white')
    Editor.place(x=51, y=0, relwidth=1, relheight=1)
    Editor.insert("insert", " ")

    Editor.bind("<Key>", update_row_numbers)  # Bind the update_row_numbers function to changes in the text widget
    Editor.bind("<KeyRelease>", colorize_text)

    # Define a function to synchronize the scrolling of the two widgets
    def sync_scrollbar(*args):
        Editor.yview_moveto(args[0])
        row_num_widget.yview_moveto(args[0])

    # Bind the <Configure> and <MouseWheel> events of both widgets to the synchronization function
    for widget in (Editor, row_num_widget):
        widget.bind("<Configure>", lambda event: sync_scrollbar(event.widget.yview()[0]))
        widget.bind("<MouseWheel>", lambda event: sync_scrollbar(event.widget.yview()[0]))

    # ======================================================== Terminal  Section ============================
    Text_Frame_2 = tk.Frame(container, border=0, bg=nav_bar_bg)
    Text_Frame_2.place(x=0, rely=0.79, relwidth=1, relheight=0.2)

    Terminal_display = tk.Text(Text_Frame_2, border=0, bg=Editor_color, font=("Courier New", 12), wrap="none")
    Terminal_display.place(x=51, y=0, relwidth=1, relheight=1)

    scrollbar2 = tk.Scrollbar(Text_Frame_2, troughcolor=Editor_color, bg=Editor_color)
    scrollbar2.pack(side="right", fill="y")

    # Link the scrollbar to the Text widget
    Terminal_display.config(yscrollcommand=scrollbar2.set)
    scrollbar2.config(command=Terminal_display.yview, bg="blue")

    app.mainloop()


if __name__ == "__main__":
    main()
