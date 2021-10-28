# encoded-video

<a href="https://colab.research.google.com/github/nateraw/encoded-video/blob/main/examples/encoded_video_demo.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

Utilities for serializing/deserializing videos w/ `pyav` and `numpy`. 

## Purpose

1. Have a helpful API for working with videos
2. Liberate myself from relying on `torch` or `tensorflow` to do the above
3. Serialize/deserialize videos without writing directly to file (helpful for sending/recieving videos over APIs)

## Acknowledgments

This is more or less a `torch`-less version of `EncodedVideo` from [`pytorchvideo`](https://github.com/facebookresearch/pytorchvideo).

## Setup

```
pip install encoded-video
```

## Usage

```python
import numpy as np
from encoded_video import bytes_to_video, read_video, video_to_bytes

vid = read_video('archery.mp4')
video_arr = vid['video']  # (T, H, W, C)
audio_arr = vid['audio']  # (S,)

out_bytes = video_to_bytes(
    video_arr,
    fps=30,
    audio_array=np.expand_dims(audio_arr, 0),
    audio_fps=vid['audio_fps'],
    audio_codec='aac'
)

restored_video = bytes_to_video(out_bytes)
```
