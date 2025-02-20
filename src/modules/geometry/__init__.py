"""
Geometry module for generating and manipulating geometric shapes.

This module provides a collection of functions and classes for creating and transforming
various geometric shapes, including semicircles, ellipsoids, and triangles. It also includes
utility functions for rotating shapes, stretching shapes, and saving shapes as STL and PNG files.

Sub-modules:
- simples_shapes: Functions for generating basic shapes (circle, triangle, quadrilateral).
- transform_utils: Utility functions for transforming shapes (rotation, stretching).
- shape_utils: Utility functions for saving shapes (STL, PNG).
"""

# Import main functions for easy access
from .simples_shapes import create_circle, create_triangle, create_quadrilateral
from .transform_utils import stretch_one_side, rotate_shape
from .shape_utils import save_as_stl, save_as_png
