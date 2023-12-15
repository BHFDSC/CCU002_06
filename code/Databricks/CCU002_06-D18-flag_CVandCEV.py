# Databricks notebook source
# MAGIC %md # CCU002_06-D18
# MAGIC  
# MAGIC **Description** This notebook flags CEV and CV inline with OpenSafely's implementation
# MAGIC
# MAGIC **Last edited** 13/06/23
# MAGIC
# MAGIC **Author(s)** Sam Ip, with thanks to definitions inputs from Venexia and Elsie and codelist importing by Teri!

# COMMAND ----------

# MAGIC %md ## Clear cache

# COMMAND ----------

# MAGIC %sql
# MAGIC CLEAR CACHE

# COMMAND ----------

# MAGIC %md ## Define functions

# COMMAND ----------

def drop_create_table(table_name:str, save2database_name:str='dsa_391419_j3w9t_collab'):
  sql(f"""DROP TABLE IF EXISTS {save2database_name}.{table_name}""")
  sql(f"""CREATE TABLE {save2database_name}.{table_name} AS SELECT * FROM {table_name} """)

# COMMAND ----------

from pyspark.sql.functions import to_date, lit, countDistinct, col, date_add, date_sub
import pyspark.sql.functions as f
from functools import reduce
import pandas as pd
import io

# COMMAND ----------

# MAGIC %md ## Define parameters

# COMMAND ----------

index_date = '2020-12-08'
index_date_lag3mo = '2020-09-08'
previous_year_date = '2019-12-08'
project_prefix='ccu002_06_'
old_collab_database_name='dars_nic_391419_j3w9t_collab'
new_collab_database_name='dsa_391419_j3w9t_collab'

codelist_table='codelists'
gdppr_data = 'gdppr_dars_nic_391419_j3w9t'
hes_apc_data = 'hes_apc_all_years'
pcmeds_data = 'primary_care_meds_dars_nic_391419_j3w9t'

# COMMAND ----------

hes_apc = spark.table(old_collab_database_name + '.' + project_prefix + hes_apc_data)
gdppr = spark.table(old_collab_database_name + '.' + project_prefix + gdppr_data )
pcmeds = spark.table(old_collab_database_name + '.' + project_prefix + pcmeds_data )

# COMMAND ----------

# MAGIC %md # CV

# COMMAND ----------

old_collab_database_name

# COMMAND ----------

sql(f"""CREATE OR REPLACE TEMP VIEW cv_codelist_all AS 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_astadm_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_ast_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_astrx_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_resp_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_cns_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_diab_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_dmres_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_sev_mental_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_smhres_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_chd_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_ckd15_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_ckd35_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_ckd_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_cld_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_immdx_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_immrx_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_spln_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_learndis_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_bmi_stage_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_sev_obesity_primis 
    UNION ALL 
    SELECT * FROM {old_collab_database_name}.ccu002_06_d17_bmi_primis""")

# COMMAND ----------

display(sql("""SELECT COUNT(*) FROM cv_codelist_all"""))

# COMMAND ----------

# MAGIC %md ### Definitions

# COMMAND ----------

# cv_ref_date = to_date(lit("2021-02-15"),'yyyy-MM-dd') # Date eligible 1st vaccination dose for >=16
# cv_ref_date = to_date(lit("2020-12-08"),'yyyy-MM-dd') # Study index date
cv_ref_date = "2020-12-08" # Study index date
cv_ever_start_date = to_date(lit("1900-01-01"),'yyyy-MM-dd')

# COMMAND ----------

# Import clinically_vulnerable CSV
cvCSV_dates_source = """variable,codelist,start_cvrefdateminusXdays,end_cvrefdateminusXdays,flag_type,source
astadm,astadm_primis,730,1,binary,gdppr
ast,ast_primis,NULL,1,binary,gdppr
astrxm1,astrx_primis,31,1,binary,pcmeds
astrxm2,astrx_primis,61,32,binary,pcmeds
astrxm3,astrx_primis,91,62,binary,gdppr
resp,resp_primis,NULL,1,binary,gdppr
cns,cns_primis,NULL,1,binary,gdppr
diab_date,diab_primis,NULL,1,date,gdppr
dmres_date,dmres_primis,NULL,1,date,gdppr
sev_mental_date,sev_mental_primis,NULL,1,date,gdppr
smhres_date,smhres_primis,NULL,1,date,gdppr
chd,chd_primis,NULL,1,binary,gdppr
ckd15_date,ckd15_primis,NULL,1,date,gdppr
ckd35_date,ckd35_primis,NULL,1,date,gdppr
ckd,ckd_primis,NULL,1,binary,gdppr
cld,cld_primis,NULL,1,binary,gdppr
immrx,immrx_primis,NULL,1,binary,pcmeds
immdx,immdx_primis,NULL,1,binary,gdppr
spln,spln_primis,NULL,1,binary,gdppr
learndis,learndis_primis,NULL,1,binary,gdppr
bmi_stage_date,bmi_stage_primis,NULL,1,date,gdppr
sev_obesity_date,sev_obesity_primis,NULL,1,date,gdppr
bmi_date,bmi_primis,NULL,1,date,gdppr
bmi_value_temp,bmi_primis,NULL,1,numeric,gdppr"""

