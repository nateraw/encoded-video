# encoded-video

Utilities for serializing/deserializing videos w/ `pyav` and `numpy`. 

This is more or less a `torch`-less version of `EncodedVideo` from [`pytorchvideo`](https://github.com/facebookresearch/pytorchvideo).

The purpose of this package is to:
1. Have a helpful API for working with videos
2. Liberate myself from relying on `torch` or `tensorflow` to do the above
3. Serialize/deserialize videos without writing directly to file (helpful for sending/recieving videos over APIs)


## Setup

```
pip install encoded-video
```

## Usage

```python

vid = read_video('archery.mp4')

out_bytes = video_to_bytes(
    vid['video'],
    fps=30,
    audio_array=np.expand_dims(vid['audio'], 0),
    audio_fps=vid['audio_fps'],
    audio_codec='aac'
)

restored_video = bytes_to_video(out_bytes)
```
