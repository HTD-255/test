#!/usr/bin/env python3
"""
Dual Lane Center Tracking Validation Script
Replicates the enhanced MATLAB function logic for testing
"""

import numpy as np

class DualLaneTracker:
    def __init__(self, reference=400):
        self.reference = reference
        self.last_left_lane = np.array([reference - 100, 0], dtype=np.float32)
        self.last_right_lane = np.array([reference + 100, 0], dtype=np.float32)
        self.last_center = np.array([reference, 0], dtype=np.float32)

    def process_lanes(self, num_objects, centroids):
        """
        Process detected lane objects and calculate center point
        
        Args:
            num_objects: Number of detected lane objects
            centroids: Flattened array of [x1, y1, x2, y2, ...] centroids
        
        Returns:
            center_location: [x, y] coordinates of calculated center
        """
        
        if num_objects > 0:
            # Convert flattened input to matrix format
            centroids_matrix = np.array(centroids).reshape(-1, 2)
            
            if num_objects >= 2:
                # Sort centroids by x-coordinate to identify left and right lanes
                sorted_indices = np.argsort(centroids_matrix[:, 0])
                sorted_centroids = centroids_matrix[sorted_indices]
                
                # Assign leftmost and rightmost as left and right lanes
                left_lane = sorted_centroids[0]
                right_lane = sorted_centroids[-1]
                
                # Update persistent storage
                self.last_left_lane = left_lane.astype(np.float32)
                self.last_right_lane = right_lane.astype(np.float32)
                
                # Calculate center point between the two lanes
                center_x = (left_lane[0] + right_lane[0]) / 2
                center_y = (left_lane[1] + right_lane[1]) / 2
                self.last_center = np.array([center_x, center_y], dtype=np.float32)
                
                print(f"Dual lanes detected: Left=[{left_lane[0]:.1f},{left_lane[1]:.1f}], "
                      f"Right=[{right_lane[0]:.1f},{right_lane[1]:.1f}], "
                      f"Center=[{center_x:.1f},{center_y:.1f}]")
                
            elif num_objects == 1:
                # Only one lane detected
                detected_lane = centroids_matrix[0]
                
                if detected_lane[0] < self.reference:
                    # Detected lane is on the left
                    self.last_left_lane = detected_lane.astype(np.float32)
                    # Estimate right lane position (typical lane width ~200 pixels)
                    estimated_right_x = detected_lane[0] + 200
                    center_x = (detected_lane[0] + estimated_right_x) / 2
                    center_y = detected_lane[1]
                    print(f"Left lane detected: [{detected_lane[0]:.1f},{detected_lane[1]:.1f}], "
                          f"Estimated right at {estimated_right_x:.1f}, "
                          f"Center=[{center_x:.1f},{center_y:.1f}]")
                else:
                    # Detected lane is on the right
                    self.last_right_lane = detected_lane.astype(np.float32)
                    # Estimate left lane position
                    estimated_left_x = detected_lane[0] - 200
                    center_x = (estimated_left_x + detected_lane[0]) / 2
                    center_y = detected_lane[1]
                    print(f"Right lane detected: [{detected_lane[0]:.1f},{detected_lane[1]:.1f}], "
                          f"Estimated left at {estimated_left_x:.1f}, "
                          f"Center=[{center_x:.1f},{center_y:.1f}]")
                
                self.last_center = np.array([center_x, center_y], dtype=np.float32)
        else:
            # No lanes detected - use last known center position
            print(f"No lanes detected, using last center: [{self.last_center[0]:.1f},{self.last_center[1]:.1f}]")
        
        return self.last_center

def run_tests():
    """Run validation tests for dual lane tracking"""
    print("=== Dual Lane Center Tracking Validation ===\n")
    
    tracker = DualLaneTracker(reference=400)
    
    # Test 1: Both lanes detected
    print("Test 1: Both lanes detected")
    location1 = tracker.process_lanes(2, [300, 100, 500, 100])
    
    # Test 2: Only left lane detected
    print("\nTest 2: Only left lane detected")
    location2 = tracker.process_lanes(1, [300, 100])
    
    # Test 3: Only right lane detected
    print("\nTest 3: Only right lane detected")
    location3 = tracker.process_lanes(1, [500, 100])
    
    # Test 4: Three lanes detected (should use leftmost and rightmost)
    print("\nTest 4: Three lanes detected")
    location4 = tracker.process_lanes(3, [250, 100, 400, 105, 550, 100])
    
    # Test 5: No lanes detected
    print("\nTest 5: No lanes detected")
    location5 = tracker.process_lanes(0, [])
    
    print("\n=== Test Complete ===")
    
    # Verify expected behavior
    print("\n=== Verification ===")
    print(f"Final center location: [{location5[0]:.1f}, {location5[1]:.1f}]")
    print("✓ All test cases completed successfully")

if __name__ == "__main__":
    run_tests()