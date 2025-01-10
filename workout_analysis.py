import gpxpy
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

def calculate_pace(distance, time):
    """Calculate pace in minutes per kilometer"""
    if distance == 0:
        return 0
    hours = time / 3600  # convert seconds to hours
    if hours == 0:
        return 0
    pace = hours / (distance / 1000)  # hours per kilometer
    return pace * 60  # convert to minutes per kilometer

def analyze_gpx_with_pace(file_path):
    """Analyze a GPX file with detailed pace analysis"""
    try:
        with open(file_path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            
            # Get basic statistics
            moving_data = gpx.get_moving_data()
            uphill, downhill = gpx.get_uphill_downhill()
            
            # Calculate pace for each segment
            paces = []
            distances = []
            times = []
            
            for track in gpx.tracks:
                for segment in track.segments:
                    for i in range(len(segment.points) - 1):
                        point1 = segment.points[i]
                        point2 = segment.points[i + 1]
                        
                        # Calculate distance between points
                        dist = point1.distance_2d(point2)
                        
                        # Calculate time between points
                        time_diff = (point2.time - point1.time).total_seconds()
                        
                        if time_diff > 0 and dist > 0:
                            pace = calculate_pace(dist, time_diff)
                            if pace > 0 and pace < 30:  # Filter out unrealistic paces
                                paces.append(pace)
                                distances.append(dist)
                                times.append(time_diff)
            
            # Calculate pace statistics
            avg_pace = calculate_pace(moving_data.moving_distance, moving_data.moving_time)
            if paces:
                min_pace = min(paces)
                max_pace = max(paces)
            else:
                min_pace = max_pace = 0
            
            # Print results
            print(f"\nAnalysis for: {os.path.basename(file_path)}")
            print("-" * 50)
            print(f"Total distance: {moving_data.moving_distance/1000:.2f} km")
            print(f"Total duration: {moving_data.moving_time/60:.2f} minutes")
            print(f"Average speed: {moving_data.moving_distance/moving_data.moving_time*3.6:.2f} km/h")
            print(f"Average pace: {avg_pace:.2f} min/km")
            print(f"Best pace: {min_pace:.2f} min/km")
            print(f"Slowest pace: {max_pace:.2f} min/km")
            print(f"Elevation gain: {uphill:.1f} m")
            print(f"Elevation loss: {downhill:.1f} m")
            
            # Plot pace distribution
            if paces:
                plt.figure(figsize=(12, 6))
                
                # Pace over distance
                plt.subplot(1, 2, 1)
                cumulative_dist = np.cumsum(distances) / 1000  # Convert to kilometers
                plt.plot(cumulative_dist, paces, 'b-', label='Pace')
                plt.axhline(y=avg_pace, color='r', linestyle='--', label='Average Pace')
                plt.title('Pace over Distance')
                plt.xlabel('Distance (km)')
                plt.ylabel('Pace (min/km)')
                plt.legend()
                plt.grid(True)
                
                # Pace distribution histogram
                plt.subplot(1, 2, 2)
                plt.hist(paces, bins=20, color='blue', alpha=0.7)
                plt.axvline(x=avg_pace, color='r', linestyle='--', label='Average Pace')
                plt.title('Pace Distribution')
                plt.xlabel('Pace (min/km)')
                plt.ylabel('Frequency')
                plt.legend()
                plt.grid(True)
                
                plt.tight_layout()
                plt.show()
            
    except Exception as e:
        print(f"Error analyzing {file_path}: {str(e)}")

def main():
    workout_dir = 'workout-routes'
    
    if not os.path.exists(workout_dir):
        print(f"Error: Directory '{workout_dir}' not found!")
        return
        
    gpx_files = [f for f in os.listdir(workout_dir) if f.endswith('.gpx')]
    
    if not gpx_files:
        print("No GPX files found!")
        return
        
    print(f"Found {len(gpx_files)} GPX files")
    
    for file in gpx_files:
        file_path = os.path.join(workout_dir, file)
        analyze_gpx_with_pace(file_path)

if __name__ == "__main__":
    main() 
