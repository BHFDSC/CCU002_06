## =============================================================================
## Pipeline (2): Reads in analysis-specific data, loads parameters, 
## gets vaccine-specific dataset -- censoring at appropriate dates
##
## Author: Samantha Ip
## =============================================================================
# print(rstudioapi::getSourceEditorContext()$path)
cat("START vac_cohort_02_pipe.R ......\n")
# specify path to data ----
date_data <- "nv_20230904"
dir_data <- "~/collab/CCU002_06/data"

fpath_cohort_spine <- file.path(dir_data, glue("ccu002_06_exclusion_cohort_spine_output_{date_data}.csv.gz"))
fpath_covars <- file.path(dir_data, glue("ccu002_06_cohort_{dose_str}_cov_{date_data}.csv.gz"))
fpath_outcomes <- file.path(dir_data, glue("ccu002_06_cohort_{dose_str}_out_{date_data}.csv.gz"))
fpath_cv <- file.path(dir_data, glue("ccu002_06_cvflag_final_onlyflagged_20201208_{date_data}.csv.gz"))
fpath_cev <- file.path(dir_data, glue("ccu002_06_cov_dose1_cev_20201208_{date_data}.csv.gz"))


# specify study parameters----
agebreaks <- c(0, 40, 60, 80, 500)
agelabels <- c("18to39", "40to59", "60to79", "80to110") # end agegroup filters below


noncase2case_ratio <- 20
if (ctrl2case_10) {noncase2case_ratio <- 10}


cohort_start_date <- as.Date("2020-12-08")
cohort_end_date <- as.Date("2022-01-23")



# cuts_weeks_since_expo <- c(2, as.numeric(ceiling(difftime(cohort_end_date,cohort_start_date)/7))) 
num_study_weeks <- as.numeric(ceiling(difftime(cohort_end_date,cohort_start_date)/7))+1
num_study_days <- as.numeric(difftime(cohort_end_date,cohort_start_date)) +1

riskp_cuts <- c(0,7*c(1,2,4,12,24, 26), num_study_days)
riskp_cuts_reduced <- c(0, 28, 26*7, num_study_days)


# Check time when booster starts ---- 
check_booster_dates <- fread(fpath_cohort_spine, select=c("vaccination_dose_booster_date"))
difftime( min(check_booster_dates$vaccination_dose_booster_date, na.rm=TRUE), cohort_start_date) # 
rm(check_booster_dates)
gc()

# expo 
if(dose_str == "dose1"){expo <- "VAC1"
  } else if (dose_str == "dose2"){expo <- "VAC2"
  } else if (dose_str == "booster"){expo <- "VAC3"}




#---- READ IN DATA ====
# cohort_vac ----
cohortspine_df_names <- fread(fpath_cohort_spine, nrows=1) %>% colnames() %>% sort()
cat("Begin fread cohort_vac ......\n")


if (dose_str=="dose1"){
  
  cohort_vac <- fread(fpath_cohort_spine, 
                    select=c("NHS_NUMBER_DEID", 
                             "cov_dose1_sex", 
                             "out_death", 
                             "cov_dose1_age", 
                             "vaccination_dose1_date", 
                             "vaccination_dose2_date",
                             "vaccination_dose1_product",
                             "cov_dose1_region"
                    ))

  
  setnames(cohort_vac, 
           old = c("cov_dose1_sex", 
                   "out_death", 
                   "cov_dose1_age", 
                   "vaccination_dose1_date", 
                   "vaccination_dose2_date",
                   "vaccination_dose1_product",
                   "cov_dose1_region"), 
           new = c("SEX", 
                   "DATE_OF_DEATH", 
                   "AGE_AT_COHORT_START", 
                   "VACCINATION_DATE", 
                   "VACCINATION_DATE_NEXT",
                   "VACCINE_PRODUCT",
                   "region_name"))
} else if (dose_str=="dose2"){
  cohort_vac <- fread(fpath_cohort_spine, 
                      select=c("NHS_NUMBER_DEID", 
                               "cov_dose2_sex", 
                               "out_death", 
                               "cov_dose2_age", 
                               "vaccination_dose1_date", 
                               "vaccination_dose2_date", 
                               "vaccination_dose1_product",
                               "vaccination_dose2_product",
                               "vaccination_dose3_date",
                               "vaccination_dose_booster_date",
                               "cov_dose2_region"
                      ))
  
  cohort_vac <- cohort_vac %>% dplyr::mutate(vaccination_dose3b_date = pmin(vaccination_dose3_date, vaccination_dose_booster_date, na.rm=TRUE))


  setnames(cohort_vac, 
           old = c("cov_dose2_sex", 
                   "out_death", 
                   "cov_dose2_age", 
                   "vaccination_dose2_date", 
                   "vaccination_dose2_product", 
                   "vaccination_dose1_date",
                   "vaccination_dose1_product",
                   "vaccination_dose3b_date",
                   "cov_dose2_region"), 
           new = c("SEX", 
                   "DATE_OF_DEATH", 
                   "AGE_AT_COHORT_START", 
                   "VACCINATION_DATE", 
                   "VACCINE_PRODUCT", 
                   "START_DATE",
                   "PRODUCT_PREV",
                   "VACCINATION_DATE_NEXT",
                   "region_name"))
} else if (dose_str=="booster"){
  cohort_vac <- fread(fpath_cohort_spine, 
                      select=c("NHS_NUMBER_DEID",
                               "cov_booster_age", 
                               "cov_booster_sex", 
                               "cov_booster_region",
                               "out_death", 
                               # index ......
                               "vaccination_dose1_date", 
                               "vaccination_dose2_date", 
                               "vaccination_dose1_product",
                               "vaccination_dose2_product",
                               # exposure ......
                               "vaccination_dose_booster_date",
                               "vaccination_dose_booster_product",
                               # censor ......
                               "vaccination_dose3_date"
                      ))
  
  
  setnames(cohort_vac, 
           old = c("cov_booster_age", 
                   "cov_booster_sex", 
                   "cov_booster_region",
                   "out_death", 
                   "vaccination_dose_booster_date", 
                   "vaccination_dose_booster_product", 
                   "vaccination_dose2_date",
                   "vaccination_dose3_date"
                   ), 
           new = c("AGE_AT_COHORT_START", 
                   "SEX", 
                   "region_name",
                   "DATE_OF_DEATH", 
                   "VACCINATION_DATE", 
                   "VACCINE_PRODUCT", 
                   "START_DATE",
                   # "PRODUCT_PREV",
                   "VACCINATION_DATE_NEXT"
                   ))
} 