df_cvCSV_dates_source = pd.read_csv(io.StringIO(cvCSV_dates_source), header=0,delimiter=',').astype(str)
df_cvCSV_dates_source = spark.createDataFrame(df_cvCSV_dates_source)
df_cvCSV_dates_source.createOrReplaceTempView("cvCSV_dates_source")

# COMMAND ----------

# https://stackoverflow.com/questions/32284620/how-to-change-a-dataframe-column-from-string-type-to-double-type-in-pyspark
from pyspark.sql.types import DoubleType, DateType, IntegerType

df_cvCSV_dates_source = df_cvCSV_dates_source.withColumn("start_cvrefdateminusXdays",col("start_cvrefdateminusXdays").cast(IntegerType())) \
.withColumn("end_cvrefdateminusXdays",col("end_cvrefdateminusXdays").cast(IntegerType()))
df_cvCSV_dates_source.printSchema()


# COMMAND ----------

# MAGIC %sql select * from cvCSV_dates_source

# COMMAND ----------

df_cvCSV_dates_source = df_cvCSV_dates_source.withColumn('start_date', f.when(f.col("start_cvrefdateminusXdays").isNotNull(), 
                                                                            f.expr(f"date_sub(to_date('{cv_ref_date}', 'yyyy-MM-dd'), start_cvrefdateminusXdays)"))\
                                                                        .otherwise(to_date(lit('1900-01-01'),'yyyy-MM-dd'))
                                                        )\
                                              .withColumn('end_date', f.when(f.col("end_cvrefdateminusXdays").isNotNull(), 
                                                                            f.expr(f"date_sub(to_date('{cv_ref_date}', 'yyyy-MM-dd'), end_cvrefdateminusXdays)").cast(DateType()))
                                                        );
df_cvCSV_dates_source.createOrReplaceTempView("cvCSV_dates_source");

display(df_cvCSV_dates_source)

# COMMAND ----------

# MAGIC %md ##Binary-GDPPR

# COMMAND ----------

vars_binary_gdppr = df_cvCSV_dates_source.where(df_cvCSV_dates_source.flag_type=="binary").where(df_cvCSV_dates_source.source=="gdppr").select("variable").toPandas().values.squeeze();
vars_binary_gdppr

# COMMAND ----------

vars_binary_gdppr = df_cvCSV_dates_source.where(df_cvCSV_dates_source.flag_type=="binary").where(df_cvCSV_dates_source.source=="gdppr").select("variable").toPandas().values.squeeze()

for variable in vars_binary_gdppr:
  # variable = "astrxm1"
  codelist = df_cvCSV_dates_source.where(df_cvCSV_dates_source.variable==variable).select("codelist").toPandas().values[0][0]
  start_date = df_cvCSV_dates_source.where(df_cvCSV_dates_source.variable==variable).select("start_date").toPandas().values[0][0]
  end_date = df_cvCSV_dates_source.where(df_cvCSV_dates_source.variable==variable).select("end_date").toPandas().values[0][0]

  sql(f"""DROP TABLE IF EXISTS {new_collab_database_name}.ccu002_06_cvflag_{variable}""") # newly created tbls -- save to dsa

  sql(f"""
      CREATE TABLE  {new_collab_database_name}.ccu002_06_cvflag_{variable} AS 
      SELECT distinct NHS_NUMBER_DEID, 1 AS {variable}
      FROM {old_collab_database_name + '.' + project_prefix + gdppr_data} 
      WHERE (CODE IN (SELECT code FROM {old_collab_database_name}.ccu002_06_d17_{codelist}) AND
            (RECORD_DATE >= CAST('{start_date}' AS DATE) AND (RECORD_DATE <= CAST('{end_date}' AS DATE))))
      """)  # newly created tbls -- save to dsa, call old tables from dars_nic

