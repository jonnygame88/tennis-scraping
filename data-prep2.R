
source('scripts/data-functions.R')

## clean percentage columns
m <- readRDS('data/main/atp-match-stats.RDS') %>% select(-round, -surface)
m <- m[-which(duplicated(m)), ]

u1 <- unique(m$p2_bpconv); space <- substr(u1[1], 2, 2)
f <- function(v, nm1, nm2) {
  u <- order_vector(unique(v))
  lookup <- lapply(u, function(x) psplit(x, space)) %>% rbind_all()
  lookup[match(v, lookup$st), 2:3] %>% give_names(c(nm1, nm2))
}

## join RDS files
p <- readRDS('data/main/atp-player-ref.RDS')
e <- readRDS('data/main/atp-events-info.RDS')
names(e)[2] <- 'event_date'
d <- inner_join(p, e, by = 'event_url') %>% select(-event_url)
d <- left_join(d, m, by = 'match_url') %>% select(-match_url)
# saveRDS(d, 'data/main/atp-full.RDS')
