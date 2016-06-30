
source('scripts/data-functions.R')

## combine player ref csvs
fs <- paste0('data/reference-csvs/', list.files('data/reference-csvs/'))
d <- lapply(fs[3:5], read.csv) %>% rbind_all()
nrow(d); length(unique(paste0(d$player_id, d$m_no)))
length(unique(d$player_id)); length(unique(d$match_url))
# write.csv(d, 'data/reference-csvs/atp-ref-10000-19999.csv', row.names = FALSE)

## combine tournament csvs
fs <- paste0('data/reference-csvs/', list.files('data/reference-csvs/'))
errs <- lapply(fs[c(1,5)], read.csv) %>% rbind_all()
d <- lapply(fs[2:3], read.csv) %>% rbind_all()
# write.csv(errs, 'data/reference-csvs/atp-events-errors.csv', row.names = FALSE)
# write.csv(d, 'data/reference-csvs/atp-events-0-Inf.csv', row.names = FALSE)

## convert events csv
d <- read.csv('data/reference-csvs/atp-events-0-Inf.csv')
i <- sapply(d, is.factor); d[i] <- lapply(d[i], as.character)
d$date <- gsub(" ", "-", d$date); d$date <- gsub(",", "", d$date)
d$date <- as.Date(d$date, '%b-%d-%Y')
# saveRDS(d, 'data/main/atp-events-info.RDS')

## create match url input
p <- readRDS('data/main/atp-player-ref.RDS')
e <- readRDS('data/main/atp-events-info.RDS')
ps <- filter(p, match_url != '') %>% group_by(match_url, event_url) %>%
  summarise(count = n()) %>% select(-count) %>% data.frame()
es <- e %>% mutate(yr = floor(decimal_date(date))) %>% select(event_url, level, yr)
d <- inner_join(ps, es) %>% select(-event_url)
# write.csv(d, 'data/reference-csvs/atp-match-urls.csv', row.names = FALSE)

## combine match csvs
fs <- paste0('data/reference-csvs/', list.files('data/reference-csvs/'))
f <- function(f_name) {
  message(f_name)
  read.csv(f_name) %>% mutate(
    set1 = as.character(set1), set2 = as.character(set2),
    set3 = as.character(set3), set4 = as.character(set4), 
    set5 = as.character(set5))
}
d <- lapply(fs[3:19], f) %>% rbind_all()
nrow(d); length(unique(d$match_url))
# write.csv(d, 'data/reference-csvs/atp-match-stats.csv', row.names = FALSE)
