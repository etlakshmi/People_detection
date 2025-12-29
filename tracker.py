import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

def process_video(video_path):
    model = YOLO("yolov8n.pt")
    tracker = DeepSort(max_age=30)

    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    zone_split = height // 2

    zone_a_ids = set()
    zone_b_ids = set()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # ---------------- Draw ZONE LINE ----------------
        cv2.line(frame, (0, zone_split), (width, zone_split), (0, 255, 255), 2)

        cv2.putText(frame, "ZONE A", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame, "ZONE B", (20, zone_split + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # -------------------------------------------------

        results = model(frame, stream=True)
        detections = []

        for r in results:
            for box in r.boxes:
                if int(box.cls[0]) == 0:  # person
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    detections.append(([x1, y1, x2 - x1, y2 - y1], conf, "person"))

        tracks = tracker.update_tracks(detections, frame=frame)

        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            l, t, r, b = map(int, track.to_ltrb())
            cy = (t + b) // 2

            # ---------- Draw Bounding Box ----------
            color = (0, 255, 0) if cy < zone_split else (0, 0, 255)
            cv2.rectangle(frame, (l, t), (r, b), color, 2)
            cv2.putText(frame, f"ID {track_id}", (l, t - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            # --------------------------------------

            if cy < zone_split:
                zone_a_ids.add(track_id)
            else:
                zone_b_ids.add(track_id)

        # Show video window (for debugging)
        cv2.imshow("Zone People Tracking", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()

    return len(zone_a_ids), len(zone_b_ids)
