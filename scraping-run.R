
## setup
pkgs <- c("dplyr", "stringr", "lubridate", "rvest")
lapply(pkgs, require, character.only = TRUE)
source("data/scraping/scraping-functions.R")

## start
player <- "AndyMurray"; get_htmls(player)
match_history <- player_df() %>% mutate(ref_player = player) %>%
  filter(date_val >= 2006) %>% arrange(-date_val)
players_list <- get_player_list("data/scraping/career-raw-data.html")
## save
# saveRDS(match_history, "data/match-history-base.RDS")
# saveRDS(players_list, "data/players-list.RDS")

## load
match_history <- readRDS("data/match-history-base.RDS")
players_list <- readRDS("data/players-list.RDS")
## iterate
no_iterations <- 5
for (i in 1:no_iterations) {
  player <- players_list[1]; get_htmls(player)
  new_data <- player_df() %>% mutate(ref_player = player)
  match_history <- rbind(match_history, new_data)
  opponents <- get_player_list("data/scraping/career-raw-data.html")
  included <- unique(match_history$ref_player)
  players_list <- setdiff(union(players_list, opponents), included)
}
## save
saveRDS(match_history, "data/match-history-base.RDS")
saveRDS(players_list, "data/players-list.RDS")

## check
str(match_history); sample_n(match_history, 10)
table(match_history$ref_player); str(players_list)
