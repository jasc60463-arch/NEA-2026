# reference
# https://www.youtube.com/watch?v=1lN4L74BwWo
# https://mediapipe.readthedocs.io/en/latest/solutions/hands.html


class Counter:

    def __init__(self, **kwargs):
        self.counter = 0 
        self.last_call = -1
        self.current_direction = ""
        self.last_direction = ""
    
    def check(self,current_direction : str) -> str | None:
        """
        compare the current direction and the previous direction every 1s
        if the direction match, return direction 
        or else return none
        """
        if current_direction is None:
            return
        import time
        now = time.time()
        # if it have been 0.75 second after the previous check
        if now - self.last_call > 0.75: # time delay 
            self.current_direction = current_direction
            self.last_call = now
                # if the current direction is the same as the previous direction 
            if self.current_direction == self.last_direction:
                return self.current_direction
            else:
                # update the previous direction
                self.last_direction = self.current_direction
        return None

def pointer(x1 : int, y1 : int, x2 : int, y2 : int, distance_calarbration : float = 0.05) -> str:
    '''
    Takes two cord and determind the direction 
    '''
    vertical = y1 - y2      # +up -down
    horrizontal = x2 - x1   # -left +right
    
    # if point 1 is higher than point 2
    if vertical > distance_calarbration:
        # if point 1 is at the right of point 2
        if horrizontal > distance_calarbration:
            return "TR"

        # if point 1 is at the left of point 2
        elif horrizontal < -distance_calarbration:
            return "TL"

        # if point 1 is next to point 2
        else:
            return "TN"

    # if point 1 is lower than point 2
    elif vertical < -distance_calarbration:
        
        # if point 1 is at the right of point 2
        if horrizontal > distance_calarbration:
            return "BR"

        # if point 1 is at the left of point 2
        elif horrizontal < -distance_calarbration:
            return "BL"

        # if point 1 is next to point 2
        else:
            return "BN"

    # if point 1 is equal height with point 2
    else:
    
        # if point 1 is at the right of point 2
        if horrizontal > distance_calarbration:
            return "NR"

        # if point 1 is at the left of point 2
        elif horrizontal < -distance_calarbration:
            return "NL"
        
        # if point 1 is next to point 2
        else:
            return "NN"

# the hand gesture detection is developed with the referneced to this youtube tutorial and the website
# https://www.youtube.com/watch?v=1lN4L74BwWo
# https://mediapipe.readthedocs.io/en/latest/solutions/hands.html
def hand_gesture_function(
    gui_callback,
    display: bool
) -> None:
    
    import cv2
    import mediapipe

    # connect camera
    cam = cv2.VideoCapture(0)
    draw = mediapipe.solutions.drawing_utils 
    hand_model = mediapipe.solutions.hands 
    exit_hand_gesture = False
    
    # load hand detection model
    with hand_model.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:
        # tell the main loop the thread is finish loading and ready to execute
        gui_callback("Ready")

        # mainloop of thread
        while True:
            # read image of the camera
            cam_status, bgr_img = cam.read()
            # if camera failed
            if not cam_status:
                print("cam failed")
                continue
            bgr_img = cv2.flip(bgr_img,1)
            # convert bgr image to rgb image
            rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
            # get the height and width of the img
            h, w, _ = bgr_img.shape

            # detect the hand
            detection = hands.process(rgb_img)
            # if there is hand detected
            if detection.multi_hand_landmarks:
                # iterate hands
                for hand_landmark in detection.multi_hand_landmarks:
                    if display:
                        # draw the hand land marks
                        draw.draw_landmarks(bgr_img,
                                            hand_landmark,
                                            hand_model.HAND_CONNECTIONS
                                            )
                        
                        fingers_tips = {
                            "thumb" : hand_landmark.landmark[4],
                            "index" : hand_landmark.landmark[8],
                            "middle" : hand_landmark.landmark[12],
                            "ring" : hand_landmark.landmark[16],
                            "pinky" : hand_landmark.landmark[20]
                        }
                        # iterate each finger tips
                        for name, landmark in fingers_tips.items():
                            # get the relative x and y of the finger tips
                            x, y = int(landmark.x * w), int(landmark.y * h)
                            # display the name of the detected finger tip on the screen
                            cv2.putText(img = bgr_img,
                                        text = name,
                                        org = (x , y - 10),
                                        fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                                        fontScale = 0.5,
                                        color = (0,0,0),
                                        thickness = 1
                                        )
                    # get position of finger index finger tips
                    x1, y1 = hand_landmark.landmark[5].x , hand_landmark.landmark[5].y  
                    # get position of finger index finger knuckle
                    x2, y2 = hand_landmark.landmark[8].x , hand_landmark.landmark[8].y  

                result = pointer(x1,y1,x2,y2)

            else:
                # no hand detected
                result = "NN"
            
            if display:
                # display the hand detection
                cv2.imshow('Debug Display',bgr_img)  

            if result != None:
                # get the state from the main thread
                exit_hand_gesture = gui_callback(result)

            cv2.waitKey(1)
            
            # exit
            if exit_hand_gesture:
                cam.release()
                cv2.destroyAllWindows()
                break

if __name__ == "__main__":
    exit()
    # hand_gesture_function(display = True)