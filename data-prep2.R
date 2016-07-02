
source('scripts/initial.R')

## clean match stats
m <- readRDS('data/main/atp-match-stats.RDS') %>% select(-round, -surface)
m <- m[-which(duplicated(m)), ]

u <- unique(m$p2_bpconv); space <- substr(u[1], 2, 2)
pconvert <- function(v, nm1, nm2) {
  w <- order_vector(unique(v))
  lookup <- lapply(w, function(x) perc_split(x, space)) %>% rbind_all()
  lookup[match(v, lookup$st), 2:3] %>% give_names(c(nm1, nm2))
}

p1_s0 <- pconvert(m$p1_s1perc, 'p1_s1in', 'p1_spts')
p1_s1 <- pconvert(m$p1_s1win, 'p1_s1won', 'p1_s1pts')
p1_s2 <- pconvert(m$p1_s2win, 'p1_s2won', 'p1_s2pts')
p1_r <- pconvert(m$p1_rwin, 'p1_rwon', 'p1_rpts')
p1_b <- pconvert(m$p1_bpconv, 'p1_bwon', 'p1_bpts')
p1_df <- do.call('cbind', list(p1_s0, p1_s1, p1_s2, p1_r, p1_b))

p2_s0 <- pconvert(m$p2_s1perc, 'p2_s1in', 'p2_spts')
p2_s1 <- pconvert(m$p2_s1win, 'p2_s1won', 'p2_s1pts')
p2_s2 <- pconvert(m$p2_s2win, 'p2_s2won', 'p2_s2pts')
p2_r <- pconvert(m$p2_rwin, 'p2_rwon', 'p2_rpts')
p2_b <- pconvert(m$p2_bpconv, 'p2_bwon', 'p2_bpts')
p2_df <- do.call('cbind', list(p2_s0, p2_s1, p2_s2, p2_r, p2_b))

m <- m %>% cbind(p1_df) %>% cbind(p2_df) %>% select(
  match_url, player1, player2, 
  p1_s1in, p1_spts, p1_s1won, p1_s1pts, p1_s2won, p1_s2pts, 
  p1_rwon, p1_rpts, p1_bwon, p1_bpts, p1_aces, p1_dfs, p1_tpwin,
  p2_s1in, p2_spts, p2_s1won, p2_s1pts, p2_s2won, p2_s2pts, 
  p2_rwon, p2_rpts, p2_bwon, p2_bpts, p2_aces, p2_dfs, p2_tpwin,
  p1_ues, p1_winners, p2_ues, p2_winners)

## clean player ref
p <- readRDS('data/main/atp-player-ref.RDS')
p$date <- as.Date(p$date, '%d %b %y')

u_scores <- order_vector(unique(p$sets))
scores_df <- data.frame(score_str = u_scores) %>% 
  cbind(rbind_all(lapply(u_scores, score_split)))

u_sets <- unlist(strsplit(u_scores, ","))
u_sets <- order_vector(unique(gsub(" ", "", u_sets)))
sets_df <- data.frame(set_str = u_sets) %>% 
  cbind(rbind_all(lapply(u_sets, set_split)))

sconvert <- function(s_col) {
  s <- scores_df[[s_col]]
  m <- match(s, sets_df$set_str)
  v1 <- sets_df$g1[m]; v2 <- sets_df$g2[m]
  v1[which(is.na(v1))] <- 0; v2[which(is.na(v2))] <- 0
  data.frame(v1, v2) %>% give_names(paste0(s_col, c('g1', 'g2')))
}
sgame_df <- do.call('cbind', lapply(paste0('s', 1:5), sconvert))
scores_df <- cbind(select(scores_df, -s1, -s2, -s3, -s4, -s5), sgame_df)

scores_df$score_str <- as.character(scores_df$score_str)
p <- left_join(p, scores_df, c('sets' = 'score_str')) %>% select(-sets)

## join RDS files
e <- readRDS('data/main/atp-events-info.RDS')
names(e)[2] <- 'event_date'
d <- inner_join(p, e, by = 'event_url') %>% select(-event_url)
d <- left_join(d, m, by = 'match_url') %>% select(-match_url, -event_date)
# saveRDS(d, 'data/main/atp-full.RDS')
