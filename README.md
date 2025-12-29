# Zone People Tracking System

A real-time video analytics system that tracks people across two horizontal zones using YOLOv8 for detection and DeepSORT for multi-object tracking.

## Demo

Below is a short demonstration of the Zone-wise People Detection system in action:

![People Detection Demo](People_detection.gif)

## Features

- **Dual Zone Tracking**: Automatically divides video frame into two zones (A and B)
- **Person Detection**: Uses YOLOv8 for accurate person detection
- **Multi-Object Tracking**: DeepSORT maintains consistent IDs across frames
- **Zone Crossing Detection**: Monitors and counts when people move between zones
- **Visual Overlays**: Real-time statistics, bounding boxes, and zone labels
- **Video Export**: Saves processed video with tracking annotations
- **Comprehensive Statistics**: Detailed tracking metrics and reports

## Requirements

### Python Version
- Python 3.8 or higher

### Dependencies

```bash
pip install opencv-python
pip install ultralytics
pip install deep-sort-realtime
pip install numpy
```

### Model Files
The script will automatically download YOLOv8n model on first run:
- `yolov8n.pt` (nano version, ~6MB)

For better accuracy, you can use larger models:
- `yolov8s.pt` (small, ~22MB)
- `yolov8m.pt` (medium, ~52MB)
- `yolov8l.pt` (large, ~87MB)

## Installation

1. Clone or download this repository

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Ensure you have a video file to process

## Usage

### Basic Usage

```python
from zone_tracker import process_video

# Process video with default settings
stats = process_video("input_video.mp4")
```

### Advanced Usage

```python
stats = process_video(
    video_path="input_video.mp4",
    output_path="output_tracked.mp4",
    show_video=True,
    confidence_threshold=0.5
)

# Access results
print(f"Zone A: {stats['zone_a_count']} people")
print(f"Zone B: {stats['zone_b_count']} people")
print(f"Crossings: {stats['crossings']}")
```

### Command Line Usage

```bash
python zone_tracker.py
```

Edit the `__main__` section to specify your input/output files.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `video_path` | str | Required | Path to input video file |
| `output_path` | str | None | Path to save output video (optional) |
| `show_video` | bool | True | Display video during processing |
| `confidence_threshold` | float | 0.5 | Minimum detection confidence (0-1) |

## Output

### Return Dictionary

```python
{
    'zone_a_count': 5,           # Unique people in Zone A
    'zone_b_count': 3,           # Unique people in Zone B
    'total_unique_people': 7,    # Total unique individuals
    'crossings': 4,              # Number of zone crossings
    'frames_processed': 1500,    # Total frames processed
    'zone_a_ids': [1, 2, 4, 5, 7],  # Track IDs in Zone A
    'zone_b_ids': [3, 6, 8]         # Track IDs in Zone B
}
```

### Visual Output

The processed video includes:
- **Yellow Line**: Zone boundary (horizontal divider)
- **Green Boxes**: People in Zone A (top half)
- **Red Boxes**: People in Zone B (bottom half)
- **ID Labels**: Unique tracking ID for each person
- **Statistics Overlay**: Real-time counts and crossings
- **Progress Indicator**: Frame count and completion

## How It Works

1. **Video Input**: Reads video frame by frame
2. **Detection**: YOLOv8 detects all people in each frame
3. **Tracking**: DeepSORT assigns and maintains unique IDs
4. **Zone Assignment**: Determines zone based on person's center point
5. **Crossing Detection**: Monitors zone changes for each tracked person
6. **Visualization**: Draws bounding boxes, labels, and statistics
7. **Output**: Saves processed video and returns statistics

## Configuration Options

### Tracking Parameters

Modify DeepSort initialization for different tracking behavior:

```python
tracker = DeepSort(
    max_age=30,           # Frames to keep lost tracks
    n_init=3,             # Frames to confirm a track
    max_iou_distance=0.7  # IoU threshold for matching
)
```

### Detection Confidence

Adjust confidence threshold to balance detection sensitivity:
- Lower (0.3-0.4): More detections, more false positives
- Medium (0.5): Balanced (recommended)
- Higher (0.6-0.7): Fewer false positives, may miss some people

### Zone Configuration

By default, zones split horizontally at 50%. To customize:

```python
zone_split = int(height * 0.6)  # Zone A is top 60%
```

## Performance Tips

1. **Use Smaller Models for Speed**:
   - `yolov8n.pt`: Fastest, good for real-time
   - `yolov8s.pt`: Balance of speed and accuracy

2. **Disable Video Display**:
   ```python
   process_video("input.mp4", show_video=False)
   ```

3. **Process Lower Resolution**:
   - Resize video before processing
   - Trade accuracy for speed

4. **GPU Acceleration**:
   - Install CUDA-enabled PyTorch
   - YOLOv8 automatically uses GPU if available

## Troubleshooting

### Issue: "Video not found" error
**Solution**: Check file path is correct and file exists

### Issue: Slow processing
**Solution**: 
- Use smaller YOLO model (`yolov8n.pt`)
- Disable video display (`show_video=False`)
- Ensure GPU acceleration is enabled

### Issue: Too many false detections
**Solution**: Increase `confidence_threshold` (try 0.6 or 0.7)

### Issue: Missing detections
**Solution**: 
- Lower `confidence_threshold` (try 0.3 or 0.4)
- Use larger YOLO model (`yolov8m.pt` or `yolov8l.pt`)

### Issue: IDs switching frequently
**Solution**: Adjust DeepSort parameters:
```python
tracker = DeepSort(max_age=50, n_init=2, max_iou_distance=0.8)
```

## Use Cases

- **Retail Analytics**: Track customer movement between store sections
- **Security**: Monitor restricted zone access
- **Traffic Analysis**: Count people crossing boundaries
- **Event Management**: Analyze crowd distribution
- **Workspace Optimization**: Study space utilization patterns

## Supported Video Formats

- MP4 (recommended)
- AVI
- MOV
- MKV
- Any format supported by OpenCV

## Limitations

- Only detects and tracks people (not other objects)
- Zones are horizontal dividers only (not custom regions)
- Performance depends on video resolution and hardware
- Occlusion can cause ID switches

## Future Enhancements

Potential features for future versions:
- Custom polygon zones
- Dwell time calculation
- Heatmap generation
- CSV export for analytics
- Multiple object classes
- Real-time webcam support
- Dashboard interface

## Credits

- **YOLOv8**: Ultralytics
- **DeepSORT**: Deep SORT implementation
- **OpenCV**: Computer vision library

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review parameter configurations
3. Test with sample videos first

---

**Version**: 1.0  
**Last Updated**: December 2025