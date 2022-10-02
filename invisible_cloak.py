import cv2
import time
import numpy as np

#To save the output in a file output.avi
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#Starting the webcam
cap = cv2.VideoCapture(0)

#Allowing the webcam to start by making the code sleep for 2 seconds
time.sleep(2)
bg = 0

#Capturing background for 60 frames
for i in range(60):
    ret, bg = cap.read()
#Flipping the background
bg = np.flip(bg, axis=1)

#Reading the captured frame until the camera is open
while (cap.isOpened()):
    ret, image, frame = cap.read()
    if not ret:
        break

     #Flipping the image for consistency
    image = np.flip(image, axis=1)
    frame = np.flip(frame, axis=1)

    #Resizing the frame for consistency
    frame = cv2.resize(frame, (640, 480))
    image = cv2.resize(image, (640, 480))

    #Generating mask to detect red colour
    #These values can also be changed as per the color
    l_black = np.array([104, 153, 70])
    u_black = np.array([30, 30,0])

    mask = cv2.inRange(frame, l_black, u_black)

    #Open and expand the image where there is mask 1 (color)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    #Keeping only the part of the images without the red color 
    #(or any other color you may choose)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    f = frame - res
    f= np.where(f == 0, image, f)

    #Generating the final output
    final_output = cv2.addWeighted(res, 1)
    output_file.write(final_output)

    #Displaying the output to the user
    cv2.imshow("magic", final_output)
    cv2.waitKey(1)


cap.release()
#out.release()
cv2.destroyAllWindows()