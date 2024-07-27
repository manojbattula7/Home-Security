# Home Security

Developed a comprehensive home security system leveraging advanced computer vision techniques. The system is designed to detect fire and unauthorized persons in real-time, ensuring enhanced safety and security for homeowners.

## Table of Contents

- [Introduction](#introduction)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Developed a sophisticated home security system using YOLO, OpenCV, and Flask. The system features real-time fire detection and unauthorized person identification, ensuring comprehensive safety and security. Fire detection leverages the YOLO model for quick response, while face recognition technology identifies unauthorized individuals. Integrated with Flask, the system offers a user-friendly web interface for monitoring alerts and accessing logs remotely. This solution enhances home safety by providing immediate notifications and detailed event records.

## System Architecture

![Architecture](https://github.com/user-attachments/assets/39e4ca91-be51-40ac-a8d0-bb88fbaedd50)

## Features

- Real-time video processing using OpenCV.
- Fire detection using YOLO model.
- Unauthorized person detection with face recognition module.
- Audible alerts for immediate threat notifications.
- Detailed logging of events with date, time, and captured frames/images.
- User-friendly web interface with Flask for remote monitoring and management.

## Installation

### Prerequisites

- Python 3.7 or later
- Flask
- OpenCV
- YOLO model files (weights and configuration files)
- Face Recognition libraries
- Webcam (for real-time video capture)


### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Download the pose estimation model and place it in the appropriate directory:

    ```bash
    # Example command to download the model
    wget https://path-to-your-model/movenet_thunder.tflite -P models/
    ```


## Project Structure

```plaintext

```

## Usage

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. Follow the on-screen instructions to select and perform a yoga pose. The system will provide real-time feedback to help you adjust your posture.

## Output Video

Here is a demonstration of the application in action:

https://github.com/user-attachments/assets/0dbc6822-e46e-46c4-9002-9d9c044392bf


## Technologies Used

- **Flask**: Web framework for building the application.
- **OpenCV**: Library for real-time video processing and computer vision tasks.
- **YOLO**: Object detection model used for real-time fire detection.
- **Face Recognition**: Technology for detecting and identifying unauthorized individuals.
- **pyttsx3**: Text-to-speech library for providing audible alerts.
- **HTML/CSS/JavaScript**: Front-end technologies for building the user interface.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with any improvements or new features.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request




