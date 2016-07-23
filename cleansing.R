
source('scripts/_setup.R')
list.files('data/on-court/')

## match history
matches <- read.csv('data/on-court/atp-match-history.csv') %>% f_conv() %>%
  mutate(match_date = ifelse(match_date == '', tour_date, match_date),
         match_date = as.Date(match_date, '%d/%m/%Y')) %>% select(-tour_date)

unique_results <- matches$result %>% unique() %>% order_vector()
unique_sets <- matches$result %>% strsplit(' ') %>% 
  unlist() %>% unique() %>% order_vector()
result_split <- function(r) {
  x <- strsplit(r, ' ')[[1]]
  if (length(x) < 5) {x <- c(x, rep('0-0', 5-length(x)))}
  data.frame(result_string = r, 
             s1 = x[1], s2 = x[2], s3 = x[3], s4 = x[4], s5 = x[5])
}
set_split <- function(s) {
  if (grepl('[A-Za-z]', s)) {
    data.frame(set_string = s, g1 = -1, g2 = -1)
  } else{
    x <- strsplit(s, '-')[[1]]; g1 <- x[1]; g2 <- x[2]
    if (grepl('\\(', g2)) {g2 <- substr(g2, 1, 1)}
    data.frame(set_string = s, g1 = as.numeric(g1), g2 = as.numeric(g2))
  }
}
set_mapping <- lapply(unique_sets, set_split) %>% bind_rows()
result_mapping <- lapply(unique_results, result_split) %>%
  bind_rows() %>% mutate(
    s1 = match(s1, set_mapping$set_string), 
    s2 = match(s2, set_mapping$set_string),
    s3 = match(s3, set_mapping$set_string), 
    s4 = match(s4, set_mapping$set_string),
    s5 = match(s5, set_mapping$set_string))
gmap <- function(s) {
  gms <- set_mapping[result_mapping[[s]], 2:3]
  names(gms) <- paste0(s, names(gms))
  gms
}
game_df <- data.frame(result = result_mapping$result_string) %>% 
  cbind(lapply(paste0('s', 1:5), gmap) %>% bind_cols())

wset <- function(g1, g2) {
  ifelse(g1 > g2, ifelse(g2 < 6, 1, 5/6), ifelse(g1 < 6, 0, 1/6))
}
matches <- inner_join(matches, game_df, by = 'result') %>% 
  mutate(s1w = as.numeric(s1g1>s1g2), s2w = as.numeric(s2g1>s2g2), 
         s3w = as.numeric(s3g1>s3g2), s4w = as.numeric(s4g1>s4g2), 
         s5w = as.numeric(s5g1>s5g2)) %>% 
  mutate(nsets = (s1g1+s1g2 > 0) + (s2g1+s2g2 > 0) +
           (s3g1+s3g2 > 0)+(s4g1+s4g2 > 0) + (s5g1+s5g2 > 0),
         wscore = (1 + wset(s1g1, s1g2) + wset(s2g1, s2g2) + wset(s3g1, s3g2) +  
                     wset(s4g1, s4g2) + wset(s5g1, s5g2))/(nsets + 1))
matches$completed <- 1
matches$completed[grep('[A-Za-z]', matches$result)] <- 0

# saveRDS(matches, 'data/cleaned/atp-match-history.RDS')
# rm(matches)

## player list
read.csv('data/on-court/atp-players.csv') %>% f_conv() %>%
  give_names(c('player_id', 'player_name', 'birth_date', 'country')) %>%
  mutate(player_name = gsub(' ', '', player_name, fixed = TRUE)) %>%
  saveRDS('data/cleaned/atp-players.RDS')

## tournament list
surface_list <- c('Clay', 'Hard', 'I.hard', 'Grass', 'Carpet', 'Acrylic')
level_list <- c('Futures', 'Challenger', 'MainTour', 'MastersSeries',
                'GrandSlam', 'DavisFedCup', 'NonTour&Juniors')

tour <- read.csv('data/on-court/atp-tournaments.csv') %>% 
  f_conv() %>% rename(level_id = tour_level) %>% 
  mutate(start_date = as.Date(start_date, '%d/%m/%Y'))
tour$surface_id <- match(tour$surface, surface_list)
tour$level <- level_list[tour$level_id+1]

select(tour, tour_id, tour_name, surface_id, surface, level_id, level,
       start_date, prize_money, country, latitude, longitude, link_id) %>%
  saveRDS('data/cleaned/atp-tournaments.RDS')

## rounds list
read.csv('data/on-court/rounds.csv') %>% give_names(c('round_id', 'round')) %>% 
  saveRDS('data/cleaned/rounds.RDS')
