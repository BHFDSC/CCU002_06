## =============================================================================
## Call model
## Author: Samantha Ip
## =============================================================================
get_vacc_res <- function(interacting_feat, subgrp, event, prev_vac_str, vac_str, agegp, cohort_vac, covars){
  # lsm <- ls_events_missing; cohort_vac_cache <-cohort_vac; cohort_vac <- cohort_vac_subgrp; subgrp <- lsm$subgrp; event <- lsm$event; prev_vac_str <- lsm$prev_vac_str; vac_str <- lsm$vac_str; agegp <- lsm$agegp; fml <-  "+ weeks + agegroup + sex"
  # cat("START vac_cohort_call_mdl.R -- get_vacc_res ......\n")
  outcome_dfname <- grep(paste0("out_", dose_str, "_", event, "$"),# for some reason sometimes the out_s are capitalised 
       fread(fpath_outcomes, nrows=1) %>% colnames(),
       ignore.case=TRUE,value=TRUE)
  if(length(outcome_dfname)!=1){stop(paste("outcome_dfname: ", outcome_dfname, "\n", sep=" "))}
  
  
  
  outcomes <- fread(fpath_outcomes, 
                    select=c("NHS_NUMBER_DEID", outcome_dfname))
  
  print(c("NHS_NUMBER_DEID", outcome_dfname))
  outcomes$name <- event
  setnames(outcomes, 
           old = c(outcome_dfname), 
           new = c("event_date"))
  
  if (dose_str %in% c("dose2", "booster")){
    cohort_vac <- cohort_vac %>% filter(!is.na(START_DATE))
  }
  
  survival_data <- cohort_vac %>% left_join(outcomes)
  
  rm(outcomes)
  gc()
  
  cat("any survival_data$START_DATE < cohort_start_date | > cohort_end_date: \n")
  print(any(survival_data$START_DATE < cohort_start_date))
  print(any(survival_data$START_DATE > cohort_end_date))
  
  
  schema <- sapply(survival_data, is.Date)
  for (colname in names(schema)[schema==TRUE]){
    print(colname)
    survival_data <- set_dates_outofrange_na(survival_data, colname)
  }
  if (dose_str %in% c("dose2", "booster")){
    survival_data <- survival_data %>% filter(!is.na(START_DATE))
  }
  
  cat(paste0("any event_date < START_DATE...... ", 
             any(survival_data$event_date < survival_data$START_DATE, na.rm=TRUE),
             "\n"))
  cat(paste0("range event_dates...... ", paste(range(survival_data$event_date, na.rm=TRUE), collapse=", "), "\n"))
  
  names(survival_data)[names(survival_data) == 'VACCINATION_DATE'] <- 'expo_date'
  
  cat("survival_data before vac specific... \n")
  print(str(survival_data))
# survival_data_cache <-survival_data
  
  vac_of_interest <- case_when(
    vac_str=="vac_az" ~ list("AstraZeneca"),
    vac_str=="vac_pf" ~ list("Pfizer"),
    vac_str=="vac_mod" ~ list("Moderna"),
    vac_str=="vac_pfmod"~ list("Pfizer", "Moderna")
  ) %>% unlist() %>% unique()
  
  prev_vac_of_interest <- case_when(
    prev_vac_str=="vac_az" ~ list("AstraZeneca"),
    prev_vac_str=="vac_pf" ~ list("Pfizer"),
    prev_vac_str=="vac_pfmod"~ list("Pfizer", "Moderna", "hack"),
    prev_vac_str=="vac_any"~ list("AstraZeneca", "Pfizer", "Moderna"),
    is.na(prev_vac_str) ~ list(NA)
  ) %>% unlist() %>% unique()
  prev_vac_of_interest <- prev_vac_of_interest[prev_vac_of_interest!="hack"]
  
  cat("prev_vac_of_interest:", prev_vac_of_interest, ";  vac_of_interest:", vac_of_interest, "\n")
  
  
  survival_data <- get_vac_specific_dataset(survival_data, vac_of_interest, prev_vac_of_interest)
  cat("After get_vac_specific_dataset......\n")
  print(str(survival_data))
  
  
  schema <- sapply(survival_data%>% dplyr::select(!DATE_VAC_CENSOR), is.Date)
  for (colname in names(schema)[schema==TRUE]){
    cat(colname, "\n")
    survival_data <- set_dates_outofrange_na(survival_data, colname)
  }
  survival_data <- survival_data %>% filter(!is.na(START_DATE))
  
  cat(paste0("any event_date > DATE_VAC_CENSOR...... ", 
             any(survival_data$DATE_OF_DEATH > survival_data$DATE_VAC_CENSOR, na.rm=TRUE),
             "\n"))
  cat(paste0("range event_dates...... ", paste(range(survival_data$event_date, na.rm=TRUE), collapse=", "), "\n"))
  
  
  
  if (dose_str == "dose2"){
    cat("\n\nwhere PRODUCT_PREV != VACCINE_PRODUCT...... \n")
    survival_data[survival_data$PRODUCT_PREV != survival_data$VACCINE_PRODUCT] %>% print()
  }
  
  # fit model ----
  
  gc()

  source(file.path(scripts_dir,"vac_SAsubgrp_cohort_fit_model.R"), local=TRUE)
  fit_model_reducedcovariates(interacting_feat, subgrp, fml, covars, prev_vac_str, vac_str, agegp, event, survival_data)

  
  cat("DONE vac_cohort_call_mdl.R -- get_vacc_res ......\n")
  
  
  
}
