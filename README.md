# Robot Rescue Pathfinding

This project is a pathfinding visualization simulation based on a Weighted Graph using Python and Pygame. The program simulates a rescue robot that must evacuate 3 victims scattered across a 6x6 node area.

## Algorithms Used

This rescue robot uses two main algorithms that can be directly compared in terms of performance:

1. **Breadth-First Search (BFS):**
An algorithm that searches for routes based on the fewest number of steps (edges), without considering the actual weight or distance between nodes.
2. **Dijkstra's Algorithm:**
A shortest-path algorithm that considers the smallest total weight (cost/distance), allowing the robot to choose a longer route if the total cost is lower.

**Rescue Logic (Greedy Nearest Neighbor)**
Since there are 3 victims to rescue, the robot is equipped with a Greedy strategy. From its current position, the robot calculates the distance to all remaining victims and automatically prioritizes rescuing the victim with the "cheapest" route first (based on steps for BFS, or total weight for Dijkstra).

##  How to Run the Program

### Prerequisites
Make sure Python 3.x is installed on your computer. This program also requires the external pygame library.

### Installation Steps

1. Clone this repository to your local machine:
```
git clone https://github.com/Kifrx/Robot-rescue.git
```
2. Navigate into the project directory:
```
cd Robot-rescue
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Run the main program:
```
python main.py
```

## How to Play??
1. When the program starts, click on one of the circles (nodes) to place the Robot.
2. Click on 3 different nodes to place the Victims.
3. Pay attention to the yellow text panel at the top for the current status instructions.
4. After all positions are set, click either the Run BFS or Run Dijkstra button.
5. Watch the robot movement animation and compare the statistics for Total Steps and Total Weight displayed at the bottom of the screen.
6. Click the Reset button to clear and restart the simulation from the beginning.
