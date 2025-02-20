import unittest
from shapely.geometry import Polygon
from modules.geometry.simples_shapes import create_circle, create_triangle, create_quadrilateral
from modules.geometry.transform_utils import stretch_one_side, rotate_shape
from modules.geometry.shape_utils import save_as_png, save_as_stl
import os

class TestGeometryModules(unittest.TestCase):

    def test_create_circle(self):
        """Test if create_circle generates a valid Polygon"""
        circle = create_circle()
        self.assertIsInstance(circle, Polygon)
        self.assertGreater(len(circle.exterior.coords), 10)  # Deve ter muitos pontos

    def test_create_triangle(self):
        """Test if create_triangle generates a valid Polygon"""
        triangle = create_triangle(edge=2.0)
        self.assertIsInstance(triangle, Polygon)
        self.assertEqual(len(triangle.exterior.coords), 4)  # Deve ter 3 pontos + 1 para fechamento

    def test_create_quadrilateral(self):
        """Test if create_quadrilateral generates a valid Polygon"""
        quadrilateral = create_quadrilateral(edge=2.0)
        self.assertIsInstance(quadrilateral, Polygon)
        self.assertEqual(len(quadrilateral.exterior.coords), 5)  # 4 pontos + fechamento

    def test_stretch_one_side(self):
        """Test if stretching one side modifies the shape correctly"""
        triangle = create_triangle(edge=2.0)
        stretched = stretch_one_side(triangle, "right", 1.5)
        self.assertIsInstance(stretched, Polygon)
        self.assertNotEqual(triangle, stretched)  # A forma deve mudar

    def test_rotate_shape(self):
        """Test if rotating a shape changes its orientation"""
        triangle = create_triangle(edge=2.0)
        rotated = rotate_shape(triangle, 45)
        self.assertIsInstance(rotated, Polygon)
        self.assertNotEqual(triangle, rotated)  # A rotação deve modificar a forma

    def test_save_as_png(self):
        """Test if the function saves PNG files correctly"""
        circle = create_circle()
        png_filename = "test_circle.png"
        save_as_png(circle, png_filename)
        self.assertTrue(os.path.exists(png_filename))
        os.remove(png_filename)  # Remover o arquivo após o teste

    def test_save_as_stl(self):
        """Test if the function saves STL files correctly"""
        triangle = create_triangle(edge=2.0)
        stl_filename = "test_triangle.stl"
        save_as_stl(triangle, stl_filename)
        self.assertTrue(os.path.exists(stl_filename))
        os.remove(stl_filename)  # Remover o arquivo após o teste

if __name__ == "__main__":
    unittest.main()
