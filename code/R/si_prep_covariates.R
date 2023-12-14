## =============================================================================
## WRANGLES & FORMATS DATA TABLE -- sets data types, deals with missing entries, 
## defines reference levels
##
## Author: Samantha Ip
## =============================================================================
library(stringr)


# Replace " " with "_" for glht's linfct ----
covars$cov_ethnicity <- gsub(" ", "_", covars$cov_ethnicity)
cohort_vac$region_name <- gsub(" ", "_", cohort_vac$region_name)

covars$cov_ethnicity <- ifelse(covars$cov_ethnicity %in% c("missing", "Missing"), "Unknown", covars$cov_ethnicity)

cat(paste0(
  "unique cov_ethnicity...... ", 
  paste(unique(covars$cov_ethnicity), collapse=", "), 
  "\n"))


#  FACTOR() ----
covars <- covars %>% dplyr::mutate(cov_disorders = cut(cov_disorders, 
                                                       breaks = c(0, 1, 2, 3, 4, 500), 
                                                       right = FALSE, 
                                                       labels = c("0", "1", "2", "3", "4plus")))

factor_covars <- names(covars %>% dplyr::select(! c("NHS_NUMBER_DEID")))


mk_factor_orderlevels <- function(covars, colname)
  {
  covars <- covars %>% mutate(
    !!sym(colname) := factor(!!sym(colname), levels = str_sort(unique(covars[[colname]]), numeric = TRUE)))
  return(covars)
}

for (colname in factor_covars){
  print(colname)
  covars <- mk_factor_orderlevels(covars, colname)
}


for (colname in c("SEX", "region_name")){
  print(colname)
  cohort_vac <- mk_factor_orderlevels(cohort_vac, colname)
}


# any NAs left? ----
stopifnot(colSums(is.na(covars)) == 0)


# specific reference levels (not alph order) ----
covars$cov_ethnicity <- relevel(covars$cov_ethnicity, ref = "White")
# covars$smoking_status <- relevel(covars$smoking_status, ref = "Never_Smoker")
cohort_vac$region_name <- relevel(factor(cohort_vac$region_name), ref = "London")


# numeric ----
cat("DONE si_prep_covariates.R final...... covars\n")
print(str(covars))
cat("DONE si_prep_covariates.R final...... cohort_vac\n")
print(str(cohort_vac))
