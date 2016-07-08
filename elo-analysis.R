
source('scripts/initial.R'); library(ggplot2)
elo_data <- readRDS('data/main/atp-elo-ratings.RDS')

## randomise player order
elo_data <- filter(elo_data, !is.na(elo1), !is.na(elo2))
elo_data <- elo_data %>% mutate(
  i = sample(1:2, nrow(elo_data), replace = TRUE),
  elo_diff = ifelse(i == 1, elo1-elo2, elo2-elo1),
  elo_win = ifelse(i == 1, 1, 0))

## check win % vs elo diff
elo_data %>% group_by(ediff = pmax(-400, pmin(400, floor(elo_diff)))) %>% 
  summarise(wins = mean(elo_win), count = n()) %>% 
  ggplot(aes(x = ediff, y = wins)) + 
  geom_point(aes(size = count)) + geom_smooth(se = FALSE)
elo_percs <- elo_data %>% filter(level != 'Futures') %>%
  group_by(level, ediff = pmax(-750, pmin(750, 10*floor(elo_diff/10)))) %>% 
  summarise(wins = mean(elo_win), count = n()) %>% data.frame()
ggplot(elo_percs, aes(x = ediff, y = wins)) + 
  geom_point(aes(size = count, colour = level)) +
  geom_smooth(aes(colour = level), se = FALSE)

## check player elos
phist <- function(pl_id) {
  d <- filter(elo_data, winner == pl_id | loser == pl_id)
  d <- arrange(d, date) %>% mutate(game_rank = nrow(d):1) %>%
    mutate(current_elo = ifelse(winner == pl_id, elo1, elo2)) %>%
    select(game_rank, current_elo)
  cbind(data.frame(player_id = as.factor(pl_id)), d)
}
player_set_plot <- function(id_set) {
  elo_df <- lapply(id_set, phist) %>% rbind_all()
  ggplot(elo_df, aes(x = game_rank, y = current_elo)) +
    geom_line(aes(colour = player_id), size = 1)
}
player_set_plot(c(5992, 677, 19, 1075, 8308, 4019))
