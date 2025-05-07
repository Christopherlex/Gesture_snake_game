import cv2
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector

# Initialize dimensions
GAME_WIDTH, GAME_HEIGHT = 600, 600
CAM_WIDTH, CAM_HEIGHT = 600, 600
SQUARE_SIZE = 20
FPS = 10

# Initialize game variables
snake_pos = [[GAME_WIDTH//2, GAME_HEIGHT//2]]
snake_dir = 'RIGHT'
food_pos = [random.randint(0, (GAME_WIDTH - SQUARE_SIZE) // SQUARE_SIZE) * SQUARE_SIZE,
            random.randint(0, (GAME_HEIGHT - SQUARE_SIZE) // SQUARE_SIZE) * SQUARE_SIZE]
game_over = False
base_speed = 15
current_speed = base_speed
speed_increase = 2
food_count = 0
lock_direction = False  # New variable to lock direction when full hand is detected

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (255, 0, 0)

# Set up the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: No camera found.")
        exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

detector = HandDetector(detectionCon=0.8, maxHands=1)

def spawn_food():
    while True:
        new_food = [random.randint(0, (GAME_WIDTH - SQUARE_SIZE) // SQUARE_SIZE) * SQUARE_SIZE,
                   random.randint(0, (GAME_HEIGHT - SQUARE_SIZE) // SQUARE_SIZE) * SQUARE_SIZE]
        if new_food not in snake_pos:
            return new_food

def move_snake():
    global snake_pos, food_pos, game_over, current_speed, food_count
    
    head = snake_pos[0].copy()
    if snake_dir == 'UP':
        head[1] -= SQUARE_SIZE
    elif snake_dir == 'DOWN':
        head[1] += SQUARE_SIZE
    elif snake_dir == 'LEFT':
        head[0] -= SQUARE_SIZE
    elif snake_dir == 'RIGHT':
        head[0] += SQUARE_SIZE
    
    snake_pos.insert(0, head)
    
    if head == food_pos:
        food_pos = spawn_food()
        food_count += 1
        current_speed = max(3, base_speed - (food_count * speed_increase))
    else:
        snake_pos.pop()

def draw_elements(img):
    # Draw game border
    cv2.rectangle(img, (0, 0), (GAME_WIDTH, GAME_HEIGHT), BLUE, 2)
    
    # Draw snake with eyes on head
    for i, segment in enumerate(snake_pos):
        color = GREEN
        cv2.rectangle(img, (segment[0], segment[1]), 
                     (segment[0] + SQUARE_SIZE, segment[1] + SQUARE_SIZE), 
                     color, -1)
        
        if i == 0:
            eye_size = SQUARE_SIZE // 4
            pupil_size = eye_size // 2
            
            if snake_dir == 'RIGHT':
                left_eye = (segment[0] + SQUARE_SIZE - eye_size - 2, segment[1] + 5)
                right_eye = (segment[0] + SQUARE_SIZE - eye_size - 2, segment[1] + SQUARE_SIZE - 5 - eye_size)
            elif snake_dir == 'LEFT':
                left_eye = (segment[0] + 2, segment[1] + 5)
                right_eye = (segment[0] + 2, segment[1] + SQUARE_SIZE - 5 - eye_size)
            elif snake_dir == 'UP':
                left_eye = (segment[0] + 5, segment[1] + 2)
                right_eye = (segment[0] + SQUARE_SIZE - 5 - eye_size, segment[1] + 2)
            else:
                left_eye = (segment[0] + 5, segment[1] + SQUARE_SIZE - eye_size - 2)
                right_eye = (segment[0] + SQUARE_SIZE - 5 - eye_size, segment[1] + SQUARE_SIZE - eye_size - 2)
            
            cv2.circle(img, left_eye, eye_size, WHITE, -1)
            cv2.circle(img, right_eye, eye_size, WHITE, -1)
            cv2.circle(img, left_eye, pupil_size, BLACK, -1)
            cv2.circle(img, right_eye, pupil_size, BLACK, -1)
    
    # Draw food
    cv2.rectangle(img, (food_pos[0], food_pos[1]), 
                 (food_pos[0] + SQUARE_SIZE, food_pos[1] + SQUARE_SIZE), 
                 RED, -1)

def check_collisions():
    head = snake_pos[0]
    if (head[0] < 0 or head[0] >= GAME_WIDTH or 
        head[1] < 0 or head[1] >= GAME_HEIGHT):
        return True
    if head in snake_pos[1:]:
        return True
    return False

def detect_hand_gesture(hand):
    global snake_dir, lock_direction
    fingers = detector.fingersUp(hand)
    
    # Check for full hand (all fingers up)
    if all(fingers):
        lock_direction = True
    # Check for only thumb up (other fingers down)
    elif fingers == [1, 0, 0, 0, 0]:
        lock_direction = False
    
    # Only change direction if not locked
    if not lock_direction:
        lmList = hand['lmList']
        thumb_tip = lmList[4]
        thumb_mcp = lmList[2]
        
        dx = thumb_tip[0] - thumb_mcp[0]
        dy = thumb_tip[1] - thumb_mcp[1]
        
        if abs(dx) > abs(dy):
            new_dir = 'RIGHT' if dx > 0 else 'LEFT'
        else:
            new_dir = 'DOWN' if dy > 0 else 'UP'
        
        if not ((new_dir == 'UP' and snake_dir == 'DOWN') or
                (new_dir == 'DOWN' and snake_dir == 'UP') or
                (new_dir == 'LEFT' and snake_dir == 'RIGHT') or
                (new_dir == 'RIGHT' and snake_dir == 'LEFT')):
            snake_dir = new_dir

cv2.namedWindow("Snake Game with Camera", cv2.WINDOW_NORMAL)

frame_count = 0

while True:
    success, cam_img = cap.read()
    if not success:
        print("Error: Could not read frame from camera")
        break
    
    cam_img = cv2.flip(cam_img, 1)
    cam_img = cv2.resize(cam_img, (CAM_WIDTH, CAM_HEIGHT))
    
    game_img = np.ones((GAME_HEIGHT, GAME_WIDTH, 3), dtype=np.uint8) * 255
    
    hands = detector.findHands(cam_img, draw=False)
    
    if hands:
        hand = hands[0]
        detect_hand_gesture(hand)
    
    frame_count += 1
    
    if not game_over:
        if frame_count % current_speed == 0:
            move_snake()
            if check_collisions():
                game_over = True
        
        draw_elements(game_img)
        
        # Display direction lock status
        if lock_direction:
            text = "DIRECTION LOCKED"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            text_x = GAME_WIDTH - text_size[0] - 20  # 20 pixels from right edge
            text_y = text_size[1] + 20  # 20 pixels from top
            cv2.putText(game_img, text, (text_x, text_y), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED, 2)
    else:
        cv2.putText(game_img, "GAME OVER", (GAME_WIDTH//2-150, GAME_HEIGHT//2-50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, RED, 3)
        cv2.putText(game_img, f"Food eaten: {food_count}", (GAME_WIDTH//2-100, GAME_HEIGHT//2+20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, BLACK, 2)
        cv2.putText(game_img, "Press 'R' to Restart", (GAME_WIDTH//2-120, GAME_HEIGHT//2+70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, BLACK, 2)
    
    combined_img = np.hstack((game_img, cam_img))
    cv2.line(combined_img, (GAME_WIDTH, 0), (GAME_WIDTH, GAME_HEIGHT), BLACK, 2)
    cv2.putText(combined_img, "SNAKE GAME", (50, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, BLACK, 2)
    cv2.putText(combined_img, "HAND CONTROL", (GAME_WIDTH + 50, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, BLACK, 2)
    
    cv2.imshow("Snake Game with Camera", combined_img)
    
    key = cv2.waitKey(1000//FPS)
    if key == ord('q'):
        break
    elif key == ord('r') and game_over:
        snake_pos = [[GAME_WIDTH//2, GAME_HEIGHT//2]]
        snake_dir = 'RIGHT'
        food_pos = spawn_food()
        game_over = False
        frame_count = 0
        current_speed = base_speed
        food_count = 0
        lock_direction = False

cap.release()
cv2.destroyAllWindows()