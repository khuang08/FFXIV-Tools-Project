import os
import json
import cv2
import numpy as np
import math
from typing import List, Tuple, Dict, Any

# Configuration
MAPS_FOLDER = "maps"
DATA_FILE = "hunt_marks.json"
OUTPUT_FOLDER = "generated_paths"

# Fixed expansion order
EXPANSION_ORDER = [
    "ARR",
    "Heavensward",
    "Stormblood",
    "Shadowbringers",
    "Endwalker",
    "Dawntrail"
]

def ensure_output_folder():
    """Create output folder if it doesn't exist"""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

def sanitize_filename(name: str) -> str:
    """Convert hunt mark name to safe filename"""
    return name.replace(" ", "_").replace("/", "-")

def draw_and_save_path(image_path: str, path: List[Tuple[int, int]], hunt_mark_name: str) -> str:
    """Draw the path on the image and save with hunt mark name"""
    img = cv2.imread(image_path)
    
    # Draw connecting lines
    for i in range(len(path)-1):
        cv2.line(img, path[i], path[i+1], (0, 0, 255), 3)  # Red lines
    
    # Mark start (green) and end (orange) points
    cv2.circle(img, path[0], 10, (0, 255, 0), -1)
    cv2.circle(img, path[-1], 10, (0, 165, 255), -1)
    
    # Create output filename
    safe_name = sanitize_filename(hunt_mark_name)
    output_path = os.path.join(OUTPUT_FOLDER, f"{safe_name}_path.jpg")
    
    # Save result
    cv2.imwrite(output_path, img)
    return output_path

def process_map(image_path: str, hunt_mark: Dict[str, Any]) -> None:
    """Process the map image and generate path"""
    # Detect all circles
    all_points = detect_red_circles(image_path)
    if not all_points:
        print("No circles detected!")
        return
    
    # Exclude outliers
    filtered_points = exclude_outliers(all_points)
    print(f"\nFiltered {len(all_points)-len(filtered_points)} outlier points")
    
    # Find leftmost point as starting point
    start_point = find_leftmost_point(filtered_points)
    
    # Generate path
    path = nearest_neighbor_path(start_point, filtered_points)
    
    # Print coordinates
    print_coordinates(path)
    
    # Draw and save path with hunt mark name
    output_path = draw_and_save_path(image_path, path, hunt_mark['name'])
    print(f"\nPath visualization saved to: {output_path}")

def load_hunt_data() -> List[Dict[str, Any]]:
    """Load hunt mark data from JSON file"""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {DATA_FILE} not found. Please create the data file.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: {DATA_FILE} contains invalid JSON.")
        exit(1)

def select_expansion(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Let user select an expansion using predefined order"""
    print("\nSelect an expansion:")
    for i, exp in enumerate(EXPANSION_ORDER, 1):
        print(f"{i}. {exp}")
    
    while True:
        try:
            selection = int(input("\nEnter expansion number: "))
            if 1 <= selection <= len(EXPANSION_ORDER):
                selected_exp = EXPANSION_ORDER[selection - 1]
                return [m for m in data if m['expansion'] == selected_exp]
            print(f"Please enter a number between 1 and {len(EXPANSION_ORDER)}")
        except ValueError:
            print("Please enter a valid number")

def select_hunt_mark(mark_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Let user select a hunt mark"""
    print(f"\nAvailable B-rank marks:")
    for mark in mark_list:
        print(f"{mark['map_code']}. {mark['name']}")
    
    while True:
        try:
            selection = input("\nEnter hunt mark ID number: ")
            if not selection.isdigit():
                print("Please enter a valid number")
                continue
                
            selection = int(selection)
            for mark in mark_list:
                if mark['map_code'] == selection:
                    return mark
            print("No hunt mark found with that ID. Try again.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            exit()

def find_map_image(filename: str) -> str:
    """Find map image file in maps folder"""
    path = os.path.join(MAPS_FOLDER, filename)
    if not os.path.exists(path):
        print(f"Error: Map image not found at {path}")
        exit(1)
    return path

def detect_red_circles(image_path: str) -> List[Tuple[int, int]]:
    """Detect red circles in the map image"""
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not load image")
        return []
    
    # Convert to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define red color ranges
    lower_red1 = np.array([0, 100, 50])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([160, 100, 50])
    upper_red2 = np.array([180, 255, 255])
    
    # Create masks for red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)
    
    # Apply morphological operations
    kernel = np.ones((3,3), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
    
    # Detect circles
    circles = cv2.HoughCircles(red_mask, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                             param1=40, param2=25, minRadius=8, maxRadius=50)
    
    if circles is None:
        return []
    
    circles = np.uint16(np.around(circles))
    return [(c[0], c[1]) for c in circles[0]]

def exclude_outliers(points: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Exclude points in bottom-left corner (X: 0-300, Y: 930-1024)"""
    return [p for p in points if not (p[0] <= 300 and p[1] >= 930)]

def find_leftmost_point(points: List[Tuple[int, int]]) -> Tuple[int, int]:
    """Find point with smallest x-coordinate"""
    return min(points, key=lambda p: p[0])

def nearest_neighbor_path(start_point: Tuple[int, int], points: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Generate path using nearest neighbor algorithm"""
    remaining_points = points.copy()
    path = [start_point]
    
    if start_point in remaining_points:
        remaining_points.remove(start_point)
    
    current_point = start_point
    while remaining_points:
        next_point = min(remaining_points, key=lambda p: math.dist(current_point, p))
        path.append(next_point)
        remaining_points.remove(next_point)
        current_point = next_point
    
    return path

def print_coordinates(path: List[Tuple[int, int]]) -> None:
    """Print coordinates in both pixel and game units"""
    print("\nPath Coordinates:")
    for i, (px, py) in enumerate(path, 1):
        game_x = round(px * (44 / 1024), 2)
        game_y = round(py * (44 / 1024), 2)
        print(f"Point {i}: Pixel ({px}, {py}) | Game ({game_x:.2f}, {game_y:.2f})")

def main():
    print("FFXIV Hunt Mark Path Generator")
    print("==============================")
    
    # Ensure output folder exists
    ensure_output_folder()
    
    # Load hunt data
    hunt_data = load_hunt_data()
    
    # Let user select expansion and hunt mark
    expansion_marks = select_expansion(hunt_data)
    hunt_mark = select_hunt_mark(expansion_marks)
    
    print(f"\nSelected: {hunt_mark['name']} (ID: {hunt_mark['map_code']})")
    
    # Find and process the map image
    map_image = find_map_image(hunt_mark['filename'])
    print(f"Processing map: {map_image}")
    
    # Process the map
    process_map(map_image, hunt_mark)

if __name__ == "__main__":
    # Create maps folder if it doesn't exist
    if not os.path.exists(MAPS_FOLDER):
        os.makedirs(MAPS_FOLDER)
    
    main()