
library(rvest)
library(stringr)
library(plyr)
library(dplyr)
options(digits = 4)

# Sys.time()
# readLines("data-scraping/test-djokovic.txt") %>% 
#   writeLines("data-scraping/scrape-career-serve.js")
# system("./phantomjs data-scraping/scrape-career-serve.js")
# Sys.time()

tennis.html <- read_html("data-scraping/career-serve-data.html")
links <- tennis.html %>% html_nodes("a") %>% html_attr("href")
table_values <- tennis.html %>% html_nodes("#matches td") %>% html_text

f <- function(n) {
  v <- table_values[(17*n+1):(17*n+17)]
  c(str_replace_all(str_replace_all(v[1], "[^[:alnum:]]", ""), "ÃÂÂ",  ""),
    str_replace_all(v[7], "[Â, ]", ""), v[2:6], v[8], v[10:17])
}
table_values[171:187]; f(10)

# stext <- read_html("javascript-scraping/career-federer.html") %>% 
#   html_nodes(".stats") %>% html_text()
# Encoding(stext) <- "latin1"
# substr(stext, 1, 300); iconv(substr(stext, 1, 300), "latin1", "ASCII", sub="")
# 
# tennis.html <- read_html("javascript-scraping/h2h-djo.html")
# H2Hs <- tennis.html %>% html_nodes(".h2hclick") %>% html_text %>% as.numeric
# Opponent <- tennis.html %>% html_nodes("#matches a") %>% html_text
# Country <- tennis.html %>% html_nodes("a+ span") %>% 
#   html_text %>% gsub("[^(A-Z)]", "", .)
# W <- tennis.html %>% html_nodes("#matches td:nth-child(3)") %>% 
#   .[-1] %>% html_text %>% as.numeric
# L <- tennis.html %>% html_nodes("#matches td:nth-child(4)") %>% 
#   .[-1] %>%  html_text %>% as.numeric
# Win.Prc <- tennis.html %>% html_nodes("#matches td:nth-child(5)") %>%
#   .[-1] %>% html_text
