function location = dual_lane_tracking_test(NumberOfObjects, u, reference)
% Test function to validate dual-lane center tracking logic
% This replicates the enhanced MATLAB function logic for validation

% Enhanced dual-lane center tracking implementation
% Detects left and right lanes separately and calculates center point

persistent last_left_lane last_right_lane last_center;

location = single([0 0]);

% Initialize persistent variables
if isempty(last_left_lane)
    last_left_lane = single([reference-100 0]);  % Offset left from reference
end
if isempty(last_right_lane)
    last_right_lane = single([reference+100 0]); % Offset right from reference  
end
if isempty(last_center)
    last_center = single([reference 0]);
end

% Process detected lane objects
if NumberOfObjects > 0
    % Convert input to matrix format for easier processing
    centroids = reshape(u, 2, [])';  % Each row is [x, y]
    
    if NumberOfObjects >= 2
        % Sort centroids by x-coordinate to identify left and right lanes
        [~, sort_idx] = sort(centroids(:,1));
        sorted_centroids = centroids(sort_idx, :);
        
        % Assign leftmost and rightmost as left and right lanes
        left_lane = sorted_centroids(1, :);
        right_lane = sorted_centroids(end, :);
        
        % Update persistent storage
        last_left_lane = single(left_lane);
        last_right_lane = single(right_lane);
        
        % Calculate center point between the two lanes
        center_x = (left_lane(1) + right_lane(1)) / 2;
        center_y = (left_lane(2) + right_lane(2)) / 2;
        last_center = single([center_x center_y]);
        
        fprintf('Dual lanes detected: Left=[%.1f,%.1f], Right=[%.1f,%.1f], Center=[%.1f,%.1f]\n', ...
                left_lane(1), left_lane(2), right_lane(1), right_lane(2), center_x, center_y);
        
    elseif NumberOfObjects == 1
        % Only one lane detected - determine if it's left or right
        detected_lane = centroids(1, :);
        
        % Compare with reference position to classify as left or right
        if detected_lane(1) < reference
            % Detected lane is on the left
            last_left_lane = single(detected_lane);
            % Estimate right lane position based on typical lane width (~200 pixels)
            estimated_right_x = detected_lane(1) + 200;
            % Calculate center point
            center_x = (detected_lane(1) + estimated_right_x) / 2;
            center_y = detected_lane(2);
            fprintf('Left lane detected: [%.1f,%.1f], Estimated right at %.1f, Center=[%.1f,%.1f]\n', ...
                    detected_lane(1), detected_lane(2), estimated_right_x, center_x, center_y);
        else
            % Detected lane is on the right  
            last_right_lane = single(detected_lane);
            % Estimate left lane position
            estimated_left_x = detected_lane(1) - 200;
            % Calculate center point
            center_x = (estimated_left_x + detected_lane(1)) / 2;
            center_y = detected_lane(2);
            fprintf('Right lane detected: [%.1f,%.1f], Estimated left at %.1f, Center=[%.1f,%.1f]\n', ...
                    detected_lane(1), detected_lane(2), estimated_left_x, center_x, center_y);
        end
        
        last_center = single([center_x center_y]);
    end
else
    % No lanes detected - use last known center position
    fprintf('No lanes detected, using last center: [%.1f,%.1f]\n', last_center(1), last_center(2));
end

% Output the calculated center location
location = last_center;

end

% Test cases
fprintf('=== Dual Lane Center Tracking Validation ===\n\n');

% Test 1: Dual lanes detected
fprintf('Test 1: Both lanes detected\n');
location1 = dual_lane_tracking_test(2, [300, 100, 500, 100], 400);

% Test 2: Only left lane detected  
fprintf('\nTest 2: Only left lane detected\n');
location2 = dual_lane_tracking_test(1, [300, 100], 400);

% Test 3: Only right lane detected
fprintf('\nTest 3: Only right lane detected\n');  
location3 = dual_lane_tracking_test(1, [500, 100], 400);

% Test 4: No lanes detected
fprintf('\nTest 4: No lanes detected\n');
location4 = dual_lane_tracking_test(0, [], 400);

fprintf('\n=== Test Complete ===\n');