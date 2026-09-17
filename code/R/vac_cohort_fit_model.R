## =============================================================================
## Fitting Cox model
##
## Author: Samantha Ip
## =============================================================================
source(file.path(scripts_dir,"infvac_get_data_surv_preeexporiskp.R"), local=TRUE)

#------------------------ GET FORMULA  ---------------------------

get_mode <- function(dataset, covariate){
  u <- unique(dataset[[covariate]])
  tab <- tabulate(match(dataset[[covariate]], u))
  relevel_with <- u[tab == max(tab)]
  return(relevel_with)
}

rm_leq2_nlevel1_covars <- function(data_surv, covar_names,fml,expo,event,agegp,sex, prev_vac_str, vac_str){
  # rm covars with <=2 occurrences per level......
  # str(data_surv)
  data_surv <- data_surv %>% droplevels() # in case of superfluous levels post random-sampling
  # Factors that are already coded as factors remembers its levels even if not in filtered set
  # Which factors after droplevels() only has one level left?
  
  factor_covars_postexpo_event <- data_surv %>% dplyr::filter((expo==1) & (event==1)) %>% 
    dplyr::select(covar_names[!covar_names %in% c("cov_ethnicity")]) %>% droplevels()
  
  print(str(factor_covars_postexpo_event))

  
  # table(factor_covars %>% dplyr::select(region_name))
  
  covars2rm <- lapply(colnames(factor_covars_postexpo_event) %>% as.list(), function(col){
    cat(col, "\n")
    counts_lvl <- table(factor_covars_postexpo_event %>% dplyr::select(col)) %>% 
      as.data.frame() %>% pull(Freq)
    df <- data.frame(covariate=col, any_leq2=any(counts_lvl<=2))
    return(df)
  }) %>% rbindlist() %>% dplyr::filter(any_leq2==TRUE) %>% pull(covariate)
  cat("covars2rm", event, "......", covars2rm, "\n")
  print(covars2rm)
  
  if(any(c("cov_deprivation", "cov_smoking_status") %in% covars2rm )){
    if("cov_deprivation" %in% covars2rm){
      factor_covars_postexpo_event <- factor_covars_postexpo_event %>% mutate(cov_deprivation= 
                                       case_when(cov_deprivation=="Deciles_1_2"~"Deciles_1_4",
                                                 cov_deprivation=="Deciles_3_4"~"Deciles_1_4",
                                                 cov_deprivation=="Deciles_5_6"~"Deciles_5_6",
                                                 cov_deprivation=="Deciles_7_8"~"Deciles_7_10",
                                                 cov_deprivation=="Deciles_9_10"~"Deciles_7_10",
                                                 TRUE ~ ""
                                                 ))
      
      factor_covars_postexpo_event$cov_deprivation <- ordered(factor_covars_postexpo_event$cov_deprivation, levels = c("Deciles_1_4","Deciles_5_6","Deciles_7_10", ""))
    }
    
    if("cov_smoking_status" %in% covars2rm){
      factor_covars_postexpo_event<-factor_covars_postexpo_event %>% mutate(cov_smoking_status = as.character(cov_smoking_status)) %>%
        mutate(cov_smoking_status= case_when(cov_smoking_status=="Never-smoker"~"Never-smoker",
                                                 cov_smoking_status=="Ex-smoker"~"Ever-smoker",
                                                 cov_smoking_status=="Current-smoker"~"Ever-smoker",
                                                 cov_smoking_status=="missing"~"Never-smoker"))
      
      factor_covars_postexpo_event <- factor_covars_postexpo_event %>% mutate(cov_smoking_status = as.factor(cov_smoking_status)) %>%
        mutate(cov_smoking_status = relevel(cov_smoking_status,ref="Never-smoker"))
      
    }
    
    covars2rm <- lapply(colnames(factor_covars_postexpo_event) %>% as.list(), function(col){
      cat(col, "\n")
      counts_lvl <- table(factor_covars_postexpo_event %>% dplyr::select(col)) %>% 
        as.data.frame() %>% pull(Freq)
      df <- data.frame(covariate=col, any_leq2=any(counts_lvl<=2))
      return(df)
    }) %>% rbindlist() %>% dplyr::filter(any_leq2==TRUE) %>% pull(covariate)
  }
  single_level_factors <- factor_covars_postexpo_event %>% dplyr::select_if(~ is.factor(.) & (nlevels(.)==1) ) %>% colnames()
  covars2rm <- c(covars2rm, single_level_factors)
  
  cat("covariates with rare level -- to remove......\n")
  ### df_rm_covars ----
  if(length(covars2rm)>0){
      tbl_rm_covars <- data.frame(covars2rm=covars2rm) %>% dplyr::mutate(
        agegp=agegp,
        sex=sex,
        prev_vac_str=prev_vac_str,
        vac_str=vac_str,
        dose=dose_str,
        event=event
      )
      tbl_rm_covars %>% print()  
      fpath_df_rm_covars <- paste0("rm_leq2/rm_leq2_nlevel1_covars_" , fml, "_", event, ".csv")
      write.table(tbl_rm_covars, fpath_df_rm_covars, append = T , 
                  col.names = ifelse(file.exists(fpath_df_rm_covars), FALSE, TRUE), sep = ",", row.names = F)
  
      
  }
  cat("rm_leq2_nlevel1_covars -- data_surv before \n")
  names(data_surv)
  data_surv <- data_surv %>% dplyr::select(-one_of(covars2rm))
  
  if("cov_deprivation" %in% names(data_surv)){
    data_surv <- data_surv %>% mutate(cov_deprivation= case_when(cov_deprivation=="Deciles_1_2"~"Deciles_1_4",
                                                                  cov_deprivation=="Deciles_3_4"~"Deciles_1_4",
                                                                  cov_deprivation=="Deciles_5_6"~"Deciles_5_6",
                                                                  cov_deprivation=="Deciles_7_8"~"Deciles_7_10",
                                                                  cov_deprivation=="Deciles_9_10"~"Deciles_7_10",
                                                                  TRUE ~ ""
                                                        ))
    
    data_surv$cov_deprivation <- ordered(data_surv$cov_deprivation, levels = c("Deciles_1_4","Deciles_5_6","Deciles_7_10", ""))
  }
  
  if("cov_smoking_status"%in% names(data_surv)){
    data_surv <- data_surv %>% mutate(cov_smoking_status = as.character(cov_smoking_status)) %>%
      mutate(cov_smoking_status= case_when(cov_smoking_status=="Never-smoker"~"Never-smoker",
                                           cov_smoking_status=="Ex-smoker"~"Ever-smoker",
                                           cov_smoking_status=="Current-smoker"~"Ever-smoker",
                                           cov_smoking_status=="missing"~"Never-smoker"))
    
    data_surv <- data_surv %>% mutate(cov_smoking_status = as.factor(cov_smoking_status)) %>%
      mutate(cov_smoking_status = relevel(cov_smoking_status,ref="Never-smoker"))
    
  }
  summary(data_surv)
  
  return(data_surv)
}

