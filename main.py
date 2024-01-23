import random
from tkinter import *

WIN_BG = "#319DA0"
TEXT_BG = "#85A389"
TIME_FG = "#E40017"
TEST_DURATION = 60       # in seconds

window = Tk()
window.title("Typing Speed Test")
window.geometry("900x800")
window.config(bg=WIN_BG)

window.option_add("*Label.Font", 'SourceCodePro 20')
window.option_add("*Button.Font", 'SourceCodePro 20')


def get_text_data():
    with open("data2.txt") as file:
        data = file.readlines()

    return random.choice(data)


def text_label_handling():

    text = get_text_data()
    global split_pt
    split_pt = 0

    global heading_label
    heading_label = Label(window, text='Test Your Typing speed in 1 Minute!', fg='purple', bg=WIN_BG)
    heading_label.place(relx=0.5, rely=0.2, anchor=S)

    global text_typed
    global text_to_type
    global char_to_type # current character(letter)
    text_typed = Label(window, text=text[0:split_pt], fg="green", bg=TEXT_BG)
    text_to_type = Label(window, text=text[split_pt:], bg=TEXT_BG)
    char_to_type = Label(window, text=text[split_pt], fg='purple', bg=TEXT_BG)

    text_typed.place(relx=0.5, rely=0.5, anchor=E)
    text_to_type.place(relx=0.5, rely=0.5, anchor=W)
    char_to_type.place(relx=0.5, rely=0.6, anchor=N)

    global writable
    writable=True

    window.bind('<Key>', handle_key_press)

    global seconds_passed
    seconds_passed = 0

    global time_label
    time_label = Label(window, text=f'{TEST_DURATION - seconds_passed} Seconds Left...', bg=TEXT_BG, fg=TIME_FG)
    time_label.place(relx=0.5, rely=0.4, anchor=S)

    window.after(TEST_DURATION*1000, end_test)
    window.after(1000, add_second)


def end_test():
    global writable
    writable = False

    total_words = len(text_typed.cget('text').split(' '))            # also gives the speed because the test duration is 1 minute

    time_label.destroy()
    char_to_type.destroy()
    text_to_type.destroy()
    text_typed.destroy()
    heading_label.destroy()

    global result_label
    result_label = Label(window, text=f"Speed (in WPM): {total_words}", bg="#8F4F4F")
    result_label.place(relx=0.5, rely=0.4, anchor=CENTER)

    global retry_btn
    retry_btn = Button(window, text='Restart Test', command=restart_test, bg="#8F4F4F")
    retry_btn.place(relx=0.5, rely=0.6, anchor=CENTER)


def restart_test():
    result_label.destroy()
    retry_btn.destroy()

    text_label_handling()


def add_second():
    global seconds_passed

    if writable:
        seconds_passed += 1
        time_label.configure(text=f'{TEST_DURATION - seconds_passed} Seconds Left...')
        window.after(1000, add_second)


def handle_key_press(event=None):

    try:

        if event.char == text_to_type.cget('text')[0]:

            text_typed.configure(text=text_typed.cget('text') + event.char)
            text_to_type.configure(text=text_to_type.cget('text')[1:])
            char_to_type.configure(text=text_to_type.cget('text')[0])

    except TclError:
        pass


text_label_handling()

window.mainloop()
