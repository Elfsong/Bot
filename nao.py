from bot import BOT
from tkinter import *

class Application(object):
    def __init__(self):
        # Init bot
        self.bot_init()

        self.window = Tk()
        self.window.title("NAO Simulator")
        x = (self.window.winfo_screenwidth() / 2) - (800 / 2)
        y = (self.window.winfo_screenheight() / 2) - (500 / 2)
        self.window.geometry("%dx%d+%d+%d" % (800, 500, x, y))
        self.window.resizable(0, 0)

        self.line_label = Message(self.window, text="Script Line", font=("Arial Bold", 40), width=600)
        self.line_label.pack(fill=BOTH, pady=10)

        self.actor_label = Label(self.window, text="Actor", font=("Arial Bold", 20), fg="DodgerBlue")
        self.actor_label.pack(fill=X)

        self.movement_label = Label(self.window, text="Movement", font=("Arial Bold", 20), fg="DodgerBlue2")
        self.movement_label.pack(fill=X)

        self.next_button = Button(self.window, text="Start", command=self.next_button_clicked)
        self.next_button.pack(fill=X, side=BOTTOM, padx=20, pady=20)
    
    def bot_init(self):
        self.bot = BOT("NAO")
        self.bot.load_script("script_1")

    def update_display(self, current_line):
        self.line_label.configure(text=current_line.content)
        self.actor_label.configure(text=current_line.actor)
        self.movement_label.configure(text=current_line.movement)
        self.window.update()

    def play_sound(self, current_line):
        if current_line.need_play_audio():
            current_line.play_audio()

    def next_button_clicked(self):
        if not self.bot.has_next_line():
            self.next_button.configure(text="Finished")
            self.next_button.configure(state=DISABLED)
        else:
            current_line_index = self.bot.get_current_line_index()
            current_line = self.bot.memory["script_line"][current_line_index]

            self.next_button.configure(text="Next line")
            self.update_display(current_line)
            self.play_sound(current_line)

            self.bot.set_current_line_index(current_line_index+1)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()

