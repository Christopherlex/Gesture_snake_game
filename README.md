# Snake Game with Hand Gesture Control
This is a simple Python-based implementation of the classic Snake game with hand gesture controls using the webcam. The game is controlled by detecting the user's hand gestures through the webcam and interpreting the thumb movement as the snake's direction.

# Features
Hand Gesture Control: Use the webcam to control the snake's movement with your hand. The snake's direction is determined by the movement of your thumb.
Snake Movement Control: The snake will keep moving when all five fingers are extended. It will only change direction when the thumb is the only finger visible.
Food Generation: The snake eats food and grows, just like the classic Snake game.
Game Over State: The game ends if the snake collides with the walls or itself.
Easy Restart: The game can be restarted by pressing 'R' after the game over screen appears.

# Required Modules:
cv2 (OpenCV) - A powerful library for computer vision tasks. It is used here for reading the webcam feed, processing images, and displaying the game interface.
numpy - Used for creating and manipulating arrays, particularly the game grid and rendering the snake and food.
cvzone - A library built on top of OpenCV that simplifies hand tracking and gesture recognition. It is used to detect hand movements and interpret them as snake direction changes.

# How to Play
Run the game: Launch the game by running the snake_game.py script.
Control the snake: The game uses hand gestures to control the snake:
The direction of the snake is determined by the movement of your thumb.
When all five fingers are visible, the snake will keep moving in the same direction.
The direction can be changed only when only the thumb is showing.
Game Over: The game ends if the snake collides with itself or the wall. Press 'R' to restart after the game ends.

# How to Run
Clone or download the repository to your local machine.
Install the required dependencies by running the pip install command.
Run the snake_game.py script.
Make sure your webcam is working and give the script access to it.
