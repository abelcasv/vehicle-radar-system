import cv2
from utils import *

# ************************************************************
# CONFIGURATION

VIDEO_PATH = "trafico.mp4"

MIN_CONTOUR_AREA = 2800       # Minimum contour area to be considered a vehicle
MAX_DISTANCE = 120            # Maximum distance to match an existing vehicle
MAX_FRAMES_MISSING = 5        # Maximum frames a vehicle can be missing before removal

COUNT_LINE_Y1 = 400           # Upper boundary of counting area
COUNT_LINE_Y2 = 900           # Lower boundary of counting area
COUNT_LINE_Y = 550            # Y position of the counting line


def main():
    # Video and structures initialization
    video = cv2.VideoCapture(VIDEO_PATH)

    background_subtractor = cv2.createBackgroundSubtractorMOG2(
        history=500,
        varThreshold=40,
        detectShadows=False
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    vehicles = []            # List of all tracked vehicles
    visible_vehicles = []    # Temporary list of vehicles detected in the current frame
    vehicle_count = 0        # Total vehicles counted
    vehicle_id_counter = 1   # Unique ID for new vehicles

    # ************************************************************
    # BUCLE PRINCIPAL

    while True:
        ret, frame = video.read()
        if not ret:
            break

        fg_mask = get_foreground_mask(frame, background_subtractor, kernel)
        contours, _ = cv2.findContours(
            fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        visible_vehicles = []  # Vehicles detected in the current frame

        for cnt in contours:
            if cv2.contourArea(cnt) < MIN_CONTOUR_AREA:
                continue

            x, y, w, h = cv2.boundingRect(cnt)
            center = (int(x + w/2), int(y + h/2))

            # Region of interest
            if not (COUNT_LINE_Y1 < center[1] < COUNT_LINE_Y2):
                continue

            vehicle_count, vehicle_id_counter = process_detection(
                center,
                (x, y, w, h),
                vehicles,
                visible_vehicles,
                COUNT_LINE_Y,
                vehicle_count,
                vehicle_id_counter,
                MAX_DISTANCE
            )

        vehicles = filter_vehicles(vehicles, visible_vehicles, MAX_FRAMES_MISSING)
        draw(frame, visible_vehicles, COUNT_LINE_Y, vehicle_count)

        cv2.imshow("Vehicle Counting", frame)
        if cv2.waitKey(2) & 0xFF == 27:  # Press ESC to exit
            break

    # ************************************************************
    # CLEANUP

    video.release()
    cv2.destroyAllWindows()
    print(f"Total vehicles: {vehicle_count}")


if __name__ == "__main__":
    main()