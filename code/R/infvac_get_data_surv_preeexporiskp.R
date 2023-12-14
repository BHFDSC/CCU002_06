## =============================================================================
## MAKE SURVIVAL DATA -- FORMAT FOR TIME-DEPENDENT COXPH
##
## Authors: Samantha Ip, Jenny Cooper
## Thanks to: Thomas Bolton, Venexia Walker and Angela Wood
## =============================================================================
fit_get_data_surv <- function(fml, prev_vac_str, vac_str, covars,  agegp, event, survival_data, riskp_cuts){
  print(paste("working on... ", event))
  
  
  cohort_start_date <- as.Date(cohort_start_date, tryFormats = c("%Y-%m-%d"))
  cohort_end_date <- as.Date(cohort_end_date, tryFormats = c("%Y-%m-%d"))
  if (any(survival_data$DATE_OF_DEATH< cohort_start_date, na.rm=TRUE) | 
      any(survival_data$record_date< cohort_start_date, na.rm=TRUE) | 
      any(survival_data$expo_date< cohort_start_date, na.rm=TRUE) | 
      any(survival_data$DATE_VAC_CENSOR < cohort_start_date, na.rm=TRUE)){
    stop("Bad dates -- < cohort_start_date!")}
  
  if (any(survival_data$DATE_OF_DEATH> cohort_end_date, na.rm=TRUE) | 
      any(survival_data$record_date> cohort_end_date, na.rm=TRUE) | 
      any(survival_data$expo_date> cohort_end_date, na.rm=TRUE) 
      # any(survival_data$DATE_VAC_CENSOR> cohort_end_date, na.rm=TRUE)
  ){
    stop("Bad dates -- > cohort_end_date!")}
  
  if (any(survival_data$START_DATE < cohort_start_date, na.rm=TRUE)  | 
      any(survival_data$record_date < survival_data$START_DATE, na.rm=TRUE) | 
      any(survival_data$expo_date < survival_data$START_DATE, na.rm=TRUE) | 
      any(survival_data$DATE_VAC_CENSOR < survival_data$START_DATE, na.rm=TRUE)
  ){
    stop("Bad dates -- START_DATE problem!!")}
  
  
  # lesser of event_date date and DATE_oF_DEATH, choose origin date to fit existing code
  survival_data$AGE_AT_COHORT_START <- as.numeric(survival_data$AGE_AT_COHORT_START)
  survival_data <- survival_data %>% dplyr::mutate(
    age=AGE_AT_COHORT_START,
    agesq=AGE_AT_COHORT_START^2
  )
  
  setDT(survival_data)[ , agegroup := cut(AGE_AT_COHORT_START, 
                                          breaks = agebreaks, 
                                          right = FALSE, 
                                          labels = agelabels)]
  print("survival_data done")
  
  if (agegp == "all"){
    survival_data -> cohort_agegp
  } else {
    survival_data %>% filter(agegroup== as.character(agegp)) -> cohort_agegp
  }
  
  # RANDOM SAMPLE NON-CASES ----
  set.seed(137)
  if (!is.na(noncase2case_ratio)){
    cohort_agegp$cox_weights <- 1
    cases <- cohort_agegp %>% dplyr::filter(!is.na(event_date)) 
    cat("num cases in cohort_agegp (", agegp, "): ", dim(cases)[1], "\n")
    print(paste0("num cases in cohort_agegp (", agegp, "): ", dim(cases)[1]))
    
    non_cases <- cohort_agegp %>% dplyr::filter(!NHS_NUMBER_DEID %in% cases$NHS_NUMBER_DEID) 
    
    if(noncase2case_ratio*dim(cases)[1] < (dim(cohort_agegp)[1]-dim(cases)[1])){
      non_cases<- sample_n(non_cases, noncase2case_ratio*dim(cases)[1], replace = FALSE) 
      non_cases$cox_weights <- (dim(cohort_agegp)[1] - dim(cases)[1])/(noncase2case_ratio*dim(cases)[1])
    }
    cat("num noncases in cohort_agegp (", agegp, "): ", dim(non_cases)[1], "\n")
    cohort_agegp <- rbind(cases, non_cases)
  }
  
  
  # end_date ----
  system.time(cohort_agegp <-  transform(cohort_agegp, end_date = pmin(event_date, DATE_OF_DEATH, DATE_VAC_CENSOR, cohort_end_date, na.rm=TRUE)))
  cat("any missing end_dates? ", any(is.na(cohort_agegp$end_date)), "\n")
  
  
  cohort_agegp$days_to_start <- as.numeric(cohort_agegp$START_DATE-cohort_start_date)
  cohort_agegp$days_to_end <- as.numeric(cohort_agegp$end_date-cohort_start_date)
  cohort_agegp$days_to_end <- ifelse((!is.na(cohort_agegp$DATE_VAC_CENSOR)) & (cohort_agegp$end_date == cohort_agegp$DATE_VAC_CENSOR), cohort_agegp$days_to_end, (cohort_agegp$days_to_end +1 ))

  cat("cohort_agegp done \n")
  print(head(cohort_agegp ))
  
  # Need to add 0.001 when days_to_end==0
  if (length(cohort_agegp$days_to_end[cohort_agegp$days_to_end==cohort_agegp$days_to_start])>0){
    cohort_agegp$days_to_end <- ifelse(cohort_agegp$days_to_end==cohort_agegp$days_to_start, cohort_agegp$days_to_end + 0.001, cohort_agegp$days_to_end) 
  }
  
  # cache age, sex, region ----
  df_sex <- cohort_agegp %>% dplyr::select(NHS_NUMBER_DEID, SEX)
   df_age_region_coxweight <- cohort_agegp %>% dplyr::select(NHS_NUMBER_DEID, age, agesq, region_name, cox_weights)
  
  cat("df_age_region_coxweight......\n")
  print(head(df_age_region_coxweight))
  print(summary(df_age_region_coxweight))
  # with_expo ===========================================
  with_expo <- cohort_agegp %>% filter(!is.na(expo_date)) 
  
  
  with_expo <- with_expo %>% 
    dplyr::select(NHS_NUMBER_DEID, expo_date, START_DATE, end_date, event_date, days_to_start, days_to_end, DATE_OF_DEATH, DATE_VAC_CENSOR) %>%  
    mutate(event_status = if_else( (!is.na(event_date)) & 
                                     (
                                       ((event_date <= end_date) & ((end_date != DATE_VAC_CENSOR) | is.na(DATE_VAC_CENSOR ))) | 
                                         ((event_date < end_date) & (end_date == DATE_VAC_CENSOR)) 
                                     ), 
                                   1, 0)) 
  
  
  
  # CHUNK UP FOLLOW-UP PERIOD by CHANGE OF STATE OF EXPOSURE
  with_expo$day_expo <- as.numeric(with_expo$expo_date - as.Date(cohort_start_date))
  with_expo$day_expo_preexporiskp <- with_expo$day_expo + riskp_cuts[1] # D1-D2 (hv min separation) but could have <0 wrt start date for D1...
  
  riskp_cuts_shifted <- riskp_cuts - riskp_cuts[1]
  
  
  
  ### split at expo, defines tstart, stop, event ----
  # now expo==1 means within period inc pre-expo riskp
  d1 <- with_expo %>% dplyr::select(NHS_NUMBER_DEID, START_DATE, end_date, expo_date, event_date, DATE_OF_DEATH, day_expo) #just to keep
  d2 <- with_expo %>% dplyr::select(NHS_NUMBER_DEID, days_to_start, day_expo_preexporiskp, days_to_end, event_status) #acted upon
  with_expo <- tmerge(data1=d1, data2=d2, id=NHS_NUMBER_DEID,
                      event=event(days_to_end, event_status), tstart=days_to_start, tstop = days_to_end,
                      expo=tdc(day_expo_preexporiskp)) 
  with_expo <- with_expo %>% dplyr::select(-any_of("id"))
  cat("with_expo ......\n")
  
  rm(list=c("d1", "d2", "non_cases", "cases"))
  gc()
  cat("tmerge done...... \n")
  
  ### cut up post-expo time ----
  with_expo_postexpo <- with_expo %>% dplyr::filter(expo==1)
  cat("with_expo_postexpo pre-survSplit...... \n")
  print(head( with_expo_postexpo %>% arrange(NHS_NUMBER_DEID)))
  with_expo_postexpo <- with_expo_postexpo %>% rename(t0=tstart, t=tstop) %>% mutate(tstart=0, tstop=t-t0)
  with_expo_postexpo <- survSplit(Surv(tstop, event)~., 
                                  with_expo_postexpo,
                                  cut= riskp_cuts_shifted[riskp_cuts_shifted>0],
                                  episode="days_cat"
  )
  cat("with_expo_postexpo post-survSplit...... \n")  
  
  with_expo_postexpo <- with_expo_postexpo %>% mutate(tstart=tstart+t0, tstop=tstop+t0) %>% dplyr::select(-c(t0,t))
  cat("with_expo_postexpo post-survSplit shifted to fit timeline...... \n")
  print(str(with_expo_postexpo))
  
  ### pre-expo time ----
  with_expo_preexpo <- with_expo %>% filter(expo==0)
  with_expo_preexpo$days_cat <- 0
  
  
  cat("with_expo_preexpo set...... \n")
  
  
  ### with_expo -- concat with_expo_preexpo, with_expo_postexpo ----
  ls_with_expo <- list(with_expo_preexpo, with_expo_postexpo)
  with_expo <- do.call(rbind, lapply(ls_with_expo, function(x) x[match(names(ls_with_expo[[1]]), names(x))]))
  
  with_expo  <- with_expo %>%
    group_by(NHS_NUMBER_DEID) %>% arrange(days_cat) %>% mutate(last_step = ifelse(row_number()==n(),1,0))
  
  cat("any event not in last step/period? \n")
  print(with_expo %>% filter((event==1) & (last_step!=1)))
  cat("with_expo done...... \n")
  
  rm(list=c("ls_with_expo", "with_expo_preexpo", "with_expo_postexpo"))
  gc()
  
  # without_expo ----
  cohort_agegp %>%
    filter(is.na(expo_date)) -> without_expo
  
  without_expo %>% 
    dplyr::select(NHS_NUMBER_DEID, expo_date, end_date, event_date, days_to_start, days_to_end, DATE_OF_DEATH, DATE_VAC_CENSOR) %>%  
    mutate(event = if_else( (!is.na(event_date)) & 
                              (
                                ((event_date <= end_date) & ((end_date != DATE_VAC_CENSOR) | is.na(DATE_VAC_CENSOR ))) | 
                                  ((event_date < end_date) & (end_date == DATE_VAC_CENSOR)) 
                              ), 
                            1, 0)) -> without_expo
  
  without_expo$tstart<- without_expo$days_to_start
  without_expo$tstop <- ifelse(without_expo$days_to_end ==0,  without_expo$days_to_end + 0.001, without_expo$days_to_end)
  without_expo$expo<- c(0)
  without_expo$days_cat <- c(0)
  print("without_expo done")
  
  
  # data_surv := rbind without_expo, with_expo ----
  common_cols <- intersect(colnames(without_expo), colnames(with_expo))
  without_expo <- without_expo %>% dplyr::select(all_of(common_cols))
  with_expo <- with_expo %>% dplyr::select(all_of(common_cols))
  data_surv <-rbind(without_expo, with_expo)
  
  rm(list=c("with_expo", "without_expo"))
  
  print("data_surv done")
  print(paste0("total num events in data_surv: ", sum(data_surv$event==1)))
  print(str(data_surv))
  print(head(data_surv))
  
  # pivot wide for weeks since expo ----
  interval_names <- mapply(function(x, y) ifelse(x == y, paste0("day", x), paste0("day", x, "_", y)), 
                           x=riskp_cuts[riskp_cuts < num_study_days], 
                           y=riskp_cuts[riskp_cuts >0], 
                           SIMPLIFY = FALSE)
  interval_names<-gsub("\\-","_neg", interval_names)
  interval_names_boosterextras <- mapply(function(x, y) ifelse(x == y, paste0("day", x), paste0("day", x, "_", y)), 
                                         x=riskp_cuts[(riskp_cuts < num_study_days) & (riskp_cuts > 125)], 
                                         y=riskp_cuts[riskp_cuts > 125][-1], 
                                         SIMPLIFY = FALSE) %>% unlist()
  
  cat("interval_names_boosterextras", interval_names_boosterextras, "\n")
  interval_names_D1D2extras <- mapply(function(x, y) ifelse(x == y, paste0("day", x), paste0("day", x, "_", y)), 
                                      x=riskp_cuts[(riskp_cuts < num_study_days) & (riskp_cuts >= 26*7)], 
                                      y=riskp_cuts[riskp_cuts >= 26*7][-1], 
                                      SIMPLIFY = FALSE) %>% unlist()
  cat("interval_names_D1D2extras", interval_names_D1D2extras, "\n")
  
  i<-0
  for (ls in interval_names){
    i <- i+1
    print(paste(c(ls, i), collapse="..."))
    data_surv[[ls[[1]]]] <- ifelse(data_surv$days_cat==i, 1, 0)
  }
  
  cat("one-hot-encoded days since expo... \n")  
  print(head(data_surv %>% arrange(NHS_NUMBER_DEID) ))
  data_surv <- data_surv %>% left_join(df_sex)
  
  
  # events count ----
  
  data_surv <- data_surv %>% dplyr::mutate(days_cat =factor(days_cat, levels = 0:length(interval_names)))
  tbl_event_count_all <- get_tbl_event_count(data_surv, interval_names)
  tbl_event_count_sex1 <- get_tbl_event_count(data_surv %>% filter(SEX==1), interval_names)
  tbl_event_count_sex2 <- get_tbl_event_count(data_surv %>% filter(SEX==2), interval_names)
  
  tbl_event_count <- list(tbl_event_count_all, tbl_event_count_sex1, tbl_event_count_sex2) %>% 
    reduce(left_join, by = "expo_day")
  
  cat("tbl_event_count...... pre- expo_day ...... \n")
  print(tbl_event_count)
  tbl_event_count$expo_day <- c("pre_expo", unlist(interval_names))
  
  
  names(tbl_event_count) <- c("expo_day", "events_total", "events_M", "events_F")
  cat("tbl_event_count...... \n")
  print(tbl_event_count)
  
  tbl_event_count <- tbl_event_count %>% rbind(
    tbl_event_count %>% dplyr::filter(expo_day!="pre_expo") %>% 
      plyr::numcolwise(sum)() %>% dplyr::mutate(expo_day="post_expo")
  )
  
  # data_surv_cache <- data_surv <- data_surv_cache
  
  data.table::fwrite(tbl_event_count, 
                     paste0("tbl_event_count/tbl_event_count_" , dose_str, "_", event, "_", agegp, "_prev", prev_vac_str, "_", vac_str,".csv"), row.names = FALSE)
  
  
  
  redacted_tbl_event_count <- tbl_event_count %>% 
    mutate(across(2:4,
                  ~ case_when(
                    is.numeric(.) & (.<10) &  (.>0) ~ 10, # less than 10 as 10*
                    TRUE ~ round(./5)*5 # Round to nearest 5
                  )))
  data.table::fwrite(redacted_tbl_event_count, 
                     paste0("tbl_event_count_redacted/redacted_tbl_event_count_" , dose_str, "_", event, "_", agegp, "_prev", prev_vac_str, "_", vac_str,".csv"), row.names = FALSE)
  
  
  
  # ind_any_zeroeventperiod ----
  ind_any_zeroeventperiod <- any((tbl_event_count[,c("events_total")] == 0) & (!identical(riskp_cuts, riskp_cuts_reduced)))
  if(dose_str=="booster"){ 
    ind_any_zeroeventperiod <- any(  # don't collapse for booster if no events >125d post-booster
      ((tbl_event_count %>% dplyr::filter(!expo_day %in% interval_names_boosterextras) %>% 
          dplyr::select(events_total) %>% pull()) == 0) & 
        (!identical(riskp_cuts, riskp_cuts_reduced)))
  } else {
    ind_any_zeroeventperiod <- any(  # don't collapse for booster if no events >26*7=182d post-booster
      ((tbl_event_count %>% dplyr::filter(!expo_day %in% interval_names_D1D2extras) %>% 
          dplyr::select(events_total) %>% pull()) == 0) & 
        (!identical(riskp_cuts, riskp_cuts_reduced)))
  }
  
  
  #===============================================================================
  # FINALIZE age, region, data_surv
  #-------------------------------------------------------------------------------
  data_surv <- data_surv %>% left_join(df_age_region_coxweight)
  cat("data_surv done......\n")
  print(head(data_surv))
  
  if (
    (!"cox_weights" %in% names(data_surv)) |
    (!is.numeric(data_surv$event) ) |  any(unique(data_surv$event) %>% sort() != c(0,1))
  ){
    stop("Bad data_surv")
  }
  
  if(dose_str=="booster"){
    days_cat_to_excl <- which(interval_names %in% interval_names_boosterextras) %>% as.character()
  } else {
    days_cat_to_excl <- which(interval_names %in% interval_names_D1D2extras) %>% as.character()
  }
  tbl_IRpersonyears <- get_personyears_prepostexpo(data_surv, days_cat_to_excl)
  dir.create(file.path(res_dir, "tbl_IRpersonyears"), recursive = TRUE);  dir.create(file.path(res_dir, "red_tbl_IRpersonyears"), recursive = TRUE)
  data.table::fwrite(tbl_IRpersonyears, file.path(res_dir, "tbl_IRpersonyears",
                                                      paste0("tbl_IRpersonyears_" , dose_str, "_", event, "_", agegp, "_prev", prev_vac_str, "_", vac_str,".csv") ), row.names = FALSE)
  data.table::fwrite(tbl_IRpersonyears %>% dplyr::select(expo_day, red_events_100Kpersonyears, red_IR), file.path(res_dir, "red_tbl_IRpersonyears",
                                                      paste0("red_tbl_IRpersonyears_" , dose_str, "_", event, "_", agegp, "_prev", prev_vac_str, "_", vac_str,".csv") ), row.names = FALSE)
  
  return(list(data_surv, unlist(interval_names), ind_any_zeroeventperiod, interval_names_boosterextras, interval_names_D1D2extras))
}


