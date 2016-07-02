
library(dplyr)
library(lubridate)

## function: order vector
order_vector <- function(v) v[order(v)]

## function: rename columns
give_names <- function(df, col_nms, col_pos = 1:ncol(df)) {
  names(df)[col_pos] <- col_nms
  df
}

## function: replace nas with value
replace_na <- function(df, x) {
  for (i in seq_len(ncol(df))) {
    df[which(is.na(df[, i])), i] <- x
  }
  df
}

## function: convert factors
f_conv <- function(df) {
  i <- sapply(df, is.factor)
  df[i] <- lapply(df[i], as.character)
  df
}

## function: split percentage string
perc_split <- function(start_str, split_str) {
  if (start_str == "" | is.na(start_str)) {
    x <- c(NA, NA)
  } else {
    s <- strsplit(start_str, split_str)[[1]]
    if (s[1] == "") {
      x <- c(0, as.numeric(s[3]))
    } else {
      x <- c(as.numeric(s[1]), as.numeric(s[3]))
    }
  }
  data.frame(st = start_str, v1 = x[1], v2 = x[2])
}

## functions: split set string, convert to numeric
score_split <- function(s) {
  x <- strsplit(s, ",")[[1]]
  if (length(x) < 5) {x <- c(x, rep(" ", 5-length(x)))}
  x <- gsub(" ", "", x)
  data.frame(s1 = x[1], s2 = x[2], s3 = x[3], s4 = x[4], s5 = x[5])
}
set_split <- function(s) {
  if (nchar(s) < 3) {
    data.frame(g1 = 0, g2 = 0)
  } else {
    x <- strsplit(s, "-")[[1]]; g1 <- x[1]; g2 <- x[2]
    g1 <- as.numeric(g1)
    if (nchar(g2) > 1 & g1 < 8) {
      g2 <- as.numeric(substr(g2, 1, 1))
      } else {
        g2 <- as.numeric(g2)
      }
    data.frame(g1 = g1, g2 = g2)
  }
}
