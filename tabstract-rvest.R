
library(rvest)
library(stringr)
library(plyr)
library(dplyr)
options(digits = 4)

# system("./phantomjs scrape-career-federer.js")
# system("./phantomjs scrape-h2h-djo.js")

stext <- read_html("career-federer.html") %>% html_nodes(".stats") %>% html_text()
Encoding(stext) <- "latin1"
substr(stext, 1, 300); iconv(substr(stext, 1, 300), "latin1", "ASCII", sub="")

tennis.html <- read_html("h2h-djo.html")
H2Hs <- tennis.html %>% html_nodes(".h2hclick") %>% html_text %>% as.numeric
Opponent <- tennis.html %>% html_nodes("#matches a") %>% html_text
Country <- tennis.html %>% html_nodes("a+ span") %>% html_text %>% gsub("[^(A-Z)]", "", .)
W <- tennis.html %>% html_nodes("#matches td:nth-child(3)") %>% .[-1] %>% html_text %>% as.numeric
L <- tennis.html %>% html_nodes("#matches td:nth-child(4)") %>% .[-1] %>% html_text %>% as.numeric
Win.Prc <- tennis.html %>% html_nodes("#matches td:nth-child(5)") %>% .[-1] %>% html_text
