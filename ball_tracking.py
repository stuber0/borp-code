import cv2
import numpy as np

# Function to detect and track red ball
def detect_red_ball():
    # Open the camera
    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture image.")
            break

        # Convert the image from BGR to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define range for red color in HSV
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        # Range for red color in HSV (another range for red, as it wraps around in HSV)
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        # Combine both masks
        mask = mask1 + mask2

        # Remove noise by performing erosion and dilation
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # If contours are found
        if contours:
            # Find the largest contour (which will likely be the ball)
            c = max(contours, key=cv2.contourArea)

            # Find the minimum enclosing circle around the largest contour
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            # Only proceed if the radius meets a minimum size
            if radius > 10:
                # Draw the circle around the ball
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

                # Optionally, draw a center point
                cv2.circle(frame, (int(x), int(y)), 5, (255, 0, 0), -1)

                # Display tracking information
                print(f"Ball Position: x={int(x)}, y={int(y)}; Radius: {int(radius)}")

        # Display the resulting frame
        cv2.imshow('Red Ball Tracking', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_red_ball()