get_tbl_event_count <- function(data_surv, interval_names){
  tbl_event_count <- table(data_surv[data_surv$event==1]$days_cat) %>% as.data.frame() 
  setnames(tbl_event_count, 
           old = c("Var1", "Freq"), 
           new = c("expo_day", "event"))
  
  return(tbl_event_count)
}


get_personyears_prepostexpo <- function(data_surv, days_cat_to_excl){
  data_surv <- data_surv[!(data_surv$days_cat %in% days_cat_to_excl), ]
  data_surv <- data_surv %>% dplyr::mutate(
    expo_day=case_when(
      days_cat==0~"pre_expo",
      TRUE ~"post_expo"
    ),
    personyrs_100k=(tstop-tstart)/(365.25*100000),
    personyrs_100k_weighted = cox_weights*personyrs_100k
  )
  
  
  summary_personyears_prepostexpo <- data_surv %>% group_by(expo_day) %>%
    summarise(
      personyrs_100k_weighted_intvl = sum(personyrs_100k_weighted),
      num_events = sum(event)
    ) %>%  
    dplyr::mutate(
      red_personyrs_100k_weighted_intvl =redact(personyrs_100k_weighted_intvl),
      red_num_events=redact(num_events),
      red_events_100Kpersonyears = glue("{red_num_events}/{red_personyrs_100k_weighted_intvl}"),
      red_IR =  sprintf("%.2f",red_num_events/red_personyrs_100k_weighted_intvl),
      expo_day = factor(expo_day, levels=c("pre_expo", "post_expo"))
    ) %>% arrange(expo_day)

  
  return(summary_personyears_prepostexpo)
}

redact <- function(col2redact) {
  redacted <- case_when(
    is.numeric(col2redact) & (col2redact<10) &  (col2redact>0) ~ 10, # less than 10 as 10*
    TRUE ~ round(col2redact/5)*5 # Round to nearest 5
  )
  return(redacted)
}