from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.resize import resize

class VideoTrimmer:
    def trim(self, video_path, start_frame, end_frame, output_path):
        with VideoFileClip(video_path) as clip:
            fps = clip.fps
            start_time = start_frame / fps
            end_time = end_frame / fps
            trimmed = clip.subclip(start_time, end_time)
            trimmed = resize(trimmed, (720, 1080))
            trimmed.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
