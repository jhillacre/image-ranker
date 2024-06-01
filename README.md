# Image Ranker App

[![License](https://img.shields.io/badge/BSD_3--Clause-brightgreen.svg?style=for-the-badge)](https://opensource.org/licenses/BSD-3-Clause)
[![Python](https://img.shields.io/badge/python-306998.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

## Description

Image Ranker is a Tkinter application that allows users to rank a local folder of pngs & jpgs in a double elimination tournament.

## Features

- Pick a local folder of images to rank.
- Choose the winner of each match-up.
- View the resulting rankings.
- Copy the rankings to the clipboard.

## Prerequisites

You'll need python, pipenv, and tkinter installed on your system to run the Image Ranker App.

On windows, tkinter is included with Python by default.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/jhillacre/image-ranker.git
    ```

2. Install the dependencies:

    ```bash
    pipenv install
    ```

## Usage

```bash
pipenv run image_ranker.py
```

## Tests

1. Install the testing dependencies:

    ```bash
    pipenv install --dev
    ```

2. Run the tests:

    ```bash
    pipenv run pytest
    ```

## Contributing

Contributions are welcome! If you would like to contribute to the Image Ranker App, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.