### no-interaction----
fml_weeks_agegroup_sex <- function(sex, covar_names, interval_names, fixed_covars){
  age_spline <- "pspline(age, df=2)" # 
  
  cat("...... + weeks + agegroup + sex ...... \n")
  if (mdl == "mdl2_agesex"){
    redcovariates_excl_region <- unique(c(interval_names))
    cat("...... redcovariates_excl_region ...... \n")
    print(unlist(redcovariates_excl_region))
    
    fml_red <- ifelse(sex=="all",
      paste0(
      "Surv(tstart, tstop, event) ~ ",
      paste(redcovariates_excl_region, collapse="+"), 
      "+ cluster(NHS_NUMBER_DEID)  + strata(region_name)+ SEX +", age_spline), 
      paste0(
        "Surv(tstart, tstop, event) ~ ",
        paste(redcovariates_excl_region, collapse="+"), 
        "+ cluster(NHS_NUMBER_DEID)  + strata(region_name) +", age_spline)
      )
    
  } else if (mdl == "mdl1_unadj"){
    redcovariates_excl_region <- unique(c(interval_names))
    cat("...... redcovariates_excl_region ...... \n")
    print(unlist(redcovariates_excl_region))
    
    fml_red <- paste0("Surv(tstart, tstop, event) ~ ",
                        paste(redcovariates_excl_region, collapse="+"))

  
  } else if (mdl == "mdl3b_fullyadj"){
    AMI_bkwdselected_covars <- covar_names
    redcovariates_excl_region <- unique(c(interval_names, AMI_bkwdselected_covars, fixed_covars))
    print(unlist(redcovariates_excl_region))
    
    fml_red <- ifelse(sex=="all",
      paste0(
        "Surv(tstart, tstop, event) ~ ",
        paste(redcovariates_excl_region, collapse="+"), 
        "+ cluster(NHS_NUMBER_DEID)  + strata(region_name) + SEX +", age_spline),
      paste0(
        "Surv(tstart, tstop, event) ~ ",
        paste(redcovariates_excl_region, collapse="+"), 
        "+ cluster(NHS_NUMBER_DEID)  + strata(region_name) + ", age_spline)
    )
    
  }
  return(fml_red)}



