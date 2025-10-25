import os
import csv
import datetime


def get_output_path(video_path, start, end):
    """Generates a clean output path in the same folder as the input video."""
    base, ext = os.path.splitext(video_path)
    filename = f"{os.path.basename(base)}_{start}To{end}{ext}"
    return os.path.join(os.path.dirname(video_path), filename)


class Logger:
    """Logs trimming data into a CSV file."""
    def __init__(self, csv_path):
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        self.csv_path = csv_path
        if not os.path.exists(csv_path):
            with open(csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Video", "Start Frame", "End Frame", "Output Path"])

    def log(self, video_path, start_frame, end_frame, output_path):
        with open(self.csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                os.path.basename(video_path),
                start_frame,
                end_frame,
                output_path
            ])
