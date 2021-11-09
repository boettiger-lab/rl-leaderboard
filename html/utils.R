# Function to create a gym column from the listed env
convert_col <- function(column) {
  if (grepl("fishing", column)) {
    output <- "Gym Fishing"
  }
  else if (grepl("ays", column)) {
    output <- "Gym Climate"
  }
  else if (grepl("wildfire", column)) {
    output <- "Gym Wildfire"
  }
  else if (grepl("conservation", column)) {
    output <- "Gym Conservation"
  }
  else if (grepl("sir", column)) {
    output <- "Gym Epidemic"
  }
  return(output)
}

select_leaderboard <- function(gym_name) {
  leaderboard <- read.csv("../leaderboard.csv") %>% select(-c(date, id))
  leaderboard$gym <- mapply(convert_col, leaderboard$env)
  selected_leaderboard <- leaderboard %>% filter(gym == gym_name) %>% head() %>% select(-gym)
  shared_leaderboard <-  SharedData$new(selected_leaderboard)
  return(shared_leaderboard)
}