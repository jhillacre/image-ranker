import os
from pathlib import Path
from tkinter import TOP, Button, Label, Tk, filedialog
from typing import Optional

from PIL import Image, ImageTk

from double_elimination_tournament import DoubleEliminationTournament


class ImageRanker:
    """
    Tkinter application to rank images in a double elimination tournament.
    """

    # modes are used to show and hide parts of the UI
    # so that buttons and labels that make sense in one mode
    # are hidden in another mode
    PICK_FOLDER = "pick_folder"
    PICK_WINNER = "pick_winner"
    SHOW_STANDINGS = "show_standings"
    MODES = {
        PICK_FOLDER,
        PICK_WINNER,
        SHOW_STANDINGS,
    }

    def __init__(self, root, setup_ui=True):
        self.root = root
        if setup_ui:
            self.setup_ui()

    def setup_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        # setup all the widgets

        # top of the window centered label
        self.label = Label(self.root, text="Select images to rank")

        # button to select folder, centered under the label
        self.select_folder_button = Button(
            self.root, text="Select Folder", command=self.select_folder
        )

        # label to show the selected folder
        self.folder_label = Label(self.root, text="")

        # button to start the tournament
        self.start_tournament_button = Button(
            self.root,
            text="Start Tournament",
            command=self.start_tournament,
            state="disabled",
        )

        # show the images
        self.image1_name: str = None
        self.image2_name: str = None
        self.image1: Image = None
        self.image2: Image = None
        self.image1_tk: ImageTk = None
        self.image2_tk: ImageTk = None
        self.image1_label = Label(self.root, image=self.image1_tk, text="Image 1")
        self.image2_label = Label(self.root, image=self.image2_tk, text="Image 2")

        # buttons to select the winner
        self.image1_button = Button(
            self.root, text="Select Image 1", command=self.select_image1
        )
        self.image2_button = Button(
            self.root, text="Select Image 2", command=self.select_image2
        )

        # the list of standings at the end of the tournament
        self.standings_text = Label(self.root, text="")

        # button to copy the standings to the clipboard
        self.copy_button = Button(self.root, text="Copy Standings", command=self.copy)

        self.final_standings: Optional[list[str]] = None

        self.mode = self.PICK_FOLDER
        self.update_ui()

    def update_ui(self):
        # clear all grids before updating
        for widget in self.root.winfo_children():
            widget.grid_remove()

        match self.mode:
            case self.PICK_FOLDER:
                self.label.grid(row=0, column=0, columnspan=2, sticky="nsew")
                self.select_folder_button.grid(
                    row=1, column=0, columnspan=2, sticky="ew"
                )
                self.folder_label.grid(row=2, column=0, columnspan=2, sticky="ew")
                self.start_tournament_button.grid(
                    row=3, column=0, columnspan=2, sticky="ew"
                )
            case self.PICK_WINNER:
                self.image1_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
                self.image2_label.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
                self.image1_button.grid(row=1, column=0, sticky="ew")
                self.image2_button.grid(row=1, column=1, sticky="ew")
            case self.SHOW_STANDINGS:
                self.standings_text.grid(row=0, column=0, columnspan=2, sticky="nsew")
                self.copy_button.grid(row=1, column=0, columnspan=2, sticky="ew")
                self.standings_text.config(
                    text="\n".join(
                        f"{i + 1}: {os.path.basename(image)}"
                        for i, image in enumerate(self.final_standings)
                    )
                )

    def select_folder(self):
        """
        Select a folder containing images.
        """
        folder = filedialog.askdirectory()
        folder_path = Path(folder)
        self.folder_label.config(text=str(folder_path))
        # Use pathlib for path operations
        self.images = {str(folder_path / file) for file in os.listdir(folder)}
        if self.images:
            self.start_tournament_button.config(state="normal")

    @staticmethod
    def resize_image(img, max_width, max_height):
        original_width, original_height = img.size
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def update_images(self, image1, image2):
        """
        Open the images and update the UI.
        """
        if image1 is None or image2 is None:
            print("image1 or image2 is None, unexpectedly.", image1, image2)
            # hide the current image
            self.image1_label.config(image=None, text="")
            self.image2_label.config(image=None, text="")
            self.image1_button.config(state="disabled")
            self.image2_button.config(state="disabled")
            return

        self.image1_name = image1
        self.image2_name = image2
        self.image1 = Image.open(image1)
        self.image2 = Image.open(image2)

        # Resize the images  to fit the window, while maintaining the aspect ratio
        max_width = max(1, self.root.winfo_width() // 2)
        max_height = max(1, self.root.winfo_height() * 0.90)

        self.image1 = self.resize_image(self.image1, max_width, max_height)
        self.image2 = self.resize_image(self.image2, max_width, max_height)

        self.image1_tk = ImageTk.PhotoImage(self.image1)
        self.image2_tk = ImageTk.PhotoImage(self.image2)
        self.image1_label.config(
            image=self.image1_tk,
            text=os.path.basename(self.image1_name),
            compound="top",
            anchor="center",
            state="normal",
        )
        self.image2_label.config(
            image=self.image2_tk,
            text=os.path.basename(self.image2_name),
            compound="top",
            anchor="center",
            state="normal",
        )

    def start_tournament(self):
        """
        Start the tournament.
        """
        self.tournament = DoubleEliminationTournament(self.images)
        self.gen = self.tournament.run_tournament()
        self.mode = self.PICK_WINNER
        self.update_ui()
        try:
            (image1, image2) = next(self.gen)
            self.update_images(image1, image2)
        except StopIteration as e:
            self.final_standings = e.value
            self.mode = self.SHOW_STANDINGS
            self.update_ui()

    def select_image1(self):
        """
        Select image 1 as the winner.
        """
        try:
            (image1, image2) = self.gen.send(self.image1_name)
            self.update_images(image1, image2)
        except StopIteration as e:
            self.final_standings = e.value
            self.mode = self.SHOW_STANDINGS
            self.update_ui()

    def select_image2(self):
        """
        Select image 2 as the winner.
        """
        try:
            (image1, image2) = self.gen.send(self.image2_name)
            self.update_images(image1, image2)
        except StopIteration as e:
            self.final_standings = e.value
            self.mode = self.SHOW_STANDINGS
            self.update_ui()

    def copy(self):
        """
        Copy the standings to the clipboard.
        """
        self.root.clipboard_clear()
        self.root.clipboard_append(
            "\n".join([os.path.basename(x) for x in self.final_standings])
        )
        self.root.update()
        self.standings_text.config(text="Copied to clipboard!")


if __name__ == "__main__":
    root = Tk()
    root.title("Image Ranker")
    # start maximized
    root.state("zoomed")
    image_ranker = ImageRanker(root)
    root.mainloop()
