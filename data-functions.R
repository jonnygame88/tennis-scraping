
library(dplyr)
library(lubridate)

## function: order vector
order_vector <- function(v) v[order(v)]

## function: rename columns
give_names <- function(df, col_nms, col_pos = 1:ncol(df)) {
  names(df)[col_pos] <- col_nms
  df
}

## function: convert factors
f_conv <- function(df) {
  i <- sapply(df, is.factor)
  df[i] <- lapply(df[i], as.character)
  df
}

## function: split percentage string
psplit <- function(start_str, split_str) {
  if (start_str == "" | is.na(start_str)) {
    x <- c(0, 0)
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
