#lang racket

;; taken from: https://github.com/dherman/calculist/blob/82f99add1e5f8911b688b30fa8ff402c7f056398/_util/date-format.rkt

(require racket/date)
(provide pretty-date)

(define *months* (vector "Jan" "Feb" "Mar" "Apr" "May" "Jun" "Jul" "Aug" "Sep" "Oct" "Nov" "Dec"))
(define *suffixes* (vector "st" "nd" "rd" "th" "th" "th" "th" "th" "th" "th"
                           "th" "th" "th" "th" "th" "th" "th" "th" "th" "th"
                           "st" "nd" "rd" "th" "th" "th" "th" "th" "th" "th"
                           "31"))

(define (pretty-date d)
  (let ([year (date-year d)]
        [month (date-month d)]
        [day (date-day d)])
    (string-append (vector-ref *months* (sub1 month))
                   " "
                   (number->string day)
                   (vector-ref *suffixes* (sub1 day))
                   ", "
                   (number->string year))))
