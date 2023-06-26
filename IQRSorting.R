# Load necessary libraries
library(ggplot2)
library(dplyr)
library(readr)
library(tidyverse)

# Define the function
process_csv <- function(input_csv, output_csv) {
  # Read the CSV file
  data <- read_csv(input_csv)
  
  # Calculate the percentiles
  quantiles <- quantile(data[[2]], probs=c(.25, .75), na.rm = TRUE)
  
  # Assign categories based on percentile
  data <- data %>%
    mutate(category = case_when(
      data[[2]] <  quantiles[1] ~ "<25",
      data[[2]] >= quantiles[1] & data[[2]] <= quantiles[2] ~ "25-75",
      data[[2]] >  quantiles[2] ~ ">75"
    ))
  
  # Create new dataframe for output
  output_data <- data.frame("<25" = rep("", nrow(data)), "25-75" = rep("", nrow(data)), ">75" = rep("", nrow(data)))
  
  # Assign values to new columns based on category
  output_data$`<25`[data$category == "<25"]   <- data[data$category == "<25",][[1]]
  output_data$`25-75`[data$category == "25-75"] <- data[data$category == "25-75",][[1]]
  output_data$`>75`[data$category == ">75"]   <- data[data$category == ">75",][[1]]
  
  # Sort each column in descending order
  output_data <- output_data %>% arrange(desc(`<25`), desc(`25-75`), desc(`>75`))
  
  # Prepare the boxplot
  boxplot <- ggplot(data, aes(x=category, y=data[[2]])) +
    geom_boxplot() +
    xlab('Percentile Category') +
    ylab('Value') +
    ggtitle('Boxplot of Value by Percentile Category')
  
  # Print the boxplot
  print(boxplot)
  
  # Write the new CSV file
  write_csv(output_data, output_csv)
}

# Run the function
process_csv("~/Desktop/EconomicsPaper/2021_median_income.csv", "~/Desktop/output_Median_2021.csv")
