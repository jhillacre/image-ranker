import os
from tkinter import Tk
from unittest.mock import MagicMock, Mock, patch

import pytest
from PIL import Image, ImageTk

from image_ranker import ImageRanker


@pytest.fixture(scope="function")
def image_ranker_app():
    root = Tk()
    app = ImageRanker(root, setup_ui=False)
    app.setup_ui()  # Now set up the UI after all test setup is complete
    root.withdraw()
    yield app
    root.destroy()


def test_initialization(image_ranker_app):
    """Test that initial widgets are set up correctly."""
    assert image_ranker_app.select_folder_button is not None
    assert image_ranker_app.select_folder_button.winfo_manager() != ""


def test_select_folder(mocker, image_ranker_app):
    """Test selecting a folder sets the folder path correctly."""
    mocker.patch("tkinter.filedialog.askdirectory", return_value="/path/to/images")
    mocker.patch("os.listdir", return_value=["image1.jpg", "image2.jpg"])
    image_ranker_app.select_folder()
    assert image_ranker_app.folder_label["text"] == "/path/to/images"
    assert os.path.join("/path/to/images", "image1.jpg") in image_ranker_app.images
    assert os.path.join("/path/to/images", "image2.jpg") in image_ranker_app.images


def test_start_tournament(image_ranker_app, mocker):
    """Test starting the tournament updates the mode and UI correctly."""
    mocker.patch("tkinter.filedialog.askdirectory", return_value="/path/to/images")
    mocker.patch("os.listdir", return_value=["image1.jpg", "image2.jpg"])
    mock_update_images = mocker.patch.object(ImageRanker, "update_images")

    image_ranker_app.select_folder()
    image_ranker_app.start_tournament()

    mock_update_images.assert_called_once()
    assert image_ranker_app.mode == ImageRanker.PICK_WINNER


def test_select_winner_image1(image_ranker_app, mocker):
    """Test selecting a winner and moving to next match or standings."""
    # Setup a simulated generator
    mocker.patch.object(ImageRanker, "update_images")
    mocker.patch.object(ImageRanker, "update_ui")

    # Simulate the generator manually since the actual logic depends on real file paths
    image_ranker_app.image1_name = "/path/to/image1.jpg"
    image_ranker_app.image2_name = "/path/to/image2.jpg"
    image_ranker_app.gen = MagicMock()
    image_ranker_app.gen.send.side_effect = [
        ("/path/to/image3.jpg", "/path/to/image4.jpg"),
        StopIteration(),
    ]

    image_ranker_app.select_image1()

    image_ranker_app.update_images.assert_called_once()
    image_ranker_app.update_ui.assert_not_called()

    image_ranker_app.gen.send.assert_called_once_with("/path/to/image1.jpg")


def test_select_winner_image2(image_ranker_app, mocker):
    """Test selecting a winner and moving to next match or standings."""
    # Setup a simulated generator
    mocker.patch.object(ImageRanker, "update_images")
    mocker.patch.object(ImageRanker, "update_ui")

    # Simulate the generator manually since the actual logic depends on real file paths
    image_ranker_app.image1_name = "/path/to/image1.jpg"
    image_ranker_app.image2_name = "/path/to/image2.jpg"
    image_ranker_app.gen = MagicMock()
    image_ranker_app.gen.send.side_effect = [
        ("/path/to/image3.jpg", "/path/to/image4.jpg"),
        StopIteration(),
    ]

    image_ranker_app.select_image2()

    image_ranker_app.update_images.assert_called_once()
    image_ranker_app.update_ui.assert_not_called()

    image_ranker_app.gen.send.assert_called_once_with("/path/to/image2.jpg")


def test_select_winner_image1_done(image_ranker_app, mocker):
    """Test selecting a winner and moving to next match or standings."""
    # Setup a simulated generator
    mocker.patch.object(ImageRanker, "update_images")
    mocker.patch.object(ImageRanker, "update_ui")

    # Simulate the generator manually since the actual logic depends on real file paths
    image_ranker_app.image1_name = "/path/to/image1.jpg"
    image_ranker_app.image2_name = "/path/to/image2.jpg"
    image_ranker_app.gen = MagicMock()
    image_ranker_app.gen.send.side_effect = [StopIteration()]

    image_ranker_app.select_image1()

    image_ranker_app.update_images.assert_not_called()
    image_ranker_app.update_ui.assert_called_once()

    image_ranker_app.gen.send.assert_called_once_with("/path/to/image1.jpg")


def test_select_winner_image2_done(image_ranker_app, mocker):
    """Test selecting a winner and moving to next match or standings."""
    # Setup a simulated generator
    mocker.patch.object(ImageRanker, "update_images")
    mocker.patch.object(ImageRanker, "update_ui")

    # Simulate the generator manually since the actual logic depends on real file paths
    image_ranker_app.image1_name = "/path/to/image1.jpg"
    image_ranker_app.image2_name = "/path/to/image2.jpg"
    image_ranker_app.gen = MagicMock()
    image_ranker_app.gen.send.side_effect = [StopIteration()]

    image_ranker_app.select_image2()

    image_ranker_app.update_images.assert_not_called()
    image_ranker_app.update_ui.assert_called_once()

    image_ranker_app.gen.send.assert_called_once_with("/path/to/image2.jpg")


def test_final_standings(image_ranker_app, mocker):
    """Test final standings are shown when tournament is over."""
    mocker.patch.object(ImageRanker, "update_images")
    mocker.patch.object(ImageRanker, "update_ui")

    image_ranker_app.image1_name = "/path/to/image1.jpg"
    image_ranker_app.image2_name = "/path/to/image2.jpg"
    image_ranker_app.gen = MagicMock()
    image_ranker_app.gen.send.side_effect = [
        StopIteration(["/path/to/image1.jpg", "/path/to/image2.jpg"]),
    ]
    image_ranker_app.select_image1()

    image_ranker_app.update_images.assert_not_called()
    image_ranker_app.update_ui.assert_called_once()
    assert image_ranker_app.mode == ImageRanker.SHOW_STANDINGS
    assert image_ranker_app.final_standings == [
        "/path/to/image1.jpg",
        "/path/to/image2.jpg",
    ]


def test_update_images(image_ranker_app):
    """Test images are updated correctly."""
    # Create mock images
    image1 = Image.new("RGB", (100, 100))
    image2 = Image.new("RGB", (100, 100))
    image1_path = "/fake/path/image1.jpg"
    image2_path = "/fake/path/image2.jpg"

    # Use patch to replace Image.open to return a mock Image
    with patch("PIL.Image.open", side_effect=[image1, image2]):
        image_ranker_app.update_images(image1_path, image2_path)

    assert isinstance(image_ranker_app.image1_tk, ImageTk.PhotoImage)
    assert isinstance(image_ranker_app.image2_tk, ImageTk.PhotoImage)


def test_update_ui(image_ranker_app):
    """Test UI is updated correctly based on mode."""
    image_ranker_app.mode = ImageRanker.PICK_WINNER
    image_ranker_app.update_ui()
    assert image_ranker_app.image1_button.winfo_manager() != ""
    assert image_ranker_app.image2_button.winfo_manager() != ""

    image_ranker_app.mode = ImageRanker.SHOW_STANDINGS
    image_ranker_app.final_standings = ["/path/to/image1.jpg", "/path/to/image2.jpg"]
    image_ranker_app.update_ui()
    assert not image_ranker_app.image1_button.winfo_manager()
    assert not image_ranker_app.image2_button.winfo_manager()
    assert image_ranker_app.standings_text.winfo_manager() != ""
