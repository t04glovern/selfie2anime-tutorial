# Raspberry Pi Video Streamer

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python streamer.py
```

## Note

You might need to update the video source (or the API endpoint) in `streamer.py`

```python
class State:
    # Device ID (typically 0)
    video_device_id = 0
    # can alternatively be a RTSP endpoint
    # video_device_id = 'http://192.168.0.1:8080/video/mjpeg'

    # GAN endpoint for inference
    gan_endpoint = 'http://image.selfie2anime.com/process'
```
