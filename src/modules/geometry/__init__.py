"""
Geometry module for generating and manipulating geometric shapes.

This module provides a collection of functions and classes for creating and transforming
various geometric shapes, including semicircles, ellipsoids, and triangles. It also includes
utility functions for rotating shapes, stretching shapes, and saving shapes as STL and PNG files.

Sub-modules:
- semicircles: Functions for generating semicircles.
- ellipsoids: Functions for generating ellipsoids.
- triangles: Functions for generating triangles.
- transform_utils: Utility functions for transforming shapes (e.g., rotation, stretching).
- shape_utils: Utility functions for saving shapes (e.g., saving as STL, PNG).

Simplified imports for users:
- from geometry import create_semicircle, generate_ellipsoids, generate_triangles
- from geometry import rotate_shape, save_as_stl
"""

# Importing functions and classes from sub-modules
from .semicircles import create_semicircle
from .ellipsoids import generate_ellipsoids
from .triangles import generate_triangles
from .transform_utils import rotate_shape, stretch_one_side
from .shape_utils import save_as_stl, save_as_png

# Simplified imports for users
# from geometry import create_semicircle, generate_ellipsoids, generate_triangles
# or
# from geometry import rotate_shape, save_as_stl
