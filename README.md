# Pomodoro Timer Application

## Overview

This Pomodoro Timer is a customizable, dark-themed desktop application designed to help users implement the Pomodoro Technique for time management and productivity. It features automatic cycling between work sessions and breaks, custom time settings, and both visual and audio notifications.

## Features

- Dark-themed graphical user interface
- Automatic cycling between Pomodoro sessions and breaks
- Customizable timer durations
- Visual and audio notifications for session changes
- Responsive design that adjusts to window size
- Start, pause, and reset functionality

## Technologies Used

- Python 3.x
- CustomTkinter: For creating the modern, dark-themed GUI
- Pygame: For audio notifications
- Plyer: For desktop notifications (with fallback to console output)
- Threading: For non-blocking timer operation

## Project Structure

The project consists of a single Python script (`pomodoro_timer.py`) that contains the entire application logic. Here's an overview of its structure:

```
pomodoro/
│
├── pomodoro_timer.py          # Main application script
├── README.md       # This file
└── requirements.txt # List of project dependencies
```

## Main Components

1. `PomodoroTimer` class: The core of the application, handling all timer logic and GUI interactions.

2. UI Elements:

   - Time display
   - Mode display (Pomodoro, Short Break, Long Break)
   - Control buttons (Start, Pause, Reset)
   - Custom time input

3. Timer Logic:

   - Automatic cycling between Pomodoro sessions and breaks
   - Handling of long breaks after every 4 Pomodoros

4. Notification System:
   - Desktop notifications (if available)
   - Fallback to console output
   - Audio alerts

## Building and Running the App

### Prerequisites

- Python 3.x installed on your system
- pip (Python package manager)

### Setup

1. Clone the repository or download the `pomodoro_timer.py` file.

2. Navigate to the project directory in your terminal.

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

   Or install them manually:

   ```
   pip install customtkinter pygame plyer
   ```

### Running the Application

1. In the project directory, run:

   ```
   python pomodoro_timer.py
   ```

2. The Pomodoro Timer window should appear, and you can start using the application.

## Usage

- Click "Start" to begin the Pomodoro timer.
- Use "Pause" to temporarily stop the timer, and click again to resume.
- "Reset" will stop the timer and reset it to the default Pomodoro duration.
- Enter a custom time in the format HH:MM:SS and click "Set Custom Time" to use a different duration.

The timer will automatically cycle between Pomodoro sessions and breaks. You'll receive notifications (desktop or console) and hear an alert sound (if available) when each session ends.

## Customization

You can modify the default Pomodoro, short break, and long break durations by changing the values in the `__init__` method of the `PomodoroTimer` class in `pomodoro_timer.py`.

## Troubleshooting

- If you encounter issues with desktop notifications, ensure you have the necessary permissions and that your system supports them. The application will fall back to console notifications if desktop notifications are unavailable.
- If audio alerts don't work, check that your system has the required sound files or modify the `load_system_sound` method to use a custom sound file.

## Contributing

Contributions to improve the Pomodoro Timer are welcome. Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

This project is open-source and available under the MIT License.
