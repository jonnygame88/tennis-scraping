
source('scripts/initial.R')
d <- readRDS('data/main/atp-full.RDS')

## first serve win rate
d <- d %>% select(-date) %>% 
  filter(!is.na(p1_s1won)) %>% replace_na(0) %>%
  mutate(s1wins = ifelse(won == 1, p1_s1won, p2_s1won),
         s1pts = ifelse(won == 1, p1_s1pts, p2_s1pts),
         player_name = ifelse(won == 1, player1, player2)) %>%
  select(player_id, player_name, s1wins, s1pts)
ds <- d %>% group_by(player_id, player_name) %>%
  summarise(wins = sum(s1wins), pts = sum(s1pts), count = n()) %>%
  filter(wins > 10000, pts > 10000) %>% mutate(winrate = wins/pts) %>% 
  data.frame() %>% arrange(-winrate)
