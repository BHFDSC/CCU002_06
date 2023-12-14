## =============================================================================
## Pipeline (1): Control center, calls relevant analysis scripts, sets working 
## and saving directories, parallelises processes
##
## Author: Samantha Ip
## =============================================================================
# system("nohup Rscript ~/dars_nic_391419_j3w9t_collab/CCU002_06/scripts_ccu00502/vac_cohort_01_pipe.R > ~/dars_nic_391419_j3w9t_collab/CCU002_06/dose2_mdl2_agesex_vac_cohort_01_pipe.out  2>&1 &")
#!/usr/bin/env Rscript
library(data.table)
library(dplyr)
library(survival)
library(table1)
library(broom)
library(DBI)
library(ggplot2)
library(nlme)
library(tidyverse)
library(R.utils)
library(lubridate)
library(purrr)
library(parallel)
# library(multcomp)
library(glue)
# options(error=recover)
options(error=NULL) # for non-interactive
# print(rstudioapi::getSourceEditorContext()$path)

# detectCores()


# con <- dbConnect(odbc::odbc(), "Databricks", timeout=60, PWD=rstudioapi::askForPassword("enter databricks personal access token:"))
rm(list=setdiff(ls(), c("con")))
gc()

# args = commandArgs(trailingOnly=TRUE)
args <- c("booster", "mdl2_agesex", "TRUE", "FALSE")
dose_str <- args[1] # dose1, dose2, booster
mdl <- args[2] # "mdl2_agesex", "mdl3b_fullyadj"
just_eventcount_and_medianlasteventtime <- as.logical(args[3])
ctrl2case_10 <- as.logical(args[4])
# nonfatal_only <- TRUE
ind_SA <- FALSE # HERE
censor_at_next_dose <- FALSE # HERE


cat(paste(dose_str, mdl, "vac_cohort_01_pipe.out", sep="_"), "\n\n", "censor_at_next_dose: ", censor_at_next_dose, "\n") # for system() only

# cat(nonfatal_only, dose_str, mdl)

res_dir_proj <- "~"
res_dir_date <- glue::glue("20230919_cev20201208_IRpy_{mdl}{ifelse(ctrl2case_10,'_c2c10','')}") # 20230203_NotCensorNextDose_Stop26wkPostexpo_PsplineAgeDF2

# specify path to scripts' directory
scripts_dir <- "~/ccu002_06/scripts_ccu00502"
ls_events <- paste("first", # By default, we will use codes recorded in first position. For rare outcomes, we will use any position. # HERE
      c("AMI","stroke_isch","PE","DVT","ICVT","portal_vein_thrombosis",
        "any_thrombocytopenia","stroke_SAH_HS","mesenteric_thrombus",
        "myocarditis","pericarditis",
        "arterial", "venous"
        ),
      sep="_") #HERE


# ls_events <- paste("first",
#                    c("pericarditis", "venous"),
#                    sep="_") #HERE

# specify model parameters, data source, outcomes of interest, read in relevant data, get prepped covariates
source(file.path(scripts_dir, paste0("vac_cohort_02_pipe.R")), local=TRUE)
# noncase2case_ratio <- 10 # HACK for composite arterial that wouldn't run on 20



gc()
# -----------SET MODEL-SPECIFIC RESULTS DIR  & CALLS MODEL SCRIPT --------------
# res_dir <- file.path(res_dir_proj, res_dir_date, mdl, dose_str)
res_dir <- file.path(res_dir_proj, res_dir_date, dose_str)

# creates if does not exist and sets working directory
dir.create(res_dir, recursive = TRUE)
dir.create(file.path(res_dir, "tbl_event_count"), recursive = TRUE)
dir.create(file.path(res_dir, "tbl_event_count_redacted"), recursive = TRUE)
dir.create(file.path(res_dir, "median_and_last_event_time"), recursive = TRUE)
dir.create(file.path(res_dir, "tbl_hr"), recursive = TRUE)
dir.create(file.path(res_dir, "rm_leq2"), recursive = TRUE)



setwd(file.path(res_dir))



source(file.path(scripts_dir,"vac_cohort_call_mdl.R"), local=TRUE)


