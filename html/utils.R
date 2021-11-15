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

select_gym_leaderboard <- function(gym_name) {
  leaderboard <- read.csv("../leaderboard.csv") %>% select(-c(date))
  leaderboard$gym <- mapply(convert_col, leaderboard$env)
  selected_leaderboard <- leaderboard %>% filter(gym == gym_name) %>% head() %>% select(-gym)
  return(selected_leaderboard)
}

display_env_leaderboard <- function(gym_leaderboard, env_name) {
  env_leaderboard <- gym_leaderboard %>% filter(env == env_name) %>% select(-env)
  env_leaderboard <- env_leaderboard %>% mutate(ref = 
                                                  paste0('<a href=', 
                                                  hash_url, '>link </a>' ))
  env_leaderboard <- env_leaderboard %>% select(-hash_url)
  shared_leaderboard <- SharedData$new(env_leaderboard)
  shared_leaderboard %>% DT::datatable(fillContainer = FALSE, options = list(order=list(3, 'desc')), escape=FALSE)
}