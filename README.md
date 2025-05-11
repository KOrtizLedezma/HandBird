# HandBird

A modern twist on the classic Flappy Bird game — this version lets you jump by making a fist and restart by showing a peace sign, using real-time hand gesture recognition powered by MediaPipe and OpenCV.

## Requirements

**Important:** This project requires Python version `3.10.13` specifically due to compatibility constraints with `mediapipe`.
Using a different version may cause import errors or runtime issues.

## Features
- Gesture Controls
  - Make a peace sign to start or restart the game.
  - Make a fist (only required 4 fingers to be bent) to jump the bird.
- Real-time gesture detection with `mediapipe`

## How to run

- Create a Virtual Environment (Recommended)

```bash
python 3.10.13 -m venv venv
source venv/bin/activate
```
- Install Dependencies
```bash
pip install pygame opencv-python mediapipe
```

- Launch the Game

```bash
python /FlappyBird/main.py
```

## Troubleshooting

- Make sure you're using **Python 3.10.13** or the game will crash due to `mediapipe` constraints.
- Ensure webcam access is granted and lightning is sufficient for gesture detection.

## Licence

This project is licensed under the MIT License. See [License](LICENSE) for details.

## Author

Developed by Kenet Ortiz. <br/>
Feel free to fork, modify and contribute.