# object-detection-app

This project is an object detection application built using Python, leveraging the YOLO (You Only Look Once) model for real-time object detection. The application features a graphical user interface (GUI) built with PyQt5, allowing users to start and stop detection easily.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [License](#license)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/object-detection-app.git
   cd object-detection-app
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Use the "Start Detection" button to begin object detection using your webcam. Click "Stop Detection" to halt the process.

## Project Structure

```
object-detection-app
├── src
│   ├── core
│   ├── gui
│   ├── utils
│   └── config
├── models
├── tests
├── requirements.txt
├── main.py
└── README.md
```

- **src/core**: Contains the core functionality, including camera handling and object detection logic.
- **src/gui**: Contains the GUI components and layout.
- **src/utils**: Utility functions for image processing.
- **src/config**: Configuration settings for the application.
- **models**: Directory for storing model weights.
- **tests**: Unit tests for the application components.
- **requirements.txt**: Lists the required Python packages.
- **main.py**: Entry point for the application.

## Dependencies

- PyQt5
- OpenCV
- Ultralytics

## License

This project is licensed under the MIT License. See the LICENSE file for details.