
source('scripts/initial.R')
d <- readRDS('data/main/atp-full.RDS')

## get unique matches
match_list <- d %>% mutate(
  winner = ifelse(won == 1, player_id, opponent_id),
  loser = ifelse(won == 0, player_id, opponent_id))
m_key <- select(match_list, winner, loser, date, round)
match_list <- match_list[-which(duplicated(m_key)), ]; rm(m_key)

## construct ordered match list
rd_lookup <- data.frame(
  round = order_vector(unique(match_list$round)),
  rd_val = c(9, 8, 4, 5, 6, 7, 0, 10, 0, 3, 1, 2, 0, 1, 2, 4, 5),
  stringsAsFactors = FALSE) %>% arrange(rd_val)
match_list <- inner_join(match_list, rd_lookup, by = "round")
match_list <- filter(match_list, completed == 1) %>% 
  select(date, round, rd_val, surface, level, winner, loser) %>%
  arrange(date, rd_val, winner) %>% select(-rd_val) %>%
  mutate(elo1 = NA, elo2 = NA)

## define tour level values
tour_levels <- order_vector(unique(match_list$level))
tour_val <- c(1600, 0, 1200, 2000, 2000, 2000, 0)

## generate initial player values
players <- order_vector(union(match_list$winner, match_list$loser))
pl_index <- sapply(1:max(players), function(x) min(which(players == x)))
no_players <- length(players)
elo_rating <- rep(NA, no_players)
matches_tour <- rep(0, no_players); matches_cycle <- rep(0, no_players)
last_match <- rep(0, no_players); k_val <- rep(32, no_players)

## get elo ratings
for (i in 1:nrow(match_list)) {
  if (i%%1000 == 0) {message(paste0(i, " ", Sys.time()))}
  tr_val <- tour_val[min(which(tour_levels == match_list$level[i]))]
  if (tr_val > 0) {
    pos1 <- pl_index[match_list$winner[i]]
    pos2 <- pl_index[match_list$loser[i]]
    rating1 <- ifelse(is.na(elo_rating[pos1]), tr_val, elo_rating[pos1])
    rating2 <- ifelse(is.na(elo_rating[pos2]), tr_val, elo_rating[pos2])
    match_list$elo1[i] <- rating1
    match_list$elo2[i] <- rating2
    pred <- 1/(1+10^((rating2-rating1)/400))
    elo_rating[pos1] <- rating1 + k_val[pos1]*(1-pred)
    elo_rating[pos2] <- rating2 + k_val[pos2]*(pred-1)
    matches_tour[pos1] <- matches_tour[pos1] + 1
    matches_tour[pos2] <- matches_tour[pos2] + 1
    mdate <- decimal_date(match_list$date[i])
    if (mdate > 0.5+last_match[pos1]) {
      matches_cycle[pos1] <- 1
    } else {
      matches_cycle[pos1] <- matches_cycle[pos1] + 1
    }
    if (mdate > 0.5+last_match[pos2]) {
      matches_cycle[pos2] <- 1
    } else {
      matches_cycle[pos2] <- matches_cycle[pos2] + 1
    }
    last_match[pos1] <- mdate
    last_match[pos2] <- mdate
    k_val[pos1] <- ifelse(matches_cycle[pos1] < 50, 32, 16)
    k_val[pos2] <- ifelse(matches_cycle[pos2] < 50, 32, 16)
  }
}
player_list <- data.frame(player_id = players, elo_rating, matches_tour)
# arrange(player_list, -elo_rating)[1:100, ] %>% View()
# saveRDS(match_list, 'data/main/atp-elo-ratings.RDS')