# COMMAND ----------

display(sql(f"""DESCRIBE HISTORY {new_collab_database_name}.ccu002_06_cvflag_ast"""))

# COMMAND ----------

# MAGIC %md ##Binary-PCmeds
# MAGIC Returns empty datasets -- but exists in GDPPR

# COMMAND ----------

vars_binary_pcmeds = df_cvCSV_dates_source.where(df_cvCSV_dates_source.flag_type=="binary").where(df_cvCSV_dates_source.source=="pcmeds").select("variable").toPandas().values.squeeze();
vars_binary_pcmeds

# COMMAND ----------

vars_binary_pcmeds = df_cvCSV_dates_source.where(df_cvCSV_dates_source.flag_type=="binary").where(df_cvCSV_dates_source.source=="pcmeds").select("variable").toPandas().values.squeeze()

for variable in vars_binary_pcmeds:
  # variable = "astrxm1"
  codelist = df_cvCSV_dates_source.where(df_cvCSV_dates_source.variable==variable).select("codelist").toPandas().values[0][0]
  start_date = df_cvCSV_dates_source.where(df_cvCSV_dates_source.variable==variable).select("start_date").toPandas().values[0][0]
  end_date = df_cvCSV_dates_source.where(df_cvCSV_dates_source.variable==variable).select("end_date").toPandas().values[0][0]

  sql(f"""DROP TABLE IF EXISTS {new_collab_database_name}.ccu002_06_cvflag_{variable}""")

  sql(f"""
      CREATE TABLE  {new_collab_database_name}.ccu002_06_cvflag_{variable} AS
      SELECT distinct person_id_deid AS NHS_NUMBER_DEID, 1 AS {variable}
      FROM {old_collab_database_name + '.' + project_prefix + pcmeds_data} 
      WHERE (PrescribedBNFCode IN (SELECT code FROM {old_collab_database_name}.ccu002_06_d17_{codelist}) AND
            (ProcessingPeriodDate >= CAST('{start_date}' AS DATE) AND (ProcessingPeriodDate <= CAST('{end_date}' AS DATE))))
      """)

# COMMAND ----------

# MAGIC %md ##Date-GDPPR

# COMMAND ----------

vars_lastdate_gdppr = df_cvCSV_dates_source.where(df_cvCSV_dates_source.flag_type=="date").where(df_cvCSV_dates_source.source=="gdppr").select("variable").toPandas().values.squeeze();
vars_lastdate_gdppr

# COMMAND ----------

vars_lastdate_gdppr = df_cvCSV_dates_source.where(df_cvCSV_dates_source.flag_type=="date").where(df_cvCSV_dates_source.source=="gdppr").select("variable").toPandas().values.squeeze()

for variable in vars_lastdate_gdppr:
  # variable = "astrxm1"
  codelist = df_cvCSV_dates_source.where(df_cvCSV_dates_source.variable==variable).select("codelist").toPandas().values[0][0]
  start_date = df_cvCSV_dates_source.where(df_cvCSV_dates_source.variable==variable).select("start_date").toPandas().values[0][0]
  end_date = df_cvCSV_dates_source.where(df_cvCSV_dates_source.variable==variable).select("end_date").toPandas().values[0][0]

  sql(f"""DROP TABLE IF EXISTS {new_collab_database_name}.ccu002_06_cvflag_{variable}""")

  sql(f"""
      CREATE OR REPLACE TEMP VIEW tmp_cvflag_{variable} AS
      SELECT NHS_NUMBER_DEID, CODE, RECORD_DATE,
              row_number() OVER (PARTITION BY NHS_NUMBER_DEID ORDER BY RECORD_DATE desc) as record_date_rank
      FROM {old_collab_database_name + '.' + project_prefix + gdppr_data} 
      WHERE (CODE IN (SELECT code FROM {old_collab_database_name}.ccu002_06_d17_{codelist}) AND
            (RECORD_DATE >= CAST('{start_date}' AS DATE) AND (RECORD_DATE <= CAST('{end_date}' AS DATE))))
      """)
  
  sql(f"""
      CREATE TABLE  {new_collab_database_name}.ccu002_06_cvflag_{variable} AS
      SELECT NHS_NUMBER_DEID, RECORD_DATE AS {variable}
      FROM tmp_cvflag_{variable} 
      WHERE record_date_rank ==1
      """)

# COMMAND ----------

# MAGIC %md ##Numeric-GDPPR
# MAGIC BMI

# COMMAND ----------