gc()

# ------------- DETERMINE WHICH COMBOS HAVE NOT BEEN COMPLETED -----------------
if (dose_str != "booster") {
  combos <- expand.grid(
  event=ls_events, 
  agegp=c("all"), #agelabels, 
  vac_str= c("vac_az", "vac_pf", "vac_mod"),
  prev_vac_str=NA
  )
} else {
  combos <- expand.grid(
  event=ls_events, 
  agegp=c("all"), # agelabels, 
  prev_vac_str= c("vac_any", "vac_pfmod", "vac_az", "vac_pf"), #"vac_az", "vac_pfmod", "vac_any"
  vac_str=c("vac_pfmod", "vac_pf", "vac_mod")
)
  }
fml <-  "+ weeks + agegroup + sex"
tbl_hr_dir <- file.path(res_dir, "tbl_hr")

haves <- list.files(tbl_hr_dir, pattern = 'tbl_hr_', recursive = TRUE, full.names = FALSE) %>% 
  gsub("_intvl.*","",.)


should_haves <- pmap(list(combos$event, combos$agegp, combos$vac_str, combos$prev_vac_str), 
                     function(event, agegp, vac_str, prev_vac_str){
                       paste0("tbl_hr_" , fml, "_", expo, "_", event, "_agegp", agegp, "_prev", prev_vac_str, "_", vac_str)}
) %>% unlist()

missings <- setdiff(should_haves, haves) # what's in should_haves but not in haves
cat("missings......\n")
# print(missings)


ls_events_missing <- data.frame()
for (i in 1:nrow(combos)) {
  row <- combos[i,]
  fpath <- paste0("tbl_hr_" , fml, "_", expo, "_", row$event, "_agegp", row$agegp, "_prev", row$prev_vac_str, "_", row$vac_str)
  # cat(fpath, "\n")
  if (fpath %in% missings) {
    ls_events_missing <- rbind(ls_events_missing, row)
  }
}


cat("ls_events_missing......\n")
print(ls_events_missing)


# ------------------------------------ LAUNCH JOBS -----------------------------
mclapply(split(ls_events_missing,seq(nrow(ls_events_missing))), mc.cores = 10,
# lapply(split(ls_events_missing[1,],seq(nrow(ls_events_missing[1,]))),
         function(ls_events_missing) {
           print(ls_events_missing)
           tryCatch(get_vacc_res(
             event=ls_events_missing$event,
             prev_vac_str=ls_events_missing$prev_vac_str,
             vac_str=ls_events_missing$vac_str,
             agegp=ls_events_missing$agegp, 
             cohort_vac=cohort_vac, 
             covars=covars
           ), error=function(e) print(e))
           })


haves <- list.files(tbl_hr_dir, pattern = 'tbl_hr_', recursive = TRUE, full.names = FALSE) %>% 
  gsub("_intvl.*","",.)

should_haves <- pmap(list(combos$event, combos$agegp, combos$vac_str, combos$prev_vac_str), 
                     function(event, agegp, vac_str, prev_vac_str){
                       paste0("tbl_hr_" , fml, "_", expo, "_", event, "_agegp", agegp, "_prev", prev_vac_str, "_", vac_str)}
) %>% unlist()

missings <- setdiff(should_haves, haves) # what's in should_haves but not in haves
ls_events_missing <- data.frame()
for (i in 1:nrow(combos)) {
  row <- combos[i,]
  row$dose <- dose_str
  fpath <- paste0("tbl_hr_" , fml, "_", expo, "_", row$event, "_agegp", row$agegp, "_prev", row$prev_vac_str, "_", row$vac_str)
  # cat(fpath, "\n")
  if (fpath %in% missings) {
    row$DONE <- "FALSE"
    ls_events_missing <- rbind(ls_events_missing, row)
  } else {
    row$DONE <- "TRUE"
    ls_events_missing <- rbind(ls_events_missing, row)
  }
}


cat("ls_events_missing......\n")
print(ls_events_missing)

fwrite(ls_events_missing, file.path(res_dir, paste0("completion_", dose_str, ".csv")), row.names=FALSE)

