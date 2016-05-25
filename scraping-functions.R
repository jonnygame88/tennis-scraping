
## get serve, return, raw urls (full career) for player
player_urls <- function(player_name) {
  base <- paste0("http://www.tennisabstract.com/cgi-bin/player.cgi?p=",
                 player_name, "&f=ACareerqq")
  list(serve_url = base, return_url = paste0(base, "r1"),
       raw_url = paste0(base, "w1"))
}

## generate js, html from player name
get_htmls <- function(player_name) {
  pl_urls <- player_urls(player_name)
  js_template <- readLines("data/scraping/template.txt")
  to_html <- function(source_url, target_html) {
    message(source_url)
    js_template[5] <- paste0("var path = 'data/scraping/", 
                             target_html, ".html'")
    js_template[7] <- paste0("page.open('", source_url, "', ")
    writeLines(js_template, "data/scraping/scrape-career-data.js")
    system("data/scraping/phantomjs data/scraping/scrape-career-data.js")
  }
  Map(to_html, c(pl_urls$serve_url, pl_urls$return_url, pl_urls$raw_url),
      c("career-serve-data", "career-return-data", "career-raw-data"))
}

## get player links from url
get_player_list <- function(source_html) {
  all_links <- read_html(source_html) %>% html_nodes("a") %>% html_attr("href")
  player_links <- unique(all_links[grep('player.cgi', all_links)])
  substr(player_links, 52, nchar(player_links))
}

## generate data frame from htmls
player_df <- function(cols = 17) {
  to_df <- function(source_html, col_names) {
    read_html(source_html) %>% html_nodes("#matches td") %>% html_text %>%
      matrix(nrow = cols) %>% t() %>% data.frame() %>% 
      give_names(col_names) %>% select(-extras)
  }
  df <- to_df("data/scraping/career-serve-data.html", cols_serve) %>%
    merge(to_df("data/scraping/career-return-data.html", cols_return)) %>%
    merge(to_df("data/scraping/career-raw-data.html", cols_raw))
  data.frame(lapply(df, as.character), stringsAsFactors=FALSE) %>%
    filter(date != "") %>% mutate(
      date = convert_date(date), date_val = decimal_date(date))
}

## auxiliary definitions
give_names <- function(df, col_names, col_pos = 1:ncol(df)) {
  names(df)[col_pos] <- col_names
  df
}

cols_base <- c("date", "tournament", "surface", "round",
               "rank1", "rank2", "players", "sets", "extras")
cols_serve <- c(cols_base, "dom_ratio", "ace_perc", "dblf_perc", 
                "s1_perc", "s1win_perc", "s2win_perc", "bp_saved", "time")
cols_return <- c(cols_base, "dom_ratio", "all_win_perc", "return_win_perc",
                 "opp_ace_perc", "r1win_perc", "r2win_perc", "bp_won", "time")
cols_raw <- c(cols_base, "total_points", "aces", "dbl_faults", 
              "serve_points", "s1_points", "s2_points", "opp_aces", "time")

convert_date <- function(d) {
  d %>% str_replace_all("[^a-zA-Z0-9]", "") %>% 
    str_replace_all("Jan", "/01/") %>% str_replace_all("Feb", "/02/") %>%
    str_replace_all("Mar", "/03/") %>% str_replace_all("Apr", "/04/") %>% 
    str_replace_all("May", "/05/") %>% str_replace_all("Jun", "/06/") %>% 
    str_replace_all("Jul", "/07/") %>% str_replace_all("Aug", "/08/") %>% 
    str_replace_all("Sep", "/09/") %>% str_replace_all("Oct", "/10/") %>% 
    str_replace_all("Nov", "/11/") %>% str_replace_all("Dec", "/12/") %>% 
    as_date("%d/%m/%Y")
}

## generate opponent column
## check opponents list matches links list
h <- head(match_history)$players
h %>% strsplit("d.Â")

## data-function: convert round to round_stage (numeric)
## data-function: adjust equal dates over tournaments
