# Dual Lane Center Tracking Implementation

## Overview
Enhanced the existing single-lane tracking system to detect both left and right lanes separately and calculate the center point between them for improved lane centering.

## Changes Made

### 1. Image Processing Enhancement
**File**: `simulink/systems/system_2836.xml` (Lane Location subsystem)
- **Modified**: Image Find Objects block parameter
- **Change**: `num_objects` increased from `1` to `3` 
- **Purpose**: Enable detection of multiple lane objects instead of just the largest one

### 2. Enhanced MATLAB Function
**File**: `simulink/stateflow/chart_104.xml` (Lane Location MATLAB Function)
- **Replaced**: Single-lane tracking logic with dual-lane center tracking
- **New Features**:
  - Separate persistent storage for left lane, right lane, and center position
  - Dual-lane detection and classification based on x-coordinate sorting
  - Center point calculation as average of left and right lane positions
  - Robust fallback for single-lane detection scenarios
  - Estimation logic when only one lane is detected (using typical 200-pixel lane width)

## Technical Details

### Algorithm Logic
1. **Multiple Lanes Detected (≥2)**:
   - Sort detected centroids by x-coordinate
   - Assign leftmost as left lane, rightmost as right lane
   - Calculate center: `(left_x + right_x) / 2, (left_y + right_y) / 2`

2. **Single Lane Detected**:
   - Compare detected lane position with reference to classify as left or right
   - Estimate missing lane position using typical lane width (200 pixels)
   - Calculate center point using detected + estimated positions

3. **No Lanes Detected**:
   - Use last known center position (maintains original fallback behavior)

### Compatibility
- ✅ Maintains existing interface (2 inputs, 2 outputs)
- ✅ Preserves data types (single precision)
- ✅ Compatible with timing constraints (500Hz, 120Hz, 100Hz)
- ✅ Keeps OCar I/O interface unchanged
- ✅ Maintains diagnostic display capabilities

## Expected Benefits
- **Improved Lane Centering**: Vehicle follows calculated center between lanes
- **Enhanced Robustness**: Better handling of varying lane widths and road conditions
- **Dual-Lane Awareness**: System now actively tracks both lane boundaries
- **Fallback Safety**: Graceful degradation when only one lane is visible

## Testing Recommendations
1. Test in scenarios with clearly visible left and right lanes
2. Verify behavior when only one lane is detected
3. Test fallback behavior in poor visibility conditions
4. Validate center point calculation accuracy
5. Confirm steering response follows calculated center point