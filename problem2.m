% 1. Convert geographic coordinates to UTM
function [utmX, utmY] = convert_to_utm(lat, lon)
    % Define UTM projection (Zone 18N, WGS84 ellipsoid)
    % Note: Requires Mapping Toolbox
    utmProj = projcrs(32618, 'Authority', 'EPSG');
    [utmX, utmY] = projfwd(utmProj, lat, lon);
end

% 2. Generate random population points within the network boundary
function populationPoints = generate_population_points(coords, numPoints)
    % Generate points uniformly within the coordinate bounds
    xMin = min(coords(:, 1));
    yMin = min(coords(:, 2));
    xMax = max(coords(:, 1));
    yMax = max(coords(:, 2));
    populationPoints = [rand(numPoints, 1) * (xMax - xMin) + xMin, ...
                        rand(numPoints, 1) * (yMax - yMin) + yMin];
end

% 3. Plot the service area with radius coverage
function plot_service_area(coords, populationPoints, busStops, radius, filename)
    figure;
    hold on;
    
    % Plot population points
    scatter(populationPoints(:, 1), populationPoints(:, 2), 10, 'b', 'filled', ...
            'DisplayName', 'Population Points');
            
    % Plot sampled bus stops
    sampledStops = busStops(1:10:end, :); % Take every 10th stop to reduce density
    scatter(sampledStops(:, 1), sampledStops(:, 2), 50, 'r', '^', ...
            'DisplayName', 'Bus Stops');
            
    % Draw coverage circles around sampled bus stops
    for i = 1:size(sampledStops, 1)
        viscircles(sampledStops(i, :), radius, 'LineStyle', '--', 'Color', 'g');
    end
    
    % Add title, labels, and legend
    title(sprintf('Service Area Coverage (Radius = %d meters)', radius), ...
          'FontSize', 16);
    xlabel('X (UTM)');
    ylabel('Y (UTM)');
    legend;
    
    % Save the plot as an image
    saveas(gcf, filename);
    close;
end

% --- MAIN SCRIPT ---
% This part should be run as a script, or put into a separate file
% as MATLAB does not allow multiple functions and a script in the same file
% unless it's a class definition.
% For demonstration, we assume this is the main script logic.

disp('Running main script to generate coverage plots...');

% Generate sample data for demonstration purposes
numBusStops = 100;
coords = rand(numBusStops, 2) * 1000; % Random bus stop coordinates (in meters)
numPopulationPoints = 1000;
populationPoints = generate_population_points(coords, numPopulationPoints); % Random population points
busStops = coords; % Assume bus stop coordinates are the same as the original coordinates

% Plot and save service area coverage for different radii
radii = [100, 200, 500, 1000];
for i = 1:length(radii)
    radius = radii(i);
    filename = sprintf('coverage_radius_%d.png', radius);
    
    % Call the plotting function
    % Note: All functions must be defined above or in separate files on the path
    plot_service_area(coords, populationPoints, busStops, radius, filename);
    
    fprintf('Image saved as %s\n', filename);
end

disp('Script finished.');
