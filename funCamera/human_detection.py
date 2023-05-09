import cv2
import numpy as np
from ultralytics import YOLO
import random
from shapely.geometry import Point, Polygon

# Load YOLOv8 model
model = YOLO("yolov8n-seg.pt")  # Make sure to use the correct YOLOv8 model file

def detect_humans(frame, results):
    detections = []
    for result in results:
        # Convert xyxy to xywh format
        xywh = result.boxes.xywh.clone()
        xywh[:, 2:] -= xywh[:, :2]
        xywh[:, :2] += xywh[:, 2:] / 2
        xywh = xywh.numpy()

        # Scale the coordinates to the frame dimensions
        xywh[:, :4] *= np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
        detections.extend(xywh)
    return detections


def draw_circles(frame, results):
    for det in results:
        if int(det[5]) == 0:  # Check if the detected object is a person (class 0)
            x, y, width, height = int(det[0]), int(det[1]), int(det[2]), int(det[3])
            center = (x + width // 2, y + height // 2)
            radius = max(width, height) // 2
            color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
            cv2.circle(frame, center, radius, color, -1)

def random_points_in_polygon(polygon, num_points):
    points = []
    min_x, min_y, max_x, max_y = polygon.bounds
    while len(points) < num_points:
        random_point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if random_point.within(polygon):
            points.append(random_point)
    return points

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform inference
        results = model(frame)
        for result in results:
            if (result.names[0] == 'person'):
                bounding_box = result.boxes[0]
                box = bounding_box.xyxy[0]
                print(result.names[0])
                print(result.masks.xy)
                x1, y1, x2, y2 = int(box[0].item()), int(box[1].item()), int(box[2].item()), int(box[3].item())
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), -1)
                cv2.rectangle(frame, (0, 0), (1000, 1000), (0, 0, 0), -1)
                prev = None
                polyline_points = np.array(result.masks.xy[0], dtype=np.int32)
                polyline_points = polyline_points.reshape((-1, 1, 2))
                polyline = []
                for p in result.masks.xy[0]:
                    polyline += [[int(p[0]), int(p[1])]]
                    # cv2.circle(frame, (int(p[0]), int(p[1])), 1, (0, 0, 255), -1)
                    prev = p
                print(np.array(polyline))
                cv2.fillPoly(frame, [np.array([[0, 0], [100, 0], [0, 100], [0, 0]])], (255, 0, 0))
                print(result.masks.xy[0])
                print([polyline])
                print(polyline_points)

                factor = 640 / 255
                for p in random_points_in_polygon(Polygon(polyline), 1000):

                    cv2.circle(frame, (int(p.x), int(p.y)), 1, (p.x / factor % 255, p.y / factor % 255, (p.x / 2 + p.y / 2) / factor % 255), 10)

                # cv2.fillPoly(frame, [np.array(polyline)], (255, 0, 0))

        cv2.imshow('Human Detection', frame)
        # res_plotted = results[0].plot()
        # cv2.imshow("result", res_plotted)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
