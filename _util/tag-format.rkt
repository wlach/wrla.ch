#lang racket

(provide reformat-tags)

(define (reformat-tags tags)
  (string-join (string-split tags ",") " ")
)