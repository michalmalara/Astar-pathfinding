# Astar-pathfinding

required modules:
  -pygame
  -numpy
  
This algorithm is used to find path between two points on 2-D space with obstacles.

How to use the application:
First define starting point (orange square) by clicking left mouse button on the board.
Second, define target point (blue square) by clicking left mouse button on the board.
Third draw obstacles (black squares) between start and end point by clicking left mouse button on the board.
Press 'Enter' to find the path step by step.
Press 'Space' to find the path instantly.

Red squares are closed points.
Green squares are open points.
The path will be marked purple.

The algorithm description:
https://en.wikipedia.org/wiki/A*_search_algorithm