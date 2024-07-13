import argparse
import service
import cv2
import csv
import time
import os
import numpy as np

def main(args, color=(224, 255, 255)):
    fd = service.UltraLightFaceDetecion("weights/RFB-320.tflite",
                                        conf_threshold=0.95)

    if args.mode in ["sparse", "pose"]:
        fa = service.DepthFacialLandmarks("weights/sparse_face.tflite")
    else:
        fa = service.DenseFaceReconstruction("weights/dense_face.tflite")
        if args.mode == "mesh":
            color = service.TrianglesMeshRender("asset/render.so",
                                                "asset/triangles.npy")

    handler = getattr(service, args.mode)
    
    # Open video file
    cap = cv2.VideoCapture(args.filepath)

    # CSV setup
    if args.mode == "dense":
        csv_file = 'face_landmarks.csv'
        csv_columns = ['timestamp', 'landmarks']
        
        if not os.path.exists(csv_file):
            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(csv_columns)

        last_record_time = time.time()

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

            if args.mode == "dense":
                # Record every 2 seconds
                if time.time() - last_record_time > 2:
                    last_record_time = time.time()
                    
                    # Extract and save landmarks to CSV
                    with open(csv_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        row = [time.time()]
                        # Serialize all landmarks into a single string
                        serialized_landmarks = ';'.join([','.join(map(str, point)) for point in results])
                        row.append(serialized_landmarks)
                        writer.writerow(row)

                    print(f"Recorded landmarks at {time.time()}")

        # Display the frame
        cv2.imshow("demo", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video demo script.")
    parser.add_argument("-f", "--filepath", type=str, required=True,
                        help="Path to the video file.")
    parser.add_argument("-m", "--mode", type=str, default="sparse",
                        choices=["sparse", "dense", "mesh", "pose"],
                        help="Mode for face reconstruction.")

    args = parser.parse_args()
    main(args)
