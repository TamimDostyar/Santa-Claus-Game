# Importing necessary libraries
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import imageio
import random


# Class for handling game settings
class Settings:
    def __init__(self):
        # Initialize the main Tkinter window
        self.root = tk.Tk()
        self.root.title("Main Page")
        self.root.geometry("1200x600")
        self.root.configure(bg="gray")

        # Creating labels and entry widgets
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

        # Creating frame and buttons for player response
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

        # Running the Tkinter main loop
        self.root.mainloop()

    # Function to handle 'Yes' button press
    def yes_pressed(self):
        player = self.textbox.get().strip()
        if player:
            # Hide the settings window and start the game
            self.root.withdraw()
            game_instance = Game(self.root)
            game_instance.yes_start()
        else:
            # Show an error message if player name is not entered
            messagebox.showinfo("Error", "Please enter your name.")

    # Function to handle 'No' button press
    def no_pressed(self):
        # Close the settings window
        self.root.destroy()


# Class for the main game functionality
class Game:
    def __init__(self, root):
        # Initialize the game window
        self.root = root
        self.window = tk.Toplevel(root)
        self.images = []
        self.items = []
        self.current_frame = 0
        self.load_images()
        self.yes_start()

    # Function to load game images
    def load_images(self):
        image_path = "santa-pulled-by-reindeer.gif"
        try:
            # Load GIF images and resize them
            gif = imageio.mimread(image_path)
            self.images = [Image.fromarray(frame) for frame in gif]
            self.images = [
                img.resize((100, 100), resample=Image.LANCZOS) for img in self.images
            ]
        except UnidentifiedImageError:
            # Show an error message if loading fails
            messagebox.showerror("Error", "Failed to load the GIF image.")
            self.root.destroy()

        self.image_index = 0
        self.image_tk = ImageTk.PhotoImage(self.images[self.image_index])

    # Function to create game items
    def create_item(self):
        x = random.randint(50, 550)
        y = 0  # Appear from the top
        emoji = random.choice(["🐥", "🐂", "🌝", "🐒"])
        item = self.canvas.create_text(
            x, y, text=emoji, font=("Arial", 20), fill="white"
        )
        self.items.append((item, emoji))

    # Function to update game items and handle collisions
    def update_items(self):
        # Check if the game is running
        if not self.game_running:
            return

        # List to store items to be removed
        items_to_remove = []

        # Loop through each item and update its position
        for item, emoji in self.items:
            try:
                self.canvas.move(item, 0, 2)
                x, y = self.canvas.coords(item)

                # Check if the item has gone beyond the window height
                if y > 500:
                    items_to_remove.append((item, emoji))
            except tk.TclError:
                # Handle TclError that may occur when moving items
                items_to_remove.append((item, emoji))

        # Remove items that have gone beyond the window
        for item, emoji in items_to_remove:
            self.canvas.delete(item)
            self.create_item()

        # List to check for collisions
        items_to_check = self.items.copy()

        # Loop through items to check for collision with the mouse
        for item, emoji in items_to_check:
            if self.check_collision(item, self.mouse):
                self.canvas.delete(item)
                self.items.remove((item, emoji))
                self.update_score(1)

        # Continue updating items if the game is still running
        if len(self.items) > 0:
            self.window.after(100, self.update_items)
        else:
            # End the game if there are no more items
            self.game_running = False
            messagebox.showinfo(
                "Game Over", f"You lost! Your final score: {self.score}"
            )
            self.window.destroy()

    # Function to clear game items
    def clear_items(self):
        # Delete all items from the canvas
        for item, _ in self.items:
            self.canvas.delete(item)
        self.items = []
        # Create a new item to restart the game
        self.create_item()

    # Function to check collision between items and the mouse
    def check_collision(self, item, mouse):
        try:
            x1, y1 = self.canvas.coords(item)
            x2, y2 = self.canvas.coords(mouse)
            # Check if the item and mouse coordinates overlap
            return x1 - 50 < x2 < x1 + 50 and y1 - 50 < y2 < y1 + 50
        except tk.TclError:
            # Handle TclError that may occur when getting item coordinates
            return False

    # Function to update the game score
    def update_score(self, value):
        # Update the score and display it on the labels
        self.score += value
        self.score_label.config(text=f"Score: {self.score}")
        self.text_label.config(
            text=f"This game was made by Tamim Dostyar. If you the emoji skips from you and hits the bottom of the canvas(screen), then you lost the game."
        )

    # Function to start the game
    def yes_start(self):
        # Set the game state to running
        self.game_running = True
        # Set up the game window
        self.window.title("Start Game")
        self.window.geometry("1200x600")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create the canvas for drawing
        self.canvas = tk.Canvas(self.window, width=600, height=500, bg="black")
        self.canvas.pack()

        # Create the mouse character on the canvas
        self.mouse = self.canvas.create_image(
            500, 100, anchor=tk.NW, image=self.image_tk
        )

        # Initialize the score labels
        self.score = 0
        self.score_label = tk.Label(
            self.window, text="Score: 0", font=("Arial", 14), fg="black", bg="white"
        )
        self.score_label.pack()
        self.text_label = tk.Label(
            self.window, text="Note", font=("Arial", 10), fg="black", bg="red"
        )
        self.text_label.pack()
        self.window.bind("<KeyPress>", self.move_mouse)

        # Create the first item to start the game
        self.create_item()
        self.update_items()

        # Update the game frame continuously
        self.update_frame()
        # Running the Tkinter main loop for the game window
        self.window.mainloop()

    # Function to update the game frame
    def update_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.images)
        self.image_tk = ImageTk.PhotoImage(self.images[self.current_frame])
        self.canvas.itemconfig(self.mouse, image=self.image_tk)
        self.window.after(100, self.update_frame)

        # Create a new item every 10 frames
        if self.game_running and self.current_frame % 10 == 0:
            self.create_item()

    # Function to move the mouse in response to key presses
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

    # Function to handle the game window closing
    def on_closing(self):
        # Restore the settings window and close the game window
        self.root.deiconify()
        self.window.destroy()


# Creating an instance of the Settings class to start the game
Settings()
