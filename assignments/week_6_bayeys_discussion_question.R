options(scipen = 999)

odds_of_disease <- 1/1000000
test_accuracy <- 0.99
have_and_test_positive <- odds_of_disease * test_accuracy
dont_have_and_test_positive <- (1-odds_of_disease) * (1-test_accuracy)

have_and_test_positive
dont_have_and_test_positive

odds_you_have_it <- (have_and_test_positive / (have_and_test_positive + dont_have_and_test_positive))

str(odds_you_have_it)