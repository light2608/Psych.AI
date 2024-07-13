#!/usr/bin/python3
# -*- coding:utf-8 -*-

import argparse
import service
import cv2
import csv
import time

def main(args, color=(224, 255, 255)):
    fd = service.UltraLightFaceDetecion("weights/RFB-320.tflite",
                                        conf_threshold=0.95)

    if args.mode == "dense":
        fa = service.DenseFaceReconstruction("weights/dense_face.tflite")
    else:
        print("Error: Only 'dense' mode is supported for full node coordinate recording.")
        return

    handler = getattr(service, args.mode)
    
    # Open the video file
    cap = cv2.VideoCapture(args.filepath)

    if not cap.isOpened():
        print(f"Error: Could not open video file {args.filepath}")
        return

    # CSV setup
    csv_file = 'face_landmarks.csv'
    csv_columns = ['timestamp'] + [f'x{i},y{i},z{i}' for i in range(67)]
    
    # Initialize start time for timestamp
    start_time = time.time()

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_columns)

    last_record_time = start_time

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # face detection
        boxes, scores = fd.inference(frame)

        # raw copy for reconstruction
        feed = frame.copy()

        for results in fa.get_landmarks(feed, boxes):
            handler(frame, results, color)

            # Record timestamp
            current_time = time.time() - start_time

            # Extract and save landmarks to CSV
            with open(csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                row = [f"{current_time:.2f}"]  # Format timestamp to two decimal places

                # Extend row with all coordinates of each node
                for i in range(67):
                    if i < len(results):
                        x, y, z = results[i][:3]  # Extract x, y, z coordinates
                    else:
                        x, y, z = 0, 0, 0  # Default to 0 if node is missing in current frame

                    row.extend([x, y, z])

                writer.writerow(row)

            print(f"Recorded landmarks at {current_time:.2f} seconds")

        # Display the frame if needed (optional)
        # cv2.imshow("demo", frame)
        # if cv2.waitKey(1) == ord("q"):
        #     break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video analysis script.")
    parser.add_argument("-f", "--filepath", type=str, required=True, help="Path to the video file")
    parser.add_argument("-m", "--mode", type=str, default="sparse",
                        choices=["sparse", "dense", "mesh", "pose"], help="Mode for facial landmark detection")

    args = parser.parse_args()
    main(args)
