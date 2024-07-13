"""
Pomodoro Timer Application

This module provides a customizable Pomodoro timer with a dark-themed graphical user interface.
It features automatic cycling between work sessions and breaks, custom time setting,
start, pause, and reset functionality, system sound notifications, and dynamic scaling
based on window size.
"""

import os
import threading
import time
from tkinter import messagebox
import customtkinter as ctk
import pygame

# Suppress pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

# Try to import notification, but don't fail if it's not available
try:
    from plyer import notification

    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False


class PomodoroTimer:
    """
    A class representing a Pomodoro timer application with a dark theme.

    This class encapsulates all the functionality of the Pomodoro timer,
    including the GUI, timer logic, notification systems, and dynamic scaling.
    """

    def __init__(self):
        """Initialize the PomodoroTimer with default settings and dark mode."""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.root = ctk.CTk()
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x300")

        self.pomodoro_time = 25 * 60
        self.short_break_time = 5 * 60
        self.long_break_time = 30 * 60
        self.time_left = self.pomodoro_time
        self.timer_running = False
        self.timer_paused = False
        self.pomodoro_count = 0
        self.current_mode = "Pomodoro"

        self.time_label = None
        self.mode_label = None
        self.start_button = None
        self.pause_button = None
        self.reset_button = None
        self.custom_entry = None
        self.custom_button = None

        self.timer_font = ctk.CTkFont(family="Roboto Mono", size=48, weight="bold")

        pygame.mixer.init()
        self.alert_sound = self.load_system_sound()

        self.setup_ui()
        self.root.bind("<Configure>", self.on_resize)

    def load_system_sound(self):
        """Load the system alert sound."""
        sound_paths = [
            "/usr/share/sounds/ubuntu/stereo/system-ready.ogg",
            "/usr/share/sounds/freedesktop/stereo/complete.oga",
            "/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga",
        ]

        for path in sound_paths:
            if os.path.exists(path):
                try:
                    return pygame.mixer.Sound(path)
                except pygame.error:
                    print(f"Failed to load sound file: {path}")

        print(
            "Warning: Could not load any system sound. Audio alerts will be disabled."
        )
        return None

    def play_alert_sound(self):
        """Play the alert sound if available."""
        if self.alert_sound:
            self.alert_sound.play()
        else:
            print("Audio alert skipped: No sound loaded.")

    def setup_ui(self):
        """Set up the user interface elements."""
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_rowconfigure(3, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        # Time display
        self.time_label = ctk.CTkLabel(self.root, text="00:25:00", font=self.timer_font)
        self.time_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 5))

        # Mode display
        self.mode_label = ctk.CTkLabel(self.root, text="Pomodoro", font=("CTkFont", 16))
        self.mode_label.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)

        # Button frame
        button_frame = ctk.CTkFrame(self.root)
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.start_button = ctk.CTkButton(
            button_frame, text="Start", command=self.start_timer, font=("CTkFont", 14)
        )
        self.start_button.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")

        self.pause_button = ctk.CTkButton(
            button_frame,
            text="Pause",
            command=self.pause_timer,
            state="disabled",
            font=("CTkFont", 14),
        )
        self.pause_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.reset_button = ctk.CTkButton(
            button_frame, text="Reset", command=self.reset_timer, font=("CTkFont", 14)
        )
        self.reset_button.grid(row=0, column=2, padx=(5, 0), pady=5, sticky="ew")

        # Custom time frame
        custom_frame = ctk.CTkFrame(self.root)
        custom_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(10, 20))
        custom_frame.grid_columnconfigure(1, weight=1)

        self.custom_entry = ctk.CTkEntry(
            custom_frame, placeholder_text="HH:MM:SS", font=("CTkFont", 14)
        )
        self.custom_entry.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        self.custom_entry.bind("<KeyRelease>", self.format_custom_time)

        self.custom_button = ctk.CTkButton(
            custom_frame,
            text="Set Custom Time",
            command=self.set_custom_time,
            font=("CTkFont", 14),
        )
        self.custom_button.grid(row=0, column=1, padx=(5, 0), pady=5, sticky="ew")

    def on_resize(self, _):
        """Handle window resize events."""
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        font_size = min(width // 10, height // 5)
        self.timer_font.configure(size=font_size)
        self.time_label.configure(font=self.timer_font)

    def format_custom_time(self, _):
        """Format the custom time input to add colons automatically."""
        current = self.custom_entry.get().replace(":", "")
        formatted = ""
        for i, char in enumerate(current):
            if i in [2, 4] and len(current) > i:
                formatted += ":"
            formatted += char
        self.custom_entry.delete(0, ctk.END)
        self.custom_entry.insert(0, formatted)

    def start_timer(self):
        """Start the timer if it's not already running."""
        if not self.timer_running:
            self.timer_running = True
            self.start_button.configure(state="disabled")
            self.pause_button.configure(state="normal")
            self.custom_button.configure(state="disabled")
            threading.Thread(target=self.run_timer, daemon=True).start()

    def run_timer(self):
        """Run the timer countdown and automatically cycle between sessions."""
        while self.timer_running:
            while self.time_left > 0 and self.timer_running:
                if not self.timer_paused:
                    self.update_time_display()
                    time.sleep(1)
                    self.time_left -= 1
                else:
                    time.sleep(0.1)

            if self.timer_running:
                self.timer_finished()

    def update_time_display(self):
        """Update the time display label."""
        hours, remainder = divmod(self.time_left, 3600)
        mins, secs = divmod(remainder, 60)
        self.time_label.configure(text=f"{hours:02d}:{mins:02d}:{secs:02d}")
        self.root.update()

    def timer_finished(self):
        """Handle actions when the timer finishes and start the next session."""
        if self.current_mode == "Pomodoro":
            self.pomodoro_count += 1
            if self.pomodoro_count % 4 == 0:
                self.current_mode = "Long Break"
                self.time_left = self.long_break_time
            else:
                self.current_mode = "Short Break"
                self.time_left = self.short_break_time
        else:
            self.current_mode = "Pomodoro"
            self.time_left = self.pomodoro_time

        self.mode_label.configure(text=self.current_mode)
        self.update_time_display()
        self.show_notification("Pomodoro Timer", f"{self.current_mode} started!")
        self.play_alert_sound()

    def show_notification(self, title, message):
        """Show a desktop notification if available, otherwise print to console."""
        if NOTIFICATIONS_AVAILABLE:
            try:
                notification.notify(
                    title=title, message=message, app_name="Pomodoro Timer", timeout=10
                )
            except NotImplementedError:
                print("Desktop notifications are not implemented on this system.")
                print(f"{title}: {message}")
            except PermissionError:
                print("Permission denied when trying to show notification.")
                print(f"{title}: {message}")
            except ImportError:
                print("Failed to import notification module.")
                print(f"{title}: {message}")
            except OSError as e:
                print(f"OS error occurred when showing notification: {e}")
                print(f"{title}: {message}")
        else:
            print(f"{title}: {message}")

    def pause_timer(self):
        """Pause or unpause the timer."""
        if self.timer_paused:
            self.timer_paused = False
            self.pause_button.configure(text="Pause")
        else:
            self.timer_paused = True
            self.pause_button.configure(text="Unpause")

    def reset_timer(self):
        """Reset the timer to its default state."""
        self.timer_running = False
        self.timer_paused = False
        self.time_left = self.pomodoro_time
        self.current_mode = "Pomodoro"
        self.pomodoro_count = 0
        self.update_time_display()
        self.mode_label.configure(text=self.current_mode)
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="disabled", text="Pause")
        self.custom_button.configure(state="normal")

    def set_custom_time(self):
        """Set a custom time for the timer."""
        try:
            time_parts = self.custom_entry.get().split(":")
            if len(time_parts) != 3:
                raise ValueError("Invalid time format")

            hours, minutes, seconds = map(int, time_parts)
            total_seconds = hours * 3600 + minutes * 60 + seconds

            if total_seconds > 0:
                self.time_left = total_seconds
                self.update_time_display()
            else:
                raise ValueError("Time must be greater than zero")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))

    def run(self):
        """Start the main event loop of the application."""
        self.root.mainloop()


def main():
    """Main function to run the Pomodoro Timer application."""
    app = PomodoroTimer()
    app.run()


if __name__ == "__main__":
    main()