# vars_lastnum_gdppr = df_cvCSV_dates_source.where(df_cvCSV_dates_source.flag_type=="numeric").where(df_cvCSV_dates_source.source=="gdppr").select("variable").toPandas().values.squeeze()

# for variable in vars_lastnum_gdppr:
variable = "bmi_value_temp"
codelist = df_cvCSV_dates_source.where(df_cvCSV_dates_source.variable==variable).select("codelist").toPandas().values[0][0]
start_date = df_cvCSV_dates_source.where(df_cvCSV_dates_source.variable==variable).select("start_date").toPandas().values[0][0]
end_date = df_cvCSV_dates_source.where(df_cvCSV_dates_source.variable==variable).select("end_date").toPandas().values[0][0]

sql(f"""DROP TABLE IF EXISTS {new_collab_database_name}.ccu002_06_cvflag_{variable}""")

sql(f"""
    CREATE OR REPLACE TEMP VIEW tmp_cvflag_{variable} AS
    SELECT NHS_NUMBER_DEID, CODE, RECORD_DATE, VALUE1_CONDITION,
            row_number() OVER (PARTITION BY NHS_NUMBER_DEID ORDER BY RECORD_DATE desc) as record_date_rank
    FROM {old_collab_database_name + '.' + project_prefix + gdppr_data} 
    WHERE (CODE IN (SELECT code FROM {old_collab_database_name}.ccu002_06_d17_{codelist}) AND
          (RECORD_DATE >= CAST('{start_date}' AS DATE) AND (RECORD_DATE <= CAST('{end_date}' AS DATE))))
    """)

sql(f"""
    CREATE OR REPLACE TEMP VIEW tmp2_cvflag_{variable} AS
    SELECT NHS_NUMBER_DEID, RECORD_DATE AS {variable}_date, VALUE1_CONDITION AS {variable}_value, (CASE WHEN VALUE1_CONDITION >= 40 THEN 1 ELSE 0 END) AS {variable}
    FROM tmp_cvflag_{variable} 
    WHERE (record_date_rank ==1) AND
          (VALUE1_CONDITION >= 12) AND (VALUE1_CONDITION <= 75)
    """)

sql(f"""
    CREATE TABLE  {new_collab_database_name}.ccu002_06_cvflag_{variable} AS
    SELECT NHS_NUMBER_DEID, {variable}_date, {variable}_value, {variable}
    FROM tmp2_cvflag_{variable} 
    WHERE ({variable} ==1)
    """)

# COMMAND ----------

# MAGIC %md ## > Full-join all flags

# COMMAND ----------

display(df_cvCSV_dates_source)

# COMMAND ----------

vars_all

# COMMAND ----------

# GDPPR
vars_all = df_cvCSV_dates_source.select("variable").toPandas().values.squeeze()
fpaths_vars_all = f"{new_collab_database_name}.ccu002_06_cvflag_" +vars_all
tbls_vars_all = [spark.read.table(fpath) for fpath in fpaths_vars_all]
tbls_nonempty_vars_all = [table for table in tbls_vars_all if table.count() > 0]

# COMMAND ----------

# # All from PCmeds are empty
# fpaths_vars_all_pcmeds = "dars_nic_391419_j3w9t_collab.ccu002_06_cvflag_" +vars_binary_pcmeds +"_pcmeds"
# tbls_vars_all_pcmeds = [spark.read.table(fpath) for fpath in fpaths_vars_all_pcmeds]
# tbls_nonempty_vars_all_pcmeds = [table for table in tbls_vars_all_pcmeds if table.count() > 0]
# tbls_nonempty_vars_all_pcmeds

# COMMAND ----------

from functools import reduce
tbl_allflags = reduce(lambda df1, df2: df1.join(df2, how='full', on="NHS_NUMBER_DEID"), tbls_nonempty_vars_all)

# COMMAND ----------

display(tbl_allflags)

# COMMAND ----------

# MAGIC %md ## > Define group variables

# COMMAND ----------

#Which columns are 
missing_columns = [col_name for col_name in vars_all if col_name not in tbl_allflags.columns]
missing_columns

# COMMAND ----------

for column_name in missing_columns:
    tbl_allflags = tbl_allflags.withColumn(column_name, lit(None))

tbl_allflags.columns

# COMMAND ----------

# Make Spark table into SQL table
tbl_allflags.createOrReplaceTempView("tbl_allflags")

# COMMAND ----------

sql(f"""DROP TABLE IF EXISTS {new_collab_database_name}.ccu002_06_cvflag_final""")

