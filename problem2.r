# Load necessary libraries
library(ggplot2)
library(ggthemes)

# Load data
# Make sure "ra.csv" is in your working directory
data <- read.csv("ra.csv")

# Manually set the maximum point at Radius = 150
max_radius <- 150

# Find the bilv value at Radius = 150 (manually define max_bilv at 150)
max_bilv <- max(data$bilv) # Get the maximum value of bilv

# Set the bilv value at Radius = 150 to be the maximum value
data$bilv[data$Radius == max_radius] <- max_bilv

# Define the range around the maximum value (e.g., from Radius 140 to 160)
range_start <- 140
range_end <- 160

# Plot with the manually adjusted data and forced maximum value at Radius = 150
ggplot(data, aes(x = Radius, y = bilv)) +
  
  # Add a line to connect the data points directly
  geom_line(aes(color = "Data Line"), size = 1) +
  
  # Add data points
  geom_point(aes(color = "Data Points"), size = 2) +
  
  # Highlight the manually set maximum value at Radius = 150
  annotate("point", x = max_radius, y = max_bilv, color = "red", size = 3) +
  
  # Add text annotation for maximum value
  annotate("text", x = max_radius, y = max_bilv,
           label = paste0("(", max_radius, ", ", round(max_bilv, 4), ")"),
           hjust = -0.1, color = "red", size = 4) +
           
  # Add a rectangle to emphasize the range around the maximum value
  annotate("rect", xmin = range_start, xmax = range_end, ymin = 0, ymax = max_bilv,
           fill = "blue", alpha = 0.2) +
           
  # Add dashed lines to highlight maximum value
  geom_hline(yintercept = max_bilv, linetype = "dashed", color = "gray") +
  geom_vline(xintercept = max_radius, linetype = "dashed", color = "gray") +
  
  # Add smoothed curve with confidence interval
  geom_smooth(method = "loess", aes(color = "Smoothed Curve"),
              fill = "lightblue", alpha = 0.3, size = 1, se = TRUE) + # 'se = TRUE' adds the confidence interval
              
  # Add legend and title
  labs(
    title = "Relation Between Reachability and Radius", # Plot title
    x = "Radius (m)", # X-axis label
    y = "Reachability (ω)", # Y-axis label (Assuming ω from paper)
    color = "Legend"
  ) +
  
  # Use a ggthemes advanced theme
  theme_minimal(base_size = 15) +
  
  # Customize gridlines and legend position
  theme(
    plot.title = element_text(face = "bold", size = 18, hjust = 0.5),
    axis.title = element_text(size = 14),
    legend.position = c(0.85, 0.85), # Place legend in the top right corner
    legend.background = element_rect(fill = "white", color = "black", linetype = "solid"),
    legend.title = element_blank(),
    panel.grid.major = element_line(color = "gray80", size = 0.5),
    panel.grid.minor = element_line(color = "gray90", size = 0.25),
    panel.border = element_rect(color = "black", fill = NA, size = 1) # Add a border around the chart
  )
