from io import BytesIO
from typing import Any, Dict, Optional

import av
import numpy as np

from encoded_video import EncodedVideo


def write_video(
    filename: str,
    video_array: np.ndarray,
    fps: float,
    video_codec: str = "libx264",
    options: Optional[Dict[str, Any]] = None,
    audio_array: Optional[np.ndarray] = None,
    audio_fps: Optional[float] = None,
    audio_codec: Optional[str] = None,
    audio_options: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Writes a 4d tensor in [T, H, W, C] format in a video file

    Args:
        filename (str): path where the video will be saved
        video_array (Tensor[T, H, W, C]): tensor containing the individual frames,
            as a uint8 tensor in [T, H, W, C] format
        fps (Number): video frames per second
        video_codec (str): the name of the video codec, i.e. "libx264", "h264", etc.
        options (Dict): dictionary containing options to be passed into the PyAV video stream
        audio_array (Tensor[C, N]): tensor containing the audio, where C is the number of channels
            and N is the number of samples
        audio_fps (Number): audio sample rate, typically 44100 or 48000
        audio_codec (str): the name of the audio codec, i.e. "mp3", "aac", etc.
        audio_options (Dict): dictionary containing options to be passed into the PyAV audio stream
    """
    # import torch
    # video_array = torch.as_tensor(video_array, dtype=torch.uint8).numpy()
    video_array = video_array.astype(np.uint8)

    # PyAV does not support floating point numbers with decimal point
    # and will throw OverflowException in case this is not the case
    if isinstance(fps, float):
        fps = np.round(fps)

    with av.open(filename, mode="w") as container:
        stream = container.add_stream(video_codec, rate=fps)
        stream.width = video_array.shape[2]
        stream.height = video_array.shape[1]
        stream.pix_fmt = "yuv420p" if video_codec != "libx264rgb" else "rgb24"
        stream.options = options or {}

        if audio_array is not None:
            audio_format_dtypes = {
                'dbl': '<f8',
                'dblp': '<f8',
                'flt': '<f4',
                'fltp': '<f4',
                's16': '<i2',
                's16p': '<i2',
                's32': '<i4',
                's32p': '<i4',
                'u8': 'u1',
                'u8p': 'u1',
            }
            a_stream = container.add_stream(audio_codec, rate=audio_fps)
            a_stream.options = audio_options or {}

            num_channels = audio_array.shape[0]
            audio_layout = "stereo" if num_channels > 1 else "mono"
            audio_sample_fmt = container.streams.audio[0].format.name

            format_dtype = np.dtype(audio_format_dtypes[audio_sample_fmt])
            audio_array = audio_array.astype(format_dtype)

            frame = av.AudioFrame.from_ndarray(audio_array, format=audio_sample_fmt, layout=audio_layout)

            frame.sample_rate = audio_fps

            for packet in a_stream.encode(frame):
                container.mux(packet)

            for packet in a_stream.encode():
                container.mux(packet)

        for img in video_array:
            frame = av.VideoFrame.from_ndarray(img, format="rgb24")
            frame.pict_type = "NONE"
            for packet in stream.encode(frame):
                container.mux(packet)

        # Flush stream
        for packet in stream.encode():
            container.mux(packet)


def video_to_bytes(
    video_array: np.ndarray,
    fps: float,
    video_codec: str = "libx264",
    options: Optional[Dict[str, Any]] = None,
    audio_array: Optional[np.ndarray] = None,
    audio_fps: Optional[float] = None,
    audio_codec: Optional[str] = None,
    audio_options: Optional[Dict[str, Any]] = None,
) -> bytes:

    """
    Writes a 4d tensor in [T, H, W, C] format to buffer

    Args:
        video_array (Tensor[T, H, W, C]): tensor containing the individual frames,
            as a uint8 tensor in [T, H, W, C] format
        fps (Number): video frames per second
        video_codec (str): the name of the video codec, i.e. "libx264", "h264", etc.
        options (Dict): dictionary containing options to be passed into the PyAV video stream
        audio_array (Tensor[C, N]): tensor containing the audio, where C is the number of channels
            and N is the number of samples
        audio_fps (Number): audio sample rate, typically 44100 or 48000
        audio_codec (str): the name of the audio codec, i.e. "mp3", "aac", etc.
        audio_options (Dict): dictionary containing options to be passed into the PyAV audio stream
    """

    bytes_mp4 = bytes()
    out_file = BytesIO(bytes_mp4)

    # Add dummy file name to stream, as write_video will be looking for it
    out_file.name = 'out.mp4'

    # writes to out_file
    write_video(out_file, video_array, fps, video_codec, options, audio_array, audio_fps, audio_codec, audio_options)

    # Return the bytes
    return out_file.getvalue()


def bytes_to_video(bpayload) -> Dict[str, Any]:
    """Take in memory video bytes and return a video clip dict containing frames, audio, and metadata"""
    vid = EncodedVideo(BytesIO(bpayload))
    clip = vid.get_clip(0, vid.duration)
    clip['duration'] = vid.duration
    clip['fps'] = float(vid._container.streams.video[0].average_rate)
    clip['audio_fps'] = None if not vid._has_audio else vid._container.streams.audio[0].sample_rate
    return clip


def read_video(filepath):
    """Read a video from file"""
    with open(filepath, 'rb') as f:
        bpayload = f.read()
    return bytes_to_video(bpayload)