sql(f"""CREATE TABLE  {new_collab_database_name}.ccu002_06_cvflag_final AS
SELECT *, 
      (CASE WHEN (astadm==1 OR (ast==1 AND astrxm1==1 AND astrxm2==1 AND astrxm3==1)) THEN 1 ELSE 0 END) AS asthma_group,
      (CASE WHEN resp==1 THEN 1 ELSE 0 END) AS resp_group,
      (CASE WHEN cns==1 THEN 1 ELSE 0 END) AS cns_group,
      (CASE WHEN (dmres_date IS NULL AND diab_date IS NOT NULL) OR (dmres_date < diab_date) THEN 1 ELSE 0 END) AS diab_group,
      (CASE WHEN (smhres_date IS NULL AND sev_mental_date iS NOT NULL) OR smhres_date < sev_mental_date THEN 1 ELSE 0 END) AS sevment_group,
      (CASE WHEN chd==1 THEN 1 ELSE 0 END) AS chd_group,
      (CASE WHEN ckd==1 OR (ckd15_date IS NOT NULL AND ckd35_date IS NOT NULL AND (ckd35_date >= ckd15_date)) OR (ckd35_date IS NOT NULL AND ckd15_date IS NULL) THEN 1 ELSE 0 END) AS ckd_group,
      (CASE WHEN cld==1 THEN 1 ELSE 0 END) AS cld_group,
      (CASE WHEN immrx==1 OR immdx==1 THEN 1 ELSE 0 END) AS immuno_group,
      (CASE WHEN spln==1 THEN 1 ELSE 0 END) AS spln_group,
      (CASE WHEN learndis==1 THEN 1 ELSE 0 END) AS learndis_group,
      (CASE WHEN (sev_obesity_date IS NOT NULL AND bmi_date IS NULL) OR (sev_obesity_date > bmi_date) OR bmi_value_temp==1 THEN 1 ELSE 0 END) AS sevobese_group
FROM tbl_allflags
""")

display(f"{new_collab_database_name}.ccu002_06_cvflag_final")

# COMMAND ----------

sql(f""" DROP TABLE IF EXISTS {new_collab_database_name}.ccu002_06_cvflag_final_onlyflagged_20201208""")

sql(f"""CREATE TABLE  {new_collab_database_name}.ccu002_06_cvflag_final_onlyflagged_20201208 AS
select NHS_NUMBER_DEID,asthma_group,resp_group,cns_group,diab_group,sevment_group,chd_group,ckd_group,cld_group,immuno_group,spln_group,learndis_group,sevobese_group
from {new_collab_database_name}.ccu002_06_cvflag_final
where asthma_group==1 or resp_group==1 or cns_group==1 or diab_group==1 or sevment_group==1 or chd_group==1 or ckd_group==1 or cld_group==1 or immuno_group==1 or spln_group==1 or learndis_group==1 or sevobese_group==1
""")

# COMMAND ----------

# MAGIC %md #CEV

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Get healthcare worker codes
# MAGIC SELECT
# MAGIC   ConceptId AS code,
# MAGIC   ConceptId_Description AS term,
# MAGIC   'SNOMED' AS system,
# MAGIC   'hcw' AS codelist
# MAGIC FROM
# MAGIC   dss_corporate.gdppr_cluster_refset
# MAGIC WHERE
# MAGIC   Cluster_ID = 'HCW_COD'

# COMMAND ----------

from pyspark.sql.functions import col, lit, when
import pyspark.sql.functions as F
import pandas as pd
cond_cev = (col("CODE")=="1300561000000107")
cond_beforeidxdate = to_date(col("RECORD_DATE"))<to_date(lit("2020-12-08"),'yyyy-MM-dd')

gdppr_cev = gdppr.select(["NHS_NUMBER_DEID", "RECORD_DATE", "CODE"]).withColumn("flag_CEV", when((cond_cev & cond_beforeidxdate), 1).otherwise(0)).dropDuplicates()

# COMMAND ----------

savename_cev = f"ccu002_06_cov_dose1_cev_{cv_ref_date}".replace("-", "")
gdppr_cev.where(col("flag_CEV") == 1).createOrReplaceTempView(savename_cev)

# COMMAND ----------

display(sql(f"""select * from {savename_cev}"""))

# COMMAND ----------

drop_create_table(table_name=savename_cev, save2database_name=new_collab_database_name)

# COMMAND ----------

display(sql(f"describe history {new_collab_database_name}.{savename_cev}"))

# COMMAND ----------

# MAGIC %md # END ----