# impose >18 age limit ----
cohort_vac <- cohort_vac %>% dplyr::filter(AGE_AT_COHORT_START >= 18)

cat("got cohort_vac ......\n")

gc()

# covars ----

if (mdl=="mdl3b_fullyadj"){
  ethnicity_deprivation <- fread(fpath_cohort_spine, 
                      select=c("NHS_NUMBER_DEID", 
                               paste0("cov_", dose_str, "_ethnicity"), 
                               paste0("cov_", dose_str, "_deprivation")
                      ))
  
  
  covar_df_names <- fread(fpath_covars, nrows=1) 
  ls_covars_fpathcovars <- c(
    "smoking_status", "diabetes", "depression", "bmi_obesity", "cancer", "copd",
    "ckd", "liver_disease", "dementia", "stroke_all", "ami", "all_vte", "thrombophilia",
    "disorders", "surgery", "prior_covid19",
    "meds_antiplatelet", "meds_bp_lowering", "meds_lipid_lowering", "meds_anticoagulant",
    "meds_cocp", "meds_hrt"
  ) %>% paste("cov", dose_str, ., sep="_")
  
  
  covars_fpathcovars <- fread(fpath_covars, select = c("NHS_NUMBER_DEID", ls_covars_fpathcovars))
  covars <- covars_fpathcovars %>% left_join(ethnicity_deprivation, by="NHS_NUMBER_DEID")
  
  rm(covars_fpathcovars, ethnicity_deprivation)
  gc()
  names(covars) <- sub(paste0(dose_str, "_"), "", names(covars))
  
  source(file.path(scripts_dir, "si_prep_covariates.R"), local = TRUE)
  
  ### CEV/CV/Neither flag ----
  ids_cev <- fread(fpath_cev) %>% filter(flag_CEV==1)%>% pull(NHS_NUMBER_DEID)
  
  ids_cv_notcev <-  fread(fpath_cv) %>% pull(NHS_NUMBER_DEID)
  ids_cv_notcev <- ids_cv_notcev[!ids_cv_notcev %in% ids_cev]
  
  covars <- covars %>% 
    dplyr::mutate(
      cev_cv_neither = case_when(
        NHS_NUMBER_DEID %in% ids_cev ~ "cev",
        NHS_NUMBER_DEID %in% ids_cv_notcev ~ "cv",
        TRUE ~ "neither"
      ),
      cev_cv_neither = factor(cev_cv_neither, levels=c("neither", "cv", "cev"))
     )
  str(covars) %>% print()
  
} else {
  covars <- data.frame()
  mk_factor_orderlevels <- function(covars, colname)
  {
    covars <- covars %>% mutate(
      !!sym(colname) := factor(!!sym(colname), levels = stringr::str_sort(unique(covars[[colname]]), numeric = TRUE)))
    return(covars)
  }
  cohort_vac$region_name <- gsub(" ", "_", cohort_vac$region_name)
  for (colname in c("SEX", "region_name")){
    # print(colname)
    cohort_vac <- mk_factor_orderlevels(cohort_vac, colname)
  }
  cohort_vac$region_name <- relevel(factor(cohort_vac$region_name), ref = "London")
}





cat("got covars......\n")


