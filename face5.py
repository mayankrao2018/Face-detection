import cv2
import tkinter as tk
from tkinter import ttk
from threading import Thread

class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detection App")


        # Create a label to display the webcam feed
        self.label = ttk.Label(root)
        self.label.pack()

        # Create a start/stop button
        self.start_stop_button = ttk.Button(root, text="Start Detection", command=self.toggle_detection)
        self.start_stop_button.pack()

        self.cap = cv2.VideoCapture(0)
        self.detecting = False
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.update()

    def toggle_detection(self):
        self.detecting = not self.detecting
        if self.detecting:
            self.start_stop_button.config(text="Stop Detection")
        else:
            self.start_stop_button.config(text="Start Detection")

    def update(self):
        ret, frame = self.cap.read()
        if self.detecting:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = tk.PhotoImage(data=cv2.imencode('.png', frame)[1].tostring())

        self.label.config(image=img)
        self.label.image = img

        if self.detecting:
            self.root.after(10, self.update)
        else:
            self.label.after(10, self.update)

    def run(self):
        self.root.mainloop()
        self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceDetectionApp(root)
    app.run()
