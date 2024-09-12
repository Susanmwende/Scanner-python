import cv2
from pyzbar.pyzbar import decode

def scan_codes():
    # Open the camera
    cap = cv2.VideoCapture(0)

    # Set camera resolution (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set height

    if not cap.isOpened():
        print("Error: Camera could not be opened.")
        return

    print("Camera is opened. Starting the scanning process...")

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Decode barcodes and QR codes in the frame
            codes = decode(frame)

            if codes:
                for code in codes:
                    # Get the code data
                    code_data = code.data.decode('utf-8')
                    code_type = code.type

                    # Draw a rectangle around the detected code
                    (x, y, w, h) = code.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Display the decoded data on the frame
                    cv2.putText(frame, f"{code_data} ({code_type})", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Print the decoded content to the terminal
                    print(f"Decoded {code_type}: {code_data}")

                    # Provide feedback about focus
                    cv2.putText(frame, "Focused!", (x, y + h + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            else:
                # Provide feedback when no codes are detected
                cv2.putText(frame, "No codes detected", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Show the frame with detected codes
            cv2.imshow("Barcode and QR Code Scanner", frame)

            # Break the loop on 'q' key press or window close
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

# Run the code scanner
if __name__ == "__main__":
    scan_codes()