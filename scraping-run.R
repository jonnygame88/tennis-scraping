
## setup
pkgs <- c("dplyr", "stringr", "rvest")
lapply(pkgs, require, character.only = TRUE)
options(digits = 4)
source("data-scraping/scraping-functions.R")

## example
player <- "TomislavBrkic"
timestamp(); get_htmls(player); d <- player_df(); timestamp()
sample_n(d, 10)
