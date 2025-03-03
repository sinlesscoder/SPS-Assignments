<center>

## Project 1 - Chess Cross Table Data Analysis

Ali Ahmed
March 2, 2025

</center>

### Introduction

Chess tournaments generate a wealth of data that can be analyzed to extract meaningful insights. The dataset in question is a cross-table from a chess tournament, which details player performance, opponent ratings, and other relevant statistics. This report documents the transformation process applied to this dataset using R, showcasing data extraction, structuring, and final analysis.

### Transformations

#### Data Extraction
The dataset is read from an external source using the following command:
```r
url <- "/project-one/tournamentinfo.txt"
df <- read.csv(file = url, sep = "\t")
```
This loads the chess cross-table into a dataframe.

#### Splitting Data
The dataset contains alternating rows of player statistics and opponent details. I segregate them using an index-based approach:
```r
start_index <- 4
head_rows <- df[seq(from = start_index, to = nrow(df), by = 3), ]

start_index <- 5
tail_rows <- df[seq(from = start_index, to = nrow(df), by = 3), ]
```
This isolates player-specific details (`head_rows`) and opponent-related data (`tail_rows`).

#### Processing Player Data
A function is created to parse and clean the player-specific rows for the following information:

1. Player Name
2. Pair Number
3. Total Points
4. Round by Round Status

```r
# Function
process_character_head_array <- function(char_array) {
  
  # Create empty arrays to store values
  team_pair_nums <- c()
  player_names <- c()
  player_total_pts <- c()
  round_nums <- c()
  player_round_statuses <- c()
  player_round_opponents <- c()
  
  # Iterate over each character array (each player's data)
  for (i in 1:length(char_array)) {
    
    row <- unlist(strsplit(char_array[i], "\\|"))  # Split by "|"
    row <- trimws(row)  # Trim whitespace
    
    pair_num <- row[1]
    pair_num <- trimws(pair_num)
    pair_num <- as.numeric(pair_num)
    
    player_name <- row[2]
    player_name <- trimws(player_name)
    
    total_pts <- row[3]
    total_pts <- trimws(total_pts)
    total_pts <- as.numeric(total_pts)
    
    # Extract rounds (Indexes 4 to end)
    rounds <- row[4:length(row)]
    
    # Iterate over rounds to split status and opponent
    for (j in seq_along(rounds)) {
      round <- trimws(rounds[j])  # Remove extra spaces
      
      if (nchar(round) > 1) {
        status <- substr(round, 1, 1)  # Extract first letter (W, D, L)
        status <- trimws(status)
        
        opponent <- substr(round, 3, nchar(round))  # Extract opponent number
        opponent <- trimws(opponent)
        opponent <- as.numeric(opponent)
        
        if (status %in% c("W", "D", "L")) {
          # Append values to arrays
          team_pair_nums <- c(team_pair_nums, pair_num)
          player_names <- c(player_names, player_name)
          player_total_pts <- c(player_total_pts, total_pts)
          round_nums <- c(round_nums, j)  # Store round number
          player_round_statuses <- c(player_round_statuses, status)
          player_round_opponents <- c(player_round_opponents, opponent)
        }
      } else {
        # Append NULL values if round data is missing or invalid
        team_pair_nums <- c(team_pair_nums, pair_num)
        player_names <- c(player_names, player_name)
        player_total_pts <- c(player_total_pts, total_pts)
        round_nums <- c(round_nums, j)  # Store round number
        player_round_statuses <- c(player_round_statuses, "NULL")
        player_round_opponents <- c(player_round_opponents, "NULL")
      }
    }
  }
  
  # Create a DataFrame from the populated arrays
  result_df <- data.frame(
    Pair_Num = team_pair_nums,
    Player_Name = player_names,
    Total_Points = player_total_pts,
    Round_Num = round_nums,  # New column to track round number
    Round_Status = player_round_statuses,
    Round_Opponent = player_round_opponents,
    stringsAsFactors = FALSE
  )
  
  return(result_df)
}


# Function Call
processed_head_array <- process_character_head_array(head_rows)
```
This function extracts the player's pairing number, name, total points, and round-by-round status.

#### Processing Additional Player Data
Similarly, player-specific data is processed in the tail array for the following information:

1. Player State
2. Player Pre-Rating

```r
# Function
# Function to process a character array
process_character_tail_array <- function(char_array) {
  
  # Create empty arrays to store values
  player_states <- c()
  player_preratings <- c()
  
  # Iterate over each character array (each player's data)
  for (i in 1:length(char_array)) {
    
    row <- unlist(strsplit(char_array[i], "\\|"))  # Split by "|"
    row <- trimws(row)  # Trim whitespace
    
    player_state <- row[1]
    player_prerating <- row[2]

    # Split the character string into an array by a : and get the second index
    player_prerating <- strsplit(player_prerating, ":")[[1]][2]

    # Split the new value into an array by the -> and get the first index
    player_prerating <- strsplit(player_prerating, "->")[[1]][1]

    # Control Flow to check if the letter P is inside the prerating and then only take the left side if it exists otherwise keep as is
    if (grepl("P", player_prerating)) {
      # Get the number left side of letter P
      player_prerating <- strsplit(player_prerating, "P")[[1]][1]
      # Remove whitespace
      player_prerating <- trimws(player_prerating)

    } else {
      # Keep rating as is since letter P not found
      player_prerating <- player_prerating
      player_prerating <- trimws(player_prerating)
    }

    # Convert to numeric to use for averages later
    player_prerating <- as.numeric(player_prerating)
    
    # Append values to arrays
    player_states <- c(player_states, player_state)
    player_preratings <- c(player_preratings, player_prerating)
    }
    
    # Create a DataFrame from the populated arrays
    result_df <- data.frame(
    Player_State = player_states,
    Player_PreRating = player_preratings,
    stringsAsFactors = FALSE
  )
  
  return(result_df)
}

# Function Call
processed_tail_array <- process_character_tail_array(tail_rows)
```
This function extracts state information and pre-ratings of players.

#### Merging Player and Opponent Data
Both processed datasets are merged based on player names:
```r
combined_df <- merge(processed_head_array, processed_tail_array, by = "Player_Name", how='left', all.x = TRUE)
```
This ensures that each player has a corresponding opponent pre-rating for further calculations.

#### Calculating Average Opponent Pre-Rating
I compute the average pre-rating of opponents faced by each player:
```r
player_avg_opponent_prerating <- mean(player_rows$Opponent_PreRating, na.rm = TRUE)
```
This is stored in a new dataframe containing player details:
```r
player_data <- data.frame(
  Player_Name = player_names,
  Player_State = player_states,
  Player_Total_Points = player_total_pts,
  Player_PreRating = player_preratings,
  Avg_Opponent_PreRating = avg_preratings
)
```

### Analysis and Conclusions

1. **Structured Representation**: The data transformation process ensures that individual player and opponent details are structured cleanly, allowing for easier analysis.
2. **Performance Insights**: By linking players with their opponent pre-ratings, I gain a better understanding of player performance relative to competition strength.
3. **Future Improvements**: Additional transformations such as performance trends over multiple tournaments or comparison of pre- and post-tournament ratings could provide deeper insights.

This report demonstrates the utility of R in handling structured tournament data, enabling effective player analysis and comparison.