# COXFIT ----

coxfit_bkwdselection <- function(fml, prev_vac_str, vac_str, data_surv, sex, interval_names, fixed_covars, event, agegp, covar_names){
  cat("...... sex ", sex, " ...... \n")
  if(mdl=="mdl3b_fullyadj"){
    data_surv <- rm_leq2_nlevel1_covars(data_surv, covar_names,fml,expo,event,agegp,sex, prev_vac_str, vac_str)
  }
  
  covar_names <- covar_names[covar_names %in% names(data_surv)]
  
  # get Surv formula 
  if (fml == "+ weeks + agegroup + sex"){
    fml_red <- fml_weeks_agegroup_sex(sex, covar_names, interval_names, fixed_covars)
  } 
  print(fml_red)
  
  # fit coxph() 
  if(is.null(data_surv$cox_weights)) stop("is.null @data_surv$cox_weights!!")
  system.time(fit_red <- coxph(
    formula = as.formula(fml_red), 
    data = data_surv, weights=data_surv$cox_weights
  ))
  # dir.create(file.path(res_dir, "RDS"), recursive = TRUE)
  # saveRDS(fit_red, paste0("RDS/pspline_fit_", expo, "_", event, "_", fml, "_", agegp,"_sex", sex, "_prev", prev_vac_str, "_", vac_str, ".rds"))
  
  # tidy for presentation ----
  fit_tidy <- broom::tidy(fit_red, exponentiate = TRUE, conf.int=TRUE)
  fit_tidy$sex<- sex
  
  gc()
  print(fit_tidy)
  return(fit_tidy)
}


