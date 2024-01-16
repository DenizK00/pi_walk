# pi_walk

<img src="output_pi100.gif" width="600" align="center">

This project focuses on exploring the nature of irrational numbers in different aspects. As the name suggests, the number I had in mind in particular was pi. The repo includes an animated visualization program named pi_walk and analysis notebooks.

## Project Overview

### Simulation and Experimentation
The main objectives of this part are:
1. Simulate the distribution of digits for the chosen irrational numbers.
2. Create a polar plot where each digit has its own axis (DigitStick) which grows over time-related to the frequency of the digit's occurrence. Keep track of the area of polygons that form with the 2 nearest digit's frequency and the old frequency. This way, we can see how each newly formed polygon's area (area_delta) contributes to the overall area -area delta's size is displayed by the color's alpha.
3. Create a bar chart that represents the current frequencies of each digit
4. Create a scatter plot for displaying the distribution of total area over time, area deltas are displayed by the size of dots, and the digits are specified by the color of dots.
5. Save the frequency of each digit as well as the area delta, total area, and the approximation up to the current precision point.
6. Save the results obtained over time as a CSV file.

### Analysis and Visualization
The main objectives of this part are:
1. In a notebook, import the data acquired by the simulation and manipulate the data.
2. Make some initial inspections on the distribution of digits, digit occurrences, digit frequencies, and proportion between frequencies of digits over time.
3. Visualize how the total_area grows over time, displaying each digit in a different color.
4. Inspect the digit occurrences further by displaying the occurrences of each digit over time.
5. Plot the kernel density on area_delta vs precision per digit, which can be helpful when comparing the analysis with the other analyses.
6. Plot area deltas over time where the size of each dot displays area_delta's divided by the precision. (Which may be indicative as the significance of a digit's occurrence decreases as the precision of the occurrence increases) e.g. 3.141, the second 1 matters less than the first 1.
7. Visualize the area delta over time further by plotting area contribution (area_delta) divided by precision.
8. Inspect the digit frequencies further by displaying the digit frequencies over precision per digit.
9. Define update periods (wait streaks) as the number of digits to see until we see the specified digit. e.g. how many digits does it take on average to get the next 0? This can also be interpreted as the difference in precisions.
10. Visualize the distribution of Update Periods per digit.
11. Visualize the update periods over precision per digit.
12. Visualize the odd, even, and prime frequencies over time.
13. (if pi) Approximate pi with Monte Carlo method, keep track of estimates over time as the number of points used in approximation grows. Plot estimates over time and estimate sample means with n=10 sample size.


## Dependencies
- Python 3.x
- Matplotlib (*)
- NumPy (*)
- Pandas (*)
- mpmath
- argparse (already installed)

*: Package may be already installed depending on the distribution.

## Using the Program
1. Ensure all the required libraries are installed.
2. Open the command prompt or terminal depending on your operating system.
3. Navigate to the directory where the repo is installed.
4. Run the program as described below:
for using the simulator, the following syntax is used.
-> python pi_walk.py
to specify arguments, the following format is used (the values shown are default values):
-> python pi_walk.py -n pi -p 100 -o 0 -c digitwise -s 1.5 -r la
where:
-n --number: number to simulate pi, e, or phi (default: pi)
-p --precision: precision to simulate the number to (to how many digits do you want to use). (default: 100)
-o --offset: offset for visualization, default: 0
-c --coloring: random or digitwise.
-s --speed: rendering speed for the simulation, default: 1.5
-r --rendering: rendering setting. l for lines, a for area, None for only points default: la









