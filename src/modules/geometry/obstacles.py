from modules.geometry.ellipsoid import generate_ellipsoids
from modules.geometry.semicircle import generate_semicircles


def generate_obstacles():
    """
    Generate both ellipsoids and semicircles.
    This function will be called when running the script as a whole.

    The function is useful for generating all obstacle shapes in one go.
    """
    # Generate and save ellipsoids
    generate_ellipsoids()

    # Generate and save semicircles
    generate_semicircles()


# Execute directly if needed
if __name__ == "__main__":
    # Uncomment one of the following lines based on what you want to test or generate
    # To generate both ellipsoids and semicircles
    generate_obstacles()