# MAIN ----
fit_model_reducedcovariates <- function(fml, covars, prev_vac_str, vac_str, agegp, event, survival_data){
  cat("START vac_cohort_fit_model.R -- fit_model_reducedcovariates ......\n")
  
  list_data_surv_ind0eventperiod <- fit_get_data_surv(fml, prev_vac_str, vac_str, covars,  agegp, event, survival_data, riskp_cuts)
  data_surv <- list_data_surv_ind0eventperiod[[1]]
  interval_names <- list_data_surv_ind0eventperiod[[2]]
  ind_any_zeroeventperiod <- list_data_surv_ind0eventperiod[[3]]
  interval_names_boosterextras <- list_data_surv_ind0eventperiod[[4]]
  interval_names_D1D2extras <- list_data_surv_ind0eventperiod[[5]]


  if (ind_any_zeroeventperiod){
    cat("...... COLLAPSING POST-EXPO INTERVALS ......\n")
    list_data_surv_ind0eventperiod <- fit_get_data_surv(fml, prev_vac_str, vac_str, covars,  agegp, event, survival_data, riskp_cuts=riskp_cuts_reduced)
    data_surv <- list_data_surv_ind0eventperiod[[1]]
    interval_names <- list_data_surv_ind0eventperiod[[2]]
    ind_any_zeroeventperiod <- list_data_surv_ind0eventperiod[[3]]
    interval_names_boosterextras <- list_data_surv_ind0eventperiod[[4]]
    interval_names_D1D2extras <- list_data_surv_ind0eventperiod[[5]]
  }


  covar_names <- names(covars)[ names(covars) != "NHS_NUMBER_DEID"]

  if(mdl=="mdl3b_fullyadj"){data_surv <- data_surv %>% left_join(covars)}

  data_surv <- data_surv %>% mutate(
    SEX = factor(SEX),
    expo = factor(expo)
    )

  cat("... data_surv ... \n")
  print(str(data_surv))


  gc()

  fixed_covars <- c() # hack for skipping backward-selection


  if (dose_str=="booster"){
    interval_names_extras <- interval_names_boosterextras
  } else{
    interval_names_extras <- interval_names_D1D2extras
  }
  cat("interval_names_extras:", interval_names_extras, "\n")


  if (!is.null(interval_names_extras)){
    # data_surv <- data_surv_cache
    data_surv <- data_surv %>% dplyr::select(!interval_names_extras) %>%
      dplyr::filter(!days_cat %in% which(interval_names %in% interval_names_extras))
    str(data_surv)
    interval_names <- interval_names[!interval_names %in% interval_names_extras]
    }

  sink("counts_TREcmprSDE.txt", append = TRUE)
  cat(glue::glue("data_surv -- Expo:{expo}, Event:{event}, Agegp:{agegp}, Prev-vac:{prev_vac_str}, Vac:{vac_str} : \n")); print(str(survival_data, vec.len = 0)); cat("\n")
  sink()

  median_and_last_event_time <- data_surv %>%
    dplyr::filter(event==1 & !is.na(expo_date) & (event_date >= expo_date)) %>%
    dplyr::select("NHS_NUMBER_DEID", "expo_date", "end_date", "event_date", "days_cat") %>%
    dplyr::mutate(event_date_minus_expo_date = event_date-expo_date) %>%
    group_by(days_cat) %>%
    summarise(median_event_time = median(event_date_minus_expo_date)+1,
              last_event_time = max(event_date_minus_expo_date, na.rm=TRUE)+1
              ) %>%
    dplyr::mutate(interval_name = interval_names)
  
  
  cat("median_and_last_event_time......\n")
  print(median_and_last_event_time)
  fwrite(median_and_last_event_time, paste0("median_and_last_event_time/median_and_last_event_time" , fml, "_", expo, "_", event, "_agegp", agegp, "_prev", prev_vac_str, "_", vac_str, ".csv"), row.names = FALSE)


  if(!just_eventcount_and_medianlasteventtime){
    fit <- coxfit_bkwdselection(fml, prev_vac_str, vac_str, data_surv, sex="all", interval_names, fixed_covars,  event, agegp, covar_names)
    fit$event <- event
    fit$agegp <- agegp
    fit$fml <- fml
    cat("... fit ... \n")
    print(fit)

    num_intervals  <- interval_names %>% unlist()%>% length()

    fwrite(fit, paste0("tbl_hr/tbl_hr_" , fml, "_", expo, "_", event, "_agegp", agegp, "_prev", prev_vac_str, "_", vac_str, "_intvl", num_intervals, ".csv"), row.names = FALSE)
    cat("fit -- all intervals ......\n")
    print(fit)

  }
  gc()
  cat("DONE vac_cohort_fit_model.R -- fit_model_reducedcovariates ......\n")


}



mk_factor_orderlevels <- function(df, colname)
{
  df <- df %>% dplyr::mutate(
    !!sym(colname) := factor(!!sym(colname), levels = str_sort(unique(df[[colname]]), numeric = TRUE)))
  return(df)
}



one_hot_encode <- function(interacting_feat, data_surv, interval_names_withpre){
  cat("...... one_hot_encode ...... \n")
  data_surv <- as.data.frame(data_surv)
  data_surv$week <- apply(data_surv[unlist(interval_names_withpre)], 1, function(x) names( x[x==1]) )
  data_surv$week <- relevel(as.factor( data_surv$week) , ref="week_pre")
  
  data_surv$tmp <- as.factor(paste(data_surv$week, data_surv[[interacting_feat]], sep="_"))
  df_tmp <- as.data.frame(model.matrix( ~ 0 + tmp, data = data_surv))
  names(df_tmp) <- substring(names(df_tmp), 4)
  
  for (colname in names(df_tmp)){
    print(colname)
    df_tmp <- mk_factor_orderlevels(df_tmp, colname)
  }
  
  data_surv <- cbind(data_surv, df_tmp)
  
  str(data_surv)
  return(data_surv)
}


