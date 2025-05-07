import pygame
import math
from constants import *

class PolygonShape:
    def __init__(self, x, y, vertices):
        """
        Initialize a polygon shape.
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
            vertices (list): List of pygame.Vector2 points relative to center
        """
        self.position = pygame.Vector2(x, y)
        self.vertices = vertices  # List of Vector2 objects relative to center
        self.rotation = 0
        self.velocity = pygame.Vector2(0, 0)
        
        # Calculate a bounding radius for broad-phase collision detection
        self.radius = max([  vertices.length() ])
    
    def get_absolute_vertices(self):
        """Returns the vertices in world coordinates, accounting for position and rotation."""
        absolute_vertices = []
        for vertex in self.vertices:

            # Rotate the vertex by the current rotation 
            rotated = vertex.rotate(self.rotation)
            # Add the position to get the absolute position # WHY
            absolute_position = self.position + rotated
            absolute_vertices.append(absolute_position)
        return absolute_vertices
    
    def draw(self, screen):
        """Draw the polygon to the screen."""
        vertices = self.get_absolute_vertices()
        pygame.draw.polygon(screen, (255, 255, 255), vertices, 2)
        
        # Optionally draw the bounding circle for debugging
        # pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), 
        #                  int(self.radius), 1)
    
    def point_in_polygon(self, point):
        """
        Check if a point is inside the polygon using the ray casting algorithm.
        
        Args:
            point (pygame.Vector2): Point to check
            
        Returns:
            bool: True if the point is inside the polygon
        """
        vertices = self.get_absolute_vertices()
        inside = False
        
        # Ray casting algorithm
        j = len(vertices) - 1
        for i in range(len(vertices)):
            if ((vertices[i].y > point.y) != (vertices[j].y > point.y)) and \
               (point.x < vertices[i].x + (vertices[j].x - vertices[i].x) * 
                (point.y - vertices[i].y) / (vertices[j].y - vertices[i].y)):
                inside = not inside
            j = i
            
        return inside
    
    def line_segment_intersection(self, line_start, line_end):
        """
        Check if a line segment intersects with any edge of the polygon.
        
        Args:
            line_start (pygame.Vector2): Start point of line
            line_end (pygame.Vector2): End point of line
            
        Returns:
            bool: True if there's an intersection
        """
        vertices = self.get_absolute_vertices()
        
        for i in range(len(vertices)):
            j = (i + 1) % len(vertices)
            
            # Line segments
            edge_start = vertices[i]
            edge_end = vertices[j]
            
            # Check intersection using line-line intersection formula
            div = ((line_end.y - line_start.y) * (edge_end.x - edge_start.x) - 
                   (line_end.x - line_start.x) * (edge_end.y - edge_start.y))
            
            if div == 0:  # Lines are parallel
                continue
                
            ua = ((line_end.x - line_start.x) * (edge_start.y - line_start.y) - 
                  (line_end.y - line_start.y) * (edge_start.x - line_start.x)) / div
            ub = ((edge_end.x - edge_start.x) * (edge_start.y - line_start.y) - 
                  (edge_end.y - edge_start.y) * (edge_start.x - line_start.x)) / div
                  
            # If ua and ub are between 0-1, the lines intersect
            if 0 <= ua <= 1 and 0 <= ub <= 1:
                return True
                
        return False
    
    def circle_collision(self, circle_pos, circle_radius):
        """
        Check for collision between this polygon and a circle.
        
        Args:
            circle_pos (pygame.Vector2): Circle center position
            circle_radius (float): Circle radius
            
        Returns:
            bool: True if there's a collision
        """
        # First, quick check using bounding circles
        if (circle_pos - self.position).length() > (self.radius + circle_radius):
            return False
        
        vertices = self.get_absolute_vertices()
        
        # Check if the circle center is inside the polygon
        if self.point_in_polygon(circle_pos):
            return True
        
        # Check if any polygon edge intersects the circle
        for i in range(len(vertices)):
            j = (i + 1) % len(vertices)
            edge_start = vertices[i]
            edge_end = vertices[j]
            
            # Find the closest point on the line segment to the circle center
            edge_vec = edge_end - edge_start
            t_max = edge_vec.length()
            if t_max == 0:  # If edge has zero length
                continue
                
            # Normalize edge vector
            edge_vec /= t_max
            
            # Vector from edge start to circle center
            circle_vec = circle_pos - edge_start
            
            # Project circle_vec onto edge_vec
            projection = circle_vec.dot(edge_vec)
            
            # Clamp projection to the edge length
            projection = max(0, min(t_max, projection))
            
            # Find the closest point on the edge to the circle center
            closest_point = edge_start + edge_vec * projection
            
            # Check if this point is within circle radius
            if (circle_pos - closest_point).length() <= circle_radius:
                return True
                
        return False
    
    def polygon_collision(self, other_polygon):
        """
        Check for collision between this polygon and another polygon.
        Uses the Separating Axis Theorem (SAT).
        
        Args:
            other_polygon (PolygonShape): The other polygon to check collision with
            
        Returns:
            bool: True if the polygons are colliding
        """
        # Quick bounding circle check first
        if (other_polygon.position - self.position).length() > (self.radius + other_polygon.radius):
            return False
            
        # Get vertices of both polygons
        vertices1 = self.get_absolute_vertices()
        vertices2 = other_polygon.get_absolute_vertices()
        
        # Check edges of this polygon
        for i in range(len(vertices1)):
            j = (i + 1) % len(vertices1)
            edge = vertices1[j] - vertices1[i]
            # Get the perpendicular vector to the edge (normal)
            normal = pygame.Vector2(-edge.y, edge.x).normalize()
            
            # Project both polygons onto the normal
            min1, max1 = self._project_onto_axis(vertices1, normal)
            min2, max2 = self._project_onto_axis(vertices2, normal)
            
            # Check for separation
            if max1 < min2 or max2 < min1:
                return False  # Found a separating axis, no collision
        
        # Check edges of the other polygon
        for i in range(len(vertices2)):
            j = (i + 1) % len(vertices2)
            edge = vertices2[j] - vertices2[i]
            normal = pygame.Vector2(-edge.y, edge.x).normalize()
            
            min1, max1 = self._project_onto_axis(vertices1, normal)
            min2, max2 = self._project_onto_axis(vertices2, normal)
            
            if max1 < min2 or max2 < min1:
                return False
        
        # No separating axis found, there is a collision
        return True
    
    def _project_onto_axis(self, vertices, axis):
        """
        Project vertices onto an axis and return min and max values.
        
        Args:
            vertices (list): List of pygame.Vector2 points
            axis (pygame.Vector2): The axis to project onto (should be normalized)
            
        Returns:
            tuple: (min_projection, max_projection)
        """
        min_proj = float('inf')
        max_proj = float('-inf')
        
        for vertex in vertices:
            projection = vertex.dot(axis)
            min_proj = min(min_proj, projection)
            max_proj = max(max_proj, projection)
            
        return min_proj, max_proj
    
    def collide_with(self, other):
        """
        Check collision with another object based on its type.
        
        Args:
            other: Another game object with position and shape attributes
            
        Returns:
            bool: True if there's a collision
        """
        if hasattr(other, 'radius'):  # If other is a circle
            return self.circle_collision(other.position, other.radius)
        elif hasattr(other, 'vertices'):  # If other is a polygon
            return self.polygon_collision(other)
        return False
    
    def update(self, dt):
        """Update the polygon position based on velocity."""
        self.position += self.velocity * dt