import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import imageio
import random

# Main Settings
class Settings:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main Page")
        self.root.geometry("600x500")
        self.root.configure(bg="gray")

        self.label = tk.Label(
            self.root,
            text="Welcome to the game",
            bg="wheat",
            fg="gray",
            font=("Arial", 30),
            padx=20,
            pady=20,
        )
        self.label.pack()

        self.labelname = tk.Label(
            text="Player Name?", bg="gray", fg="wheat", font=("Arial", 20)
        )
        self.labelname.pack()

        self.textbox = tk.Entry(bg="darkred", font=("Arial", 15))
        self.textbox.pack()

        self.label1 = tk.Label(
            self.root,
            text="Do you want to play?",
            font=("Arial", 25),
            fg="wheat",
            bg="gray",
            padx=15,
            pady=15,
        )
        self.label1.pack()

        self.frame = tk.Frame(self.root, background="red")
        self.frame.pack()

        self.button1 = tk.Button(
            self.frame, text="Yes", fg="red", command=self.yes_pressed
        )
        self.button1.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.button2 = tk.Button(
            self.frame, text="No", fg="red", command=self.no_pressed
        )
        self.button2.grid(row=0, column=1)

        self.root.mainloop()
    # If user clicks yes
    def yes_pressed(self):
        player = self.textbox.get().strip()
        if player:
            self.root.withdraw()
            game_instance = Game(self.root)
            game_instance.yes_start()
        else:
            messagebox.showinfo("Error", "Please enter your name.")
    # If user clicka no
    def no_pressed(self):
        self.root.destroy()

# When user clicks yes, this is the main game
class Game:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.images = []
        self.items = []
        self.current_frame = 0
        self.load_images()
        self.yes_start()
    # Inputting the gif
    def load_images(self):
        image_path = "santa-pulled-by-reindeer.gif"
        try:
            gif = imageio.mimread(image_path)
            self.images = [Image.fromarray(frame) for frame in gif]
            self.images = [
                img.resize((100, 100), resample=Image.LANCZOS) for img in self.images
            ]
        except UnidentifiedImageError:
            messagebox.showerror("Error", "Failed to load the GIF image.")
            self.root.destroy()

        self.image_index = 0
        self.image_tk = ImageTk.PhotoImage(self.images[self.image_index])
    # Adding the emojis and using random function to add different emojis
    def create_item(self):
        x = random.randint(50, 550)
        y = 0
        emoji = random.choice(["🏃🏻", "👻", "👽", "🐒", "🪿", "🚗", "🫡"])
        item = self.canvas.create_text(
            x, y, text=emoji, font=("Arial", 20), fill="white"
        )
        self.items.append((item, emoji))
    # Adding this function in case the user wants to restart
    def update_items(self):
        if not self.game_running:
            return

        items_to_remove = []

        for item, emoji in self.items:
            try:
                self.canvas.move(item, 0, 2)
                x, y = self.canvas.coords(item)

                if y > 500:
                    items_to_remove.append((item, emoji))
            except tk.TclError:
                items_to_remove.append((item, emoji))

        for item, emoji in items_to_remove:
            self.canvas.delete(item)
            self.create_item()

        items_to_check = self.items.copy()

        for item, emoji in items_to_check:
            if self.check_collision(item, self.mouse):
                self.canvas.delete(item)
                self.items.remove((item, emoji))
                self.update_score(1)

        if len(self.items) > 0:
            self.window.after(100, self.update_items)
        else:
            self.game_running = False
            messagebox.showinfo(
                "Game Over", f"You lost! Your final score: {self.score}"
            )
            self.window.destroy()

    def clear_items(self):
        for item, _ in self.items:
            self.canvas.delete(item)
        self.items = []
        self.create_item()
    # Tracking the emojis location
    def check_collision(self, item, mouse):
        try:
            x1, y1 = self.canvas.coords(item)
            x2, y2 = self.canvas.coords(mouse)
            return x1 - 50 < x2 < x1 + 50 and y1 - 50 < y2 < y1 + 50
        except tk.TclError:
            return False
    # Tracking the user score
    def update_score(self, value):
        self.score += value
        self.score_label.config(text=f"Score: {self.score}")
        self.text_label.config(
            text=f"This game was made by Tamim Dostyar. If the emoji skips from you and hits the bottom of the canvas (screen), then you lose the game."
        )
    # The game's window
    def yes_start(self):
        self.game_running = True
        self.window.title("Start Game")
        self.window.geometry("650x600")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.canvas = tk.Canvas(self.window, width=600, height=500, bg="black")
        self.canvas.pack()

        self.mouse = self.canvas.create_image(
            500, 100, anchor=tk.NW, image=self.image_tk
        )

        self.score = 0
        self.score_label = tk.Label(
            self.window, text="Score: 0", font=("Arial", 14), fg="black", bg="white"
        )
        self.score_label.pack()
        self.try_again_clicked = False
        self.try_game = tk.Button(
            self.window,
            text="Try Again",
            font=("Arial", 14),
            fg="black",
            bg="white",
            command=self.try_again,
        )
        self.try_game.pack()
        self.text_label = tk.Label(
            self.window, text="Note", font=("Arial", 10), fg="black", bg="red"
        )
        self.text_label.pack()
        self.window.bind("<KeyPress>", self.move_mouse)

        self.create_item()
        self.update_items()
        self.update_frame()
        self.window.mainloop()

    def update_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.images)
        self.image_tk = ImageTk.PhotoImage(self.images[self.current_frame])
        self.canvas.itemconfig(self.mouse, image=self.image_tk)
        self.window.after(100, self.update_frame)

        if self.game_running and self.current_frame % 10 == 0:
            self.create_item()

    def move_mouse(self, event):
        key = event.keysym
        if key == "Up":
            self.canvas.move(self.mouse, 0, -10)
        elif key == "Down":
            self.canvas.move(self.mouse, 0, 10)
        elif key == "Left":
            self.canvas.move(self.mouse, -10, 0)
        elif key == "Right":
            self.canvas.move(self.mouse, 10, 0)

    def on_closing(self):
        self.root.deiconify()
        self.window.destroy()
        self.try_again_clicked = False
    # Below allows the user to restart the game by pressing try again
    def try_again(self):
        if self.try_again_clicked:
            return

        # Reset game-related variables
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.text_label.config(
            text="This game was made by Tamim Dostyar. If the emoji skips from you and hits the bottom of the canvas (screen), then you lose the game."
        )

        # Clear items on the canvas
        self.clear_items()

        # Reset game state
        self.game_running = True

        # Restart the game loop
        self.update_items()
        self.update_frame()

        self.try_again_clicked = True

        # Reset the flag after a delay to allow the player to start a new game
        self.window.after(1000, lambda: setattr(self, "try_again_clicked", False))


Settings()