#Functions ----
set_dates_outofrange_na <- function(df, colname)
{
  if (dose_str=="dose1"){df$START_DATE <- cohort_start_date}
  
 
  df <- df %>% mutate(
    !!sym(colname) := as.Date(ifelse((!!sym(colname) > cohort_end_date) | 
                                       (!!sym(colname) < START_DATE) | 
                                       (!!sym(colname) < cohort_start_date), 
                                     NA, !!sym(colname) ), origin='1970-01-01')
  )


  if ("DATE_VAC_CENSOR" %in%  colnames(df)){
    df <- df %>% dplyr::mutate(
      !!sym(colname) := as.Date(ifelse((!is.na(DATE_VAC_CENSOR)) & (!!sym(colname)  >= DATE_VAC_CENSOR), NA, !!sym(colname) ), origin='1970-01-01'))
    }

  return(df)
}

get_vac_specific_dataset <- function(survival_data, vac_of_interest, prev_vac_of_interest){

  if (censor_at_next_dose){
    
    if (dose_str=="dose1"){
      survival_data$DATE_VAC_CENSOR <- as.Date(ifelse(!(survival_data$VACCINE_PRODUCT %in% vac_of_interest),
                                                      survival_data$expo_date, 
                                                      NA), origin='1970-01-01')
      survival_data <-  transform(survival_data, DATE_VAC_CENSOR = pmin(VACCINATION_DATE_NEXT,  DATE_VAC_CENSOR, na.rm=TRUE))
    } else if (dose_str=="dose2"){
      survival_data <- survival_data %>% dplyr::filter((survival_data$PRODUCT_PREV %in% vac_of_interest))
      survival_data$DATE_VAC_CENSOR <- as.Date(ifelse((!(survival_data$VACCINE_PRODUCT %in% vac_of_interest)),
                                                      survival_data$expo_date, 
                                                      NA), origin='1970-01-01')
      survival_data <-  transform(survival_data, DATE_VAC_CENSOR = pmin(VACCINATION_DATE_NEXT,  DATE_VAC_CENSOR, na.rm=TRUE))
    } else if (dose_str=="booster"){
      survival_data <- survival_data %>% dplyr::filter((!is.na(vaccination_dose2_product)) & (vaccination_dose1_product==vaccination_dose2_product)) %>% 
        dplyr::mutate(PRODUCT_PREV = vaccination_dose2_product) %>% 
        dplyr::filter(PRODUCT_PREV %in% prev_vac_of_interest)
      survival_data$DATE_VAC_CENSOR <- as.Date(ifelse((!(survival_data$VACCINE_PRODUCT %in% vac_of_interest)),
                                                      survival_data$expo_date, 
                                                      NA), origin='1970-01-01')
      survival_data <-  transform(survival_data, DATE_VAC_CENSOR = pmin(VACCINATION_DATE_NEXT,  DATE_VAC_CENSOR, na.rm=TRUE))
    }
    
  } else if (!censor_at_next_dose) {
    if (dose_str=="dose1"){
      survival_data$DATE_VAC_CENSOR <- as.Date(ifelse(!(survival_data$VACCINE_PRODUCT %in% vac_of_interest),
                                                      survival_data$expo_date, 
                                                      NA), origin='1970-01-01')
      survival_data <-  transform(survival_data, DATE_VAC_CENSOR = pmin(expo_date+26*7, DATE_VAC_CENSOR, na.rm=TRUE))
    } else if (dose_str=="dose2"){
      survival_data <- survival_data %>% dplyr::filter((survival_data$PRODUCT_PREV %in% vac_of_interest))
      survival_data$DATE_VAC_CENSOR <- as.Date(ifelse((!(survival_data$VACCINE_PRODUCT %in% vac_of_interest)),
                                                      survival_data$expo_date, 
                                                      NA), origin='1970-01-01')
      survival_data <-  transform(survival_data, DATE_VAC_CENSOR = pmin(expo_date+26*7, DATE_VAC_CENSOR, na.rm=TRUE))
    } else if (dose_str=="booster"){
      survival_data <- survival_data %>% dplyr::filter((!is.na(vaccination_dose2_product)) & (vaccination_dose1_product==vaccination_dose2_product)) %>% 
        dplyr::mutate(PRODUCT_PREV = vaccination_dose2_product) %>% 
        dplyr::filter(PRODUCT_PREV %in% prev_vac_of_interest)
      survival_data$DATE_VAC_CENSOR <- as.Date(ifelse((!(survival_data$VACCINE_PRODUCT %in% vac_of_interest)),
                                                      survival_data$expo_date, 
                                                      NA), origin='1970-01-01')
      survival_data <-  transform(survival_data, DATE_VAC_CENSOR = pmin(expo_date+26*7, DATE_VAC_CENSOR, na.rm=TRUE))
    }
  }

  return(survival_data)
}

cat("DONE vac_cohort_02_pipe.R ......\n")