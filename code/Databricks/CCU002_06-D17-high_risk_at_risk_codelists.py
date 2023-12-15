# Databricks notebook source
# MAGIC %md # CCU002_06-D17-high_risk_at_risk_codelists
# MAGIC
# MAGIC **Description** This notebook adds, for the CCU002_06 project, codelists to identify high risk and at risk individuals.
# MAGIC
# MAGIC **Last edited** 23/05/23
# MAGIC
# MAGIC **Authors** Teri North
# MAGIC
# MAGIC **Notes** The "at risk" codes were obtained from here https://github.com/opensafely/covid-ve-change-over-time/tree/define-covs-at-svp/codelists.
# MAGIC The "high risk" code can be obtained from here (not currently listed below) 
# MAGIC https://www.opencodelists.org/codelist/primis-covid19-vacc-uptake/shield/v.1.5.3/#full-list

# COMMAND ----------

# MAGIC %md ## Clear cache

# COMMAND ----------

# MAGIC %sql
# MAGIC CLEAR CACHE

# COMMAND ----------

# MAGIC %md ## Define functions

# COMMAND ----------

# Define create table function by Sam Hollings
# Source: Workspaces/dars_nic_391419_j3w9t_collab/DATA_CURATION_wrang000_functions

def create_table(table_name:str, database_name:str='dars_nic_391419_j3w9t_collab', select_sql_script:str=None) -> None:
  """Will save to table from a global_temp view of the same name as the supplied table name (if no SQL script is supplied)
  Otherwise, can supply a SQL script and this will be used to make the table with the specificed name, in the specifcied database."""
  
  spark.conf.set("spark.sql.legacy.allowCreatingManagedTableUsingNonemptyLocation","true")
  
  if select_sql_script is None:
    select_sql_script = f"SELECT * FROM global_temp.{table_name}"
  
  spark.sql(f"""CREATE TABLE {database_name}.{table_name} AS
                {select_sql_script}
             """)
  spark.sql(f"ALTER TABLE {database_name}.{table_name} OWNER TO {database_name}")
  
def drop_table(table_name:str, database_name:str='dars_nic_391419_j3w9t_collab', if_exists=True):
  if if_exists:
    IF_EXISTS = 'IF EXISTS'
  else: 
    IF_EXISTS = ''
  spark.sql(f"DROP TABLE {IF_EXISTS} {database_name}.{table_name}")

# COMMAND ----------

# MAGIC %md ## Import functions

# COMMAND ----------

import pandas as pd
import io

# COMMAND ----------

# MAGIC %md ## "At risk" codelists obtained from https://github.com/opensafely/covid-ve-change-over-time/tree/define-covs-at-svp/codelists

# COMMAND ----------

# MAGIC %md ## astadm_primis

# COMMAND ----------

c1 = """code,term
183478001,Emergency hospital admission for asthma
708358003,Emergency asthma admission since last encounter"""

c1_df = pd.read_csv(io.StringIO(c1), header=0,delimiter=',').astype(str)
spark.createDataFrame(c1_df).createOrReplaceGlobalTempView("ccu002_06_d17_astadm_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_astadm_primis

# COMMAND ----------

# MAGIC %md ## ast_primis

# COMMAND ----------

c2 = """code,term
103781000119103,Allergic bronchopulmonary mycosis
10674711000119105,Acute severe exacerbation of asthma co-occurrent with allergic rhinitis
10674991000119104,Intermittent allergic asthma
10675391000119101,Severe controlled persistent asthma
10675431000119106,Severe persistent allergic asthma
10675471000119109,Acute severe exacerbation of severe persistent allergic asthma
10675551000119104,Acute severe exacerbation of severe persistent asthma co-occurrent with allergic rhinitis
10675751000119107,Severe uncontrolled persistent asthma
10675871000119106,Mild persistent allergic asthma
10675911000119109,Acute severe exacerbation of mild persistent allergic asthma
10675991000119100,Acute severe exacerbation of mild persistent allergic asthma co-occurrent with allergic rhinitis
10676391000119108,Moderate persistent allergic asthma
10676431000119103,Acute severe exacerbation of moderate persistent allergic asthma
10676511000119109,Acute severe exacerbation of moderate persistent asthma co-occurrent with allergic rhinitis
10692681000119108,Aspirin exacerbated respiratory disease
10692721000119102,Chronic obstructive asthma co-occurrent with acute exacerbation of asthma
10692761000119107,Asthma-chronic obstructive pulmonary disease overlap syndrome
10742121000119104,Asthma in mother complicating childbirth
1086701000000102,Life threatening acute exacerbation of allergic asthma
1086711000000100,Life threatening acute exacerbation of intrinsic asthma
1103911000000103,Severe asthma with fungal sensitisation
11641008,Millers' asthma
12428000,Intrinsic asthma without status asthmaticus
124991000119109,Severe persistent asthma co-occurrent with allergic rhinitis
125001000119103,Moderate persistent asthma co-occurrent with allergic rhinitis
125011000119100,Mild persistent asthma co-occurrent with allergic rhinitis
125021000119107,Intermittent asthma co-occurrent with allergic rhinitis
135171000119106,Acute exacerbation of moderate persistent asthma
135181000119109,Acute exacerbation of mild persistent asthma
16584951000119101,Oral steroid-dependent asthma
1741000119102,Intermittent asthma uncontrolled
1751000119100,Acute exacerbation of chronic obstructive airways disease with asthma
18041002,Printers' asthma
195949008,Chronic asthmatic bronchitis
195967001,Asthma
195977004,Mixed asthma
19849005,Meat-wrappers' asthma
225057002,Brittle asthma
233678006,Childhood asthma
233679003,Late onset asthma
233683003,Hay fever with asthma
233687002,Colophony asthma
233688007,Sulfite-induced asthma
2360001000004109,Steroid dependent asthma
266361008,Non-allergic asthma
281239006,Exacerbation of asthma
304527002,Acute asthma
31387002,Exercise-induced asthma
34015007,Bakers' asthma
370218001,Mild asthma
370219009,Moderate asthma
370220003,Occasional asthma
370221004,Severe asthma
37981002,Allergic bronchopulmonary aspergillosis
389145006,Allergic asthma
401000119107,Asthma with irreversible airway obstruction
404804003,Platinum asthma
404806001,Cheese-makers' asthma
404808000,Isocyanate induced asthma
405944004,Asthmatic bronchitis
407674008,Aspirin-induced asthma
409663006,Cough variant asthma
41553006,Detergent asthma
418395004,Tea-makers' asthma
423889005,Non-immunoglobulin E mediated allergic asthma
424199006,Substance induced asthma
424643009,Immunoglobulin E-mediated allergic asthma
425969006,Exacerbation of intermittent asthma
426656000,Severe persistent asthma
426979002,Mild persistent asthma
427295004,Moderate persistent asthma
427603009,Intermittent asthma
427679007,Mild intermittent asthma
442025000,Acute exacerbation of chronic asthmatic bronchitis
445427006,Seasonal asthma
55570000,Asthma without status asthmaticus
56968009,Asthma caused by wood dust
57607007,Occupational asthma
59786004,Weavers' cough
63088003,Allergic asthma without status asthmaticus
703953004,Allergic asthma caused by Dermatophagoides pteronyssinus
703954005,Allergic asthma caused by Dermatophagoides farinae
707444001,Uncomplicated asthma
707445000,Exacerbation of mild persistent asthma
707446004,Exacerbation of moderate persistent asthma
707447008,Exacerbation of severe persistent asthma
707511009,Uncomplicated mild persistent asthma
707512002,Uncomplicated moderate persistent asthma
707513007,Uncomplicated severe persistent asthma
707979007,Acute severe exacerbation of severe persistent asthma
707980005,Acute severe exacerbation of moderate persistent asthma
707981009,Acute severe exacerbation of mild persistent asthma
708038006,Acute exacerbation of asthma
708090002,Acute severe exacerbation of asthma
708093000,Acute exacerbation of immunoglobulin E-mediated allergic asthma
708094006,Acute exacerbation of intrinsic asthma
708095007,Acute severe exacerbation of immunoglobin E-mediated allergic asthma
708096008,Acute severe exacerbation of intrinsic asthma
72301000119103,Asthma in pregnancy
733858005,Acute severe refractory exacerbation of asthma
734904007,Life threatening acute exacerbation of asthma
734905008,Moderate acute exacerbation of asthma
735588005,Uncomplicated allergic asthma
735589002,Uncomplicated non-allergic asthma
762521001,Exacerbation of allergic asthma
782513000,Acute severe exacerbation of allergic asthma
782520007,Exacerbation of allergic asthma due to infection
786836003,Near fatal asthma
829976001,Thunderstorm asthma
866881000000101,Chronic asthma with fixed airflow obstruction
92807009,Chemical-induced asthma
93432008,Drug-induced asthma
99031000119107,Acute exacerbation of asthma co-occurrent with allergic rhinitis"""

c2_df = pd.read_csv(io.StringIO(c2), header=0,delimiter=',').astype(str)
spark.createDataFrame(c2_df).createOrReplaceGlobalTempView("ccu002_06_d17_ast_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_ast_primis

# COMMAND ----------

# MAGIC %md ## astrx_primis

# COMMAND ----------

c3 = """code,term
10409611000001103,Prednisolone 1mg tablets (Arrow Generics Ltd) (product)
10410111000001103,Prednisolone 5mg tablets (Arrow Generics Ltd) (product)
110811000001100,Prednisolone 5mg tablets (Approved Prescription Services) (product)
13053211000001103,Prednisolone 1.5mg/5ml oral suspension (Special Order) (product)
13053711000001105,Prednisolone 1.5mg/5ml oral solution (Special Order) (product)
13054411000001101,Prednisolone 10mg/5ml oral suspension (Special Order) (product)
13054711000001107,Prednisolone 10mg/5ml oral solution (Special Order) (product)
13055311000001107,Prednisolone 15mg/5ml oral suspension (Special Order) (product)
13055911000001108,Prednisolone 15mg/5ml oral solution (Special Order) (product)
13056211000001105,Prednisolone 1mg/5ml oral suspension (Special Order) (product)
13056511000001108,Prednisolone 1mg/5ml oral solution (Special Order) (product)
13056811000001106,Prednisolone 2.5mg/5ml oral suspension (Special Order) (product)
13057411000001106,Prednisolone 2.5mg/5ml oral solution (Special Order) (product)
13058011000001101,Prednisolone 20mg/5ml oral suspension (Special Order) (product)
13058311000001103,Prednisolone 20mg/5ml oral solution (Special Order) (product)
13058611000001108,Prednisolone 25mg/5ml oral suspension (Special Order) (product)
13058911000001102,Prednisolone 25mg/5ml oral solution (Special Order) (product)
13078311000001101,Prednisolone 1.5mg/5ml oral solution (product)
13078411000001108,Prednisolone 1.5mg/5ml oral suspension (product)
13078511000001107,Prednisolone 10mg/5ml oral solution (product)
13078611000001106,Prednisolone 10mg/5ml oral suspension (product)
13078711000001102,Prednisolone 15mg/5ml oral solution (product)
13078811000001105,Prednisolone 15mg/5ml oral suspension (product)
13078911000001100,Prednisolone 1mg/5ml oral solution (product)
13079011000001109,Prednisolone 1mg/5ml oral suspension (product)
13079111000001105,Prednisolone 2.5mg/5ml oral solution (product)
13079211000001104,Prednisolone 2.5mg/5ml oral suspension (product)
13079311000001107,Prednisolone 20mg/5ml oral solution (product)
13079411000001100,Prednisolone 20mg/5ml oral suspension (product)
13079511000001101,Prednisolone 25mg/5ml oral solution (product)
13079611000001102,Prednisolone 25mg/5ml oral suspension (product)
13120111000001109,Prednisolone 5mg/5ml oral suspension (Special Order) (product)
13120411000001104,Prednisolone 5mg/5ml oral solution (Special Order) (product)
13133111000001100,Prednisolone 5mg/5ml oral solution (product)
13133211000001106,Prednisolone 5mg/5ml oral suspension (product)
13245311000001104,Prednisolone 1mg tablets (Dowelhurst Ltd) (product)
13245511000001105,Prednisolone 5mg tablets (Dowelhurst Ltd) (product)
13245711000001100,Prednisolone 2.5mg gastro-resistant tablets (Dowelhurst Ltd) (product)
13245911000001103,Prednisolone 5mg gastro-resistant tablets (Dowelhurst Ltd) (product)
14173111000001101,Prednisolone 1.67mg/5ml oral solution (Special Order) (product)
14173511000001105,Prednisolone 1.67mg/5ml oral suspension (Special Order) (product)
14204411000001101,Prednisolone 1.67mg/5ml oral solution (product)
14204511000001102,Prednisolone 1.67mg/5ml oral suspension (product)
14786411000001103,Prednisolone 1mg tablets (LPC Medical (UK) Ltd) (product)
14786811000001101,Prednisolone 5mg tablets (LPC Medical (UK) Ltd) (product)
15172311000001102,Prednisolone 5mg soluble tablets (Sigma Pharmaceuticals Plc) (product)
15175511000001102,Prednisolone 1mg tablets (Sigma Pharmaceuticals Plc) (product)
15175711000001107,Prednisolone 2.5mg gastro-resistant tablets (Sigma Pharmaceuticals Plc) (product)
15176111000001100,Prednisolone 5mg gastro-resistant tablets (Sigma Pharmaceuticals Plc) (product)
157711000001100,Prednisolone 5mg soluble tablets (Unichem Plc) (product)
17916411000001100,Prednisolone 2.5mg gastro-resistant tablets (Phoenix Healthcare Distribution Ltd) (product)
17916811000001103,Prednisolone 5mg gastro-resistant tablets (Phoenix Healthcare Distribution Ltd) (product)
17917211000001102,Prednisolone 25mg tablets (Phoenix Healthcare Distribution Ltd) (product)
17999311000001104,Prednisolone 2.5mg gastro-resistant tablets (Phoenix Labs Ltd) (product)
17999611000001109,Prednisolone 5mg gastro-resistant tablets (Phoenix Labs Ltd) (product)
18285011000001109,Prednisolone 1mg tablets (Co-Pharma Ltd) (product)
18285211000001104,Prednisolone 5mg tablets (Co-Pharma Ltd) (product)
18307011000001109,Prednisolone 2.5mg gastro-resistant tablets (Teva UK Ltd) (product)
18307211000001104,Prednisolone 5mg gastro-resistant tablets (Teva UK Ltd) (product)
18625211000001107,Prednisolone 5mg tablets (Phoenix Healthcare Distribution Ltd) (product)
19743011000001109,Prednisolone 2.5mg gastro-resistant tablets (Almus Pharmaceuticals Ltd) (product)
19743211000001104,Prednisolone 5mg gastro-resistant tablets (Almus Pharmaceuticals Ltd) (product)
21851211000001107,Prednisolone 1mg tablets (Waymade Healthcare Plc) (product)
21851411000001106,Prednisolone 5mg tablets (Waymade Healthcare Plc) (product)
22452711000001102,Prednisolone 2.5mg gastro-resistant tablets (Waymade Healthcare Plc) (product)
22453011000001108,Prednisolone 5mg gastro-resistant tablets (Waymade Healthcare Plc) (product)
238511000001107,Prednisolone 1mg tablets (Approved Prescription Services) (product)
245011000001108,Prednisolone 5mg soluble tablets (A A H Pharmaceuticals Ltd) (product)
255211000001101,Prednisolone 5mg gastro-resistant tablets (Unichem Plc) (product)
28808411000001103,Prednisolone 10mg tablets (product)
28808611000001100,Prednisolone 2.5mg tablets (product)
28808711000001109,Prednisolone 20mg tablets (product)
28937511000001104,Prednisolone 5mg soluble tablets (Focus Pharmaceuticals Ltd) (product)
28995411000001102,Prednisolone 1mg/ml oral solution (Logixx Pharma Solutions Ltd) (product)
29361211000001105,Prednisolone 5mg/5ml oral solution unit dose (Logixx Pharma Solutions Ltd) (product)
29424511000001109,Prednisolone 5mg/5ml oral solution unit dose (product)
29559211000001100,Prednisolone 5mg/5ml oral solution unit dose (A A H Pharmaceuticals Ltd) (product)
29879111000001105,Prednisolone 10mg/ml oral solution sugar free (Focus Pharmaceuticals Ltd) (product)
29904211000001102,Prednisolone 10mg/ml oral solution sugar free (product)
30114011000001105,Prednisolone 2.5mg gastro-resistant tablets (DE Pharmaceuticals) (product)
30114311000001108,Prednisolone 5mg gastro-resistant tablets (DE Pharmaceuticals) (product)
30114611000001103,Prednisolone 5mg soluble tablets (DE Pharmaceuticals) (product)
30114811000001104,Prednisolone 1mg tablets (DE Pharmaceuticals) (product)
30115011000001109,Prednisolone 5mg tablets (DE Pharmaceuticals) (product)
30129111000001103,Prednisolone 10mg/ml oral solution sugar free (A A H Pharmaceuticals Ltd) (product)
30858911000001100,Prednisolone 1mg tablets (Mawdsley-Brooks & Company Ltd) (product)
30859111000001105,Prednisolone 5mg tablets (Mawdsley-Brooks & Company Ltd) (product)
30991311000001108,Prednisolone 25mg tablets (Accord Healthcare Ltd) (product)
31386211000001109,Prednisolone Dompe 5mg/5ml oral solution unit dose (Logixx Pharma Solutions Ltd) (product)
313911000001107,Prednisolone 25mg tablets (Unichem Plc) (product)
325426006,Product containing precisely prednisolone 1 milligram/1 each conventional release oral tablet (clinical drug)
325427002,Product containing precisely prednisolone 5 milligram/1 each conventional release oral tablet (clinical drug)
325442004,Product containing precisely prednisolone 2.5 milligram/1 each gastro-resistant oral tablet (clinical drug)
325443009,Product containing precisely prednisolone 5 milligram/1 each gastro-resistant oral tablet (clinical drug)
325444003,Prednisolone 5mg soluble tablet (product)
325445002,Product containing precisely prednisolone 50 milligram/1 each conventional release oral tablet (clinical drug)
325450008,Product containing precisely prednisolone 25 milligram/1 each conventional release oral tablet (clinical drug)
32584711000001105,Prednisolone 1mg gastro-resistant tablets (Phoenix Labs Ltd) (product)
32611811000001105,Prednisolone 1mg gastro-resistant tablets (product)
32688311000001106,Prednisolone 5mg/5ml oral solution unit dose (Alliance Healthcare (Distribution) Ltd) (product)
32771211000001106,Prednisolone 10mg tablets (Accord Healthcare Ltd) (product)
32772911000001108,Prednisolone 2.5mg tablets (Accord Healthcare Ltd) (product)
32773211000001105,Prednisolone 20mg tablets (Accord Healthcare Ltd) (product)
32774411000001107,Prednisolone 30mg tablets (Actavis UK Ltd) (product)
32776111000001109,Prednisolone 2.5mg tablets (A A H Pharmaceuticals Ltd) (product)
32776311000001106,Prednisolone 10mg tablets (A A H Pharmaceuticals Ltd) (product)
32776511000001100,Prednisolone 20mg tablets (A A H Pharmaceuticals Ltd) (product)
32776711000001105,Prednisolone 30mg tablets (A A H Pharmaceuticals Ltd) (product)
32781411000001102,Prednisolone 30mg tablets (product)
32807911000001101,Prednisolone 1mg tablets (Genesis Pharmaceuticals Ltd) (product)
32808311000001101,Prednisolone 5mg tablets (Genesis Pharmaceuticals Ltd) (product)
33425811000001105,Prednisolone 1mg gastro-resistant tablets (A A H Pharmaceuticals Ltd) (product)
33428411000001103,Prednisolone 1mg gastro-resistant tablets (Alliance Healthcare (Distribution) Ltd) (product)
34035411000001102,Prednisolone 5mg soluble tablets (Actavis UK Ltd) (product)
34172711000001106,Prednisolone 5mg soluble tablets (Phoenix Labs Ltd) (product)
34444511000001106,Prednisolone 5mg gastro-resistant tablets (Bristol Laboratories Ltd) (product)
350611000001104,Prednisolone 5mg tablets (Kent Pharmaceuticals Ltd) (product)
36568211000001107,Prednisolone 2.5mg gastro-resistant tablets (Bristol Laboratories Ltd) (product)
37130011000001104,Prednisolone 1mg gastro-resistant tablets (Mawdsley-Brooks & Company Ltd) (product)
37130211000001109,Prednisolone 2.5mg gastro-resistant tablets (Mawdsley-Brooks & Company Ltd) (product)
37130611000001106,Prednisolone 5mg gastro-resistant tablets (Mawdsley-Brooks & Company Ltd) (product)
37131011000001108,Prednisolone 25mg tablets (Mawdsley-Brooks & Company Ltd) (product)
37727411000001103,Prednisolone 5mg soluble tablets (Pilsco Ltd) (product)
37778311000001107,Prednisolone 1mg gastro-resistant tablets (DE Pharmaceuticals) (product)
37778511000001101,Prednisolone 10mg/ml oral solution sugar free (DE Pharmaceuticals) (product)
37778711000001106,Prednisolone 25mg tablets (DE Pharmaceuticals) (product)
37941611000001100,Prednisolone 10mg/ml oral solution sugar free (Alliance Healthcare (Distribution) Ltd) (product)
380011000001100,Prednisolone 2.5mg gastro-resistant tablets (Accord Healthcare Ltd) (product)
38721711000001107,Prednisolone 5mg tablets (NorthStar Healthcare Unlimited Company) (product)
392511000001108,Prednisolone 5mg soluble tablets (Sovereign Medical) (product)
416533002,Product containing precisely prednisolone 3 milligram/1 milliliter conventional release oral solution (clinical drug)
4208511000001105,Prednisolone 2.5mg gastro-resistant tablets (Approved Prescription Services) (product)
4208911000001103,Prednisolone 5mg gastro-resistant tablets (Approved Prescription Services) (product)
429995001,Product containing precisely prednisolone 2 milligram/1 milliliter conventional release oral solution (clinical drug)
432224007,Product containing precisely prednisolone 1 milligram/1 milliliter conventional release oral suspension (clinical drug)
432225008,Product containing precisely prednisolone 3 milligram/1 milliliter conventional release oral suspension (clinical drug)
447211000001105,Prednisolone 5mg gastro-resistant tablets (Kent Pharmaceuticals Ltd) (product)
4752611000001107,Prednisolone 50mg tablets (A A H Pharmaceuticals Ltd) (product)
4752811000001106,Prednisolone 50mg tablets (Approved Prescription Services) (product)
4852811000001108,Prednisolone 25mg tablets (Beacon Pharmaceuticals Ltd) (product)
512811000001108,Prednisolone 5mg gastro-resistant tablets (Accord Healthcare Ltd) (product)
52911000001107,Prednisolone 1mg tablets (Unichem Plc) (product)
646211000001106,Prednisolone 1mg tablets (Accord Healthcare Ltd) (product)
649711000001109,Prednisolone 1mg tablets (A A H Pharmaceuticals Ltd) (product)
662011000001105,Prednisolone 5mg gastro-resistant tablets (A A H Pharmaceuticals Ltd) (product)
685311000001104,Prednisolone 2.5mg gastro-resistant tablets (Kent Pharmaceuticals Ltd) (product)
707911000001100,Prednisolone 1mg tablets (Kent Pharmaceuticals Ltd) (product)
716111000001103,Prednisolone 25mg tablets (A A H Pharmaceuticals Ltd) (product)
772111000001107,Prednisolone 5mg tablets (Unichem Plc) (product)
779211000001109,Prednisolone 2.5mg gastro-resistant tablets (Unichem Plc) (product)
798611000001108,Prednisolone 1mg tablets (The Boots Company) (product)
844111000001103,Prednisolone 1mg tablets (C P Pharmaceuticals Ltd) (product)
85511000001101,Prednisolone 5mg tablets (Alpharma Limited) (product)
858811000001104,Prednisolone 2.5mg gastro-resistant tablets (A A H Pharmaceuticals Ltd) (product)
8651111000001103,Prednisolone 2mg/5ml oral suspension (Special Order) (product)
86711000001103,Prednisolone 5mg tablets (The Boots Company) (product)
8672011000001109,Prednisolone 2mg/5ml oral suspension (product)
876911000001107,Prednisolone 5mg tablets (A A H Pharmaceuticals Ltd) (product)
940311000001100,Prednisolone 5mg tablets (C P Pharmaceuticals Ltd) (product)
9807711000001108,Prednisolone 1mg tablets (Almus Pharmaceutical Ltd) (product)
9807911000001105,Prednisolone 5mg tablets (Almus Pharmaceutical Ltd) (product)"""

c3_df = pd.read_csv(io.StringIO(c3), header=0,delimiter=',').astype(str)
spark.createDataFrame(c3_df).createOrReplaceGlobalTempView("ccu002_06_d17_astrx_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_astrx_primis

# COMMAND ----------

# MAGIC %md ## resp_primis

# COMMAND ----------

c4 = """code,term
10041001,Tracheal stenosis following tracheostomy
102361000119104,Chronic pneumonia
103851000119100,Restrictive lung disease due to amyotrophic lateral sclerosis
103871000119109,Restrictive lung disease due to Parkinson disease
10501004,Pulmonary alveolar proteinosis
10713006,Diffuse interstitial rheumatoid disease of lung
10785007,Vinyard sprayers' lung
1078881000119102,Primary adenocarcinoma of lower lobe of left lung
1078901000119100,Primary adenocarcinoma of upper lobe of left lung
1078931000119107,Primary adenocarcinoma of lower lobe of right lung
1078961000119104,Primary adenocarcinoma of upper lobe of right lung
109371002,Overlapping malignant neoplasm of bronchus and lung
109390005,Kaposi's sarcoma of lung
111292008,Necrotizing sarcoid granulomatosis
111901001,Bronchocentric granulomatosis
11296007,Stenosis of trachea
115666004,Animal handlers' lung
11944003,Feather-pickers' disease
12070002,Congenital stenosis of larynx
12088005,Budgerigar-fanciers' disease
12181002,Tropical pulmonary alveolitis
12240951000119107,Squamous cell carcinoma of left lung
12240991000119102,Squamous cell carcinoma of right lung
12295008,Bronchiectasis
123713005,Chronic atelectasis
1259003,Schistosis
129451001,Respiratory bronchiolitis associated interstitial lung disease
129452008,Nonspecific interstitial pneumonia
13151001,Flax-dressers' disease
13217005,Fusiform bronchiectasis
13274008,Atrophic fibrosis of lung
13394002,Suberosis
133971000119108,Chronic pulmonary embolism
13645005,Chronic obstructive lung disease
146081000119104,Lung disease due to connective tissue disorder
14700006,Bauxite fibrosis of lung
152921000119101,Dependence on respiratory device
154283005,Pulmonary tuberculosis
15956181000119102,Secondary adenocarcinoma of bilateral lungs
15956341000119105,Adenocarcinoma of left lung
15956381000119100,Adenocarcinoma of right lung
161672008,History of being lung transplant recipient
162974009,On examination - fibrosis of lung present
16419651000119103,Dependence on biphasic positive airway pressure ventilation due to central sleep apnea syndrome
1661000119106,Metastasis to lung from adenocarcinoma
16623004,Coffee-workers' lung
17097001,Chronic disease of respiratory system
17385007,Graphite fibrosis of lung
174802006,Allotransplant of heart and lung
17996008,Pneumoconiosis caused by inorganic dust
18354001,Chronic induration of lung
186175002,Infiltrative lung tuberculosis
186177005,Tuberculosis of lung with cavitation
186193001,"Tuberculosis of lung, confirmed by sputum microscopy with or without culture"
186194007,"Tuberculosis of lung, confirmed by culture only"
186195008,"Tuberculosis of lung, confirmed histologically"
186203002,"Tuberculosis of lung, bacteriologically and histologically negative"
186204008,"Tuberculosis of lung, bacteriological and histological examination not done"
18690003,Farmers' lung
187233002,Sarcoidosis of lung with sarcoidosis of lymph nodes
187862007,Malignant neoplasm of upper lobe of lung
187864008,"Malignant neoplasm of middle lobe, bronchus or lung"
187865009,Malignant neoplasm of middle lobe bronchus
187866005,Malignant neoplasm of middle lobe of lung
187870002,Malignant neoplasm of lower lobe of lung
189262006,Carcinoma in situ of bronchus and lung
189265008,Carcinoma in situ of upper lobe bronchus and lung
189266009,Carcinoma in situ of middle lobe bronchus and lung
189267000,Carcinoma in situ of lower lobe bronchus and lung
189815007,Pulmonary blastoma
19076009,Sick building syndrome
190905008,Cystic fibrosis
190966007,Extreme obesity with alveolar hypoventilation
192658007,Giant cell interstitial pneumonitis
19274004,Grain-handlers' disease
195985008,Post-infective bronchiectasis
195989002,Pituitary snuff-takers' disease
196017002,Pneumoconiosis associated with tuberculosis
196028003,Chronic pulmonary fibrosis caused by chemical fumes
196049002,Chronic pulmonary radiation disease
196051003,Drug-induced interstitial lung disorder
196053000,Chronic drug-induced interstitial lung disorders
196115007,Pulmonary congestion and hypostasis
196116008,Pulmonary hypostasis
196124003,Alveolar capillary block
196125002,Diffuse interstitial pulmonary fibrosis
196190001,Chronic pulmonary insufficiency following surgery
196191002,Postprocedural subglottic stenosis
197367007,Hepatic granulomas in berylliosis
204550009,"Congenital stenosis of larynx, trachea and bronchus"
204551008,Congenital bronchial stenosis
204552001,Congenital subglottic stenosis
204553006,Congenital supraglottic stenosis
213152006,Heart-lung transplant failure and rejection
22607003,Asbestosis
22668006,Subglottic stenosis
23022004,Tuberculous bronchiectasis
230494007,Alveolar sleep apnea
232440009,Acquired laryngeal stenosis
232657004,Single lung transplant
232658009,Double lung transplant
232659001,Double lung transplant as a block
232660006,Bilateral sequential single lung transplant
23315001,Sequoiosis
233615002,Chronic pulmonary coccidioidomycosis
233623000,Mononuclear interstitial pneumonia
233627004,Congenital cystic bronchiectasis
233628009,Acquired bronchiectasis
233629001,Idiopathic bronchiectasis
233634002,Post-lung transplantation bronchiectasis
233659006,Asbestos-induced pleural plaque
233672007,Byssinosis grade 3
233694004,Dog house disease
233695003,Dry rot lung
233696002,Lycoperdonosis
233697006,New Guinea lung
233698001,Paprika splitters' lung
233699009,Pyrethrum alveolitis
233700005,Rodent handlers' lung
233701009,Sewage workers' lung
233702002,Summer-type hypersensitivity pneumonitis
233703007,Interstitial lung disease
233716007,Micronodular pulmonary ossification
233717003,Diffuse pulmonary neurofibromatosis
233718008,Pulmonary tuberous sclerosis
233724002,Toxic diffuse interstitial pulmonary fibrosis
233725001,Drug-induced diffuse interstitial pulmonary fibrosis
233726000,Localized pulmonary fibrosis
233737004,Familial fibrous mediastinitis
233744008,Hilar lymph node sarcoidosis
233748006,Simple pneumoconiosis
233749003,Complicated pneumoconiosis
233750003,Erionite pneumoconiosis
233751004,Metal pneumoconiosis
233753001,Subacute berylliosis
233754007,Cerium pneumoconiosis
233755008,Nickel pneumoconiosis
233756009,Thorium pneumoconiosis
233757000,Zirconium pneumoconiosis
233758005,Mica pneumoconiosis
233759002,Mixed mineral dust pneumoconiosis
233760007,Acute silicosis
233761006,Subacute silicosis
233762004,Chronic silicosis
233763009,Silicotuberculosis
233764003,Wollastonite pneumoconiosis
233767005,Stage 1 pulmonary sarcoidosis
233768000,Stage 2 pulmonary sarcoidosis
233769008,Stage 3 pulmonary sarcoidosis
233770009,Stage 4 pulmonary sarcoidosis
233771008,Endobronchial sarcoidosis
233772001,Sarcoid pulmonary calcification
233774000,Humidifier fever
233786002,Acquired tracheal stenosis
233787006,Acquired subglottic stenosis
233796006,Acquired bronchial stenosis
233805005,Bronchial anastomotic stricture
233940007,Pulmonary tumor embolism
235978006,Cystic fibrosis of pancreas
236302005,Acute interstitial pneumonia
236432001,Pulmonary renal syndrome
238676008,Lofgrens syndrome
240702004,Chronic necrotizing pulmonary aspergillosis
24369008,Pulmonary sarcoidosis
249460003,Supraglottic stenosis
254625005,Malignant tumor of lung parenchyma
254626006,Adenocarcinoma of lung
254628007,Carcinoma of lung parenchyma
254629004,Large cell carcinoma of lung
254631008,Giant cell carcinoma of lung
254632001,Small cell carcinoma of lung
254633006,Oat cell carcinoma of lung
254634000,Squamous cell carcinoma of lung
254635004,Epithelioid hemangioendothelioma of lung
254637007,Non-small cell lung cancer
254638002,Pancoast tumor
254639005,Carcinoma in situ of lung parenchyma
25897000,Malt-workers' lung
26427008,Chronic pulmonary histoplasmosis
266368002,Post-inflammatory pulmonary fibrosis
269464000,"Malignant neoplasm of upper lobe, bronchus or lung"
276635001,Acquired subglottic stenosis in newborn
276636000,Post-intubation subglottic stenosis
277485007,Secondary pulmonary hypoplasia
277486008,Pulmonary hypoplasia associated with short gestation
277656005,Primary pulmonary hypoplasia
277844007,Pulmonary lymphangioleiomyomatosis
285604008,Metastasis to lung of unknown primary
2912004,Cystic-bullous disease of the lung
29422001,Coal workers' pneumoconiosis
30042003,Confluent fibrosis of lung
30188007,Alpha-1-antitrypsin deficiency
302913000,Diffuse pulmonary calcinosis
312603000,Lung transplant rejection
313353007,Squamous cell carcinoma of bronchus in left lower lobe
313354001,Squamous cell carcinoma of bronchus in left upper lobe
313355000,Squamous cell carcinoma of bronchus in right lower lobe
313356004,Squamous cell carcinoma of bronchus in right middle lobe
313357008,Squamous cell carcinoma of bronchus in right upper lobe
314954002,Local recurrence of malignant tumor of lung
317931000119101,Pulmonary disease due to allergic granulomatosis angiitis
319841000119107,Rheumatoid lung disease with rheumatoid arthritis
32139003,Mixed dust pneumoconiosis
32477003,Heart-lung transplant with recipient cardiectomy-pneumonectomy
328641000119109,Genetic disorder of surfactant dysfunction
328661000119108,Interstitial lung disease of childhood
33548005,Anthracosilicosis
34004002,Siderosilicosis
35037009,Primary atypical interstitial pneumonia
3514002,Peribronchial fibrosis of lung
353561000119103,Secondary malignant neoplasm of right lung
353741000119106,Secondary malignant neoplasm of left lung
35491000119107,Restrictive lung mechanics due to neuromuscular disease
36042005,Parietoalveolar pneumopathy
361196000,Idiopathic hilar fibrosis
363358000,Malignant tumor of lung
36485005,Restrictive lung disease
36696005,Kaolinosis
371067004,Hepatopulmonary syndrome
37180002,Chronic nonspecific lung disease
372110008,"Primary malignant neoplasm of lower lobe, bronchus or lung"
372111007,"Carcinoma of lower lobe, bronchus or lung"
372112000,"Primary malignant neoplasm of middle lobe, bronchus or lung"
372113005,"Carcinoma of middle lobe, bronchus or lung"
372135002,"Primary malignant neoplasm of upper lobe, bronchus or lung"
372136001,"Carcinoma of upper lobe, bronchus or lung"
37471005,Extrinsic allergic alveolitis
37711000,Cadmium pneumonitis
38729007,Wheat weevil disease
398640008,Rheumatoid pneumoconiosis
398726004,Rheumatoid lung disease
39905002,Scimitar syndrome
40122008,Pneumoconiosis
40218008,Carbon electrode makers' pneumoconiosis
404807005,Cheese-washers' lung
40527005,Idiopathic pulmonary hemosiderosis
405570007,Pulmonary fibrosis due to and following radiotherapy
40640008,Massive fibrosis of lung co-occurrent and due to silicosis
413839001,Chronic lung disease
41997000,Asthmatic pulmonary alveolitis
422968005,"Non-small cell carcinoma of lung, TNM stage 3"
423050000,"Large cell carcinoma of lung, TNM stage 2"
423121009,"Non-small cell carcinoma of lung, TNM stage 4"
423295000,"Squamous cell carcinoma of lung, TNM stage 1"
423468007,"Squamous cell carcinoma of lung, TNM stage 2"
423600008,"Large cell carcinoma of lung, TNM stage 4"
424132000,"Non-small cell carcinoma of lung, TNM stage 1"
424938000,"Large cell carcinoma of lung, TNM stage 1"
424970000,"Large cell carcinoma of lung, TNM stage 3"
425048006,"Non-small cell carcinoma of lung, TNM stage 2"
425230006,"Squamous cell carcinoma of lung, TNM stage 3"
425376008,"Squamous cell carcinoma of lung, TNM stage 4"
425951002,Shrinking lung syndrome
426705001,Diabetes mellitus co-occurrent and due to cystic fibrosis
426853005,Pneumoconiosis caused by silicate
426964009,"Non-small cell lung cancer, positive for epidermal growth factor receptor expression"
427038005,"Non-small cell lung cancer, negative for epidermal growth factor receptor expression"
427123006,Interstitial lung disease due to collagen vascular disease
427777003,Restrictive lung disease due to muscular dystrophy
427896006,Chronic respiratory insufficiency
427908002,Restrictive lung disease due to kyphoscoliosis
427928003,Disorder related to lung transplantation
428697002,Inactive tuberculosis of lung
429091008,Dependence on biphasic positive airway pressure ventilation
429332008,Transplantation of single lobe of lung
429487005,Dependence on continuous positive airway pressure ventilation
431223003,Acute rejection of lung transplant
431507002,Accelerated rejection of lung transplant
432066002,Lung disorder due to autoimmune disorder
432774005,Hyperacute rejection of lung transplant
438773007,Recurrent pulmonary embolism
440173001,Nonsquamous nonsmall cell neoplasm of lung
44165003,Complication of transplanted lung
44274007,Lymphoid interstitial pneumonia
444932008,Dependence on ventilator
445378003,Acute exacerbation of bronchiectasis
44547005,Chalicosis
446946005,Reinfection pulmonary tuberculosis
447006007,Relapse pulmonary tuberculosis
447810006,Congenital stenosis of trachea due to complete rings
447811005,Congenital stenosis of trachea due to tracheal web
448305002,Vascular ring with malrotation and dextroversion of heart and hypoplasia of right lung and left arterial duct
448372003,Non-Hodgkin's lymphoma of lung
448595006,Scimitar syndrome with additional anomalous pulmonary venous connection
448672006,Follicular non-Hodgkin's lymphoma of lung
448867004,Diffuse non-Hodgkin's lymphoma of lung
448993007,Malignant epithelial neoplasm of lung
46847001,Chronic pulmonary edema
47515009,Simple silicosis
48347002,Humidifier lung
49840000,Complicated silicosis
50076003,Baritosis
50196008,Perialveolar fibrosis of lung
50581000,Goodpasture's syndrome
50589003,Silver polishers' lung disease
51277007,Stannosis
51615001,Fibrosis of lung
52333004,Mushroom workers' lung
52500008,Saccular bronchiectasis
52571006,Chronic tracheobronchitis
526071000000104,Arthropathy in cystic fibrosis
54867000,Rheumatoid fibrosing alveolitis
56440001,Segmental tracheal stenosis
56841008,Massive fibrosis of lung
58691003,Antimony pneumoconiosis
59128005,Congenital honeycomb lung
59773008,Simple pulmonary alveolitis
599006,Chronic pneumothorax
59940009,Hypersensitivity alveolitis in lungworm infection
60631000119109,Dependence on home ventilator
60651000119103,Dependence on continuous supplemental oxygen
62371005,Pulmonary siderosis
62511003,Autotransplant of lung
63480004,Chronic bronchitis
63841001,Chronic pulmonary congestion
64631008,Fullers' earth disease
64667001,Interstitial pneumonia
67242002,Bagassosis
67811000119102,"Primary small cell malignant neoplasm of lung, TNM stage 1"
67821000119109,"Primary small cell malignant neoplasm of lung, TNM stage 2"
67831000119107,"Primary small cell malignant neoplasm of lung, TNM stage 3"
67841000119103,"Primary small cell malignant neoplasm of lung, TNM stage 4"
68333005,Furriers' lung
683991000119103,Extensive stage primary small cell carcinoma of lung
69339004,Bird-fanciers' lung
69454006,Chronic respiratory condition caused by fumes AND/OR vapors
697921005,Pulmonary hypertension in sarcoidosis
697923008,Pulmonary hypertension in lymphangioleiomyomatosis
700249006,Idiopathic interstitial pneumonia
702432006,"Diaphragmatic hernia, abnormal face and distal limb anomalies"
703228009,Non-small cell lung cancer with mutation in epidermal growth factor receptor
703230006,Non-small cell lung cancer without mutation in epidermal growth factor receptor
707403002,Primary fetal adenocarcinoma of lung
707404008,Primary mixed subtype adenocarcinoma of lung
707405009,Primary adenosquamous carcinoma of lung
707407001,Primary signet ring cell carcinoma of lung
707408006,Primary small cell non-keratinizing squamous cell carcinoma of lung
707409003,Primary acinar cell carcinoma of lung
707410008,Primary solid carcinoma of lung
707411007,Primary papillary adenocarcinoma of lung
707412000,Chronic pulmonary thromboembolism
707413005,Chronic pulmonary thromboembolism without pulmonary hypertension
707433009,Lymphangioleiomyomatosis due to tuberous sclerosis syndrome
707434003,Pulmonary fibrosis due to Hermansky-Pudlak syndrome
707442002,Congenital pulmonary alveolar proteinosis
707443007,Autoimmune pulmonary alveolar proteinosis
707451005,Primary adenocarcinoma of lung
707452003,Primary mucinous adenocarcinoma of lung
707453008,Primary clear cell squamous cell carcinoma of lung
707454002,Primary basaloid squamous cell carcinoma of lung
707455001,Primary papillary squamous cell carcinoma of lung
707456000,Primary undifferentiated carcinoma of lung
707457009,Primary spindle cell carcinoma of lung
707458004,Primary pleomorphic carcinoma of lung
707460002,Primary pseudosarcomatous carcinoma of lung
707464006,Primary myoepithelial carcinoma of lung
707465007,Primary mucoepidermoid carcinoma of lung
707466008,Primary adenoid cystic carcinoma of lung
707467004,Primary salivary gland type carcinoma of lung
707468009,Primary mixed mucinous and non-mucinous bronchiolo-alveolar carcinoma of lung
707469001,Primary non-mucinous bronchiolo-alveolar carcinoma of lung
707470000,Primary mucinous bronchiolo-alveolar carcinoma of lung
707510005,Secondary pulmonary alveolar proteinosis
707595001,Primary mucinous cystadenocarcinoma of lung
707596000,Primary carcinosarcoma of lung
707670009,Pleuropulmonary blastoma
707671008,Pleuropulmonary blastoma type I
707672001,Pleuropulmonary blastoma type II
707673006,Pleuropulmonary blastoma type III
707766007,Exocrine pancreatic manifestation co-occurrent and due to cystic fibrosis
708026002,Chronic pneumonitis of infancy
711379004,Interstitial lung disease due to connective tissue disease
711414003,Primary clear cell adenocarcinoma of lung
71193007,Fibrosis of lung caused by radiation
713244007,Drug induced pulmonary fibrosis
714203003,Acute bronchitis co-occurrent with bronchiectasis
716088000,Follicular hamartoma with alopecia and cystic fibrosis syndrome
716198008,Growth delay with hydrocephalus and lung hypoplasia syndrome
718200007,Primary pulmonary lymphoma
719218000,Cryptogenic organizing pneumonia
720401009,Cystic fibrosis with gastritis and megaloblastic anemia syndrome
721076000,Siegler Brewer Carey syndrome
721095007,"Diaphragmatic defect, limb deficiency, skull defect syndrome"
721977007,"Lung fibrosis, immunodeficiency, 46,XX gonadal dysgenesis syndrome"
722425009,Reactive oxygen species 1 positive non-small cell lung cancer
722528008,Primary malignant neuroendocrine neoplasm of lung
72270005,Collagenous pneumoconiosis
722912007,Congenital pulmonary hypoplasia due to prolonged premature rupture of membranes
722913002,Congenital pulmonary hypoplasia due to lung space occupying lesion
723301009,Squamous non-small cell lung cancer
723829000,"Pulmonary fibrosis, hepatic hyperplasia, bone marrow hypoplasia syndrome"
724056005,Malignant neoplasm of lower lobe of right lung
724058006,Malignant neoplasm of upper lobe of left lung
724059003,Malignant neoplasm of lower lobe of left lung
724060008,Malignant neoplasm of right upper lobe of lung
725052002,Fetal cystic fibrosis
725415009,House allergic alveolitis
73144008,Pneumoconiosis caused by talc
733171006,Chronic pulmonary aspergillosis
733453005,"Congenital nephrotic syndrome, interstitial lung disease, epidermolysis bullosa syndrome"
733497009,Chronic suppuration of bronchus
7343008,Liparitosis
73448002,Fish-meal workers' lung
737181009,Interstitial lung disease due to systemic disease
737182002,Interstitial lung disease due to granulomatous disease
737183007,Interstitial lung disease due to metabolic disease
737184001,Interstitial lung disease co-occurrent and due to systemic vasculitis
737281001,Artificial larynx in situ
7436001,Alveolar pneumopathy
74387008,Tuberculosis of hilar lymph nodes
7548000,Rheumatic pneumonia
75547007,Stenosis of larynx
76157009,Bituminosis
762269004,Classical cystic fibrosis
762270003,Atypical cystic fibrosis
762271004,Subclinical cystic fibrosis
762618008,Bronchiolitis obliterans syndrome due to and after lung transplantation
770674007,Tubercular lesion of lung
770760006,16q24.1 microdeletion syndrome
77593006,Congenital bronchiectasis
784266000,History of heart-lung transplant recipient
785345002,Pneumoconiosis caused by sisal dust
78723001,Cannabinosis
79031000119101,Dependence on respirator
79877004,Stenosis of bronchus
805002,Pneumoconiosis caused by silica
805261000000101,Bronchiolitis obliterans syndrome after lung transplantation
80602006,Nodular tuberculosis of lung
80614003,Prolonged pulmonary alveolitis
80825009,Congenital hypoplasia of lung
81423003,Cystic fibrosis without meconium ileus
81554001,Tuberculosis of lung with involvement of bronchus
820361000000105,Allotransplantation of lobe of lung from live donor
822969007,Acinar cell cystadenocarcinoma of lung
8247009,Berylliosis
829972004,Diffuse hemorrhage of pulmonary alveolar
830055006,Anaplastic lymphoma kinase fusion oncogene negative non-small cell lung cancer
830060005,Reactive oxygen species 1 negative non-small cell lung cancer
830151004,Anaplastic lymphoma kinase fusion oncogene positive non-small cell lung cancer
83457000,Cylindrical bronchiectasis
846634000,Chronic respiratory condition caused by fumes
846635004,Chronic respiratory condition caused by vapors
85438006,Diatomaceous earth disease
8549006,Desquamative interstitial pneumonia
85761009,Byssinosis
859041000000103,Exacerbation of cystic fibrosis
860890006,Fetal interstitial neoplasm of lung
86092005,Cystic fibrosis with meconium ileus
86263001,Cobaltosis
86555001,Cystic fibrosis of the lung
866103007,Interstitial lung disease due to juvenile polymyositis
86638007,Maple-bark strippers' lung
870573008,Interstitial pneumonia with autoimmune features
87119009,Congenital cystic lung
87153008,Pulmonary alveolar microlithiasis
87909002,Hard metal pneumoconiosis
88039007,Transplant of lung
88687001,Manganese pneumonitis
89201000119106,Dependence on supplemental oxygen when ambulating
89241000119108,Dependence on nocturnal oxygen therapy
90117007,Tuberculous fibrosis of lung
90610005,Interstitial pulmonary fibrosis of prematurity
90623003,Aluminosis of lung
92552003,Carcinoma in situ of bronchus of left lower lobe
92553008,Carcinoma in situ of bronchus of left upper lobe
92554002,Carcinoma in situ of bronchus of right lower lobe
92555001,Carcinoma in situ of bronchus of right middle lobe
92556000,Carcinoma in situ of bronchus of right upper lobe
92609009,Carcinoma in situ of hilus of lung
92639004,Carcinoma in situ of left lower lobe of lung
92640002,Carcinoma in situ of left upper lobe of lung
92649001,Carcinoma in situ of lung
92701002,Carcinoma in situ of right lower lobe of lung
92702009,Carcinoma in situ of right middle lobe of lung
92703004,Carcinoma in situ of right upper lobe of lung
931000119107,Dependence on supplemental oxygen
93729006,Primary malignant neoplasm of bronchus of left lower lobe
93730001,Primary malignant neoplasm of bronchus of left upper lobe
93731002,Primary malignant neoplasm of bronchus of right lower lobe
93732009,Primary malignant neoplasm of bronchus of right middle lobe
93733004,Primary malignant neoplasm of bronchus of right upper lobe
93827000,Primary malignant neoplasm of hilus of lung
93864006,Primary malignant neoplasm of lower lobe of left lung
93865007,Primary malignant neoplasm of upper lobe of left lung
93880001,Primary malignant neoplasm of lung
93991009,Primary malignant neoplasm of right lower lobe of lung
93992002,Primary malignant neoplasm of right middle lobe of lung
93993007,Primary malignant neoplasm of upper lobe of right lung
94227002,Secondary malignant neoplasm of bronchopulmonary lymph nodes
94228007,Secondary malignant neoplasm of bronchus of left lower lobe
94229004,Secondary malignant neoplasm of bronchus of left upper lobe
94230009,Secondary malignant neoplasm of bronchus of right lower lobe
94231008,Secondary malignant neoplasm of bronchus of right middle lobe
94232001,Secondary malignant neoplasm of bronchus of right upper lobe
94329002,Secondary malignant neoplasm of hilus of lung
94375005,Secondary malignant neoplasm of left lower lobe of lung
94376006,Secondary malignant neoplasm of left upper lobe of lung
94391008,Secondary malignant neoplasm of lung
94522007,Secondary malignant neoplasm of right lower lobe of lung
94523002,Secondary malignant neoplasm of right middle lobe of lung
94524008,Secondary malignant neoplasm of right upper lobe of lung
9660004,Congenital stenosis of trachea"""

c4_df = pd.read_csv(io.StringIO(c4), header=0,delimiter=',').astype(str)
spark.createDataFrame(c4_df).createOrReplaceGlobalTempView("ccu002_06_d17_resp_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_resp_primis

# COMMAND ----------

# MAGIC %md ## cns_primis

# COMMAND ----------

c5 = """code,term
10007009,Coffin-Siris syndrome
100941000119100,Epilepsy in mother complicating pregnancy
101421000119107,Dementia due to Parkinson's disease
102831000119104,Paralytic syndrome of both lower limbs as sequela of stroke
10349009,Multi-infarct dementia with delirium
103761000119107,Paralytic syndrome of all four limbs as sequela of stroke
104461000119104,Ophthalmoplegia due to Graves disease
1055001,Stenosis of precerebral artery
106018006,Hereditary degenerative disease of central nervous system
106021000119105,Multi-infarct dementia due to atherosclerosis
10750951000119106,Epilepsy in mother complicating childbirth
108691000119102,Spasticity as sequela of stroke
10878002,Aneurysm of common carotid artery
1089411000000104,Cerebral infarction due to occlusion of cerebral artery
1089421000000105,Cerebral infarction due to stenosis of cerebral artery
1089501000000102,Presenile dementia with psychosis
1089521000000106,Predominantly cortical dementia
1089531000000108,Predominantly cortical vascular dementia
109478007,Kohlschutter's syndrome
109561000,Cerebrofacial dysplasia
109911004,Overlapping malignant neoplasm of brain and other parts of the central nervous system
109915008,Primary malignant neoplasm of meninges
111296006,Basilar artery embolism
111298007,Chronic cerebral ischemia
111299004,Atheroma of cerebral arteries
111337001,Dyke-Davidoff-Masson syndrome
111385000,Tay-Sachs disease
111480006,Psychoactive substance-induced organic dementia
111496009,Syringomyelia
111497000,Arterial thrombosis of spinal cord
111498005,Extratemporal epilepsy
111499002,Déjérine-Sottas disease
111500006,Muscular dystrophy-deafmutism syndrome
111501005,Congenital hereditary muscular dystrophy
111502003,Fukuyama congenital muscular dystrophy
111503008,Merosin deficient congenital muscular dystrophy
111505001,"Muscle-eye-brain disease, congenital muscular dystrophy"
111506000,"Distal muscular dystrophy, Miyoshi type"
111508004,Emery-Dreifuss muscular dystrophy
111527005,Partial optic atrophy
1131000119105,Sequela of cerebrovascular accident
11442006,Hereditary sensory neuropathy
11538006,Quadriplegia
116811000119106,Non-Hodgkin lymphoma of central nervous system metastatic to lymph node of lower limb
116821000119104,Non-Hodgkin lymphoma of central nervous system metastatic to lymph node of upper limb
11701009,Hemicephaly
119001000119108,Intractable simple partial epilepsy
12242711000119109,Weakness of left facial muscle due to and following cerebrovascular accident
12242751000119105,Weakness of right facial muscle due to and following cerebrovascular accident
12246008,Acute neuronopathic Gaucher's disease
12348006,Presenile dementia
123615007,Secondary optic atrophy
12367511000119101,Paraplegia due to and following cerebrovascular accident
1239331000000100,Significant intellectual disability
12454008,Cauda equina syndrome with neurogenic bladder
125081000119106,Cerebral infarction due to occlusion of precerebral artery
125501000119105,Fetus with complete trisomy 21 syndrome
125511000119108,Fetus with complete trisomy 18 syndrome
125521000119101,Fetus with complete trisomy 13 syndrome
126011000119107,Acquired caroticocavernous sinus fistula
126944002,Brain disorder resulting from a period of impaired oxygen delivery to the brain
126945001,Perinatal anoxic-ischemic brain injury
128171000119104,Spontaneous caroticocavernous sinus fistula
128190004,Inherited metabolic disorder of nervous system
128203003,Hereditary motor and sensory neuropathy with optic atrophy
128204009,Hereditary motor and sensory neuropathy with retinitis pigmentosa
128205005,Hereditary sensory and autonomic neuropathy
128206006,Congenital sensory neuropathy with selective loss of small myelinated fibers
128209004,Chronic inflammatory demyelinating polyradiculoneuropathy
128212001,"Spinal muscular atrophy, type II"
128213006,Neuromuscular junction disorder
128218002,Disorder of intracranial venous sinus
12853006,Embolism of torcular Herophili
128608001,Cerebral arterial aneurysm
128609009,Intracranial aneurysm
129583005,Paralysis of palate
129596006,Menopausal muscular dystrophy syndrome
129608008,Progressive pyramidopallidal degeneration
129614001,"Paralysis of vagus, spinal accessory and hypoglossal nerves"
129620000,Scapuloperoneal muscular dystrophy
129621001,"Nemaline myopathy, early onset type"
129622008,"Nemaline myopathy, late onset type"
130121000119104,Dementia due to Rett's syndrome
13092008,Pick's disease
133981000119106,Dysarthria as late effects of cerebrovascular disease
133991000119109,Fluency disorder as sequela of cerebrovascular disease
134771000119108,Alteration of sensation as late effect of stroke
13973009,Grand mal status
140281000119108,Hemiparesis as late effect of cerebrovascular disease
14070001,Multi-infarct dementia with depression
142031000119104,Visual field defect due to and following cerebrovascular accident
14210003,Lipofuscinosis
14246007,Embolism of intracranial venous sinus
14309005,Anterior choroidal artery syndrome
14401000119109,Partial frontal lobe epilepsy
147101000119108,Primary malignant astrocytoma of central nervous system
147131000119101,Glioblastoma multiforme of central nervous system
148871000119109,Weakness as a late effect of cerebrovascular accident
14977000,Multiple AND bilateral precerebral artery thrombosis
149821000119103,Cerebral infarction due to carotid artery occlusion
15080006,Myotubular myopathy with type I atrophy
15182000,Coffin-Lowry syndrome
15523002,Benign focal epilepsy of childhood
15632811000119100,Optic atrophy of right eye
15632851000119104,Optic atrophy of left eye
15648201000119100,Aneurysm of intracranial portion of right internal carotid artery
15648241000119103,Aneurysm of intracranial portion of left internal carotid artery
15648281000119108,Aneurysm of extracranial portion of right internal carotid artery
15648321000119103,Aneurysm of extracranial portion of left internal carotid artery
15648361000119108,Aneurysm of right internal carotid artery
15648401000119104,Aneurysm of left internal carotid artery
15648441000119102,Aneurysm of right common carotid artery
15648481000119107,Aneurysm of left common carotid artery
15648521000119107,Aneurysm of right carotid artery
15648561000119102,Aneurysm of left carotid artery
15662003,Senile dementia
15699121000119104,Hereditary right optic atrophy
15699161000119109,Hereditary left optic atrophy
15705007,Phlebitis of basilar sinus
15707961000119109,Dissection of bilateral carotid arteries
15708001000119106,Dissection of left carotid artery
15708041000119108,Dissection of right carotid artery
15710641000119100,Dissection of bilateral vertebral arteries
15710681000119105,Dissection of right vertebral artery
15710721000119104,Dissection of left vertebral artery
1591000119103,Dementia with behavioral disturbance
1593000,Infantile hemiplegia
15978431000119106,Thrombosis of right vertebral artery
15978471000119109,Thrombosis of left vertebral artery
15978631000119109,Occlusion of bilateral vertebral arteries
15982271000119104,Weakness of right facial muscle due to and following cerebrovascular disease
15982311000119104,Weakness of left facial muscle due to and following cerebrovascular disease
15988351000119101,Acquired right carotid cavernous fistula
15988391000119106,Acquired left carotid cavernous fistula
16218291000119100,Acute cerebral ischemia
16260551000119106,Dysphasia due to and following cerebrovascular accident
16276361000119109,Vascular dementia without behavioral disturbance
16279401000119108,Occlusion of right cilioretinal artery
16279441000119105,Occlusion of left cilioretinal artery
163594004,On examination - salaam attack
163601006,On examination - hemiplegia
163604003,On examination - paraplegia
163605002,On examination - quadriplegia
163606001,On examination - diplegia
16415361000119105,Radiologically isolated syndrome
16418006,Embolism of basilar sinus
16476641000119100,Acquired arteriovenous fistula of dura of cerebrum
16662331000119106,Aneurysm of right vertebral artery
16662371000119109,Aneurysm of left vertebral artery
1670004,Cerebral hemiparesis
16703551000119107,Memory deficit due to and following cerebrovascular disease
16703661000119105,Memory deficit due to and following cerebrovascular accident
16703761000119102,Memory deficit due to and following ischemic cerebrovascular accident
16703821000119101,Memory deficit due to and following hemorrhagic cerebrovascular accident
16709811000119106,Spontaneous hemorrhage of subarachnoid space from anterior communicating artery
16851005,Mitochondrial myopathy
171822009,Acute atrophic spinal paralysis
17409003,Facial hemiparesis
18058007,Phlebitis of intracranial venous sinus
18322005,Thrombosis of torcular Herophili
1845001,Paraparesis
186317009,Listerial cerebral arteritis
186476008,Acute paralytic non-bulbar poliomyelitis
186478009,"Acute paralytic poliomyelitis, vaccine-associated"
186479001,"Acute paralytic poliomyelitis, wild virus, imported"
186480003,"Acute paralytic poliomyelitis, wild virus, indigenous"
186831000119104,Apraxia due to and following cerebrovascular accident
186893003,Rupture of syphilitic cerebral aneurysm
18756002,Juvenile GM1 gangliosidosis
187931000119106,Atypical absence epilepsy
188312005,Malignant neoplasm of cerebral dura mater
188313000,Malignant neoplasm of cerebral arachnoid mater
188315007,Malignant neoplasm of cerebral pia mater
18927009,"Niemann-Pick disease, type D"
191449005,Uncomplicated senile dementia
191451009,Uncomplicated presenile dementia
191452002,Presenile dementia with delirium
191454001,Presenile dementia with paranoia
191455000,Presenile dementia with depression
191457008,Senile dementia with depressive or paranoid features
191458003,Senile dementia with paranoia
191459006,Senile dementia with depression
191461002,Senile dementia with delirium
191463004,Uncomplicated arteriosclerotic dementia
191464005,Arteriosclerotic dementia with delirium
191465006,Arteriosclerotic dementia with paranoia
191466007,Arteriosclerotic dementia with depression
191475009,Chronic alcoholic brain syndrome
191493005,Drug-induced dementia
191519005,Dementia associated with another disease
192673008,Sarcoid meningitis
192685000,Subacute sclerosing panencephalitis
192753009,Phlebitis and thrombophlebitis of intracranial sinuses
192754003,Embolism cavernous sinus
192755002,Embolism superior longitudinal sinus
192756001,Embolism lateral sinus
192757005,Embolism transverse sinus
192759008,Cerebral venous sinus thrombosis
192760003,Thrombosis of superior longitudinal sinus
192764007,Phlebitis cavernous sinus
192765008,Phlebitis of superior longitudinal sinus
192769002,Thrombophlebitis of central nervous system venous sinuses
192770001,Thrombophlebitis of cavernous sinus
192771002,Thrombophlebitis of superior longitudinal venous sinus
192781003,Leukodystrophy
192782005,Galactosylceramide beta-galactosidase deficiency
192787004,B variant hexosaminidase A deficiency
192788009,Retinal dystrophy in cerebroretinal lipidosis
192845009,Myoclonic encephalopathy
192904000,Myelopathy due to another disorder
192906003,Myelopathy due to neoplastic disease
192928003,Generalized multiple sclerosis
192929006,Exacerbation of multiple sclerosis
192949002,Congenital paraplegia
192964002,Flaccid tetraplegia
192965001,Spastic tetraplegia
192966000,Flaccid paraplegia
192967009,Spastic paraplegia
192976002,Progressive supranuclear palsy
192979009,Generalized non-convulsive epilepsy
192990004,Benign myoclonic epilepsy in infancy
192999003,Partial epilepsy with impairment of consciousness
193000002,Temporal lobe epilepsy
193002005,Psychosensory epilepsy
193008009,Somatosensory epilepsy
193009001,Partial epilepsy with autonomic symptoms
193010006,Visual reflex epilepsy
193021002,Cursive (running) epilepsy
193022009,Localization-related(focal)(partial)idiopathic epilepsy and epileptic syndromes with seizures of localized onset
193165008,Neuropathy in association with hereditary ataxia
193195000,Sarcoid neuropathy
193207007,Juvenile or adult myasthenia gravis
193209005,Myasthenic syndrome due to another disorder
193212008,Myasthenic syndrome due to hypothyroidism
193213003,Myasthenic syndrome due to pernicious anemia
193214009,Myasthenic syndrome due to thyrotoxicosis
193216006,Congenital and developmental myasthenia
193225000,Hereditary progressive muscular dystrophy
193227008,Pelvic muscular dystrophy
193230001,Distal muscular dystrophy with juvenile onset
193237003,Myotonic disorder
193238008,Infantile myotonia
19373007,External ophthalmoplegia
194043004,Optic atrophy secondary to retinal disease
19448008,Optic atrophy associated with retinal dystrophy
195154000,Ruptured berry aneurysm
195155004,Subarachnoid hemorrhage from carotid siphon and bifurcation
195160000,Intracranial subarachnoid hemorrhage from vertebral artery
195180004,Basilar artery occlusion
195182007,Vertebral artery occlusion
195183002,Multiple and bilateral precerebral arterial occlusion
195185009,Cerebral infarct due to thrombosis of precerebral arteries
195186005,Cerebral infarction due to embolism of precerebral arteries
195189003,Cerebral infarction due to thrombosis of cerebral arteries
195190007,Cerebral infarction due to embolism of cerebral arteries
195199008,Vertebrobasilar artery syndrome
195229008,Non-pyogenic venous sinus thrombosis
195230003,"Cerebral infarction due to cerebral venous thrombosis, non-pyogenic"
195232006,Occlusion and stenosis of middle cerebral artery
195233001,Occlusion and stenosis of anterior cerebral artery
195234007,Occlusion and stenosis of posterior cerebral artery
195235008,Occlusion and stenosis of cerebellar arteries
195236009,Occlusion and stenosis of multiple and bilateral cerebral arteries
195239002,Late effects of cerebrovascular disease
195241001,Sequelae of intracerebral hemorrhage
195243003,Sequelae of cerebral infarction
19598007,Generalized epilepsy
199451000000106,Simple partial epileptic seizure
19972008,Postencephalitic parkinsonism
20022000,Hemiparesis
200258006,Obstetric cerebral venous thrombosis
200259003,Cerebral venous thrombosis in pregnancy
200260008,Cerebral venous thrombosis in the puerperium
200330000,Puerperal cerebrovascular disorder - delivered
200331001,Puerperal cerebrovascular disorder - delivered with postnatal complication
200332008,Puerperal cerebrovascular disorder with antenatal complication
200333003,Puerperal cerebrovascular disorder with postnatal complication
20059004,Occlusion of cerebral artery
20121000119105,Partial occipital lobe epilepsy
20305008,"Congenital myotonia, autosomal recessive form"
204036008,Lissencephaly
204040004,Agenesis of cerebrum
204052006,Cebocephaly
20447006,Plasma cell dyscrasia with polyneuropathy
204493007,Arteriovenous malformation of precerebral vessels
204497008,Cerebrovascular system anomalies
204501003,Congenital stricture of cerebral artery
204745000,Total intestinal aganglionosis
205615000,Trisomy 21- meiotic nondisjunction
205619006,"Trisomy 13, meiotic nondisjunction"
205620000,Trisomy 13 - mitotic nondisjunction mosaicism
205623003,Trisomy 18 - meiotic nondisjunction
205624009,Trisomy 18 - mitotic nondisjunction mosaicism
2065009,Dominant hereditary optic atrophy
20725005,Familial visceral neuropathy
21007002,Wernicke's disease
21086008,Cockayne syndrome
21098003,Primary optic atrophy
21111006,Complete trisomy 13 syndrome
213044006,Mechanical complication of carotid artery bypass
213208008,Anoxic brain damage complication
213209000,Cerebral anoxia complication
21361000119109,Paraneoplastic peripheral neuropathy
21391000119102,Partial parietal lobe epilepsy
21524000,Relaxation of diaphragm
2198002,Visceral epilepsy
22126005,Hereditary neuraxial edema
223176004,Cerebellar disorder
22381000119105,Primary degenerative dementia
22386003,Syphilitic optic atrophy
22811006,Leukoencephalopathy
22881000119100,Quadriplegia with quadriparesis
230156002,Malignant meningitis
230193008,Neurosarcoidosis
230220006,Intracranial septic embolism
230221005,Intracranial arterial septic embolism
230222003,Septic thrombophlebitis of straight sinus
230223008,Septic thrombophlebitis of sigmoid sinus
230224002,Septic thrombophlebitis of cortical vein
230226000,System disorder of the nervous system
230232005,Late onset cerebellar ataxia
230233000,Progressive cerebellar ataxia
230234006,Periodic ataxia
230237004,Progressive spinocerebellar ataxia with decreased tendon reflexes
230239001,Progressive cerebellar ataxia with palatal myoclonus
230240004,Progressive cerebellar ataxia with hypogonadism
230244008,Disorder primarily affecting the motor pathways
230247001,Distal spinal muscular atrophy
230248006,Scapuloperoneal spinal muscular atrophy
230249003,Facioscapulohumeral spinal muscular atrophy
230250003,Facioscapulohumeral spinal muscular atrophy with sensory loss
230251004,Scapulohumeral spinal muscular atrophy
230252006,Oculopharyngeal spinal muscular atrophy
230253001,Bulbospinal neuronopathy
230254007,Western Pacific motor neurone disease
230255008,Madras-type motor neurone disease
230257000,Paraneoplastic motor neurone disease
230258005,Amyotrophic lateral sclerosis with dementia
230264003,Troyer syndrome
230282000,Post-traumatic dementia
230283005,Punch drunk syndrome
230285003,Vascular dementia of acute onset
230286002,Subcortical vascular dementia
230287006,Mixed cortical and subcortical vascular dementia
230289009,Patchy dementia
230291001,Juvenile Parkinson's disease
230296006,Vascular parkinsonism
230297002,Multiple system atrophy
230298007,Disorder presenting primarily with chorea
230329009,Posthemiplegic dystonia
230363006,Progressive neuronal degeneration of childhood
230368002,Type III transitional Pelizaeus-Merzbacher disease
230369005,Type IV adult Pelizaeus-Merzbacher disease
230370006,Type V atypical Pelizaeus-Merzbacher disease
230371005,Type VI Cockayne Pelizaeus-Merzbacher disease
230372003,Acute relapsing multiple sclerosis
230373008,Chronic progressive multiple sclerosis
230375001,Subacute hemorrhagic leukoencephalitis
230380005,Balo concentric sclerosis
230381009,Localization-related epilepsy
230382002,Benign frontal epilepsy of childhood
230383007,Benign psychomotor epilepsy of childhood
230384001,Benign atypical partial epilepsy in childhood
230386004,Childhood epilepsy with occipital paroxysms
230387008,Benign occipital epilepsy of childhood - early onset variant
230388003,Benign occipital epilepsy of childhood - late onset variant
230389006,Primary inherited reading epilepsy
230390002,Localization-related symptomatic epilepsy
230393000,Lateral temporal epilepsy
230394006,Frontal lobe epilepsy
230395007,Supplementary motor epilepsy
230397004,Anterior frontopolar epilepsy
230398009,Orbitofrontal epilepsy
230399001,Dorsolateral epilepsy
230400008,Opercular epilepsy
230401007,Non-progressive Kozhevnikow syndrome
230403005,Parietal lobe epilepsy
230404004,Occipital lobe epilepsy
230406002,Localization-related symptomatic epilepsy with specific precipitant
230407006,Hemiplegia-hemiconvulsion-epilepsy syndrome
230408001,Localization-related cryptogenic epilepsy
230412007,Myoclonic epilepsy of early childhood
230413002,Juvenile absence epilepsy
230414008,Epilepsy with grand mal seizures on awakening
230415009,Cryptogenic generalized epilepsy
230416005,Cryptogenic West syndrome
230417001,Symptomatic West syndrome
230418006,Lennox-Gastaut syndrome
230419003,Cryptogenic Lennox-Gastaut syndrome
230420009,Symptomatic Lennox-Gastaut syndrome
230422001,Myoclonic absence epilepsy
230423006,Unverricht-Lundborg syndrome
230425004,Lafora disease
230427007,Cryptogenic myoclonic epilepsy
230428002,Idiopathic myoclonic epilepsy
230429005,Early infantile epileptic encephalopathy with suppression bursts
230430000,Symptomatic myoclonic epilepsy
230435005,Epilepsy undetermined whether focal or generalized
230437002,Severe myoclonic epilepsy in infancy
230438007,Acquired epileptic aphasia
230439004,Epilepsy with continuous spike wave during slow-wave sleep
230440002,Secondary reading epilepsy
230444006,Menstrual epilepsy
230445007,Nocturnal epilepsy
230447004,Eyelid myoclonus with absences
230448009,Writing epilepsy
230450001,Eating epilepsy
230452009,Toothbrushing epilepsy
230453004,Decision-making epilepsy
230454005,Aquagenic epilepsy
230456007,Status epilepticus
230457003,Non-convulsive status epilepticus with three per second spike wave
230458008,Non-convulsive status epilepticus without three per second spike wave
230459000,Non-convulsive simple partial status epilepticus
230460005,Complex partial status epilepticus
230466004,Alternating hemiplegia of childhood
230530003,Congenital nuclear ophthalmoplegia
230552007,X-linked hereditary motor and sensory neuropathy
230553002,Autosomal dominant sensory neuropathy
230556005,X-linked recessive sensory neuropathy
230557001,Hereditary dysautonomia with motor neuropathy
230558006,Hereditary liability to pressure palsies
230559003,Hereditary hypertrophic neuropathy with paraproteinemia
230561007,Congenital neuropathy with arthrogryposis multiplex congenita
230562000,Congenital hypomyelinating neuropathy
230564004,Chronic inflammatory demyelinating polyradiculoneuropathy with central nervous system demyelination
230586003,Neuropathy due to multiple myeloma
230594005,Critical illness polyneuropathy
230666006,Paraneoplastic autonomic dysfunction
230669004,Genetically determined myasthenia
230670003,Familial infantile myasthenia
230671004,Acetylcholine resynthesis deficiency
230672006,Congenital myasthenic syndrome
230673001,Congenital end-plate acetylcholine receptor deficiency
230674007,Pseudomyopathic myasthenia
230675008,Slow channel syndrome
230676009,Putative defect in acetylcholine synthesis or packaging
230677000,Congenital end-plate acetylcholinesterase deficiency
230678005,Decrease of motor end-plate potential amplitude without acetylcholine receptor deficiency
230679002,Abnormality of synaptic vesicles
230684008,Ocular myasthenia
230685009,Myasthenia gravis associated with thymoma
230686005,Generalized myasthenia
230687001,Myopathy in myasthenia gravis
230692004,Infarction - precerebral
230693009,Anterior cerebral circulation infarction
230694003,Total anterior cerebral circulation infarction
230695002,Partial anterior cerebral circulation infarction
230696001,Posterior cerebral circulation infarction
230698000,Lacunar infarction
230699008,Pure motor lacunar infarction
230700009,Pure sensory lacunar infarction
230701008,Pure sensorimotor lacunar infarction
230702001,Lacunar ataxic hemiparesis
230703006,Dysarthria-clumsy hand syndrome
230704000,Multi-infarct state
230706003,Hemorrhagic cerebral infarction
230707007,Anterior cerebral circulation hemorrhagic infarction
230708002,Posterior cerebral circulation hemorrhagic infarction
230720005,Cerebral venous thrombosis of straight sinus
230721009,Cerebral venous thrombosis of sigmoid sinus
230722002,Cerebral venous thrombosis of cortical vein
230724001,Cerebral amyloid angiopathy
230725000,Sporadic cerebral amyloid angiopathy
230730001,Dissection of vertebral artery
230731002,Cerebral arteritis in systemic vasculitis
230732009,Cerebral arteritis in giant cell arteritis
230735006,Syphilitic cerebral arteritis
230738008,Asymptomatic cerebrovascular disease
230739000,Spinal cord stroke
230745008,Hydrocephalus
232036006,Cilioretinal artery occlusion
232059000,Laurence-Moon syndrome
233718008,Pulmonary tuberous sclerosis
233964008,Internal carotid artery stenosis
233983001,Ruptured cerebral aneurysm
233988005,Carotid artery aneurysm
234005004,Vertebral artery rupture
234006003,Carotid artery rupture
234142008,Cerebral arteriovenous malformation
234149004,Congenital arteriovenous fistula of brain
23501004,Arginase deficiency
236529001,"Prune belly syndrome with pulmonic stenosis, mental retardation and deafness"
23671000119107,Sequela of ischemic cerebral infarction
23728006,Partial bilateral paralysis
23740006,Bilateral paralysis of tongue
237612000,"Photomyoclonus, diabetes mellitus, deafness, nephropathy and cerebral dysfunction"
237867001,Hereditary cerebrovascular amyloidosis
237960000,D-2-hydroxyglutaric aciduria
237961001,L-2-hydroxyglutaric aciduria
238018004,Total hexosaminidase deficiency - infantile
238019007,Total hexosaminidase deficiency - juvenile
238020001,Total hexosaminidase deficiency - adult
238021002,B variant hexosaminidase A deficiency - infantile
238022009,B variant hexosaminidase A deficiency - juvenile
238023004,B variant hexosaminidase A deficiency - adult
238024005,B1 variant hexosaminidase A deficiency
238025006,GM1 gangliosidosis
238026007,Infantile GM1 gangliosidosis
238027003,Adult GM1 gangliosidosis
238030005,Galactocerebroside beta-galactosidase deficiency - early onset
238031009,Arylsulfatase A deficiency
238048001,Alpha-N-acetylgalactosaminidase deficiency
23808003,Rolandic vein occlusion syndrome
23819000,Embolism of cavernous venous sinus
23849003,Sandhoff disease
238826008,de Barsy syndrome
23941000119108,Arnold Chiari type 2 without hydrocephalus
240046001,Muscular dystrophy with predominantly proximal limb girdle distribution
240047005,X-linked muscular dystrophy with limb girdle distribution
240048000,X-linked muscular dystrophy with abnormal dystrophin
240049008,Intermediate X-linked muscular dystrophy
240050008,Manifesting female carrier of X-linked muscular dystrophy
240051007,X-linked limb girdle muscular dystrophy with normal dystrophin
240052000,Ji muscular dystrophy
240053005,Hereditary myopathy limited to females
240054004,Autosomal recessive muscular dystrophy with limb girdle distribution
240055003,Autosomal recessive muscular dystrophy with abnormal dystrophin-associated glycoprotein
240056002,Severe autosomal recessive muscular dystrophy of childhood - North African type
240057006,Autosomal recessive muscular dystrophy with gene located at 15q
240058001,Reunion-Indiana Amish type muscular dystrophy
240059009,Congenital muscular dystrophy
240060004,Western type of congenital muscular dystrophy
240061000,Congenital muscular dystrophy with arthrogryposis multiplex congenita
240062007,Ullrich congenital muscular dystrophy
240063002,Eichsfeld type congenital muscular dystrophy
240064008,Hutterite type of muscular dystrophy
240065009,Adult onset autosomal recessive muscular dystrophy with normal dystrophin
240067001,Autosomal dominant muscular dystrophy with limb girdle distribution
240068006,Autosomal dominant muscular dystrophy with gene located at 5q31
240069003,Late onset proximal muscular dystrophy with dysarthria
240070002,Muscular dystrophy not predominantly limb girdle in distribution
240071003,X-linked muscular dystrophy not predominantly limb girdle
240072005,Benign scapuloperoneal muscular dystrophy with cardiomyopathy
240073000,Autosomal recessive muscular dystrophy not predominantly limb girdle
240074006,Scapulohumeral muscular dystrophy
240075007,Autosomal dominant muscular dystrophy not predominantly limb girdle
240076008,Benign scapuloperoneal muscular dystrophy
240077004,Severe scapuloperoneal muscular dystrophy with cardiomyopathy
240078009,Benign congenital muscular dystrophy with finger flexion contractures
240081004,Autosomal recessive centronuclear myopathy
240082006,Myopathy with abnormality of histochemical fiber type
240083001,Myopathy with type I hypotrophy
240084007,Congenital myopathy with fiber type disproportion
240085008,Congenital myopathy with uniform fiber type
240086009,Myopathy with cytoplasmic inclusions
240087000,Myopathy with tubular aggregates
240104008,Congenital myotonic dystrophy
240460008,Acute paralytic poliomyelitis
241006,Epilepsia partialis continua
2421000119107,Hallucinations co-occurrent and due to late onset dementia
24326000,"Metachromatic leukodystrophy, adult type"
24473007,Persistent vegetative state
24624008,Aneurysm of internal carotid artery
24700007,Multiple sclerosis
2495006,Congenital cerebral arteriovenous aneurysm
253098009,Neural tube defect
253116006,Fissured spine with hydrocephalus
253143001,Absence of septum pellucidum
253147000,Type 1 lissencephaly
253148005,Miller Dieker syndrome
253149002,Type 2 lissencephaly
253158009,Hydranencephaly with proliferative vasculopathy
253159001,Schizencephaly
253160006,Colpocephaly
253186001,Chiari malformation type III
25362006,Phytanic acid storage disease
253699002,Isolation of common carotid artery
254243001,"Ash leaf spot, tuberous sclerosis"
254775002,Bregeat's syndrome
254972008,Malignant tumor of optic nerve and sheath
254973003,Malignant astrocytoma of optic nerve
254974009,Malignant tumor of optic nerve sheath
254975005,Malignant meningioma of optic nerve sheath
256321009,Disorder of neuromuscular transmission
257277002,Combined disorder of muscle AND peripheral nerve
25772007,Multi-infarct dementia with delusions
2593002,Dubowitz's syndrome
26015003,"Maroteaux-Lamy syndrome, intermediate form"
26021000119107,Vertigo as sequela of cerebrovascular disease
262711004,Transection of cervical cord
26360005,Hereditary optic atrophy
26595007,Congenital absence of part of brain
266253001,Precerebral arterial occlusion
266254007,Occlusion of carotid artery
266257000,Transient ischemic attack
267581004,Progressive myoclonic epilepsy
267592003,Motor cortex epilepsy
267604001,Myasthenic syndrome due to diabetic mellitus
268612007,Senile and presenile organic psychotic conditions
26954004,Thrombophlebitis of superior sagittal sinus
27148008,Hereditary motor end-plate disease
271986005,Disorder of brain ventricular shunt
274100004,Cerebral hemorrhage
275363001,Rupture of superficial cerebral vein
276219001,Occipital cerebral infarction
276594006,Perinatal rupture of superficial cerebral vein
276599001,Cerebral leukomalacia
277196008,Berry aneurysm
277299009,Ruptured cerebral arteriovenous malformation
277315000,Ruptured aneurysm of anterior cerebral artery
277316004,Ruptured aneurysm of middle cerebral artery
277319006,Ruptured aneurysm of posterior cerebral artery
277320000,Ruptured aneurysm of anterior communicating artery
277322008,Ruptured aneurysm of posterior communicating artery
277324009,Ruptured aneurysm of basilar artery
277325005,Ruptured aneurysm of posterior inferior cerebellar artery
277328007,Ruptured internal carotid-anterior communicating artery zone aneurysm
277329004,Ruptured internal carotid-posterior communicating artery zone aneurysm
277330009,Ruptured internal carotid bifurcation aneurysm
277373000,Severe childhood autosomal recessive muscular dystrophy
277530005,Malignant melanoma of meninges
277922001,Aprosencephaly
277949001,Combined malformation of central nervous system and skeletal muscle
277950001,Muscle eye brain disease
278284007,Right hemiplegia
278285008,Left hemiplegia
278286009,Right hemiparesis
278287000,Left hemiparesis
278510009,Localization-related idiopathic epilepsy
28055006,West syndrome
281004,Dementia associated with alcoholism
281411007,Spastic diplegia
28366008,Cerebral arteritis
284811000119102,Aneurysm of extracranial portion of internal carotid artery
284821000119109,Aneurysm of intracranial portion of internal carotid artery
284861000119104,Atherosclerosis of bilateral carotid arteries
284871000119105,Atherosclerosis of left carotid artery
284881000119108,Atherosclerosis of right carotid artery
285161000119105,Occlusion of left carotid artery
285171000119104,Occlusion of right carotid artery
285191000119103,Stenosis of left carotid artery
285201000119100,Stenosis of right carotid artery
286742002,Impending cerebrovascular accident
287731003,Cerebral ischemia
28778005,Phrenic nerve paralysis as birth trauma
28790007,Obstruction of precerebral artery
288631000119104,Vascular dementia with behavioral disturbance
288723005,Acute ill-defined cerebrovascular disease
28978003,Progressive supranuclear ophthalmoplegia
290401000119108,Complete paraplegia
290411000119106,Incomplete paraplegia
290461000119109,Spastic hemiplegia of left dominant side
290471000119103,Spastic hemiplegia of left nondominant side
290481000119100,Spastic hemiplegia of right dominant side
290491000119102,Spastic hemiplegia of right nondominant side
290581000119101,Ataxia due to and following cerebrovascular accident
290631000119103,Dysarthria due to and following cerebrovascular accident
290641000119107,Dysphagia due to and following non-traumatic intracerebral hemorrhage
290671000119100,Status epilepticus due to complex partial epileptic seizure
290681000119102,Status epilepticus due to refractory complex partial seizures
290691000119104,Status epilepticus due to generalized idiopathic epilepsy
290711000119101,Status epilepticus due to intractable idiopathic generalized epilepsy
290721000119108,Status epilepticus due to refractory epilepsy
290741000119102,Intractable idiopathic partial epilepsy
290761000119103,Status epilepticus due to refractory simple partial epilepsy
290791000119105,Fluency disorder due to and following cerebrovascular accident
290871000119101,Infantile spasms co-occurrent with status epilepticus
290881000119103,Refractory infantile spasms co-occurrent with status epilepticus
29093005,Crossed hemiparesis
291311000119108,Status epilepticus in benign Rolandic epilepsy
291351000119109,Spontaneous hemorrhage of subarachnoid space from basilar artery
291371000119100,Spontaneous hemorrhage of subarachnoid space from intracranial artery
291411000119104,Spontaneous hemorrhage of subarachnoid space from left posterior communicating artery
291481000119105,Spontaneous haemorrhage of subarachnoid space from right posterior communicating artery
29159009,Familial dysautonomia
291721000119102,Aphasia due to and following non-traumatic intracerebral hemorrhage
29188005,Complete bilateral paralysis
292621000119100,Occlusion of right vertebral artery
292631000119102,Occlusion of left vertebral artery
292851000119109,Lacunar ataxic hemiparesis of right dominant side
292861000119106,Lacunar ataxic hemiparesis of left dominant side
292991000119106,Eaton Lambert syndrome without underlying malignancy
29322000,Acute cerebrovascular insufficiency
293811000119100,Cerebral infarction due to vertebral artery stenosis
293831000119105,Cerebral infarction due to stenosis of precerebral artery
294041000119107,Flaccid hemiplegia of left dominant side
294051000119109,Flaccid hemiplegia of left nondominant side
294061000119106,Flaccid hemiplegia of right dominant side
294071000119100,Flaccid hemiplegia of right nondominant side
294101000119109,Hemiplegia of left dominant side
294111000119107,Hemiplegia of left nondominant side
294121000119100,Hemiplegia of right dominant side
294131000119102,Hemiplegia of right nondominant side
29426003,Paralytic syndrome
297138001,Embolus of circle of Willis
297157005,Intracranial venous thrombosis
297176007,Vertebral artery aneurysm
297278001,Metachromatic leukodystrophy due to deficiency of cerebroside sulfatase activator
29774004,Vascular myelopathy
298282001,Spastic quadriparesis
29941000119105,Ataxia as sequela of cerebrovascular disease
29951000119107,Ataxic hemiparesis
30023002,Hydranencephaly
300920004,Carotid atherosclerosis
302213007,Caroticocavernous sinus fistula
302878004,Intracranial septic thrombophlebitis
302879007,Septic thrombophlebitis of cavernous sinus
302880005,Septic thrombophlebitis of sagittal sinus
302887008,Neuropathy in secondary amyloidosis
302909007,Diffuse cerebrovascular disease
30400005,Middle meningeal hemorrhage following injury
305719002,Neuromyotonia
307356008,Motor epilepsy
307357004,"Jacksonian, focal or motor epilepsy"
307360006,Leucodystrophy without a known biochemical basis
307362003,Intracranial venous septic embolism
307363008,Multiple lacunar infarcts
307649006,Microglioma
307766002,Left sided cerebral infarction
307767006,Right sided cerebral infarction
30915001,Holoprosencephaly sequence
31076000,Congenital ischemic atrophy of central nervous system structure
31081000119101,Presenile dementia with delusions
31097004,Post poliomyelitis syndrome
31216003,Profound intellectual disability
312586003,Intracranial thrombophlebitis
312944002,Compressive optic atrophy
313434001,Residual hemiplegia
315608004,Cardiomyopathy in Duchenne muscular dystrophy
31839002,"Myasthenia gravis, adult form"
32162001,Facial hemiplegia
322112361000132104,Epilepsy due to scarring of brain
32875003,Inhalant-induced persisting dementia
329481000119106,Occlusion of right middle cerebral artery
329491000119109,Occlusion of left middle cerebral artery
329561000119101,Occlusion of right posterior cerebral artery
329571000119107,Occlusion of left posterior cerebral artery
330411000119109,Lacunar ataxic hemiparesis of left nondominant side
330421000119102,Lacunar ataxic hemiparesis of right nondominant side
33301000119105,Sequela of cardioembolic stroke
33316007,GM 2 gangliosidosis
33331000119103,Sequela of lacunar stroke
336191000119105,Occlusion of right central retinal artery
3371000119106,Refractory generalized convulsive epilepsy
341801000119101,Occlusion of left central retinal artery
34181000119102,Cerebral infarction due to occlusion of basilar artery
34191000119104,Cerebral infarction due to vertebral artery occlusion
347011000119102,Occlusion of bilateral central retinal arteries
34781003,Vertebral artery syndrome
352818000,Tonic-clonic epilepsy
35386004,Cavernous sinus syndrome
359683002,Complete optic atrophy
36025004,Fibrous skin tumor of tuberous sclerosis
361000119103,Paralytic syndrome on one side of the body as late effect of cerebrovascular accident
361123003,Psychomotor epilepsy
363235000,Hereditary disorder of nervous system
363474009,Malignant neoplasm of cerebral meninges
363497007,Malignant tumor of meninges
363498002,Malignant tumor of optic nerve
36803009,Idiopathic generalized epilepsy
3681008,Thrombophlebitis of torcular Herophili
371024007,Senile dementia with delusion
371026009,Senile dementia with psychosis
371029002,Ischemic disorder of spinal cord
371120001,Quadriplegic spinal paralysis
371129000,Paralysis from birth trauma
371158002,Disorder of basilar artery
371160000,Disorder of carotid artery
371313002,Congenital cerebellar cortical atrophy
372062007,Malignant neoplasm of central nervous system
372310001,Paralysis due to lesion of spinal cord
37340000,Motor neuron disease
373587001,Chiari malformation type II
37934003,Mitochondrial-lipid-glycogen storage myopathy
37943007,Multiple AND bilateral precerebral artery embolism
380941000000104,"Progressive encephalopathy with oedema, hypsarrhythmia and optic atrophy syndrome"
38228000,Paralysis of tongue
38523005,Syphilitic parkinsonism
38742007,Central retinal artery occlusion
387732009,Becker muscular dystrophy
389098007,Anoxic encephalopathy
389100007,Ischemic encephalopathy
390936003,Cerebral autosomal dominant arteriopathy with subcortical infarcts and leukoencephalopathy
39390005,"Niemann-Pick disease, type B"
396338004,Metachromatic leucodystrophy
397734008,Hereditary sensory and autonomic neuropathy type I
398040009,"Charcot-Marie-Tooth disease, type I"
398100001,Hereditary motor and sensory neuropathy
398148000,Hereditary sensory and autonomic neuropathy type II
398187000,"Charcot-Marie-Tooth disease, type II"
398229007,Amyloid polyneuropathy type I
398432008,Bulbar weakness
399091004,Facioscapulohumeral muscular dystrophy
40161000119102,Weakness of face muscles as sequela of stroke
402460000,Familial amyloid polyneuropathy with cutaneous amyloidosis
40259002,Progressive sensory ataxia of Charolais
40276003,Embolism of precerebral artery
40354009,De Lange syndrome
403815003,Axillary freckling due to neurofibromatosis
403816002,Multiple café-au-lait macules due to neurofibromatosis
403817006,Multiple neurofibromas in neurofibromatosis
403819009,Elephantiasis neurofibromatosa
40425004,Postconcussion syndrome
40450001,Embolism of superior sagittal sinus
404664002,Malignant optic glioma
404689008,Alternating hemiplegia
40632002,"Charcot-Marie-Tooth disease, type IA"
4069002,Anoxic brain damage during AND/OR resulting from a procedure
40700009,Severe intellectual disability
40802007,"Metachromatic leukodystrophy, congenital type"
40816002,Retropulsion petit mal
408371000000100,[X]Cerebral palsy and other paralytic syndromes
408664007,Pontine artery occlusion
408665008,Pontine artery thrombosis
40980002,Spastic paralysis due to birth injury
410057002,Hereditary AND/OR degenerative disease of central nervous system
41040004,Complete trisomy 21 syndrome
41142009,"Globoid cell leukodystrophy, late-onset"
41283003,Cerebro-oculo-facio-skeletal syndrome
413101007,Stress-induced epilepsy
414927004,Ocular myasthenia with strabismus
41574007,Paramyotonia congenita
41590007,"Familial amyloid polyneuropathy, Jewish type"
4183003,"Charcot-Marie-Tooth disease, type IC"
42012007,Neuronal ceroid lipofuscinosis
420718004,Central nervous system demyelinating disease associated with acquired immunodeficiency syndrome
420788006,Intraocular non-Hodgkin malignant lymphoma
421998001,Central nervous disorder associated with acquired immunodeficiency syndrome
422474003,Partial absence of septum pellucidum
422513000,"Epilepsy, not refractory"
422724001,Refractory localization-related epilepsy
422873003,Refractory epilepsia partialis continua
42295001,Familial amyloid polyneuropathy
423144007,Multifactorial encephalopathy
423771003,Acquired neuromuscular ptosis
424795008,Non dystrophic myotonia
425054007,Refractory occipital lobe epilepsy
425219008,Progressive spinal ataxia
425237009,Refractory frontal lobe epilepsy
425349008,Refractory parietal lobe epilepsy
425390006,Dementia associated with Parkinson's Disease
425420004,Thrombosis of internal carotid artery
425500002,Secondary progressive multiple sclerosis
425687007,Spina bifida aperta of cervical spine
425882004,Paralytic syndrome as late effect of stroke
425932008,Thrombosis of posterior communicating artery
426033005,Dysphagia as a late effect of cerebrovascular accident
426107000,Acute lacunar infarction
4262001,Phlebitis of superior sagittal sinus
426373005,Relapsing remitting multiple sclerosis
426651005,Occlusion of bilateral carotid arteries
426788002,Vertigo as late effect of stroke
426814001,Transient cerebral ischemia due to atrial fibrillation
427020007,Cerebral vasculitis
427296003,Thalamic infarction
427432001,Paralytic syndrome as late effect of thalamic stroke
427943001,Ophthalmoplegia due to diabetes mellitus
428700003,Primary progressive multiple sclerosis
429458009,Dementia due to Creutzfeldt Jakob disease
429466000,Spina bifida aperta of lumbar spine
42970005,Nonpyogenic thrombosis of intracranial venous sinus
42986003,"Charcot-Marie-Tooth disease, type IB"
429998004,Vascular dementia
430947007,Paralytic syndrome of nondominant side as late effect of stroke
430959006,Paralytic syndrome of dominant side as late effect of stroke
43100002,Late cortical cerebellar atrophy
432504007,Cerebral infarction
433183000,Neurogenic bladder as late effect of cerebrovascular accident
434541000124109,"Benign childhood epilepsy with centrotemporal spikes, refractory"
434551000124106,"Benign childhood epilepsy with centrotemporal spikes, non-refractory"
43532007,Hereditary oculoleptomeningeal amyloid angiopathy
43658003,Vertebral artery obstruction
438511000,Benign multiple sclerosis
439567002,Malignant multiple sclerosis
44145005,Benign Rolandic epilepsy
441526008,Infarct of cerebrum due to iatrogenic cerebrovascular accident
441529001,Dysphasia as late effect of cerebrovascular disease
441630004,Aphasia as late effect of cerebrovascular disease
441678004,Refractory generalized nonconvulsive epilepsy
441688003,Incomplete quadriplegia due to spinal cord lesion between first and fourth cervical vertebra
441705005,Complete quadriplegia due to spinal cord lesion between first and fourth cervical vertebra
441717007,Hemiplegia of nondominant side
441722007,Spastic hemiplegia of nondominant side
441735003,Sensory disorder as a late effect of cerebrovascular disease
441759008,Abnormal vision as a late effect of cerebrovascular disease
441794001,Incomplete quadriplegia due to spinal cord lesion between fifth and seventh cervical vertebra
441892008,Spastic hemiplegia of dominant side
441960006,Speech and language deficit as late effect of cerebrovascular accident
441980007,Complete quadriplegia due to spinal cord lesion between fifth and seventh cervical vertebra
441991000,Hemiparesis as late effect of cerebrovascular accident
442020005,Flaccid hemiplegia of dominant side
442024001,Hemiplegia as late effect of cerebrovascular disease
442077006,Flaccid hemiplegia of nondominant side
442155009,Hemiplegia of dominant side
442344002,Dementia due to Huntington chorea
442481002,Epilepsy characterized by intractable complex partial seizures
442511009,"Progressive encephalopathy with edema, hypsarrhythmia and optic atrophy syndrome"
442512002,Nonconvulsive status epilepticus
442617003,Aphasia as late effect of cerebrovascular accident
442668000,Hemiplegia of nondominant side as late effect of cerebrovascular disease
442676003,Hemiplegia of dominant side as late effect of cerebrovascular disease
442733008,Hemiplegia as late effect of cerebrovascular accident
44359008,"Metachromatic leukodystrophy, juvenile type"
443929000,Small vessel cerebrovascular disease
444024002,"Multiple system atrophy, cerebellar variant"
444172003,Recurrent transient cerebral ischemic attack
444197004,"Multiple system atrophy, Parkinson variant"
445109004,Isolation of left common carotid artery
445349004,Isolation of right common carotid artery
445355009,Refractory epilepsy
445475001,Paraneoplastic sensorimotor neuropathy
4463009,"Familial amyloid polyneuropathy, type II"
446311006,Acute bulbar poliomyelitis caused by Human poliovirus 2
446712002,Thromboembolus of precerebral artery
446957000,Acute bulbar poliomyelitis caused by Human poliovirus 1
446958005,Acute paralytic poliomyelitis caused by Human poliovirus 1
447262002,Acute paralytic poliomyelitis caused by Human poliovirus 2
447378002,Acute paralytic poliomyelitis caused by Human poliovirus 3
4477007,Juvenile myopathy AND lactate acidosis
448054001,Adult onset autosomal dominant leukodystrophy
448227009,X-linked periventricular heterotopia
448254007,Non-Hodgkin's lymphoma of central nervous system
448995000,Follicular non-Hodgkin's lymphoma of central nervous system
449221001,Diffuse non-Hodgkin's lymphoma of central nervous system
449305009,Paraneoplastic sensory neuropathy
45502001,Cerebrovascular amyloidosis
45853006,Roussy-Lévy syndrome
460307002,Systemic to pulmonary collateral artery from right carotid artery
460312001,Systemic to pulmonary collateral artery from left carotid artery
460890003,Anomalous common origin of brachiocephalic artery and left common carotid artery
460899002,Anomalous origin of left common carotid artery from brachiocephalic artery
461326001,Anomalous separate origins of internal carotid arteries and external carotid arteries from single aortic arch
46251005,Corticospinal motor disease
46252003,Progressive external ophthalmoplegia
46421000119102,Behavior disorder as sequela of cerebral infarction
46659004,Von Hippel-Lindau syndrome
46804001,Severe x-linked myotubular myopathy
472320005,Maternally inherited mitochondrial cardiomyopathy and myopathy
472746006,Cerebrovascular disorder due to paradoxical embolus
472916000,Toxic metabolic encephalopathy
47391000119107,Primary generalized absence epilepsy
47683004,"Metachromatic leukodystrophy, late infantile type"
48163001,Triparesis
48522003,Spinal cord disorder
48601000119107,Paralytic syndrome on one side of the body as effect of cerebrovascular accident
48601002,Thrombosis of precerebral artery
48662007,Cerebral paraplegia
49049000,Parkinson's disease
49562005,Adult chronic GM 2 gangliosidosis
49605003,Ophthalmoplegic migraine
49692006,Schilder's disease
49776008,Centrencephalic epilepsy
49793008,Hereditary motor neuron disease
49823009,Internuclear ophthalmoplegia
50582007,Hemiplegia
508171000000105,Severe learning disability
50866000,Childhood absence epilepsy
509341000000107,Petit-mal epilepsy
50967008,Gangliosidosis
5134006,"Familial amyloid polyneuropathy, type VI"
51500006,Complete trisomy 18 syndrome
52165006,"Niemann-Pick disease, type A"
52448006,Dementia
5262007,Spinal muscular atrophy
52677002,Deficiency of N-acetylgalactosamine-4-sulfatase
53633000,Peutz-Jeghers polyps of small bowel
53857003,Heredofamilial brachial plexus paralysis syndrome
54099005,Diplegia of upper limbs
54265003,Congenital anomaly of cerebral artery
54280009,Kugelberg-Welander disease
54364001,Lethal neonatal spasticity
54411001,Peutz-Jeghers syndrome
54519002,Basilar artery stenosis
55016009,Congenital muscular hypertrophy-cerebral syndrome
55051001,"Myasthenia gravis, juvenile form"
55382008,Cerebral atherosclerosis
55709000,Ethmocephalus
55734000,Endophlebitis of basilar sinus
56155002,Hemispheric cerebral agenesis
56267009,Multi-infarct dementia
56453003,"Hereditary cerebral amyloid angiopathy, Dutch type"
56989000,Eaton-Lambert syndrome
57938005,"Congenital myotonia, autosomal dominant form"
58263000,"Maroteaux-Lamy syndrome, severe form"
58459009,Sphingomyelin/cholesterol lipidosis
58557008,Spina bifida aperta
58610003,Leber's optic atrophy
58795000,Distal muscular dystrophy
590005,Congenital aneurysm of anterior communicating artery
5963005,Subacute neuronopathic Gaucher's disease
59636002,"Pelizaeus-Merzbacher disease, connatal variant"
60192008,Lethal multiple pterygium syndrome
60389000,Paraplegia
60706008,Phlebitis of torcular Herophili
608874000,Eaton Lambert syndrome with underlying malignancy
609553000,Paralytic syndrome of both lower limbs
609554006,Paralytic syndrome of all four limbs
609557004,Paralytic syndrome on one side of the body
61091005,Aneurysm of external carotid artery
6118003,Demyelinating disease of central nervous system
61200008,Pallidonigroluysian degeneration
62158001,Status marmoratus
62239001,Parkinson-dementia complex of Guam
62440002,Infantile GM 2 gangliosidosis
62702001,Cerebral vein occlusion
62914000,Cerebrovascular disease
62985007,Hereditary insensitivity to pain with anhidrosis
63081009,Acute infarction of spinal cord
63135006,Amyotonia congenita
63795001,Thrombosis of intracranial venous sinus of pregnancy AND/OR puerperium
64228003,Paralysis of diaphragm
64383006,Werdnig-Hoffmann disease
64586002,Carotid artery stenosis
64764001,"Acute paralytic poliomyelitis, bulbar"
64775002,Vertebral artery thrombosis
6481005,Diplegia
64855000,Pelizaeus-Merzbacher disease
65017003,Hereditary peripheral neuropathy
65084004,Vertebral artery embolism
65120008,Generalized convulsive epilepsy
65312002,Cerebral arteriosclerosis
65587001,Congenital anomaly of cerebrovascular system
65764006,Pseudo-Hurler polydystrophy
6594005,Cerebrovascular disorder in the puerperium
66521008,Deficiency of cerebroside-sulfatase
66751000,"Niemann-Pick disease, type C"
672441000119103,Hemiplegia of nondominant side due to and following ischemic cerebrovascular accident
672461000119104,Hemiplegia of dominant side due to and following ischemic cerebrovascular accident
672501000119104,Dysarthria due to and following ischemic cerebrovascular accident
672511000119101,Dysarthria due to and following hemorrhagic cerebrovascular accident
672521000119108,Dysphasia due to and following ischemic cerebrovascular accident
672531000119106,Dysphasia due to and following hemorrhagic cerebrovascular accident
672541000119102,Aphasia due to and following ischemic cerebrovascular accident
672551000119100,Aphasia due to and following hemorrhagic cerebrovascular accident
6729006,Cerebral-retinal arteriovenous aneurysm
674091000119108,Vertigo due to and following ischemic cerebrovascular accident
674111000119100,Ataxia due to and following ischemic cerebrovascular accident
674121000119107,Ataxia due to and following hemorrhagic cerebrovascular accident
674361000119104,Apraxia due to and following ischemic cerebrovascular accident
674381000119108,Weakness of facial muscle due to and following ischemic cerebrovascular accident
674391000119106,Speech and language deficit due to and following hemorrhagic cerebrovascular accident
674401000119108,Speech and language deficit due to and following ischemic cerebrovascular accident
67747009,Ocular muscular dystrophy
67854007,"Maroteaux-Lamy syndrome, mild form"
67855008,"Niemann-Pick disease, type C, subacute form"
67992007,Multiple AND bilateral precerebral artery obstruction
68186003,Congenital myopathy with abnormal subcellular organelles
68390005,Sphingolipid activator protein 1 deficiency
68618008,Rett's disorder
690171000119105,Weakness of facial muscle due to and following embolic cerebrovascular accident
690201000119109,Ataxia due to and following embolic cerebrovascular accident
690271000119104,Hemiplegia of nondominant side due to and following embolic cerebrovascular accident
690311000119104,Dysarthria due to and following embolic cerebrovascular accident
690321000119106,Aphasia due to and following embolic cerebrovascular accident
690331000119109,Speech and language deficit due to and following embolic cerebrovascular accident
690351000119103,Dysphasia due to and following embolic cerebrovascular accident
69131009,Spinal ataxia
69463008,Maroteaux-Lamy syndrome
69763009,Exophthalmic ophthalmoplegia
69798007,Carotid artery obstruction
697991001,Paralysis of uvula
698021005,Autosomal dominant nocturnal frontal lobe epilepsy
698291007,Acute paraplegia
698292000,Chronic paraplegia
698363002,Postoperative thromboembolus of precerebral artery
698624003,Dementia associated with cerebral lipidosis
698625002,Dementia associated with normal pressure hydrocephalus
698626001,Dementia associated with multiple sclerosis
698627005,Postoperative phlebitis and thrombophlebitis of intracranial sinuses
698687007,Post-traumatic dementia with behavioral change
698725008,Dementia associated with neurosyphilis
698726009,Dementia associated with viral encephalitis
698741009,Acute complete quadriplegia due to spinal cord lesion between first and fourth cervical vertebra
698742002,Chronic incomplete quadriplegia due to spinal cord lesion between first and fourth cervical vertebra
698743007,Acute complete quadriplegia due to spinal cord lesion between fifth and seventh cervical vertebra
698744001,Chronic incomplete quadriplegia due to spinal cord lesion between fifth and seventh cervical vertebra
698754002,Chronic paralysis due to lesion of spinal cord
698755001,Acute paralysis due to lesion of spinal cord
698760002,Generalized non-convulsive absence epilepsy
698762005,Refractory myoclonic epilepsy
698763000,Postoperative status epilepticus
698764006,Post infectious grand mal epilepsy
698767004,Post-cerebrovascular accident epilepsy
698781002,Dementia associated with cerebral anoxia
698846009,Tibial muscular dystrophy
698870008,2-hydroxyglutaric aciduria
698948009,Vascular dementia in remission
698949001,Dementia in remission
699184009,Perry syndrome
699190008,Paroxysmal extreme pain disorder
699688008,Generalized epilepsy with febrile seizures plus
699706000,Embolism of middle cerebral artery
700467001,Reversible cerebral vasoconstriction syndrome
70199000,I-cell disease
702326000,Progressive myoclonus epilepsy with ataxia
702327009,Monocarboxylate transporter 8 deficiency
702343002,Early onset myopathy with fatal cardiomyopathy
702363009,Cold-induced sweating syndrome
702382000,Inclusion body myopathy 2
702383005,Distal myopathy 2
702433001,"Congenital cataracts, facial dysmorphism and neuropathy"
702439002,Agenesis of corpus callosum with peripheral neuropathy
702441001,Fatal X-linked ataxia with deafness and loss of vision
702442008,Ataxia with vitamin E deficiency
702463005,Paralytic syndrome of two limbs
702464004,Paralytic syndrome of three limbs
702465003,Paralytic syndrome on both sides of the body
702575003,Retinocochleocerebral vasculopathy
702611008,Congenital brain aplasia
703163006,Secondary cerebrovascular disease
703166003,Dural arteriovenous fistula
703176000,Ruptured aneurysm of vertebral artery
703180005,Asymptomatic occlusion of extracranial carotid artery
703184001,Asymptomatic occlusion of intracranial carotid artery
703205008,Asymptomatic occlusion of posterior cerebral artery
703206009,Asymptomatic occlusion of basilar artery
703207000,Asymptomatic occlusion of anterior cerebral artery
703208005,Asymptomatic occlusion of middle cerebral artery
703218000,Cerebral vasoconstriction syndrome
703219008,Cerebral autosomal recessive arteriopathy with subcortical infarcts and leukoencephalopathy
703221003,Congenital intracranial vascular malformation
703226008,Familial cerebral saccular aneurysm
703266007,Cerebrofacial arteriovenous metameric syndrome
703267003,Cerebrofacial arteriovenous metameric syndrome type 1
703268008,Cerebrofacial arteriovenous metameric syndrome type 3
703300001,Hypoxic ischemic encephalopathy
7033004,Petit mal status
703301002,Mild hypoxic ischemic encephalopathy
703302009,Moderate hypoxic ischemic encephalopathy
703303004,Severe hypoxic ischemic encephalopathy
703304005,Hypoxic ischemic encephalopathy due to strangulation
703305006,Hypoxic ischemic encephalopathy due to cardiac arrest
703311009,Cerebral arteritis due to infectious disease
703312002,Primary cerebral arteritis
703313007,Cerebral amyloid angiopathy associated with systemic amyloidosis
703429003,Malignant optic glioma of adulthood
70350007,Degenerative myelopathy
703524005,Spinal muscular atrophy with progressive myoclonic epilepsy
703535000,Mowat-Wilson syndrome
703544004,Inclusion body myopathy with early-onset Paget disease and frontotemporal dementia
705066004,Dissection of internal carotid artery
705128004,Cerebral infarction due to embolism of middle cerebral artery
705129007,Thrombosis of middle cerebral artery
705130002,Cerebral infarction due to thrombosis of middle cerebral artery
70528007,Mucolipidosis
70607008,Thrombosis of superior sagittal sinus
70694009,Diabetes mellitus AND insipidus with optic atrophy AND deafness
709281006,Rippling muscle disease
70936005,"Multi-infarct dementia, uncomplicated"
709415008,Mitochondrial membrane protein associated neurodegeneration
709469005,Periodontitis co-occurrent with Down syndrome
710046001,Refractory idiopathic generalized epilepsy
710575003,Transient ischemic attack due to embolism
711151004,Hypomagnesemia with secondary hypocalcemia
711406009,Autosomal recessive axonal neuropathy with neuromyotonia
711409002,"3-methylglutaconic aciduria type IV with sensorineural deafness, encephalopathy and Leigh-like syndrome"
711483003,Spinal muscular atrophy with respiratory distress type 1
71253000,"Tay-Sachs disease, variant AB"
712637001,Ribonucleic acid polymerase III-related leukodystrophy
713035000,Dissection of precerebral artery
713081000,Dissection of cerebral artery
713265001,Nontraumatic ruptured cerebral aneurysm
713327005,Malignant meningioma of meninges of brain
713401006,Combined D-2-hydroxyglutaric aciduria and L-2-hydroxyglutaric aciduria
713488003,Presenile dementia co-occurrent with human immunodeficiency virus infection
713543002,Demyelinating disease of central nervous system co-occurrent with human immunodeficiency virus infection
713844000,Dementia co-occurrent with human immunodeficiency virus infection
71444005,Cerebral arterial thrombosis
715317001,Proximal myotonic myopathy
715340002,Autosomal recessive limb girdle muscular dystrophy type 2D
715341003,Autosomal recessive limb girdle muscular dystrophy type 2A
715344006,Neurofibromatosis Noonan syndrome
715345007,Young onset Parkinson disease
715374003,Autosomal dominant optic atrophy plus syndrome
715406003,Isolated lissencephaly type 1 without known genetic defect
715419004,Lethal congenital contracture syndrome type 2
715422002,Craniotelencephalic dysplasia
715429006,Congenital muscular dystrophy with infantile cataract and hypogonadism syndrome
715434005,Holoprosencephaly craniosynostosis syndrome
715565004,Lethal arthrogryposis co-occurrent with anterior horn cell disease
715624006,"Chronic ataxic neuropathy, ophthalmoplegia, monoclonal immunoglobulin M protein, cold agglutinin and disialosyl antibody syndrome"
715629001,Generalized epilepsy and paroxysmal dyskinesia syndrome
715645004,Hereditary thermosensitive neuropathy
715646003,Desmin related myopathy with Mallory body-like inclusions
715665006,Hereditary motor and sensory neuropathy Okinawa type
715666007,Charcot-Marie-Tooth disease type IE
715780008,Lissencephaly type 1 due to doublecortin gene mutation
715794009,Progressive encephalopathy with severe infantile anorexia
715795005,Charcot-Marie-Tooth disease type 4
715796006,Charcot-Marie-Tooth disease type 4A
715797002,Charcot-Marie-Tooth disease type 4C
715798007,Charcot-Marie-Tooth disease type 4D
715799004,Charcot-Marie-Tooth disease type 4G
715800000,Charcot-Marie-Tooth disease type 4B2
715801001,Charcot-Marie-Tooth disease type 4F
715802008,Charcot-Marie-Tooth disease type 4H
715803003,Charcot-Marie-Tooth disease type 4B1
715952000,Waardenburg syndrome co-occurrent with Hirschsprung disease
716091000,Holoprosencephaly and postaxial polydactyly syndrome
716107009,Early onset parkinsonism and intellectual disability syndrome
716169009,Holoprosencephaly sequence with hypokinesia and congenital joint contracture syndrome
716233007,Steinfeld syndrome
716243005,Deafness with malformation of ear and facial palsy syndrome
716278005,Jeavons syndrome
716662004,Autosomal dominant late onset Parkinson disease
716696006,Autosomal dominant centronuclear myopathy
716706009,Female restricted epilepsy with intellectual disability syndrome
716745004,Livedo reticularis and cerebrovascular accident syndrome
717008005,Autosomal dominant Charcot-Marie-Tooth disease type 2B
717010007,Autosomal dominant Charcot-Marie-Tooth disease type 2C
717011006,Autosomal dominant Charcot-Marie-Tooth disease type 2D
717012004,Autosomal dominant Charcot-Marie-Tooth disease type 2E
717013009,Autosomal dominant Charcot-Marie-Tooth disease type 2I
717014003,Autosomal dominant Charcot-Marie-Tooth disease type 2J
717016001,Autosomal dominant Charcot-Marie-Tooth disease type 2A1
717042001,Pelizaeus Merzbacher like disease
717223008,X-linked epilepsy with learning disability and behavior disorder syndrome
717266001,Sensory ataxic neuropathy with dysarthria and ophthalmoparesis syndrome
717336005,Autosomal dominant optic atrophy classic form
71779008,X-linked hydrocephalus syndrome
717812000,"Congenital cataract, hypertrophic cardiomyopathy, mitochondrial myopathy syndrome"
717825008,Hereditary sensory and autonomic neuropathy type 1B
717826009,Hereditary sensory and autonomic neuropathy with deafness and global delay
717943008,"Brain malformation, congenital heart disease, postaxial polydactyly syndrome"
717964007,Juvenile primary lateral sclerosis
717968005,Melanoma and neural system tumor syndrome
717975006,Autosomal dominant optic atrophy and peripheral neuropathy syndrome
717977003,Lissencephaly syndrome Norman Roberts type
718176005,Autosomal recessive limb girdle muscular dystrophy type 2C
718177001,Autosomal recessive limb girdle muscular dystrophy type 2F
718178006,Autosomal dominant limb girdle muscular dystrophy type 1B
718179003,Autosomal recessive limb girdle muscular dystrophy type 2B
718180000,Autosomal recessive limb girdle muscular dystrophy type 2I
718210003,Deficiency of monoamine oxidase A
718214007,Mitochondrial neurogastrointestinal encephalomyopathy syndrome
718221007,Behr syndrome
71831005,Symptomatic generalized epilepsy
718555006,Juvenile amyotrophic lateral sclerosis
718556007,Cranio-cerebello-cardiac dysplasia syndrome
718572004,Bethlem myopathy
718685006,Orthostatic hypotension co-occurrent and due to Parkinson's disease
718713000,Hypertrophic cardiomyopathy with hypotonia and lactic acidosis syndrome
718719001,Lissencephaly type 3 familial fetal akinesia sequence syndrome
718720007,Lissencephaly type 3 metacarpal bone dysplasia syndrome
718759003,Lissencephaly due to tubulin alpha 1A mutation
718847005,X-linked neurodegenerative syndrome Hamel type
718849008,X-linked neurodegenerative syndrome Bertini type
718850008,Autosomal recessive limb girdle muscular dystrophy type 2E
719069008,Shprintzen Goldberg craniosynostosis syndrome
719205008,Spondylometaphyseal dysplasia with cone-rod dystrophy syndrome
719395001,Microcephalus facio-cardio-skeletal syndrome Hadziselimovic type
719430008,Leber plus disease
719510006,Autosomal dominant Charcot-Marie-Tooth disease type 2F
719511005,Autosomal dominant Charcot-Marie-Tooth disease type 2G
719512003,Autosomal dominant Charcot-Marie-Tooth disease type 2K
719513008,Autosomal dominant Charcot-Marie-Tooth disease type 2L
719514002,Autosomal dominant Charcot-Marie-Tooth disease type 2M
719515001,Autosomal dominant Charcot-Marie-Tooth disease type 2N
719517009,Autosomal dominant optic atrophy and cataract
719717006,Psychosis co-occurrent and due to Parkinson's disease
719815005,X-linked myopathy with excessive autophagy
719819004,Xeroderma pigmentosum and Cockayne syndrome complex
719836007,X-linked distal arthrogryposis multiplex congenita
719838008,X-linked hereditary sensory and autonomic neuropathy with deafness
7199000,Tuberous sclerosis syndrome
719979008,Charcot-Marie-Tooth disease type ID
719980006,Charcot-Marie-Tooth disease type IF
719981005,Charcot-Marie-Tooth disease type 2B2
719985001,Autosomal dominant limb girdle muscular dystrophy type 1A
719986000,Autosomal dominant limb girdle muscular dystrophy type 1C
719987009,Autosomal dominant limb girdle muscular dystrophy type 1D
719988004,Autosomal dominant limb girdle muscular dystrophy type 1E
719989007,Autosomal dominant limb girdle muscular dystrophy type 1F
719990003,Autosomal dominant limb girdle muscular dystrophy type 1G
720410001,Acrootoocular syndrome
720519003,"Atherosclerosis, deafness, diabetes, epilepsy, nephropathy syndrome"
720522001,Autosomal recessive limb girdle muscular dystrophy type 2G
720523006,Autosomal recessive limb girdle muscular dystrophy type 2K
720626009,Dissection of carotid artery
720634003,"Cerebellar ataxia, areflexia, pes cavus, optic atrophy, sensorineural hearing loss syndrome"
720637005,Charcot-Marie-Tooth disease type 2H
720638000,Charcot-Marie-Tooth disease type 4J
720809000,Dissection of external carotid artery
720852000,Cervical hypertrichosis and peripheral neuropathy syndrome
720855003,Cerebrooculonasal syndrome
721088003,"Developmental delay, epilepsy, neonatal diabetes syndrome"
721200000,Early-onset X-linked optic atrophy
721221000,Hirschsprung disease with deafness and polydactyly syndrome
721222007,Hirschsprung disease with type D brachydactyly syndrome
721223002,Hirschsprung disease with nail hypoplasia and dysmorphism
721297008,Galloway Mowat syndrome
721843003,"Growth retardation, alopecia, pseudoanodontia, optic atrophy syndrome"
721979005,Lymphedema and cerebral arteriovenous anomaly syndrome
722004001,Agenesis of internal carotid artery
722006004,Isotretinoin embryopathy-like syndrome
722064003,Odontoleukodystrophy
722110003,"Osteogenesis imperfecta, retinopathy, seizures, intellectual disability syndrome"
722209002,"Spastic paraplegia, intellectual disability, palmoplantar hyperkeratosis syndrome"
722213009,Severe X-linked intellectual disability Gustavson type
722283003,"Agnathia, holoprosencephaly, situs inversus syndrome"
722294004,Autosomal dominant intermediate Charcot-Marie-Tooth disease type E
722377004,Paraganglioma and gastric stromal sarcoma syndrome
722389002,Congenital hereditary facial paralysis with variable hearing loss syndrome
722432000,"Duane anomaly, myopathy, scoliosis syndrome"
722456001,"Intellectual disability, developmental delay, contracture syndrome"
722599008,Parkinsonism due to hereditary spastic paraplegia
722671009,Metastatic malignant neoplasm of meninges
722718001,Primary malignant meningioma
722977005,Dementia co-occurrent and due to neurocysticercosis
722978000,Dementia caused by toxin
722979008,Dementia due to metabolic abnormality
722980006,Dementia due to chromosomal anomaly
722987009,Amyotrophic lateral sclerosis plus syndrome
722990003,Congenital atrophy of optic nerve
722997000,Inherited autonomic nervous system disorder
723082006,Silent cerebral infarct
723083001,Late effects of cerebral ischemic stroke
723084007,Sequela of non-traumatic intracerebral hemorrhage
723124007,Primary progressive apraxia of speech
723125008,Epileptic encephalopathy
723156000,Flaccid diplegia of upper limbs
723157009,Spastic diplegia of upper limbs
723158004,Diplegia of lower limbs
723304001,"Microcephaly, seizure, intellectual disability, heart disease syndrome"
723306004,Facial onset sensory and motor neuronopathy syndrome
723308003,Epidermolysis bullosa simplex with muscular dystrophy
723366001,"Macrostomia, preauricular tag, external ophthalmoplegia syndrome"
723390000,Rapidly progressive dementia
723405001,Microlissencephaly micromelia syndrome
723452007,"Polyneuropathy, hearing loss, ataxia, retinitis pigmentosa, cataract syndrome"
723497003,Peripheral neuropathy with sensorineural hearing impairment syndrome
723621000,"Spastic tetraplegia, retinitis pigmentosa, intellectual disability syndrome"
723622007,X-linked spastic paraplegia type 2
723676007,"Severe intellectual disability, epilepsy, anal anomaly, distal phalangeal hypoplasia syndrome"
723825006,Autosomal recessive spastic paraplegia type 55
723826007,Autosomal recessive spastic paraplegia type 57
723857007,Silent micro-hemorrhage of brain
724091002,Neuroectodermal melanolysosomal disease
724138007,Mitochondrial myopathy with sideroblastic anemia syndrome
724146008,Metaphyseal chondromatosis co-occurrent with D-2 hydroxyglutaric aciduria
724207001,Kleefstra syndrome
724349009,"Hereditary inclusion body myopathy, joint contracture, ophthalmoplegia syndrome"
724357007,Hereditary cerebral hemorrhage with amyloidosis
724427002,Asymptomatic stenosis of intracranial artery
724428007,Asymptomatic stenosis of extracranial artery
724549005,Epilepsy due to infectious disease of central nervous system
724572007,Neuromuscular junction disorder caused by organic phosphorus compound ingestion
724576005,Pyridoxal 5-phosphate dependent epilepsy
724643004,Transient abnormal myelopoiesis co-occurrent with Down syndrome
724644005,Myeloid leukemia co-occurrent with Down syndrome
724761004,Sporadic Parkinson disease
724769002,Ataxia co-occurrent and due to phytanic acid storage disease
724776007,Dementia due to disorder of central nervous system
724777003,Dementia due to infectious disease
724778008,Progressive relapsing multiple sclerosis
724780002,Demyelination of central nervous system co-occurrent and due to neurosarcoidosis
724781003,Demyelination of central nervous system co-occurrent and due to systemic lupus erythematosus
724782005,Demyelination of central nervous system co-occurrent and due to Sjogren disease
724783000,Demyelination of central nervous system co-occurrent and due to Behcet disease
724784006,Demyelination of central nervous system co-occurrent and due to mitochondrial disease
724785007,Epilepsy due to perinatal stroke
724786008,Epilepsy due to perinatal anoxic-ischemic brain injury
724787004,Epilepsy due to cerebrovascular accident
724788009,Epilepsy due to and following traumatic brain injury
724789001,Epilepsy due to intracranial tumor
724813004,Autonomic nervous system disorder co-occurrent and due to neurodegenerative disorder
724819000,Functional paraparesis
724820006,Functional hemiparesis
72488000,"Niemann-Pick disease, type C, chronic form"
724990004,Epilepsy due to immune disorder
724991000,Epilepsy co-occurrent and due to demyelinating disorder
724992007,Epilepsy co-occurrent and due to dementia
724993002,Cerebral ischemic stroke due to occlusion of extracranial large artery
724994008,Cerebral ischemic stroke due to stenosis of extracranial large artery
724999003,Isolated optic nerve hypoplasia
725042001,Autosomal recessive limb girdle muscular dystrophy type 2J
725043006,Autosomal recessive limb girdle muscular dystrophy type 2O
725047007,Autosomal recessive Charcot-Marie-Tooth disease with hoarseness
725048002,Charcot-Marie-Tooth disease type 2B1
725097006,Crisponi syndrome
725139005,"Spastic paraplegia, optic atrophy, neuropathy syndrome"
725146001,Atypical juvenile parkinsonism
725163002,"X-linked spasticity, intellectual disability, epilepsy syndrome"
725296006,Mucolipidosis type IV
725420009,Congenital muscular dystrophy Paradas type
725464001,Adult-onset chronic progressive external ophthalmoplegia with mitochondrial myopathy
725898002,Delirium co-occurrent with dementia
725907002,Autosomal recessive limb girdle muscular dystrophy type 2Y
726031001,"Cerebellar ataxia, intellectual disability, optic atrophy, skin abnormalities syndrome"
726051002,Myotonia congenita
726107008,Distal myopathy Welander type
72655000,Alternating hypoglossal hemiplegia
726614009,Autosomal recessive limb girdle muscular dystrophy type 2P
726615005,Autosomal recessive limb girdle muscular dystrophy type 2Q
726616006,Autosomal recessive limb girdle muscular dystrophy type 2L
726617002,Autosomal recessive limb girdle muscular dystrophy type 2N
726618007,Autosomal recessive limb girdle muscular dystrophy type 2M
726669007,"Central nervous system calcification, deafness, tubular acidosis, anemia syndrome"
726704006,"Cataract, congenital heart disease, neural tube defect syndrome"
73173006,Spasm of cerebral arteries
73192008,Multiple AND bilateral precerebral artery stenosis
732245008,Pure mitochondrial myopathy
732261005,Cyprus facial neuromusculoskeletal syndrome
732264002,Coenzyme A synthase protein associated neurodegeneration
732929002,Autosomal recessive limb girdle muscular dystrophy type 2S
732930007,Autosomal recessive limb girdle muscular dystrophy type 2T
732931006,Autosomal recessive limb girdle muscular dystrophy type 2R
732951005,"Mitochondrial myopathy, lactic acidosis, deafness syndrome"
732959007,Beta-propeller protein-associated neurodegeneration
73297009,Muscular dystrophy
733028000,"Multiple sclerosis, ichthyosis, factor VIII deficiency syndrome"
733032006,Epilepsy telangiectasia syndrome
733044009,Dermatoleukodystrophy
733068001,"Absent tibia, polydactyly, arachnoid cyst syndrome"
733071009,"Deafness, small bowel diverticulosis, neuropathy syndrome"
733082001,Early-onset Lafora body disease
733091002,Isolated hereditary congenital facial paralysis
733184002,Dementia caused by heavy metal exposure
733185001,Dementia following injury caused by exposure to ionizing radiation
733190003,Dementia due to primary malignant neoplasm of brain
733191004,Dementia due to chronic subdural hematoma
733192006,Dementia due to herpes encephalitis
733194007,Dementia co-occurrent and due to Down syndrome
733195008,Epilepsy of infancy with migrating focal seizures
733199002,Multifocal cerebral infarction due to and following procedure on cardiovascular system
733469003,"Hereditary congenital hypomelanotic and hypermelanotic cutaneous macules, growth retardation, intellectual disability syndrome"
733489002,Distal myopathy with posterior leg and anterior hand involvement
733599009,Adult-onset multiple mitochondrial deoxyribonucleic acid deletion syndrome due to deoxyguanosine kinase deficiency
733623005,"Autism spectrum disorder, epilepsy, arthrogryposis syndrome"
733630004,Deficiency of alpha-ketoglutarate dehydrogenase
733636005,3-phosphoglycerate dehydrogenase deficiency juvenile form
733650000,Adult familial nephronophthisis with spastic quadriparesia syndrome
73390009,Endophlebitis of cavernous venous sinus
733926004,Ganglioneuroblastoma of central nervous system
734017008,"Ectodermal dysplasia, intellectual disability, central nervous system malformation syndrome"
734022008,Wolfram-like syndrome
734066005,Diffuse large B-cell lymphoma of central nervous system
734099007,Neuroblastoma of central nervous system
734326000,Stenosis of left vertebral artery
734327009,Stenosis of right vertebral artery
734374000,Thrombosis of left carotid artery
734382000,Thrombosis of right carotid artery
734383005,Thrombosis of left middle cerebral artery
734384004,Thrombosis of right middle cerebral artery
734396006,Spontaneous rupture of left posterior communicating artery
734397002,Spontaneous rupture of right posterior communicating artery
734434007,Pyridoxine-dependent epilepsy
734879002,Ruptured aneurysm of right posterior communicating artery
734880004,Ruptured aneurysm of left posterior communicating artery
734959006,Embolus of left cerebellar artery
734960001,Embolus of right cerebellar artery
734961002,Embolus of left posterior cerebral artery
734963004,Embolus of right posterior cerebral artery
734964005,Embolus of left middle cerebral artery
734965006,Embolus of right middle cerebral artery
735114006,Occlusion of right pontine artery
735115007,Occlusion of left pontine artery
735131004,Occlusion of left cerebellar artery
735132006,Occlusion of right cerebellar artery
73663008,Neurologic xeroderma pigmentosum
737159004,Aneurysm of basilar artery
737160009,Dissection of basilar artery
7379000,Pseudobulbar palsy
74073002,Cerebellar hemangioblastomatosis
75023009,Post-traumatic epilepsy
75046006,Combined pyramidal-extrapyramidal syndrome
75072002,Nemaline myopathy
75111000,Painful ophthalmoplegia
751371000000107,Personal history of transient ischaemic attack
75138007,Endophlebitis of superior sagittal sinus
75299005,Spastic spinal syphilitic paralysis
75491005,Amyotrophia congenita
75543006,Cerebral embolism
76043009,"Hereditary sensory-motor neuropathy, type V"
762350007,Dementia due to prion disease
762351006,Dementia due to and following injury of head
762352004,Demyelination due to systemic vasculitis
762629007,Occlusion of right middle cerebral artery by embolus
762630002,Occlusion of left middle cerebral artery by embolus
762632005,Occlusion of left cerebellar artery by embolus
762633000,Occlusion of right cerebellar artery by embolus
762648006,Stenosis of right cerebellar artery
762649003,Stenosis of left cerebellar artery
762651004,Occlusion of right posterior cerebral artery by embolus
762652006,Occlusion of left posterior cerebral artery by embolus
762707000,Subcortical dementia
763067000,Autosomal dominant congenital benign spinal muscular atrophy
763135001,Charcot-Marie-Tooth disease type 4E
763136000,"Charcot-Marie-Tooth disease, deafness, intellectual disability syndrome"
763314009,Congenital muscular dystrophy with hyperlaxity
763315005,Congenital myopathy with myasthenic-like onset
763345008,Charcot-Marie-Tooth disease type 4B3
763347000,X-linked Charcot-Marie-Tooth disease type 6
763400005,X-linked Charcot-Marie-Tooth disease type 4
763455008,X-linked Charcot-Marie-Tooth disease type 1
763457000,X-linked Charcot-Marie-Tooth disease type 2
763458005,X-linked Charcot-Marie-Tooth disease type 3
763460007,X-linked Charcot-Marie-Tooth disease type 5
763533003,Distal hereditary motor neuropathy Jerash type
763534009,Hot water reflex epilepsy
763622006,Thinking epilepsy
763632004,Startle epilepsy
763669001,Spastic ataxia with congenital miosis
763718009,Finnish upper limb onset distal myopathy
763743003,"Intellectual disability, spasticity, ectrodactyly syndrome"
763776004,Kelch like family member 9 related early-onset distal myopathy
763802009,Micturition induced epilepsy
763827002,Orgasm induced epilepsy
763829004,Oculopharyngodistal myopathy
763895001,Myosclerosis
76402003,Carotid artery insufficiency syndrome
764453009,Action myoclonus renal failure syndrome
764522009,Familial focal epilepsy with variable foci
764525006,Cylindrical spirals myopathy
764730007,Autosomal dominant Charcot-Marie-Tooth disease type 2 due to kinesin family member 5A mutation
764733009,"Progressive external ophthalmoplegia, myopathy, emaciation syndrome"
764812008,Autosomal recessive myogenic arthrogryposis multiplex congenita
764850002,Autosomal dominant Charcot-Marie-Tooth disease type 2A2
764854006,Autosomal dominant slowed nerve conduction velocity
764859001,Laing early-onset distal myopathy
764944006,Congenital muscular dystrophy type 1B
764945007,Congenital myopathy with internal nuclei and atypical cores
765046002,Autosomal dominant Charcot-Marie-Tooth disease type 2U
765047006,"SURF1, cytochrome c oxidase assembly factor related Charcot-Marie-Tooth disease type 4"
765093009,"Rolandic epilepsy, speech dyspraxia syndrome"
765170001,Sodium voltage-gated channel alpha subunit 8-related epilepsy with encephalopathy
765197008,Symptomatic form of muscular dystrophy of Duchenne and Becker in female carrier
765202001,Familial multiple benign meningioma
765216006,Audiogenic epilepsy
765325002,"Peripheral demyelinating neuropathy, central dysmyelinating leukodystrophy, Waardenburg syndrome, Hirschsprung disease"
765331004,Autosomal dominant polycystic kidney disease type 1 with tuberous sclerosis
765434008,Human immunodeficiency virus type I enhancer binding protein 2 related intellectual disability
765744006,Autosomal dominant intermediate Charcot-Marie-Tooth disease type A
765745007,Autosomal dominant intermediate Charcot-Marie-Tooth disease type B
765746008,Autosomal dominant intermediate Charcot-Marie-Tooth disease type C
765747004,Autosomal dominant intermediate Charcot-Marie-Tooth disease type D
765758008,Microcephalic primordial dwarfism Montreal type
766032007,"Holoprosencephaly, ectrodactyly, cleft lip, cleft palate syndrome"
766044005,Acute encephalopathy with biphasic seizures and late reduced diffusion
766251006,Lethal infantile mitochondrial myopathy
76670001,Duchenne muscular dystrophy
766752000,Neurolymphomatosis
766753005,Nijmegen breakage syndrome-like disorder
766764008,X-linked distal spinal muscular atrophy type 3
766815007,Perioral myoclonia with absences
766931003,Hypomyelination neuropathy arthrogryposis syndrome
766977007,Severe early-onset axonal neuropathy due to mitofusin 2 deficiency
766987006,Moebius syndrome
768473009,Purine rich element binding protein A syndrome
768555009,5q31.3 microdeletion syndrome
768666006,Syntaxin binding protein 1 encephalopathy with epilepsy
76880004,Angelman syndrome
769065000,Tubulin beta 4A class IVa related leukodystrophy
77015008,Crossed hemiplegia
770430000,Autosomal recessive distal spinal muscular atrophy type 3
770431001,"Early-onset epileptic encephalopathy and intellectual disability due to glutamate receptor, ionotropic, N-methyl-D-aspartate, subunit 2A mutation"
770438007,Infantile spasm and broad thumb syndrome
770560008,Lissencephaly due to LIS1 mutation
770596007,Rippling muscle disease with myasthenia gravis
770623004,Benign occipital lobe epilepsy
770624005,Benign partial epilepsy of infancy with complex partial seizures
770625006,Combined immunodeficiency with faciooculoskeletal anomalies syndrome
770626007,Congenital Horner syndrome
770627003,Desmin-related myofibrillar myopathy
770630005,Distal hereditary motor neuropathy type 1
770655004,"Microcephalus, brain defect, spasticity, hypernatremia syndrome"
770723007,"Optic atrophy, intellectual disability syndrome"
770727008,Spinal muscular atrophy with respiratory distress type 2
770758009,New-onset refractory status epilepticus
770759001,Autosomal dominant intermediate Charcot-Marie-Tooth disease type F
770786001,Hereditary inclusion body myopathy type 4
770792007,Adult-onset distal myopathy due to valosin containing protein mutation
77097004,Oculopharyngeal muscular dystrophy
771081007,Distal hereditary motor neuropathy type 7
771141002,Benign partial epilepsy with secondarily generalized seizures in infancy
771143004,Hereditary motor and sensory neuropathy type 5
771144005,Hereditary motor and sensory neuropathy with acrodystrophy
771147003,Isolated arhinencephaly
771238004,"Spinal atrophy, ophthalmoplegia, pyramidal syndrome"
771261002,Digital extensor muscle aplasia with polyneuropathy
771263004,Ptosis and vocal cord paralysis syndrome
771267003,Congenital muscular dystrophy with integrin alpha-7 deficiency
771272007,Congenital muscular dystrophy due to lamin A/C mutation
771302009,Autosomal recessive lower motor neuron disease with childhood onset
771304005,Benign nocturnal alternating hemiplegia of childhood
771307003,Charcot-Marie-Tooth disease type 2B5
771334000,Autosomal dominant limb-girdle muscular dystrophy type 1H
771336003,Polymicrogyria with optic nerve hypoplasia
771448004,Autism epilepsy syndrome due to branched chain ketoacid dehydrogenase kinase deficiency
771471002,"Optic nerve edema, splenomegaly syndrome"
771475006,Young adult-onset distal hereditary motor neuropathy
771509001,Hypertrophic cardiomyopathy and renal tubular disease due to mitochondrial deoxyribonucleic acid mutation
771514002,"Early-onset progressive neurodegeneration, blindness, ataxia, spasticity syndrome"
772129007,Autosomal dominant childhood-onset proximal spinal muscular atrophy
773230003,Cyclin-dependent kinase-like 5 deficiency
773306002,Congenital lethal myopathy Compton North type
773308001,Autosomal recessive intermediate Charcot-Marie-Tooth disease type A
773330000,Autosomal recessive intermediate Charcot-Marie-Tooth disease type B
773393001,Autosomal dominant Charcot-Marie-Tooth disease type 2Q
773398005,"Congenital cataract, progressive muscular hypotonia, hearing loss, developmental delay syndrome"
773414009,Autosomal recessive intermediate Charcot-Marie-Tooth disease type C
773415005,Contiguous ABCD1 DXS1357E deletion syndrome
773421009,Infantile-onset mesial temporal lobe epilepsy with severe cognitive regression
773492007,Childhood-onset spasticity with hyperglycinemia
773555005,Severe neurodegenerative syndrome with lipodystrophy
773643006,"Multiple congenital anomalies, hypotonia, seizures syndrome type 2"
773648002,"Congenital cataract, hearing loss, severe developmental delay syndrome"
773737004,Nephrocystin 3-related Meckel-like syndrome
774069007,Protein kinase cAMP-dependent type I regulatory subunit beta-related neurodegenerative dementia with intermediate filaments
774070008,"Fibulin 1-related developmental delay, central nervous system anomaly, syndactyly syndrome"
774147002,Charcot-Marie-Tooth disease type 2R
774149004,"Severe intellectual disability, progressive postnatal microcephaly, midline stereotypic hand movements syndrome"
774150004,"Sacral agenesis, abnormal ossification of vertebral bodies, persistent notochordal canal syndrome"
774205007,"Growth and developmental delay, hypotonia, vision impairment, lactic acidosis syndrome"
77461000119109,Myasthenia gravis with exacerbation
77471000119103,Myasthenia gravis without exacerbation
77659000,Paraneoplastic neuropathy
777999008,Hypomyelination with brain stem and spinal cord involvement and leg spasticity
778001003,Potassium voltage-gated channel subfamily Q member 2 related epileptic encephalopathy
778003000,Autosomal dominant intermediate Charcot-Marie-Tooth disease with neuropathic pain
778021002,"Microphthalmia, retinitis pigmentosa, foveoschisis, optic disc drusen syndrome"
778027003,Primary CD59 deficiency
778047006,Myoclonic epilepsy in non-progressive encephalopathy
778063003,Cryptogenic late-onset epileptic spasms
77835008,Ophthalmoplegia plus syndrome
77956009,Steinert myotonic dystrophy syndrome
780827006,Synaptic Ras GTPase activating protein 1- related intellectual disability
78097002,Total ophthalmoplegia
782675008,Distal myopathy with anterior tibial onset
782723007,"Severe intellectual disability, progressive spastic diplegia syndrome"
782739000,Male emopamil-binding protein disorder with neurological defect
782742006,Autosomal dominant Charcot-Marie-Tooth disease type 2 with giant axons
782744007,Lipoic acid synthetase deficiency
782752005,"Peripheral neuropathy, myopathy, hoarseness, hearing loss syndrome"
782754006,"Foveal hypoplasia, optic nerve decussation defect, anterior segment dysgenesis syndrome"
782822006,Infantile cerebellar and retinal degeneration
782824007,Sodium channelopathy-related small fiber neuropathy
782826009,Charcot-Marie-Tooth disease type 2P
782829002,Autosomal dominant Charcot-Marie-Tooth disease type 2O
782881002,Hereditary sensorimotor neuropathy with hyperelastic skin
782886007,"Infantile spasms, psychomotor retardation, progressive brain atrophy, basal ganglia disease syndrome"
782887003,Inherited congenital spastic tetraplegia
782941005,Richieri Costa-da Silva syndrome
782945001,"Ophthalmoplegia, intellectual disability, lingua scrotalis syndrome"
783057002,DNA replication helicase/nuclease 2-related mitochondrial deoxyribonucleic acid deletion syndrome
78306007,Epidural ascending spinal paralysis
783065004,Autosomal recessive optic atrophy type 7
783091003,"46,XY gonadal dysgenesis, motor and sensory neuropathy syndrome"
783148005,Distal nebulin myopathy
783160006,Hereditary gelsolin amyloidosis
783166000,Distal anoctaminopathy
783175003,Congenital muscular dystrophy without intellectual disability
783413008,Multiple aneurysms of cerebral artery
783415001,Aneurysm of internal carotid bifurcation
783416000,Aneurysm of anterior cerebral artery
783417009,Aneurysm of posterior inferior cerebellar artery
783418004,Aneurysm of anterior communicating artery
783419007,Aneurysm of posterior cerebral artery
783420001,Aneurysm of middle cerebral artery
783421002,Aneurysm of posterior communicating artery
783422009,Aneurysm of internal carotid-anterior communicating artery zone
783423004,Aneurysm of internal carotid-posterior communicating artery zone
783550006,Hereditary sensory and autonomic neuropathy type 7
783554002,Autosomal recessive limb girdle muscular dystrophy type 2U
783558004,Combined oxidative phosphorylation defect type 11
783618006,Lower motor neuron syndrome with late-adult onset
783629005,Congenital aneurysm of cerebral artery
783630000,Congenital aneurysm of precerebral artery
783707003,Cerebral aneurysm due to dissection of cerebral artery
783716004,Acquired aneurysm of cerebral artery
783722008,Myopathy and diabetes mellitus
783731008,Fibromuscular dysplasia of wall of carotid artery
783733006,Fibromuscular dysplasia of wall of bilateral carotid arteries
783739005,Familial temporal lobe epilepsy
784341001,Amyotrophic lateral sclerosis type 4
784346006,Navajo neurohepatopathy
784347002,"Autosomal recessive spastic ataxia, optic atrophy, dysarthria syndrome"
784352007,X-linked scapuloperoneal muscular dystrophy
784370005,Mitochondrial myopathy with reversible cytochrome C oxidase deficiency
784372002,Familial mesial temporal lobe epilepsy with febrile seizures
784377008,Autosomal dominant epilepsy with auditory features
784391002,Autosomal dominant adult-onset proximal spinal muscular atrophy
78468005,Erb's muscular dystrophy
785299009,Cobblestone lissencephaly without muscular or ocular involvement
785809005,Mills syndrome
785810000,Synucleinopathy
78689005,Chronic brain syndrome
787037000,Congenital muscular dystrophy type 1A
787044009,Stenosis of bilateral carotid arteries
787172004,Childhood-onset autosomal recessive myopathy with external ophthalmoplegia
788417006,"Alopecia, epilepsy, intellectual disability syndrome Moynahan type"
788454002,Stenosis of bilateral vertebral arteries
788455001,Occlusion of bilateral pontine arteries
788898005,Dementia caused by volatile inhalant
789005009,Paralysis of uvula after diphtheria
789674008,"Spastic paraplegia, optic atrophy, neuropathy and spastic paraplegia, optic atrophy neuropathy-related disorder"
791000124107,2-methyl-3-hydroxybutyric aciduria
7931000119101,Anterior choroidal artery thrombosis
79633009,Spastic hemiplegia
79745005,Reflex epilepsy
80328002,Progressive cone-rod dystrophy
80544005,Spongy degeneration of central nervous system
80606009,Carotid artery embolism
80690008,Degenerative disease of the central nervous system
80901002,Endophlebitis of torcular Herophili
80935004,Flaccid hemiplegia
80976008,Myasthenic crisis
81211007,Primary lateral sclerosis
81308009,Disorder of brain
8166000,Thrombophlebitis of basilar sinus
816984002,Progressive multiple sclerosis
81854007,Alexander's disease
818967003,Medulloepithelioma of central nervous system
82077006,Myotubular myopathy
82361000119107,Altered behavior in dementia due to Huntington chorea
82371000119101,Dementia due to multiple sclerosis with altered behavior
82381000119103,Epileptic dementia with behavioral disturbance
82501000119102,Anaplastic astrocytoma of central nervous system
8269002,Cerebrospinal angiopathy
827115000,Autosomal dominant progressive external ophthalmoplegia
827117008,Autosomal recessive progressive external ophthalmoplegia
8291000119107,Atonic epilepsy
838275008,Stenosis of cerebral artery
838307002,Childhood-onset autosomal dominant optic atrophy
838308007,Fibromuscular dysplasia of wall of intracranial artery
838309004,Cerebrovascular abnormality due to Takayasu disease
83832001,Metachromatic leukodystrophy without arylsulfatase deficiency
838345001,Autosomal recessive optic atrophy type 6
840419005,Dissection of extracranial carotid artery
840420004,Dissection of extracranial vertebral artery
840422007,Dissection of anterior cerebral artery
840434004,Dissection of posterior cerebral artery
840436002,Dissection of middle cerebral artery
840437006,Dissection of multiple cerebral arteries
840438001,Dissection of intracranial vertebral artery
840439009,Dissection of intracranial carotid artery
840441005,Dissection of intracranial artery
840464007,Dementia due to carbon monoxide poisoning
840505007,Down syndrome co-occurrent with leukemoid reaction associated transient neonatal pustulosis
84160009,Laryngeal hemiplegia
84161000119100,Partial epileptic seizure of parietal lobe with impairment of consciousness
84171000119106,Partial epileptic seizure of frontal lobe with impairment of consciousness
84181000119109,Partial epileptic seizure of occipital lobe with impairment of consciousness
84191000119107,Partial epileptic seizure of temporal lobe with impairment of consciousness
84201000119105,Intractable partial temporal lobe epilepsy with impairment of consciousness
84211000119108,Intractable partial parietal lobe epilepsy with impairment of consciousness
84216001,Cerebral venous thrombosis of pregnancy AND/OR puerperium
84221000119101,Intractable partial frontal lobe epilepsy with impairment of consciousness
84231000119103,Intractable partial occipital lobe epilepsy with impairment of consciousness
84455002,Spinal paraplegia
84590007,Lower motor neuron disease
84757009,Epilepsy
85102008,Cerebellar ataxia
85505000,Adult spinal muscular atrophy
8563000,Cholinergic crisis
85641006,Hemianencephaly
85672005,Anterior horn cell disease
86003009,Carotid artery thrombosis
86044005,Amyotrophic lateral sclerosis
860804005,Epilepsy due to infectious encephalitis
860806007,Epilepsy due to infectious meningitis
860807003,Hereditary autonomic neuropathy
860809000,Hereditary sensory autonomic neuropathy type IIA
860810005,Hereditary sensory autonomic neuropathy type IIB
860811009,Hereditary sensory autonomic neuropathy type ID
860812002,Hereditary sensory autonomic neuropathy type IE
860813007,Hereditary sensory autonomic neuropathy type IA
860814001,Hereditary sensory autonomic neuropathy type IC
860815000,Epilepsy due to neonatal central nervous system infection
860881004,Flaccid diplegia of lower extremities
86444004,"Niemann-Pick disease, type C, acute form"
866050001,Mixed germ cell neoplasm of central nervous system
866051002,Motor neuron disease due to lead intoxication
870284000,Pelizaeus Merzbacher like disease due to HSPD1 mutation
870285004,Pelizaeus Merzbacher like disease due to SLC16A2 mutation
870286003,Pelizaeus Merzbacher like disease due to AIMP1 mutation
870287007,Pelizaeus Merzbacher like disease due to GJC2 mutation
870319003,Optic atrophy due to late syphilis
870544005,Occlusion of distal basilar artery
870566003,Occlusion of anterior choroidal artery
870579007,Occlusion of branch of basilar artery
870637009,Dissection of cervical artery
87151000119105,Malignant glioma of central nervous system
871637001,Thrombosis of multiple cerebral veins
87551000119101,Visual disturbance as sequela of cerebrovascular disease
87607002,"Pelizaeus-Merzbacher disease, classic form"
87842000,Generalized neuromuscular exhaustion syndrome
87937009,Endophlebitis of intracranial venous sinus
88174006,Basilar artery thrombosis
88922007,Thrombosis of basilar sinus
88923002,Progressive muscular atrophy
89142007,Progressive intracranial arterial occlusion
89437009,Cerebral paraparesis
89980009,Thrombosis of cavernous venous sinus
903741000000102,Uhthoff phenomenon
90520006,Vertebral artery stenosis
91327001,Quadriparesis
9133005,"Familial amyloid polyneuropathy, Iowa type"
91502009,Spinocerebellar disease
91601000119109,Sequela of thrombotic stroke
91637004,Myasthenia gravis
92341000119107,Weakness of extremities as sequela of stroke
92503002,Neurofibromatosis type 2
92824003,Neurofibromatosis type 1
92962004,Congenital absence of carotid artery
92997002,Congenital anomaly of carotid artery
93054001,Congenital dilatation of carotid artery
93153005,Limb-girdle muscular dystrophy
93312006,Congenital malposition of carotid artery
93396008,Congenital stenosis of carotid artery
936271000000100,Congenital anomaly of precerebral vessel
93744007,Primary malignant neoplasm of central nervous system
93747000,Primary malignant neoplasm of cerebral meninges
93931007,Primary malignant neoplasm of optic nerve
94243009,Secondary malignant neoplasm of central nervous system
94246001,Secondary malignant neoplasm of cerebral meninges
943181000000103,Degenerative disease of basal ganglia
94452002,Secondary malignant neoplasm of optic nerve
95208000,Photogenic epilepsy
95235009,Retroesophageal carotid artery
9537004,Juvenile GM 2 gangliosidosis
95455008,Thrombosis of cerebral veins
95458005,Cerebellar artery occlusion
95461006,Thrombophlebitis of cerebral vein
95477007,Congenital degeneration of nervous system
95610008,Congenital brain damage
95647008,Upper motor neuron disease
95650006,Transient hemiplegia
95651005,Chronic progressive paraparesis
95774001,Atrophy of optic disc
95775000,Retrobulbar optic nerve atrophy
9611000119107,Symptomatic carotid artery stenosis
97381000119100,Neurogenic bladder due to quadriplegia
97391000119102,Paraplegia with neurogenic bladder
9753004,Triplegia
984681000000101,Profound learning disability
99451000119105,Cerebral infarction due to stenosis of carotid artery"""


c5_df = pd.read_csv(io.StringIO(c5), header=0,delimiter=',').astype(str)
spark.createDataFrame(c5_df).createOrReplaceGlobalTempView("ccu002_06_d17_cns_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_cns_primis

# COMMAND ----------

# MAGIC %md ## diab_primis

# COMMAND ----------

c6 = """code,term
102621000119101,Ulcer of skin due to type 2 diabetes mellitus
102781000119107,Sensory neuropathy due to type 1 diabetes mellitus
103981000119101,Proliferative retinopathy following surgery due to diabetes mellitus
104941000119109,Ischemia of retina due to type 1 diabetes mellitus
104951000119106,Vitreous hemorrhage due to type 1 diabetes mellitus
104961000119108,Ischemia of retina due to type 2 diabetes mellitus
105401000119101,Diabetes mellitus due to pancreatic injury
106281000119103,Pre-existing diabetes mellitus in mother complicating childbirth
10656231000119100,Ulcer of skin of toe due to type 1 diabetes mellitus
10656271000119102,Ulcer of skin of toe due to type 2 diabetes mellitus
10660471000119109,Ulcer of left foot due to type 2 diabetes mellitus
10661671000119102,Ulcer of right foot due to type 2 diabetes mellitus
10754881000119104,Diabetes mellitus in mother complicating childbirth
109171000119104,Retinal edema due to type 1 diabetes mellitus
110141000119100,Ulcer of lower limb due to type 1 diabetes mellitus
110171000119107,Ulcer of lower limb due to type 2 diabetes mellitus
110181000119105,Peripheral sensory neuropathy due to type 2 diabetes mellitus
1102351000000105,Ketosis-prone diabetes mellitus
111231000119109,Dyslipidemia with high density lipoprotein below reference range and triglyceride above reference range due to type 2 diabetes mellitus
111307005,Leprechaunism syndrome
111552007,Diabetes mellitus without complication
111556005,Ketoacidosis without coma due to diabetes mellitus
112991000000101,Lipoatrophic diabetes mellitus without complication
11530004,Brittle diabetes mellitus
11687002,Gestational diabetes mellitus
119831000119106,Hypoglycemia unawareness due to type 2 diabetes mellitus
120711000119108,Hypoglycemic unawareness due to type 1 diabetes mellitus
120731000119103,Hypoglycemia due to type 2 diabetes mellitus
123763000,Houssay's syndrome
126534007,Mixed sensorimotor polyneuropathy due to diabetes mellitus
126535008,Motor polyneuropathy due to diabetes mellitus
127011001,Sensory neuropathy due to diabetes mellitus
127012008,Lipoatrophic diabetes
127013003,Disorder of kidney due to diabetes mellitus
127014009,Peripheral angiopathy due to diabetes mellitus
137931000119102,Hyperlipidemia due to type 2 diabetes mellitus
137941000119106,Hyperlipidemia due to type 1 diabetes mellitus
138881000119106,Mild nonproliferative retinopathy due to type 1 diabetes mellitus
138891000119109,Moderate nonproliferative retinopathy due to type 1 diabetes mellitus
138911000119106,Mild nonproliferative retinopathy due to type 2 diabetes mellitus
138921000119104,Moderate nonproliferative retinopathy due to type 2 diabetes mellitus
140101000119109,Hypertension in chronic kidney disease stage 5 due to type 2 diabetes mellitus
140111000119107,Hypertension in chronic kidney disease stage 4 due to type 2 diabetes mellitus
140121000119100,Hypertension in chronic kidney disease stage 3 due to type 2 diabetes mellitus
140131000119102,Hypertension in chronic kidney disease stage 2 due to type 2 diabetes mellitus
140391000119101,Ulcer of toe due to type 2 diabetes mellitus
140521000119107,Ischemic ulcer of foot due to type 2 diabetes mellitus
1481000119100,Diabetes mellitus type 2 without retinopathy
1491000119102,Vitreous hemorrhage due to type 2 diabetes mellitus
1501000119109,Proliferative retinopathy due to type 2 diabetes mellitus
1511000119107,Peripheral neuropathy due to type 2 diabetes mellitus
1521000119100,Ulcer of foot due to type 2 diabetes mellitus
1531000119102,Dermopathy due to type 2 diabetes mellitus
1551000119108,Nonproliferative retinopathy due to type 2 diabetes mellitus
1571000119104,Mixed hyperlipidemia due to type 1 diabetes mellitus
157141000119108,Proteinuria due to type 2 diabetes mellitus
164881000119109,Ulcer of foot due to type 1 diabetes mellitus
164971000119101,Type 2 diabetes mellitus controlled by diet
16891151000119103,Coronary artery disease due to type 2 diabetes mellitus
170745003,Diabetic on diet only
170746002,Diabetic on oral treatment
170747006,Diabetic on insulin
170766006,Loss of hypoglycemic warning due to diabetes mellitus
18521000119106,Microalbuminuria due to type 1 diabetes mellitus
190330002,Hyperosmolar coma due to type 1 diabetes mellitus
190331003,Hyperosmolar coma due to type 2 diabetes mellitus
190368000,Type I diabetes mellitus with ulcer
190372001,Type I diabetes mellitus maturity onset
190388001,Multiple complications due to type 2 diabetes mellitus
190389009,Type II diabetes mellitus with ulcer
190406000,Ketoacidosis due to malnutrition related diabetes mellitus
190407009,Malnutrition-related diabetes mellitus with renal complications
190410002,Malnutrition-related diabetes mellitus with peripheral circulatory complications
190411003,Multiple complications due to malnutrition related diabetes
190412005,Malnutrition-related diabetes mellitus without complications
190416008,Steroid-induced diabetes mellitus without complication
190447002,Steroid-induced diabetes
193141005,Mononeuritis multiplex due to diabetes mellitus
193183000,Acute painful neuropathy due to diabetes mellitus
193184006,Chronic painful neuropathy due to diabetes mellitus
193185007,Asymptomatic neuropathy due to diabetes mellitus
193349004,Preproliferative retinopathy due to diabetes mellitus
193350004,Advanced maculopathy due to diabetes mellitus
193489006,Iritis due to diabetes mellitus
19378003,Pseudotabes due to diabetes mellitus
197605007,Nephrotic syndrome due to diabetes mellitus
198121000000103,Hypoglycaemic warning impaired
198131000000101,Hypoglycaemic warning good
199225007,Diabetes mellitus during pregnancy - baby delivered
199226008,Diabetes mellitus in the puerperium - baby delivered during current episode of care
199227004,Diabetes mellitus during pregnancy - baby not yet delivered
199228009,Diabetes mellitus in the puerperium - baby delivered during previous episode of care
199229001,Pre-existing type 1 diabetes mellitus
199230006,Pre-existing type 2 diabetes mellitus
199231005,Pre-existing malnutrition-related diabetes mellitus
200687002,Cellulitis of foot due to diabetes mellitus
201000119106,Disorder due to well controlled type 2 diabetes mellitus
201250006,Ischemic ulcer of foot due to diabetes mellitus
201252003,Mixed diabetic ulcer - foot
201723002,Cheiroarthropathy due to diabetes mellitus
201724008,Neuropathic arthropathy due to diabetes mellitus
23045005,Insulin dependent diabetes mellitus type IA
230572002,Neuropathy due to diabetes mellitus
230574001,Acute painful polyneuropathy due to diabetes mellitus
230575000,Chronic painful polyneuropathy due to diabetes mellitus
230576004,Asymmetric polyneuropathy due to diabetes mellitus
230577008,Mononeuropathy due to diabetes mellitus
230579006,Thoracic radiculopathy due to diabetes mellitus
232020009,Disorder of macula due to diabetes mellitus
232021008,Proliferative retinopathy with optic disc neovascularization due to diabetes mellitus
232022001,Proliferative retinopathy with neovascularization elsewhere than the optic disc due to diabetes mellitus
232023006,Traction detachment of retina due to diabetes mellitus
236499007,Microalbuminuric nephropathy due to diabetes mellitus
236500003,Proteinuric nephropathy due to diabetes mellitus
237599002,Insulin treated type 2 diabetes mellitus
237600004,Malnutrition-related diabetes mellitus - fibrocalculous
237601000,Secondary endocrine diabetes mellitus
237604008,"Maturity onset diabetes of the young, type 2"
237612000,"Photomyoclonus, diabetes mellitus, deafness, nephropathy and cerebral dysfunction"
237617006,"Megaloblastic anemia, thiamine-responsive, with diabetes mellitus and sensorineural deafness"
237619009,Diabetes-deafness syndrome maternally transmitted
237620003,Abnormal metabolic state due to diabetes mellitus
237621004,Severe hyperglycemia due to diabetes mellitus
237627000,Pregnancy and type 2 diabetes mellitus
237632004,Hypoglycemic event due to diabetes
237633009,Hypoglycemia due to diabetes mellitus
237635002,Nocturnal hypoglycemia due to diabetes mellitus
237652003,Insulin resistance - type B
238981002,Disorder of soft tissue due to diabetes mellitus
238982009,Dermopathy due to diabetes mellitus
238983004,Thick skin syndrome due to diabetes mellitus
238984005,Rubeosis faciei due to diabetes mellitus
24203005,"Extreme insulin resistance with acanthosis nigricans, hirsutism AND abnormal insulin receptors"
243421000119104,Proteinuria due to type 1 diabetes mellitus
24471000000103,Type 2 diabetic on insulin
24481000000101,Type 2 diabetic on diet only
25093002,Disorder of eye due to diabetes mellitus
25412000,Microaneurysm of retinal artery due to diabetes mellitus
26298008,Ketoacidotic coma due to diabetes mellitus
267604001,Myasthenic syndrome due to diabetic mellitus
2751001,Fibrocalculous pancreatic diabetes
276560009,Diabetes mellitus in neonate small for gestational age
280137006,Diabetic foot
28032008,Insulin dependent diabetes mellitus type IB
28331000119107,Retinal edema due to type 2 diabetes mellitus
290002008,Brittle type I diabetes mellitus
309426007,Glomerulopathy due to diabetes mellitus
310387003,Intracapillary glomerulosclerosis of kidney due to diabetes mellitus
310505005,Hyperosmolar non-ketotic state due to diabetes mellitus
311366001,Kimmelstiel-Wilson syndrome
311782002,Advanced retinal disease due to diabetes mellitus
31211000119101,Peripheral angiopathy due to type 1 diabetes mellitus
312903003,Mild nonproliferative retinopathy due to diabetes mellitus
312904009,Moderate nonproliferative retinopathy due to diabetes mellitus
312905005,Severe nonproliferative retinopathy due to diabetes mellitus
312906006,Non-high-risk proliferative retinopathy due to diabetes mellitus
312907002,High risk proliferative retinopathy due to diabetes mellitus
312908007,Quiescent proliferative retinopathy due to diabetes mellitus
312909004,Proliferative retinopathy with iris neovascularization due to diabetes mellitus
312910009,Vitreous hemorrhage due to diabetes mellitus
312912001,Macular edema due to diabetes mellitus
31321000119102,Diabetes mellitus type 1 without retinopathy
313435000,Type I diabetes mellitus without complication
313436004,Type II diabetes mellitus without complication
314010006,Diffuse exudative maculopathy due to diabetes mellitus
314011005,Focal exudative maculopathy due to diabetes mellitus
314014002,Ischemic maculopathy due to diabetes mellitus
314015001,Mixed maculopathy due to diabetes mellitus
314194001,Diabetic on insulin and oral treatment
314537004,Optic papillopathy due to diabetes mellitus
314893005,Arthropathy due to type 1 diabetes mellitus
314902007,Peripheral angiopathy due to type 2 diabetes mellitus
314903002,Arthropathy due to type 2 diabetes mellitus
33559001,Pineal hyperplasia AND diabetes mellitus syndrome
335621000000101,Maternally inherited diabetes mellitus
35777006,Mononeuropathy multiplex due to diabetes mellitus
359611005,Neuropathy with neurologic complication due to diabetes mellitus
359642000,Diabetes mellitus type 2 in nonobese
361216007,Femoral mononeuropathy due to diabetes mellitus
367261000119100,Hyperosmolarity due to drug induced diabetes mellitus
367991000119101,Hyperglycemia due to type 1 diabetes mellitus
368051000119109,Hyperglycemia due to type 2 diabetes mellitus
368171000119104,Dermatitis due to drug induced diabetes mellitus
368521000119107,Disorder of nerve co-occurrent and due to type 1 diabetes mellitus
368551000119104,Dyslipidemia due to type 1 diabetes mellitus
368561000119102,Hyperosmolarity due to type 1 diabetes mellitus
368581000119106,Neuropathy due to type 2 diabetes mellitus
368591000119109,Cheiroarthropathy due to diabetes mellitus type 2
368601000119102,Hyperosmolar coma due to secondary diabetes mellitus
368711000119106,Mild nonproliferative retinopathy due to secondary diabetes mellitus
368721000119104,Non-proliferative retinopathy due to secondary diabetes mellitus
368741000119105,Moderate non-proliferative retinopathy due to secondary diabetes mellitus
371087003,Ulcer of foot due to diabetes mellitus
38046004,Diffuse glomerulosclerosis of kidney due to diabetes mellitus
38205001,Diarrhea due to diabetes mellitus
385041000000108,Diabetes mellitus with multiple complications
385051000000106,Pre-existing diabetes mellitus
39058009,Lumbosacral radiculoplexus neuropathy due to diabetes mellitus
390834004,Nonproliferative retinopathy due to diabetes mellitus
39127005,Symmetric proximal motor neuropathy due to diabetes mellitus
39181008,Radiculoplexus neuropathy due to diabetes mellitus
395204000,Hyperosmolar non-ketotic state due to type 2 diabetes mellitus
398140007,Post hypoglycemic hyperglycemia due to diabetes mellitus
399862001,High risk proliferative retinopathy without macular edema due to diabetes mellitus
399863006,Very severe nonproliferative retinopathy without macular edema due to diabetes mellitus
399864000,Macular edema not clinically significant due to diabetes mellitus
399865004,Very severe proliferative retinopathy due to diabetes mellitus
399866003,Venous beading of retina due to diabetes mellitus
399868002,Intraretinal microvascular anomaly due to diabetes mellitus
399869005,High risk proliferative retinopathy not amenable to photocoagulation due to diabetes mellitus
399870006,Non-high-risk proliferative retinopathy with no macular edema due to diabetes mellitus
399871005,Visually threatening retinopathy due to diabetes mellitus
399872003,Severe nonproliferative retinopathy with clinically significant macular edema due to diabetes mellitus
399873008,Severe nonproliferative retinopathy without macular edema due to diabetes mellitus
399874002,High risk proliferative retinopathy with clinically significant macula edema due to diabetes mellitus
399875001,Non-high-risk proliferative retinopathy with clinically significant macular edema due to diabetes mellitus
399876000,Very severe nonproliferative retinopathy due to diabetes mellitus
399877009,Very severe nonproliferative retinopathy with clinically significant macular edema due to diabetes mellitus
402864004,Wet gangrene of foot due to diabetes mellitus
408409007,On examination - right eye background diabetic retinopathy
408410002,On examination - left eye background diabetic retinopathy
408411003,On examination - right eye preproliferative diabetic retinopathy
408412005,On examination - left eye preproliferative diabetic retinopathy
408413000,On examination - right eye proliferative diabetic retinopathy
408414006,On examination - left eye proliferative diabetic retinopathy
408539000,Insulin autoimmune syndrome
408540003,Diabetes mellitus caused by non-steroid drugs
413183008,Diabetes mellitus caused by non-steroid drugs without complication
414894003,On examination - left eye stable treated proliferative diabetic retinopathy
414910007,On examination - right eye stable treated proliferative diabetic retinopathy
417677008,On examination - sight threatening diabetic retinopathy
419100001,Infection of foot due to diabetes mellitus
41911000119107,Glaucoma due to type 2 diabetes mellitus
420270002,Ketoacidosis due to type 1 diabetes mellitus
420279001,Renal disorder due to type 2 diabetes mellitus
420422005,Ketoacidosis due to diabetes mellitus
420436000,Mononeuropathy due to type 2 diabetes mellitus
420486006,Exudative maculopathy due to type 1 diabetes mellitus
420514000,Persistent proteinuria due to type 1 diabetes mellitus
420662003,Coma due to diabetes mellitus
420683009,Disorder of nervous system due to malnutrition related diabetes mellitus
420715001,Persistent microalbuminuria due to type 2 diabetes mellitus
420756003,Cataract of eye due to diabetes mellitus type 2
420789003,Retinopathy due to type 1 diabetes mellitus
420825003,Gangrene due to type 1 diabetes mellitus
420868002,Disorder due to type 1 diabetes mellitus
420918009,Mononeuropathy due to type 1 diabetes mellitus
420996007,Coma due to malnutrition-related diabetes mellitus
421075007,Ketoacidotic coma due to type 1 diabetes mellitus
421256007,Disorder of eye due to malnutrition related diabetes mellitus
421305000,Persistent microalbuminuria due to type 1 diabetes mellitus
421326000,Disorder of nervous system due to type 2 diabetes mellitus
421365002,Peripheral circulatory disorder due to type 1 diabetes mellitus
421437000,Hypoglycemic coma due to type 1 diabetes mellitus
421468001,Disorder of nervous system due to type 1 diabetes mellitus
421631007,Gangrene due to type 2 diabetes mellitus
421725003,Hypoglycemic coma due to diabetes mellitus
421750000,Ketoacidosis due to type 2 diabetes mellitus
421779007,Exudative maculopathy due to type 2 diabetes mellitus
421847006,Ketoacidotic coma due to type 2 diabetes mellitus
421893009,Renal disorder due to type 1 diabetes mellitus
421895002,Peripheral vascular disorder due to diabetes mellitus
421920002,Cataract of eye due to diabetes mellitus type 1
421966007,Non-ketotic non-hyperosmolar coma due to diabetes mellitus
421986006,Persistent proteinuria due to type 2 diabetes mellitus
422014003,Disorder due to type 2 diabetes mellitus
422034002,Retinopathy due to type 2 diabetes mellitus
422088007,Disorder of nervous system due to diabetes mellitus
422099009,Disorder of eye due to type 2 diabetes mellitus
422126006,Hyperosmolar coma due to diabetes mellitus
422166005,Peripheral circulatory disorder due to type 2 diabetes mellitus
422183001,Skin ulcer due to diabetes mellitus
422228004,Multiple complications due to type 1 diabetes mellitus
422275004,Gangrene due to diabetes mellitus
424736006,Peripheral neuropathy due to diabetes mellitus
425455002,Glomerulonephritis due to diabetes mellitus
426705001,Diabetes mellitus co-occurrent and due to cystic fibrosis
426875007,Latent autoimmune diabetes mellitus in adult
426907004,Small vessel disease due to type 1 diabetes mellitus
427027005,Lumbosacral radiculoplexus neuropathy due to type 2 diabetes mellitus
427089005,Diabetes mellitus due to cystic fibrosis
427134009,Small vessel disease due to type 2 diabetes mellitus
427571000,Lumbosacral radiculoplexus neuropathy due to type 1 diabetes mellitus
427943001,Ophthalmoplegia due to diabetes mellitus
428007007,Erectile dysfunction due to type 2 diabetes mellitus
428896009,Hyperosmolality due to uncontrolled type 1 diabetes mellitus
42954008,Diabetes mellitus associated with receptor abnormality
43959009,Cataract of eye due to diabetes mellitus
44054006,Diabetes mellitus type 2
441628001,Multiple complications due to diabetes mellitus
441656006,Hyperglycemic crisis due to diabetes mellitus
445170001,Macroalbuminuric nephropathy due to diabetes mellitus
445260006,Posttransplant diabetes mellitus
445353002,Brittle type II diabetes mellitus
46635009,Diabetes mellitus type 1
4783006,Maternal diabetes mellitus with hypoglycemia affecting fetus OR newborn
4855003,Retinopathy due to diabetes mellitus
48951005,Bullous disease due to diabetes mellitus
49455004,Polyneuropathy due to diabetes mellitus
49817004,Neonatal diabetes mellitus
50620007,Autonomic neuropathy due to diabetes mellitus
51002006,Diabetes mellitus associated with pancreatic disease
530558861000132104,Atypical diabetes mellitus
5368009,Drug-induced diabetes mellitus
57886004,Protein-deficient diabetes mellitus
59079001,Diabetes mellitus associated with hormonal etiology
59276001,Proliferative retinopathy due to diabetes mellitus
5969009,Diabetes mellitus associated with genetic syndrome
60951000119105,Blindness due to type 2 diabetes mellitus
609561005,Maturity-onset diabetes of the young
609562003,"Maturity onset diabetes of the young, type 1"
609563008,Pre-existing diabetes mellitus in pregnancy
609564002,Pre-existing type 1 diabetes mellitus in pregnancy
609565001,Permanent neonatal diabetes mellitus
609566000,Pregnancy and type 1 diabetes mellitus
609567009,Pre-existing type 2 diabetes mellitus in pregnancy
609568004,Diabetes mellitus due to genetic defect in beta cell function
609569007,Diabetes mellitus due to genetic defect in insulin action
609570008,"Maturity-onset diabetes of the young, type 3"
609571007,"Maturity-onset diabetes of the young, type 4"
609572000,"Maturity-onset diabetes of the young, type 5"
609573005,"Maturity-onset diabetes of the young, type 6"
609574004,"Maturity-onset diabetes of the young, type 7"
609575003,"Maturity-onset diabetes of the young, type 8"
609576002,"Maturity-onset diabetes of the young, type 9"
609577006,"Maturity-onset diabetes of the young, type 10"
609578001,"Maturity-onset diabetes of the young, type 11"
60961000119107,Nonproliferative diabetic retinopathy due to type 1 diabetes mellitus
60971000119101,Proliferative retinopathy due to type 1 diabetes mellitus
60991000119100,Blindness due to type 1 diabetes mellitus
62260007,Pretibial pigmental patches due to diabetes mellitus
63510008,Nodular glomerulosclerosis of kidney due to diabetes mellitus
691000119103,Erectile dysfunction due to type 1 diabetes mellitus
701000119103,Mixed hyperlipidemia due to type 2 diabetes mellitus
706894000,Retinopathy due to unstable diabetes mellitus type 1
70694009,Diabetes mellitus AND insipidus with optic atrophy AND deafness
707221002,Glomerulosclerosis of kidney due to diabetes mellitus
709147009,Gingivitis co-occurrent with diabetes mellitus
711000119100,Chronic kidney disease stage 5 due to type 2 diabetes mellitus
712882000,Autonomic neuropathy due to type 1 diabetes mellitus
712883005,Autonomic neuropathy due to type 2 diabetes mellitus
713457002,Neovascular glaucoma due to diabetes mellitus
713702000,Gastroparesis due to type 1 diabetes mellitus
713703005,Gastroparesis due to type 2 diabetes mellitus
713704004,Gastroparesis due to diabetes mellitus
713705003,Polyneuropathy due to type 1 diabetes mellitus
713706002,Polyneuropathy due to type 2 diabetes mellitus
71421000119105,Hypertension in chronic kidney disease due to type 2 diabetes mellitus
71441000119104,Nephrotic syndrome due to type 2 diabetes mellitus
716362006,Gingival disease co-occurrent with diabetes mellitus
71701000119105,Hypertension in chronic kidney disease due to type 1 diabetes mellitus
71721000119101,Nephrotic syndrome due to type 1 diabetes mellitus
71771000119100,Neuropathic arthropathy due to type 1 diabetes mellitus
71791000119104,Peripheral neuropathy due to type 1 diabetes mellitus
719216001,Hypoglycemic coma due to type 2 diabetes mellitus
719566006,Diabetic on non-insulin injectable medication
72021000119109,Dermopathy due to type 1 diabetes mellitus
72031000119107,Severe malnutrition due to type 1 diabetes mellitus
72041000119103,Osteomyelitis due to type 1 diabetes mellitus
72051000119101,Severe malnutrition due to type 2 diabetes mellitus
720519003,"Atherosclerosis, deafness, diabetes, epilepsy, nephropathy syndrome"
72061000119104,Osteomyelitis due to type 2 diabetes mellitus
721000119107,Chronic kidney disease stage 4 due to type 2 diabetes mellitus
721088003,"Developmental delay, epilepsy, neonatal diabetes syndrome"
721283000,Acidosis due to type 1 diabetes mellitus
721284006,Acidosis due to type 2 diabetes mellitus
72141000119104,Chronic ulcer of skin due to type 1 diabetes mellitus
722206009,"Pancreatic hypoplasia, diabetes mellitus, congenital heart disease syndrome"
722454003,"Intellectual disability, craniofacial dysmorphism, hypogonadism, diabetes mellitus syndrome"
723074006,Renal papillary necrosis due to diabetes mellitus
724067006,Permanent neonatal diabetes mellitus with cerebellar agenesis syndrome
724136006,Mastopathy due to diabetes mellitus
724876003,Lesion of skin due to diabetes mellitus
731000119105,Chronic kidney disease stage 3 due to type 2 diabetes mellitus
73211009,Diabetes mellitus
733072002,"Alaninuria, microcephaly, dwarfism, enamel hypoplasia, diabetes mellitus syndrome"
734022008,Wolfram-like syndrome
735200002,Absence of lower limb due to diabetes mellitus
735537007,Hyperosmolar hyperglycemic coma due to diabetes mellitus without ketoacidosis
735538002,Lactic acidosis due to diabetes mellitus
735539005,Metabolic acidosis due to diabetes mellitus
737212004,Diabetes mellitus caused by chemical
739681000,Disorder of eye due to type 1 diabetes mellitus
741000119101,Chronic kidney disease stage 2 due to type 2 diabetes mellitus
74627003,Complication due to diabetes mellitus
751000119104,Chronic kidney disease stage 1 due to type 2 diabetes mellitus
75524006,Malnutrition related diabetes mellitus
75682002,Diabetes mellitus caused by insulin receptor antibodies
761000119102,Dyslipidemia due to type 2 diabetes mellitus
762489000,Acute complication due to diabetes mellitus
76751001,"Diabetes mellitus in mother complicating pregnancy, childbirth AND/OR puerperium"
768792007,Cataract of right eye due to diabetes mellitus
768793002,Cataract of left eye due to diabetes mellitus
768794008,Cataract of bilateral eyes due to diabetes mellitus
768797001,Iritis of right eye due to diabetes mellitus
768798006,Iritis of left eye due to diabetes mellitus
768799003,Iritis of bilateral eyes due to diabetes mellitus
769181007,Preproliferative retinopathy of right eye due to diabetes mellitus
769182000,Preproliferative retinopathy of left eye due to diabetes mellitus
769183005,Mild nonproliferative retinopathy of right eye due to diabetes mellitus
769184004,Mild nonproliferative retinopathy of left eye due to diabetes mellitus
769185003,Moderate nonproliferative retinopathy of right eye due to diabetes mellitus
769186002,Moderate nonproliferative retinopathy of left eye due to diabetes mellitus
769187006,Severe nonproliferative retinopathy of right eye due to diabetes mellitus
769188001,Severe nonproliferative retinopathy of left eye due to diabetes mellitus
769190000,Very severe nonproliferative retinopathy of right eye due to diabetes mellitus
769191001,Very severe nonproliferative retinopathy of left eye due to diabetes mellitus
769217008,Macular edema of right eye due to diabetes mellitus
769218003,Macular edema of left eye due to diabetes mellitus
769219006,Macular edema due to type 1 diabetes mellitus
769220000,Macular edema due to type 2 diabetes mellitus
769221001,Clinically significant macular edema of right eye due to diabetes mellitus
769222008,Clinically significant macular edema of left eye due to diabetes mellitus
769244003,Disorder of right macula due to diabetes mellitus
769245002,Disorder of left macula due to diabetes mellitus
770094004,Cervical radiculoplexus neuropathy due to diabetes mellitus
770095003,Cranial nerve palsy due to diabetes mellitus
770096002,Erectile dysfunction due to diabetes mellitus
770097006,Clinically significant macular edema due to diabetes mellitus
770098001,Cranial nerve palsy due to type 1 diabetes mellitus
770323005,Retinal edema due to diabetes mellitus
770324004,Ischemia of retina due to diabetes mellitus
770361008,Vitreous hemorrhage of right eye due to diabetes mellitus
770362001,Vitreous hemorrhage of left eye due to diabetes mellitus
770581008,Microaneurysm of right retinal artery due to diabetes mellitus
770582001,Microaneurysm of left retinal artery due to diabetes mellitus
770599000,Venous beading of right retina due to diabetes mellitus
770600002,Venous beading of left retina due to diabetes mellitus
770765001,Proliferative retinopathy of right eye due to diabetes mellitus
770766000,Proliferative retinopathy of left eye due to diabetes mellitus
771000119108,Chronic kidney disease due to type 2 diabetes mellitus
773001000000103,Symptomatic diabetic peripheral neuropathy
775841000000109,Diabetic retinopathy detected by national screening programme
781000119106,Neuropathic arthropathy due to type 2 diabetes mellitus
782755007,"Primary microcephaly, mild intellectual disability, young-onset diabetes syndrome"
782825008,"Primary microcephaly, epilepsy, permanent neonatal diabetes syndrome"
783722008,Myopathy and diabetes mellitus
788878000,Cardiomyopathy due to diabetes mellitus
789542009,Neuropathy due to type 1 diabetes mellitus
789562001,Ulcer of heel due to diabetes mellitus
789567007,Ulcer of heel due to type 2 diabetes mellitus
789568002,Ulcer of midfoot due to diabetes mellitus
789571005,Ulcer of heel due to type 1 diabetes mellitus
789572003,Ulcer of midfoot due to type 1 diabetes mellitus
789585000,Sensory polyneuropathy due to diabetes mellitus
791000119109,Angina due to type 2 diabetes mellitus
792926007,Armanni-Ebstein kidney due to diabetes mellitus
79554005,Asymmetric proximal motor neuropathy due to diabetes mellitus
81531005,Diabetes mellitus type 2 in obese
816067005,"Diabetes, hypogonadism, deafness, intellectual disability syndrome"
816177009,Nonproliferative retinopathy of left eye due to diabetes mellitus
816178004,Nonproliferative retinopathy of right eye due to diabetes mellitus
816961009,Stable treated proliferative retinopathy of right eye due to diabetes mellitus
816962002,Stable treated proliferative retinopathy of left eye due to diabetes mellitus
81830002,Mononeuropathy simplex due to diabetes mellitus
822995009,Hyperglycemia due to diabetes mellitus
82541000119100,Traction detachment of retina due to type 2 diabetes mellitus
82551000119103,Rubeosis iridis due to type 2 diabetes mellitus
82571000119107,Traction detachment of retina due to type 1 diabetes mellitus
82581000119105,Rubeosis iridis due to type 1 diabetes mellitus
82980005,Anemia due to diabetes mellitus
84361000119102,Insulin reactive hypoglycemia due to type 2 diabetes mellitus
84371000119108,Hypoglycemia due to type 1 diabetes mellitus
860721006,Disorder of macula of bilateral eyes due to diabetes mellitus
860798008,Glaucoma due to diabetes mellitus
860977000,Ulcer of right foot due to diabetes mellitus
860978005,Ulcer of left foot due to diabetes mellitus
860979002,Chronic ulcer of right foot due to diabetes mellitus
860980004,Chronic ulcer of left foot due to diabetes mellitus
870420005,Severe nonproliferative retinopathy with venous beading of retina due to diabetes mellitus
870421009,Cystoid macular edema due to diabetes mellitus
870529009,Persistent macular edema due to diabetes mellitus
871778008,Centrally involved macular edema due to diabetes mellitus
871781003,Non centrally involved macular edema due to diabetes mellitus
87441000119104,Ulcer of ankle due to type 2 diabetes mellitus
87461000119100,Ulcer of forefoot due to type 2 diabetes mellitus
87471000119106,Ulcer of ankle due to type 1 diabetes mellitus
87491000119107,Ulcer of forefoot due to type 1 diabetes mellitus
87921000119104,Cranial nerve palsy due to type 2 diabetes mellitus
8801005,Secondary diabetes mellitus
894741000000107,Hypoglycaemic warning absent
90721000119101,Chronic kidney disease stage 1 due to type 1 diabetes mellitus
90731000119103,Chronic kidney disease stage 2 due to type 1 diabetes mellitus
90741000119107,Chronic kidney disease stage 3 due to type 1 diabetes mellitus
90751000119109,Chronic kidney disease stage 4 due to type 1 diabetes mellitus
90761000119106,Chronic kidney disease stage 5 due to type 1 diabetes mellitus
90771000119100,End stage renal disease on dialysis due to type 1 diabetes mellitus
90781000119102,Microalbuminuria due to type 2 diabetes mellitus
90791000119104,End stage renal disease on dialysis due to type 2 diabetes mellitus
91352004,Diabetes mellitus due to structurally abnormal insulin
96441000119101,Chronic kidney disease due to type 1 diabetes mellitus
97331000119101,Macular edema and retinopathy due to type 2 diabetes mellitus
97341000119105,Proliferative retinopathy with retinal edema due to type 2 diabetes mellitus
97621000119107,Stasis ulcer due to type 2 diabetes mellitus
976341000000101,Diabetic on oral treatment and glucagon-like peptide 1 receptor agonist
976361000000100,Diabetic on insulin and glucagon-like peptide 1 receptor agonist
9859006,Acanthosis nigricans due to type 2 diabetes mellitus"""


c6_df = pd.read_csv(io.StringIO(c6), header=0,delimiter=',').astype(str)
spark.createDataFrame(c6_df).createOrReplaceGlobalTempView("ccu002_06_d17_diab_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_diab_primis

# COMMAND ----------

# MAGIC %md ## dmres_primis

# COMMAND ----------

c7 = """code,term
315051004,Diabetes resolved"""


c7_df = pd.read_csv(io.StringIO(c7), header=0,delimiter=',').astype(str)
spark.createDataFrame(c7_df).createOrReplaceGlobalTempView("ccu002_06_d17_dmres_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_dmres_primis

# COMMAND ----------

# MAGIC %md ## sev_mental_primis

# COMMAND ----------

c8 = """code,term
10760421000119102,Psychotic disorder in mother complicating childbirth
10760461000119107,Psychotic disorder in mother complicating pregnancy
1086471000000103,"Recurrent reactive depressive episodes, severe, with psychosis"
10875004,"Severe mixed bipolar I disorder with psychotic features, mood-incongruent"
1089481000000106,Cataleptic schizophrenia
1089511000000100,Recurrent depression with current severe episode and psychotic features
1089661000000104,Mania with mood-congruent psychotic features
1089671000000106,Mania with mood-incongruent psychotic features
1089681000000108,Mania with psychotic features
1089691000000105,Acute predominantly delusional psychotic disorder
10981006,Severe mixed bipolar I disorder with psychotic features
111482003,Subchronic schizophrenia with acute exacerbations
111483008,Catatonic schizophrenia in remission
111484002,Undifferentiated schizophrenia
111485001,Mixed bipolar I disorder in full remission
1127191000000108,First episode psychosis
1196001,"Chronic bipolar II disorder, most recent episode major depressive"
12939007,Chronic disorganized schizophrenia
129602009,Symbiotic infantile psychosis
12969000,"Severe bipolar II disorder, most recent episode major depressive, in full remission"
133091000119105,Rapid cycling bipolar I disorder
13313007,Mild bipolar disorder
13581000,"Severe bipolar I disorder, single manic episode with psychotic features, mood-congruent"
13746004,Bipolar disorder
14291003,Subchronic disorganized schizophrenia with acute exacerbations
14495005,"Severe bipolar I disorder, single manic episode without psychotic features"
1499003,"Bipolar I disorder, single manic episode with postpartum onset"
15193003,"Severe recurrent major depression with psychotic features, mood-incongruent"
162004,Severe manic bipolar I disorder without psychotic features
16238741000119105,Bipolar disorder caused by drug
16295005,"Bipolar II disorder, most recent episode major depressive"
16506000,Mixed bipolar I disorder
16990005,Subchronic schizophrenia
17262008,Non-alcoholic Korsakoff's psychosis
17782008,"Bipolar I disorder, most recent episode manic with catatonic features"
18260003,Postpartum psychosis
191447007,Organic psychotic condition
191499009,Transient organic psychoses
191525009,Non-organic psychosis
191526005,Schizophrenic disorders
191527001,Simple schizophrenia
191531007,Acute exacerbation of chronic schizophrenia
191542003,Catatonic schizophrenia
191547009,Acute exacerbation of subchronic catatonic schizophrenia
191548004,Acute exacerbation of chronic catatonic schizophrenia
191554003,Acute exacerbation of subchronic paranoid schizophrenia
191555002,Acute exacerbation of chronic paranoid schizophrenia
191559008,Latent schizophrenia
191561004,Subchronic latent schizophrenia
191562006,Chronic latent schizophrenia
191563001,Acute exacerbation of subchronic latent schizophrenia
191564007,Acute exacerbation of chronic latent schizophrenia
191565008,Latent schizophrenia in remission
191567000,Schizoaffective schizophrenia
191569002,Subchronic schizoaffective schizophrenia
191570001,Chronic schizoaffective schizophrenia
191571002,Acute exacerbation of subchronic schizoaffective schizophrenia
191572009,Acute exacerbation of chronic schizoaffective schizophrenia
191574005,Schizoaffective schizophrenia in remission
191577003,Cenesthopathic schizophrenia
191583000,"Single manic episode, mild"
191584006,"Single manic episode, moderate"
191586008,"Single manic episode, severe, with psychosis"
191588009,Single manic episode in full remission
191590005,Recurrent manic episodes
191592002,"Recurrent manic episodes, mild"
191593007,"Recurrent manic episodes, moderate"
191595000,"Recurrent manic episodes, severe, with psychosis"
191597008,"Recurrent manic episodes, in full remission"
191604000,"Single major depressive episode, severe, with psychosis"
191613003,"Recurrent major depressive episodes, severe, with psychosis"
191618007,"Bipolar affective disorder, current episode manic"
191620005,"Bipolar affective disorder, currently manic, mild"
191621009,"Bipolar affective disorder, currently manic, moderate"
191623007,"Bipolar affective disorder, currently manic, severe, with psychosis"
191625000,"Bipolar affective disorder, currently manic, in full remission"
191627008,"Bipolar affective disorder, current episode depression"
191629006,"Bipolar affective disorder, currently depressed, mild"
191630001,"Bipolar affective disorder, currently depressed, moderate"
191634005,"Bipolar affective disorder, currently depressed, in full remission"
191636007,Mixed bipolar affective disorder
191638008,"Mixed bipolar affective disorder, mild"
191639000,"Mixed bipolar affective disorder, moderate"
191641004,"Mixed bipolar affective disorder, severe, with psychosis"
191643001,"Mixed bipolar affective disorder, in full remission"
191658009,Atypical manic disorder
191667009,Paranoid disorder
191668004,Simple paranoid state
191670008,Shared paranoid disorder
191672000,Paranoia querulans
191676002,Reactive depressive psychosis
191677006,Acute hysterical psychosis
191678001,Reactive confusion
191680007,Psychogenic paranoid psychosis
191683009,Psychogenic stupor
192362008,"Bipolar affective disorder, current episode mixed"
19300006,"Severe bipolar II disorder, most recent episode major depressive with psychotic features, mood-congruent"
20250007,"Severe major depression, single episode, with psychotic features, mood-incongruent"
20960007,"Severe bipolar II disorder, most recent episode major depressive with psychotic features, mood-incongruent"
21900002,"Bipolar I disorder, most recent episode depressed with catatonic features"
22121000,Depressed bipolar I disorder in full remission
22407005,"Bipolar II disorder, most recent episode major depressive with catatonic features"
231437006,Reactive psychoses
231438001,Presbyophrenic psychosis
231444002,Organic bipolar disorder
231449007,Epileptic psychosis
231450007,Psychosis associated with intensive care
231485007,Post-schizophrenic depression
231487004,Persistent delusional disorder
231489001,Acute transient psychotic disorder
231494001,Mania
231495000,Manic stupor
231496004,Hypomania
237351003,Mild postnatal psychosis
237352005,Severe postnatal psychosis
23741000119105,Severe manic bipolar I disorder
247804008,Schizophrenic prodrome
26025008,Residual schizophrenia
261000119107,Severe depressed bipolar I disorder
26203008,"Severe depressed bipolar I disorder with psychotic features, mood-incongruent"
26530004,"Severe bipolar disorder with psychotic features, mood-incongruent"
268612007,Senile and presenile organic psychotic conditions
268617001,Acute schizophrenic episode
268619003,"Manic disorder, single episode"
268622001,Chronic paranoid psychosis
268624000,Acute paranoid reaction
270901009,"Schizoaffective disorder, mixed type"
271000119101,Severe mixed bipolar I disorder
271428004,"Schizoaffective disorder, manic type"
27387000,Subchronic disorganized schizophrenia
274952002,Borderline schizophrenia
274953007,Acute polymorphic psychotic disorder
278506006,Involutional paranoid state
278852008,Paranoid-hallucinatory epileptic psychosis
278853003,Acute schizophrenia-like psychotic disorder
28475009,Severe recurrent major depression with psychotic features
28663008,Severe manic bipolar I disorder with psychotic features
288751000119101,"Reactive depressive psychosis, single episode"
28884001,"Moderate bipolar I disorder, single manic episode"
29599000,Chronic undifferentiated schizophrenia
29929003,"Bipolar I disorder, most recent episode depressed with atypical features"
30336007,Chronic residual schizophrenia with acute exacerbations
30520009,"Severe bipolar II disorder, most recent episode major depressive with psychotic features"
30687003,"Bipolar II disorder, most recent episode major depressive with postpartum onset"
307417003,Cycloid psychosis
307504004,Oneirophrenia
30935000,Manic bipolar I disorder in full remission
31027006,Schizotypal personality disorder
31373002,Disorganized schizophrenia in remission
31446002,"Bipolar I disorder, most recent episode hypomanic"
31658008,Chronic paranoid schizophrenia
33078009,"Severe recurrent major depression with psychotic features, mood-congruent"
33380008,"Severe manic bipolar I disorder with psychotic features, mood-incongruent"
33736005,"Severe major depression with psychotic features, mood-congruent"
34315001,"Bipolar II disorder, most recent episode major depressive with melancholic features"
35218008,Chronic disorganized schizophrenia with acute exacerbation
35252006,Disorganized schizophrenia
3530005,"Bipolar I disorder, single manic episode, in full remission"
35481005,Mixed bipolar I disorder in remission
35722002,"Severe bipolar II disorder, most recent episode major depressive, in remission"
357705009,Cotard's syndrome
35846004,"Moderate bipolar II disorder, most recent episode major depressive"
36158005,Schizophreniform disorder with good prognostic features
36583000,Mixed bipolar I disorder in partial remission
371026009,Senile dementia with psychosis
371596008,Bipolar I disorder
371599001,Severe bipolar I disorder
371600003,Severe bipolar disorder
371604007,Severe bipolar II disorder
38368003,"Schizoaffective disorder, bipolar type"
39610001,Undifferentiated schizophrenia in remission
408858002,Infantile psychosis
40926005,Moderate mixed bipolar I disorder
41552001,"Mild bipolar I disorder, single manic episode"
416340002,Late onset schizophrenia
417601000000102,"[X]Schizophrenia, schizotypal and delusional disorders"
41832009,"Severe bipolar I disorder, single manic episode with psychotic features"
41836007,Bipolar disorder in full remission
41932008,Amok
42868002,Subchronic catatonic schizophrenia
430852001,"Severe major depression, single episode, with psychotic features"
43568002,"Bipolar II disorder, most recent episode major depressive with atypical features"
43769008,Mild mixed bipolar I disorder
441704009,Affective psychosis
441833000,Lethal catatonia
4441000,Severe bipolar disorder with psychotic features
45479006,Manic bipolar I disorder in remission
46229002,Severe mixed bipolar I disorder without psychotic features
473452003,Atypical psychosis
47447001,Grandiose delusion disorder
48500005,Delusional disorder
48937005,"Bipolar II disorder, most recent episode hypomanic"
4926007,Schizophrenia in remission
49468007,Depressed bipolar I disorder
49512000,Depressed bipolar I disorder in partial remission
51133006,Residual schizophrenia in remission
51637008,"Chronic bipolar I disorder, most recent episode depressed"
53049002,Severe bipolar disorder without psychotic features
53607008,Depressed bipolar I disorder in remission
5464005,Brief reactive psychosis
54761006,"Severe depressed bipolar I disorder with psychotic features, mood-congruent"
55516002,"Bipolar I disorder, most recent episode manic with postpartum onset"
55736003,Schizophreniform disorder without good prognostic features
5703000,Bipolar disorder in partial remission
58214004,Schizophrenia
58647003,"Severe mood disorder with psychotic features, mood-congruent"
59617007,Severe depressed bipolar I disorder with psychotic features
60099002,"Severe major depression with psychotic features, mood-incongruent"
60123008,"Delusional disorder, mixed type"
60401000119104,Postpartum psychosis in remission
61403008,Severe depressed bipolar I disorder without psychotic features
61831009,Induced psychotic disorder
63181006,Paranoid schizophrenia in remission
63204009,Bouffée délirante
63249007,Manic bipolar I disorder in partial remission
64731001,"Severe mixed bipolar I disorder with psychotic features, mood-congruent"
64905009,Paranoid schizophrenia
65042007,"Bipolar I disorder, most recent episode mixed with postpartum onset"
66631006,Moderate depressed bipolar I disorder
67002003,"Severe bipolar II disorder, most recent episode major depressive, in partial remission"
68569003,Manic bipolar I disorder
68890003,Schizoaffective disorder
68995007,Chronic catatonic schizophrenia
69322001,Psychotic disorder
698951002,Delusional disorder in remission
7025000,Subchronic undifferentiated schizophrenia with acute exacerbations
70546001,"Severe bipolar disorder with psychotic features, mood-congruent"
70814008,Subchronic residual schizophrenia with acute exacerbations
71103003,Chronic residual schizophrenia
712824002,Acute polymorphic psychotic disorder without symptoms of schizophrenia
712850003,Acute polymorphic psychotic disorder co-occurrent with symptoms of schizophrenia
71294008,"Mild bipolar II disorder, most recent episode major depressive"
719717006,Psychosis co-occurrent and due to Parkinson's disease
71984005,Mild manic bipolar I disorder
723899008,Delusional disorder currently symptomatic
723903001,Bipolar type I disorder currently in full remission
723905008,Bipolar type II disorder currently in full remission
724755002,Positive symptoms co-occurrent and due to primary psychotic disorder
724756001,Negative symptoms co-occurrent and due to primary psychotic disorder
724758000,Manic symptoms co-occurrent and due to primary psychotic disorder
724759008,Psychomotor symptom co-occurrent and due to psychotic disorder
724760003,Cognitive impairment co-occurrent and due to primary psychotic disorder
726772006,Major depression with psychotic features
73471000,"Bipolar I disorder, most recent episode mixed with catatonic features"
73867007,Severe major depression with psychotic features
74686005,Mild depressed bipolar I disorder
75360000,"Bipolar I disorder, single manic episode, in remission"
755301000000102,Paranoid state in remission
755311000000100,Non-organic psychosis in remission
755321000000106,"Single major depressive episode, severe, with psychosis, psychosis in remission"
755331000000108,"Recurrent major depressive episodes, severe, with psychosis, psychosis in remission"
75752004,"Bipolar I disorder, most recent episode depressed with melancholic features"
760721000000109,"Mixed bipolar affective disorder, in partial remission"
764591000000108,"Mixed bipolar affective disorder, severe"
764621000000106,"Recurrent manic episodes, severe"
764641000000104,"Single manic episode, severe"
764671000000105,"Recurrent manic episodes, in partial remission"
764681000000107,"Recurrent manic episodes, in remission"
764731000000103,Single manic episode in partial remission
764741000000107,Single manic episode in remission
765176007,Psychosis and severe depression co-occurrent and due to bipolar affective disorder
76566000,Subchronic residual schizophrenia
767631007,"Bipolar disorder, most recent episode depression"
767632000,"Bipolar disorder, most recent episode manic"
767633005,"Bipolar affective disorder, most recent episode mixed"
767635003,"Bipolar I disorder, most recent episode manic"
767636002,"Bipolar I disorder, most recent episode depression"
77911002,"Severe major depression, single episode, with psychotic features, mood-congruent"
78269000,"Bipolar I disorder, single manic episode, in partial remission"
78640000,"Severe manic bipolar I disorder with psychotic features, mood-congruent"
789061003,Rapid cycling bipolar II disorder
79204003,Chronic undifferentiated schizophrenia with acute exacerbations
79584002,Moderate bipolar disorder
79866005,Subchronic paranoid schizophrenia
81319007,"Severe bipolar II disorder, most recent episode major depressive without psychotic features"
82998009,Moderate manic bipolar I disorder
83225003,Bipolar II disorder
83746006,Chronic schizophrenia
84760002,"Schizoaffective disorder, depressive type"
85248005,Bipolar disorder in remission
85861002,Subchronic undifferentiated schizophrenia
86058007,"Severe bipolar I disorder, single manic episode with psychotic features, mood-incongruent"
87203005,"Bipolar I disorder, most recent episode depressed with postpartum onset"
87950005,"Bipolar I disorder, single manic episode with catatonic features"
88975006,Schizophreniform disorder
9340000,"Bipolar I disorder, single manic episode"
"""


c8_df = pd.read_csv(io.StringIO(c8), header=0,delimiter=',').astype(str)
spark.createDataFrame(c8_df).createOrReplaceGlobalTempView("ccu002_06_d17_sev_mental_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_sev_mental_primis

# COMMAND ----------

# MAGIC %md ## smhres_primis

# COMMAND ----------

c9 = """code,term
111483008,Catatonic schizophrenia in remission
111485001,Mixed bipolar I disorder in full remission
12969000,"Severe bipolar II disorder, most recent episode major depressive, in full remission"
191565008,Latent schizophrenia in remission
191574005,Schizoaffective schizophrenia in remission
191588009,Single manic episode in full remission
191597008,"Recurrent manic episodes, in full remission"
191625000,"Bipolar affective disorder, currently manic, in full remission"
191634005,"Bipolar affective disorder, currently depressed, in full remission"
191643001,"Mixed bipolar affective disorder, in full remission"
22121000,Depressed bipolar I disorder in full remission
30935000,Manic bipolar I disorder in full remission
31373002,Disorganized schizophrenia in remission
3530005,"Bipolar I disorder, single manic episode, in full remission"
35481005,Mixed bipolar I disorder in remission
35722002,"Severe bipolar II disorder, most recent episode major depressive, in remission"
39610001,Undifferentiated schizophrenia in remission
41836007,Bipolar disorder in full remission
45479006,Manic bipolar I disorder in remission
4926007,Schizophrenia in remission
51133006,Residual schizophrenia in remission
53607008,Depressed bipolar I disorder in remission
60401000119104,Postpartum psychosis in remission
63181006,Paranoid schizophrenia in remission
698951002,Delusional disorder in remission
723901004,Delusional disorder currently in full remission
723903001,Bipolar type I disorder currently in full remission
723905008,Bipolar type II disorder currently in full remission
75360000,"Bipolar I disorder, single manic episode, in remission"
755301000000102,Paranoid state in remission
755311000000100,Non-organic psychosis in remission
755321000000106,"Single major depressive episode, severe, with psychosis, psychosis in remission"
755331000000108,"Recurrent major depressive episodes, severe, with psychosis, psychosis in remission"
764681000000107,"Recurrent manic episodes, in remission"
764741000000107,Single manic episode in remission
85248005,Bipolar disorder in remission"""


c9_df = pd.read_csv(io.StringIO(c9), header=0,delimiter=',').astype(str)
spark.createDataFrame(c9_df).createOrReplaceGlobalTempView("ccu002_06_d17_smhres_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_smhres_primis

# COMMAND ----------

# MAGIC %md ## chd_primis 

# COMMAND ----------

c10 = """code,term
1001000119102,Pulmonary embolism with pulmonary infarction
100751000119101,Venous thrombosis due to central venous access device
10190003,Aortocoronary bypass of four or more coronary arteries
103011000119106,Coronary arteriosclerosis in patient with history of previous myocardial infarction
10326007,"Coronary artery bypass with autogenous graft, three grafts"
10451007,Double aortic arch
1051801000000108,Replacement of single chamber intravenous cardiac pacemaker system
1051811000000105,Replacement of dual chamber intravenous cardiac pacemaker system
1051821000000104,Replacement of biventricular intravenous cardiac pacemaker system
1051831000000102,Replacement of single chamber cardiac pacemaker system
1051841000000106,Replacement of biventricular cardiac pacemaker
1051851000000109,Replacement of dual chamber cardiac pacemaker system
105981003,Disorder of cardiac function
10749961000119104,Occlusion of aortoiliac artery
10750641000119101,Cardiac arrest due to failed attempted abortion
10759191000119106,Postpartum septic thrombophlebitis
10759311000119104,Pulmonary embolism in childbirth
10760181000119109,Cardiac arrest due to miscarriage
10811961000119109,Cardiac arrest due to incomplete miscarriage
10818008,Congenital malposition of heart
108411000119109,Mural thrombus of left atrium
10930001,Congenital atresia of pulmonary artery
10964002,Progressive pulmonary hypertension
11029002,Pulmonary apoplexy
11101003,Percutaneous transluminal coronary angioplasty
111289009,Arteriovenous fistula of pulmonary vessels
111293003,Venous thrombosis
111296006,Basilar artery embolism
111319002,"Truncus arteriosus, Edwards' type IV"
111321007,Right aortic arch
111322000,Congenital anomaly of pulmonary veins
111323005,Total anomalous pulmonary venous return
111458008,Postpartum venous thrombosis
111497000,Arterial thrombosis of spinal cord
11399002,Pulmonary hypertensive arterial disease
11614003,Congenital stenosis of pulmonary veins
116291000119103,Occlusion of renal artery due to embolism
11851006,Mitral valve disorder
119564002,Internal mammary-coronary artery bypass graft
119565001,"Coronary artery bypass graft, anastomosis of artery of thorax to coronary artery"
119772003,Coronary artery closure
119773008,Coronary artery reconstruction
120041000119109,Atrial fibrillation with rapid ventricular response
12075007,Congenital hypoplasia of ascending aorta
120871000119108,Systolic heart failure stage B
120901000119108,Diastolic heart failure stage B
12232008,Syphilitic aneurysm of aorta
12236991000119103,Pain at rest of bilateral lower limbs co-occurrent and due to atherosclerosis
12237111000119107,Pain at rest of left lower limb co-occurrent and due to atherosclerosis
12237231000119107,Pain at rest of right lower limb co-occurrent and due to atherosclerosis
12237791000119102,Acute thrombosis of superficial vein of bilateral upper limbs
12237831000119108,Acute thrombosis of superficial vein of left upper limb
12237871000119106,Acute thrombosis of superficial vein of right upper limb
123659003,Congenital malrotation of heart
123660008,Dextrorotation of heart
125963005,Patent ductus arteriosus with left-to-right shunt
125964004,Patent ductus arteriosus with right-to-left shunt
126037009,Traumatic rupture of aorta
127014009,Peripheral angiopathy due to diabetes mellitus
12770006,Cyanotic congenital heart disease
1279006,Repair of cardiac pacemaker pocket in skin AND/OR subcutaneous tissue
128053003,Deep venous thrombosis
128054009,Deep venous thrombosis of upper extremity
128055005,Deep venous thrombosis of pelvic vein
128238001,Chronic heart disease
128404006,Right heart failure
128551005,Aortic fistula
128566008,Congenital pulmonary vein confluence
128584005,Congenital pulmonary artery conduit
12951009,"Implantation of electrode into cardiac atrium, replacement"
132091000119104,Chronic deep venous thrombosis of lower limb due to coronary artery bypass grafting
132111000119107,Acute deep venous thrombosis of lower limb due to coronary artery bypass grafting
13213009,Congenital heart disease
132131000119102,Chronic deep venous thrombosis of calf
132141000119106,Chronic deep venous thrombosis of lower extremity
132151000119108,Chronic deep venous thrombosis of popliteal vein
132161000119105,Chronic deep venous thrombosis of tibial vein
132171000119104,Chronic deep venous thrombosis of thigh
132191000119103,Chronic deep venous thrombosis of femoral vein
132201000119100,Chronic deep venous thrombosis of iliofemoral vein
132221000119109,Chronic deep venous thrombosis of upper extremity
132241000119103,Acute deep venous thrombosis of calf
132251000119101,Acute deep venous thrombosis of popliteal vein
132261000119104,Acute deep venous thrombosis of tibial vein
132271000119105,Acute deep venous thrombosis of thigh
132281000119108,Acute deep venous thrombosis
132291000119106,Acute deep venous thrombosis of femoral vein
132301000119107,Acute deep venous thrombosis of iliofemoral vein
132321000119103,Acute deep venous thrombosis of upper extremity
132531000119105,Chronic thrombosis of superficial vein of upper extremity
132551000119104,Chronic thrombosis of subclavian vein
132591000119109,Acute thrombosis of superficial vein of upper extremity
132601000119102,Acute deep venous thrombosis of pelvic vein
132611000119104,Acute thrombosis of subclavian vein
133411000119108,Chronic thrombosis of mesenteric vein
133421000119101,Acute thrombosis of mesenteric vein
133971000119108,Chronic pulmonary embolism
134399007,Deep vein thrombosis of leg related to air travel
134961000119104,Acute deep venous thrombosis of axillary vein
135001000119100,Acute deep venous thrombosis of internal jugular vein
135011000119102,Chronic deep venous thrombosis of internal jugular vein
135061000119104,Chronic thrombosis of superior vena cava
135071000119105,Acute thrombosis of superior vena cava
136751000119108,Chronic deep venous thrombosis of upper extremity as complication of procedure
136771000119104,Acute deep venous thrombosis of upper extremity as complication of procedure
136781000119101,Acute deep venous thrombosis of lower extremity as complication of procedure
13730001000004107,Thrombosis of vein of upper limb
13756000,Check artificial pacemaker for electrode impedance
13867009,Preductal coarctation of aorta
13957003,Aortocaval fistula
13963007,Repair of coronary arteriovenous chamber fistula
14201006,Coronary angioplasty by open chest approach
142111000119108,Ectasia of thoracic aorta
142121000119101,Abdominal aortic ectasia
14323007,Aortocoronary bypass of three coronary arteries
14336007,Ruptured abdominal aortic aneurysm
143551000119106,Chronic thrombosis of splenic vein
143561000119108,Acute thrombosis of splenic vein
14534009,Splenic vein thrombosis
14886009,Abdominal heart
14977000,Multiple AND bilateral precerebral artery thrombosis
15191001,Origin of innominate artery from left side of aortic arch
15386007,Stricture of pulmonary vessel
153911000119104,Peripheral arterial insufficiency
15459006,Endocardial cushion defect
15648601000119102,Atherosclerosis of artery of right upper limb
15648691000119108,Atherosclerosis of artery of left upper limb
15648731000119101,Atherosclerosis of right renal artery
15648771000119103,Atherosclerosis of bilateral renal arteries
15648821000119105,Atherosclerosis of left renal artery
15649941000119102,Gangrene of bilateral lower limbs co-occurrent and due to atherosclerosis
15708201000119101,Acute deep vein thrombosis of right upper limb following procedure
15708401000119100,Acute deep vein thrombosis of left upper limb following procedure
15711241000119106,Acute deep vein thrombosis of right lower limb following procedure
15711401000119105,Acute deep vein thrombosis of left lower limb following procedure
15712161000119106,Acute thrombosis of inferior vena cava
15712441000119103,Chronic thrombosis of inferior vena cava
15712641000119101,Ischemia of right upper limb
15723004,Electronic analysis of internal pacemaker system
15742000,Thrombosis of inferior sagittal sinus
15760351000119105,Chronic deep venous thrombosis
15842009,Thrombosis of renal vein
15960021000119107,Dilatation of aortic root co-occurrent and due to Marfan syndrome
15960541000119107,Unstable angina due to arteriosclerosis of autologous vein coronary artery bypass graft
15964901000119107,Atypical atrial flutter
15964981000119104,Congenital anomaly of cardiac chamber
15967301000119102,Stenosis of bilateral subclavian arteries
15967341000119100,Stenosis of right subclavian artery
15972461000119101,Thrombosis of left iliac artery
15972501000119101,Thrombosis of right iliac artery
15972541000119104,Thrombosis of bilateral iliac arteries
15972701000119106,Thrombosis of splenic artery
15978431000119106,Thrombosis of right vertebral artery
15978471000119109,Thrombosis of left vertebral artery
16002551000119103,Pain of left upper limb co-occurrent and due to ischemia
16002711000119105,Pain of right upper limb co-occurrent and due to ischemia
16005391000119108,Occlusion of distal artery of right upper limb
16005471000119100,Occlusion of distal artery of left upper limb
16006031000119103,Thrombophlebitis of vein of right upper limb
16006071000119100,Thrombophlebitis of vein of left upper limb
16006111000119107,Thrombophlebitis of superficial vein of bilateral upper limbs
16006151000119108,Thrombophlebitis of superficial vein of right upper limb
16006191000119103,Thrombophlebitis of superficial vein of left upper limb
16006351000119106,Thrombophlebitis of vein of bilateral upper limbs
16007751000119109,Thrombosis of artery of right upper extremity
16007871000119108,Thrombosis of artery of left upper extremity
16009271000119101,Embolism of artery of right upper limb
16009431000119100,Embolism of artery of left upper limb
16011391000119108,Stenosis of artery of left lower limb
16011431000119103,Stenosis of artery of right lower limb
16011751000119102,Thrombophlebitis of left saphenous vein
16011791000119107,Thrombophlebitis of right saphenous vein
16012511000119101,Embolism of artery of left lower limb
16012551000119100,Embolism of artery of right lower limb
16012591000119105,Embolism of left popliteal artery
16012671000119108,Embolism of right popliteal artery
16012711000119107,Atheroembolism of bilateral lower limbs
16012791000119103,Thrombosis of artery of right lower extremity
16012831000119109,Thrombosis of artery of left lower extremity
16012911000119105,Thrombosis of left popliteal artery
16012951000119106,Thrombosis of right popliteal artery
16012991000119101,Thrombosis of left femoral artery
16013031000119107,Thrombosis of right femoral artery
16013111000119103,Thrombosis of right common femoral artery
16013151000119102,Thrombosis of left common femoral artery
16014311000119102,Thrombophlebitis of vein of bilateral lower limbs
16014471000119103,Thrombophlebitis of vein of right lower limb
16014511000119107,Thrombophlebitis of superficial vein of right lower limb
16014551000119108,Thrombophlebitis of superficial vein of left lower limb
16014591000119103,Thrombophlebitis of superficial vein of bilateral lower limbs
16014631000119103,Thrombophlebitis of vein of left lower limb
16014671000119100,Occlusion of left femoral artery
16014711000119101,Occlusion of right popliteal artery
16014791000119105,Occlusion of left popliteal artery
16014871000119101,Occlusion of right femoral artery
16018831000119106,Atherosclerosis of bilateral iliac arteries
16018911000119107,Atherosclerosis of non-biological bypass graft of bilateral lower limbs
16019471000119104,Atherosclerosis of left iliac artery
16019511000119108,Atherosclerosis of right iliac artery
16025551000119102,Thrombophlebitis of left jugular vein
16025591000119107,Thrombophlebitis of right jugular vein
16026391000119106,Thrombosis of aorta
16026431000119101,Chronic venous thrombosis
161502000,History of myocardial infarct at age less than sixty
161503005,History of myocardial infarct at age greater than sixty
161666008,History of heart recipient
162710004,On examination - collapse -cardiac arrest
16567006,Mesocardia
16573007,Senile cardiac amyloidosis
16574001,Cardiac arrest after obstetrical surgery AND/OR other procedure including delivery
16624001000119104,Intramural hematoma of aorta
16624051000119100,Intramural hematoma of thoracic aorta
16624151000119101,Intramural hematoma of abdominal aorta
16750002,Deep thrombophlebitis
16780001000004106,Abscess of aorta
16781006,Removal of cardiac pacemaker from epicardium with replacement of atrial and/or ventricular leads
16899261000119106,Atherosclerosis of superior mesenteric artery
16972009,Congenital aneurysm of aorta
17024001,Aortopulmonary window
17073005,Aortocoronary artery bypass graft with vein graft
17355002,Aorto-esophageal fistula
1748006,Thrombophlebitis of deep femoral vein
174802006,Allotransplant of heart and lung
174803001,Revision of transplantation of heart and lung
174808005,Xenotransplant of heart
174809002,Heterotopic allotransplant of heart
174810007,Revision of implantation of prosthetic heart
175021005,Allograft bypass of coronary artery
175029007,Prosthetic bypass of coronary artery
175045009,Connection of mammary artery to coronary artery
175047001,Double implantation of mammary arteries into coronary arteries
175048006,Single anastomosis of mammary artery to left anterior descending coronary artery
175050003,Single implantation of mammary artery into coronary artery
175066001,Percutaneous transluminal balloon angioplasty of bypass graft of coronary artery
175137001,Resiting of lead of intravenous pacemaker system
175138006,Maintenance of battery of intravenous cardiac pacemaker system
175140001,Complete removal of implanted cardiac pacemaker system
175142009,Implantation of permanent intravenous cardiac pacemaker
175221003,Construction of central aortopulmonary interposition shunt
175223000,Creation of shunt from ascending aorta to right pulmonary artery using interposition tube prosthesis
175224006,Creation of shunt from ascending aorta to left pulmonary artery using interposition tube prosthesis
175228009,Construction of aortopulmonary window
17920008,Portal vein thrombosis
17954009,Replacement of transvenous atrial pacemaker electrode leads
179924009,Cardiac arrest in fetus OR newborn
17993000,Pulmonary arteritis
18000001000004101,Stenosis of left subclavian artery
180906006,Neonatal cardiac arrest
181869007,Neonatal cardiorespiratory arrest
18322005,Thrombosis of torcular Herophili
18590009,Cardiac pacing
186893003,Rupture of syphilitic cerebral aneurysm
1871002,Repair of aneurysm of coronary artery
18723003,Demand pacing
18919000,Transplantation of coronary artery
19057007,Status anginosus
19242006,Pulmonary edema
192753009,Phlebitis and thrombophlebitis of intracranial sinuses
192759008,Cerebral venous sinus thrombosis
192760003,Thrombosis of superior longitudinal sinus
192761004,Thrombosis transverse sinus
192770001,Thrombophlebitis of cavernous sinus
192771002,Thrombophlebitis of superior longitudinal venous sinus
192772009,Thrombophlebitis lateral venous sinus
194823009,Acute coronary insufficiency
194828000,Angina
194862000,Hemopericardium due to and following acute myocardial infarction
194865003,Rupture of cardiac wall without hemopericardium as current complication following acute myocardial infarction
194883006,Postoperative pulmonary embolus
194892009,Pulmonary artery aneurysm
195002007,Multiple valve disease
195080001,Atrial fibrillation and flutter
195126007,Atrial hypertrophy
195137008,Acquired cardiac septal defect
195229008,Non-pyogenic venous sinus thrombosis
195258006,Thoracic aortic aneurysm which has ruptured
195265003,"Thoracoabdominal aortic aneurysm, ruptured"
195268001,Leaking abdominal aortic aneurysm
195394007,Phlebitis and thrombophlebitis
195396009,Superficial thrombophlebitis of long saphenous vein
195397000,Superficial thrombophlebitis of short saphenous vein
195410000,Thrombophlebitis of the femoral vein
195411001,Thrombophlebitis of the popliteal vein
195412008,Thrombophlebitis of the anterior tibial vein
195414009,Thrombophlebitis of the posterior tibial vein
195425000,Thrombophlebitis of the common iliac vein
195426004,Thrombophlebitis of the internal iliac vein
195427008,Thrombophlebitis of the external iliac vein
195437003,Embolism and thrombosis of the vena cava
195438008,Embolism and thrombosis of the renal vein
196999001,Superior mesenteric artery embolus
197000003,Superior mesenteric artery thrombosis
197001004,Superior mesenteric vein thrombosis
200232006,Antenatal deep vein thrombosis - delivered
200233001,Antenatal deep vein thrombosis with antenatal complication
200237000,Postnatal deep vein thrombosis - delivered with postnatal complication
200238005,Postnatal deep vein thrombosis with postnatal complication
200258006,Obstetric cerebral venous thrombosis
200259003,Cerebral venous thrombosis in pregnancy
200260008,Cerebral venous thrombosis in the puerperium
200284000,Obstetric pulmonary embolism
200308001,Obstetric pyemic and septic pulmonary embolism - delivered
200310004,Obstetric pyemic and septic pulmonary embolism with antenatal complication
200311000,Obstetric pyemic and septic pulmonary embolism with postnatal complication
204296002,Discordant ventriculoarterial connection
204297006,Total great vessel transposition
204299009,Dextrotransposition of aorta
204300001,Incomplete great vessel transposition
204311009,Eisenmenger's complex
204395001,Congenital aneurysm of heart
204397009,Cor triloculare
204398004,Congenital epicardial cyst
204399007,Hemicardia
204423002,Anomalous origin of the aortic arch
204427001,Persistent aortic arch convolutions
204431007,Atresia and stenosis of aorta
204433005,Aplasia of aorta
204443008,Pulmonary artery atresia
204451006,Anomalies of great veins
204456001,Subdiaphragmatic total anomalous pulmonary venous return
204457005,Supradiaphragmatic total anomalous pulmonary venous return
204463001,Absence of inferior vena cava
204464007,Absence of superior vena cava
204467000,Pulmonary vein atresia
20453006,Relocation of cardiac pacemaker pocket to new site in subcutaneous tissue
20721001,Tricuspid valve disorder
20735004,Syphilitic aortitis
20852007,Romano-Ward syndrome
21234008,Congenital stenosis of aorta
21258007,Thrombosis of lateral venous sinus
213037002,Mechanical complication of coronary bypass
213046008,Mechanical complication of intra-aortic balloon
213220000,Postoperative deep vein thrombosis
213310008,Thrombophlebitis after infusion
21379009,Ruptured sinus of Valsalva
21470009,Syncope anginosa
21631000119105,Limb ischemia
218728005,Interrupted aortic arch
2213002,Congenital anomaly of vena cava
2250001,Resection of ascending aorta with anastomosis
225566008,Ischemic chest pain
22750001,Anomalous pulmonary venous drainage to abdominal portion of inferior vena cava
228630004,Repositioning of permanent transvenous electrodes
22870004,Repair of sinus of Valsalva fistula with cardiopulmonary bypass
229577006,Replacement of permanent transvenous electrodes
230221005,Intracranial arterial septic embolism
230222003,Septic thrombophlebitis of straight sinus
230223008,Septic thrombophlebitis of sigmoid sinus
230224002,Septic thrombophlebitis of cortical vein
230225001,Septic thrombophlebitis of great cerebral vein
230361000000100,Pacemaker testing
230588002,Reposition of cardiac pacemaker pocket
230720005,Cerebral venous thrombosis of straight sinus
230721009,Cerebral venous thrombosis of sigmoid sinus
230722002,Cerebral venous thrombosis of cortical vein
230723007,Cerebral venous thrombosis of great cerebral vein
230735006,Syphilitic cerebral arteritis
230740003,Anterior spinal artery thrombosis
231847000,Orbital thrombophlebitis
232038007,Central retinal vein occlusion with neovascularization
232039004,Central retinal vein occlusion with macular edema
232040002,Central retinal vein occlusion - juvenile
232041003,Central retinal vein occlusion - juvenile with neovascularization
232042005,Central retinal vein occlusion - juvenile with macular edema
232043000,Hemispheric retinal vein occlusion
232044006,Hemispheric retinal vein occlusion with neovascularization
232045007,Hemispheric retinal vein occlusion with macular edema
232046008,Branch retinal vein occlusion with neovascularization
232048009,Branch retinal vein occlusion with macular edema
232334003,Replacement of battery of intravenous cardiac pacemaker system
232717009,Coronary artery bypass grafting
232719007,Coronary artery bypass graft x 1
232720001,Coronary artery bypass grafts x 2
232721002,Coronary artery bypass grafts x 3
232722009,Coronary artery bypass grafts x 4
232723004,Coronary artery bypass grafts x 5
232724005,Coronary artery bypass grafts greater than 5
232849000,Aortic valve replacement and plication of ascending aorta
232973007,Allotransplant of heart
232974001,Orthotopic allotransplant of heart
232981000000109,Implantation of single chamber cardiac pacemaker system
232991000000106,Implantation of dual chamber cardiac pacemaker system
233096003,Construction of conduit - left ventricle to ascending aorta
233124005,Construction of intraventricular left ventricle to aorta tunnel
233125006,Construction of intraventricular left ventricle to aorta spiral tunnel
233174007,Cardiac pacemaker procedure
233175008,Temporary cardiac pacemaker procedure
233176009,Direct temporary cardiac pacemaker procedure
233177000,Insertion of epicardial electrode for temporary cardiac pacing
233178005,Insertion of endocardial electrode for temporary cardiac pacing
233179002,Indirect temporary cardiac pacemaker procedure
233180004,Transesophageal cardiac pacing procedure
233181000,Transthoracic cardiac pacing procedure
233182007,Permanent cardiac pacemaker procedure
233183002,Insertion of permanent epicardial cardiac pacemaker system
233184008,Maintenance procedure for cardiac pacemaker system
233185009,Reprogramming of cardiac pacemaker
233187001,Removal of implanted cardiac pacemaker system or components
233188006,Removal of cardiac pacing electrode
233224003,Central aortopulmonary shunt operation
233225002,Disconnection of pulmonary trunk and reanastomosis of distal end to ascending aorta
23325006,Repair of cardiac pacemaker
233815004,Persistent pulmonary hypertension of the newborn
233821000,New onset angina
233847009,Cardiac rupture due to and following acute myocardial infarction
233848004,Disorder of endocardium and heart valve
233885007,Post-infarction pericarditis
233886008,Chronic infective pericarditis
233887004,Chronic pericardial effusion caused by cholesterol
233889001,Post-infarction hemopericardium
233910005,Lone atrial fibrillation
233911009,Non-rheumatic atrial fibrillation
233927002,Cardiac arrest with successful resuscitation
233928007,Myocardial dysfunction
233929004,Post-infarction mural thrombus
233930009,Intracardiac thrombosis in low output state
233936003,Acute massive pulmonary embolism
233937007,Subacute massive pulmonary embolism
233940007,Pulmonary tumor embolism
233941006,Solitary pulmonary hypertension
233942004,Small vessel pulmonary hypertension
233943009,Sporadic primary pulmonary hypertension
233944003,Familial primary pulmonary hypertension
233945002,Pulmonary hypertension caused by drug
233946001,Large vessel pulmonary hypertension
233948000,Post-arteritic pulmonary hypertension
233949008,Pulmonary capillary hemangiomatosis
233950008,Pulmonary hypertension associated with chronic underventilation
233954004,High altitude pulmonary hypertension
233955003,Abdominal aortic atherosclerosis
233958001,Peripheral ischemia
233959009,Upper limb ischemia
233960004,Critical upper limb ischemia
233961000,Lower limb ischemia
233962007,Critical lower limb ischemia
233965009,Stenosis of thoracic aorta
233966005,Stenosis of abdominal aorta
233967001,Common iliac artery stenosis
233968006,External iliac artery stenosis
233969003,Superficial femoral artery stenosis
233970002,Coronary artery stenosis
233972005,Aortic bifurcation embolus
233973000,Femoral artery embolus
233974006,Brachial artery embolus
233976008,Aortic bifurcation thrombosis
233984007,Thoracoabdominal aortic aneurysm
233985008,Abdominal aortic aneurysm
233994002,Dissection of thoracic aorta
233995001,Type I dissection of thoracic aorta
233996000,Type II dissection of thoracic aorta
233997009,Dissection of distal aorta
234011001,Thoracic aorta perforation
234036007,Superficial thrombophlebitis of cephalic vein
234037003,Superficial thrombophlebitis of basilic vein
234040003,Saphenous vein thrombophlebitis
234041004,Inferior mesenteric vein thrombosis
234043001,Thrombosis of vein of lower leg
234044007,Iliofemoral deep vein thrombosis
234045008,Thrombosis of transplanted vein
234046009,Transplant renal vein thrombosis
234047000,Radiation thrombophlebitis
234048005,Recurrent idiopathic thrombophlebitis
234062003,Pulmonary vein stenosis
234065001,Superior vena cava stenosis
234132006,Congenital abnormality of great veins and coronary sinus
234161007,Familial pulmonary capillary hemangiomatosis
234172002,Electromechanical dissociation
234240008,Intra-aortic balloon rupture
234241007,Intra-aortic balloon infection
234242000,Intra-aortic balloon thrombosis
234243005,Inadequate aortic balloon augmentation
235842000,Occlusive mesenteric ischemia
23627006,Chronic pericarditis
236488005,Renal artery occlusion
236489002,Cholesterol embolus syndrome
236721000000106,Implantation of intravenous dual chamber cardiac pacemaker system
23685000,Rheumatic heart disease
237226002,Heart disease during pregnancy
237771000000107,Distant pacemaker test
239297008,Lymphomatoid granulomatosis of lung
239937004,Idiopathic aortitis
239948006,Secondary aortitis
23999003,Implantation of rate-responsive cardiac single-chamber device
240567009,Syphilitic coronary artery disease
241041000000108,Temporary transvenous pacing
241051000000106,Transvenous pacemaker sensitivity measurement
243286001,Acute mesenteric arterial occlusion
243410003,Thrombosis of mesenteric artery
24395005,Check artificial pacemaker for waveform artifact
24596005,Venous retinal branch occlusion
2477008,Superficial thrombophlebitis
24805007,Portal thrombophlebitis
250996007,Complex mitral valve orifice
251036003,Aortic root dilatation
251038002,Aortic root congenital abnormality
251042004,Peripheral pulmonary artery disease
251045002,Peripheral pulmonary artery A/V aneurysm
251046001,Multiple peripheral pulmonary artery stenoses
251047005,Dilatation of pulmonary artery
25263003,Grafting of heart for revascularization
25267002,Insertion of intracardiac pacemaker
253264007,"Congenital heart disease, septal and bulbar anomalies"
253267000,Congenital abnormality of relationship of cardiac component
253269002,Criss-cross heart
253270001,Abnormal relationship of aortic orifice to pulmonary orifice
253271002,Mirror-imaged heart
253272009,Congenital abnormality of cardiac connection
253273004,Cardiac septal defects
253274005,Abnormal atrioventricular connection
253275006,Abnormal atrioventricular connection - biventricular
253277003,Discordant atrioventricular connection
253278008,Ambiguous atrioventricular connection
253279000,Absent atrioventricular connection with straddling valve
253280002,Abnormal atrioventricular connection - univentricular
253285007,Absent right sided atrioventricular connection
253287004,Left sided atrium connecting to right ventricle
253288009,Left sided atrium connecting to both ventricles
253289001,Left sided atrium connecting to ventricle of indeterminate morphology
253290005,Absent left sided atrioventricular connection
253293007,Right sided atrium connecting to both ventricles
253294001,Right sided atrium connecting to ventricle of indeterminate morphology
253295000,Abnormal ventriculoarterial connection
253297008,Transposition of aorta
253302006,Single outlet ventriculoarterial connection
253304007,Solitary pulmonary trunk with aortic atresia
253305008,Solitary arterial trunk
253306009,Abnormality of right superior vena cava
253307000,Atretic right superior vena cava
253308005,Absent right superior vena cava
253309002,Saccular dilatation of right superior vena cava
253310007,Anomalous insertion of right superior vena cava to left atrium
253311006,Bilateral superior vena cava
253312004,Absent bridging vein
253313009,Inferior vena cava interruption with left sided hemiazygos continuation
253314003,Inferior vena cava interruption with right sided azygos continuation
253315002,Inferior vena cava interruption with bilateral azygos continuation
253316001,Abnormal inferior vena caval connection
253317005,Inferior vena cava connecting to morphological left atrium
253318000,Inferior vena cava connecting to coronary sinus
253319008,Inferior vena cava to left of spine
253320002,Inferior cava to left of spine with right descending aorta
253321003,Anomalous termination of right pulmonary vein
253322005,Obstructed pulmonary venous connection
253324006,Coronary sinus defect in left atrium
253327004,Congenital coronary sinus stenosis
253334002,Congenital abnormality of atria and atrial septum
253337009,Isomerism of left atrial appendage
253339007,Right atrial abnormality
253353007,Divided left atrium
253354001,Supramitral left atrial ring
253356004,Left atrial appendage absent
253357008,Left atrial appendage - right - juxtaposition
253358003,Left atrial appendage aneurysm
253359006,Left atrial endocardial fibroelastosis
253360001,Left atrial hypoplasia
253361002,Left atrial dilatation
253362009,Giant left atrium
253364005,Foramen ovale valvar aneurysm
2534005,Congenital absence of vena cava
253438003,Common atrioventricular valve prolapse
253579004,Truncal valve abnormality
253614008,Tubular hypoplasia of aorta
253615009,Anomalies of the aorta excluding coarction
253620009,Pulmonary trunk abnormality
253621008,Pulmonary trunk stenosis
253622001,Pulmonary trunk hypoplasia
253623006,Pulmonary trunk atresia
253627007,Pulmonary trunk absent with confluent pulmonary arteries
253628002,Pulmonary trunk absent with non-confluent pulmonary arteries
253629005,Pulmonary trunk absent with absent pulmonary artery
253630000,Pulmonary trunk dilatation
253631001,Peripheral pulmonary artery stenosis
253632008,Abnormal origin of right pulmonary artery
253633003,Anomalous origin of right pulmonary artery from ductus arteriosus
253634009,Anomalous origin of right pulmonary artery from ascending aorta
253635005,Abnormal origin of left pulmonary artery
253636006,Anomalous origin of left pulmonary artery from ductus arteriosus
253637002,Anomalous origin of left pulmonary artery from ascending aorta
253638007,Anomalous origin of left pulmonary artery from right pulmonary artery
253640002,Ascending aorta abnormality
253641003,Localized supravalvar aortic stenosis
253642005,Diffuse supravalvar aortic stenosis
253643000,Ascending aortic atresia
253644006,Ascending aorta absent
253645007,Ascending aorta dilatation
253646008,Congenital aneurysm of ascending aorta
253647004,Sinus of Valsalva abnormality
253648009,Sinus of Valsalva aneurysm with rupture
253649001,Aortic tunnel
253651002,Aortic arch and descending aorta abnormality
253652009,Right descending aorta
253653004,Left aortic arch and right descending aorta
253654005,Right aortic arch and right descending aorta
253655006,Right aortic arch and left descending aorta
253656007,Aortic arch centrally descending
253657003,Cervical aortic arch
253660005,Double aortic arch with both patent
253663007,Vascular ring with left aortic arch
253664001,Vascular ring with right aortic arch
253672004,Preductal aortic stenosis
253673009,Preductal interruption of aorta
253674003,Preductal hypoplasia of aorta
253675002,Juxtaductal aortic coarctation
253676001,Postductal aortic stenosis
253677005,Postductal interruption of aorta
253678000,Thoracic aortic coarctation
253679008,Abdominal aortic coarctation
253680006,Postductal hypoplasia of aorta
253681005,Interrupted aortic arch distal to left subclavian artery
253682003,Interrupted aortic arch between left subclavian and left common carotid artery
253683008,Interrupted aortic arch between left common carotid and brachiocephalic artery
253685001,Patent ductus arteriosus - delayed closure
253690003,Systemic to pulmonary collateral artery
253691004,Stenosis of systemic to pulmonary artery collateral artery
253692006,Bronchopulmonary collateral artery
253698005,Isolation of brachiocephalic trunk
253732001,Totally absent pericardium
25559009,Congenital absence of left pulmonary artery
257812009,Chronic peri-aortitis
261195002,Circulatory arrest
26146002,Complete transposition of great vessels
261538006,Open intracoronary repair of coronary artery fistula
261756009,Coronary interposition technique
26214006,Thrombosis of retinal artery
262943006,Transection of aorta
264086008,Malaligned outlet septum
265481001,Double anastomosis of mammary arteries to coronary arteries
265482008,Implantation of emergency intravenous cardiac pacemaker
266267005,Deep vein phlebitis and thrombophlebitis of the leg
26660001,Dilatation of aorta
266810008,Replacement of IV endocardial electrode
267284008,Obstetric pyemic and septic pulmonary embolism
26780008,Coarctation of pulmonary artery
268174004,Bulbus cordis and cardiac septal closure anomalies
268180007,Right hypoplastic heart syndrome
268184003,Hypoplasia of aorta
268185002,Supravalvar aortic stenosis
268187005,Congenital pulmonary artery aneurysm
26865008,Congenital absence of superior vena cava
26954004,Thrombophlebitis of superior sagittal sinus
27017003,Chronic effusive pericarditis
270512000,Pulmonary arteriovenous aneurysm
271432005,Congenital renal artery stenosis
271573009,Congenital abnormality of thoracic aorta and pulmonary arteries
271984008,Disorder of prosthetic cardiac valve
271985009,Disorder of intra-aortic pulsation balloon
27277001,Tophus of heart co-occurrent and due to gout
274096000,Pulmonary heart disease
274097009,Non-rheumatic heart valve disorder
274098004,Rupture of chordae tendineae
27443008,Removal of transvenous electrodes
275215001,Left internal mammary artery single anastomosis
275216000,Right internal mammary artery single anastomosis
275217009,Ligation of sinus of Valsalva fistula
275252001,Left internal mammary artery sequential anastomosis
275253006,Right internal mammary artery sequential anastomosis
275514001,Impaired left ventricular function
275516004,Cardiomegaly - hypertensive
275517008,Superficial vein thrombosis
275905002,History of myocardial problem
276308001,General maintenance of cardiac pacemaker
27631000146108,Dissection of aortic arch
27637000,Dextrocardia
276500007,Mesenteric embolus
27651000146102,Dissection of descending aorta
276637009,Hemorrhagic pulmonary edema
276792008,Pulmonary hypertension with extreme obesity
276793003,Pulmonary hypertension with occult mitral stenosis
276794009,Facultative pulmonary hypertension with shunt at atrial level
277192005,Coronary artery graft placement
27944006,Removal of electronic heart device pulse generator
27986000,Congenital pulmonary arteriovenous aneurysm
280966008,Phlegmasia alba dolens - obstetric
281170005,Arrhythmogenic right ventricular cardiomyopathy
281556002,Insertion of temporary cardiac pacemaker
281595001,Thrombosis of inferior vena cava
281596000,Thrombosis of superior vena cava
281597009,Brachiocephalic vein thrombosis
28256002,"Electronic wave or pacemaker analysis, remote"
282664001,Renal artery stenosis of unknown cause
2831000119107,Aneurysm of descending thoracic aorta
285251000119101,Dextrotransposition of the great arteries
285381000119104,Acute deep vein thrombosis of bilateral femoral veins
285721000119104,History of acute ST segment elevation myocardial infarction
285781000119100,Infection of cardiac graft
286071000119109,Congenital peripheral pulmonary artery stenosis
286331000119109,Total anomalous pulmonary venous connection to coronary sinus
286341000119100,Total anomalous pulmonary venous connection to hepatic vein
286351000119103,Total anomalous pulmonary venous connection to right atrium
286361000119101,Total anomalous pulmonary venous connection to superior vena cava
286959000,Peripheral arterial embolism
28714002,Debridement of skin or subcutaneous tissue of pacemaker pocket
287696002,Atrial overdrive pacing
287698001,Fixed-rate cardiac pacemaker
287699009,Emergency cardiac pacemaker
288183004,Insertion of intravenous endocardial electrode
288184005,Removal of IV endocardial electrode
289923007,Acquired renal artery stenosis
293451000119102,Chronic deep vein thrombosis of right iliac vein
293461000119100,Chronic deep vein thrombosis of left iliac vein
293481000119109,Acute deep vein thrombosis of right iliac vein
293491000119107,Acute deep vein thrombosis of left iliac vein
297135003,Subclavian artery embolus
297136002,Axillary artery embolus
297137006,Celiac artery embolus
297138001,Embolus of circle of Willis
297140006,Inferior mesenteric artery embolus
297141005,Popliteal artery embolus
297143008,Suprarenal artery embolus
297146000,Brachial artery thrombosis
297148004,Celiac artery thrombosis
297149007,Common femoral artery thrombosis
297150007,Common iliac artery thrombosis
297151006,External iliac artery thrombosis
297152004,Internal iliac artery thrombosis
297153009,Profunda femoris artery thrombosis
297154003,Subclavian artery thrombosis
297155002,Superficial femoral artery thrombosis
297156001,Axillary vein thrombosis
297157005,Intracranial venous thrombosis
297162006,Crural artery thrombosis
297218007,Congenital abnormality of ductus arteriosus
297911000000108,Electrical capture by temporary transvenous pacing
297921000000102,Mechanical capture by temporary transvenous pacing
29819009,Aortocoronary bypass of one coronary artery
29899005,Coronary artery embolism
29934004,Anomalous pulmonary venous drainage to coronary sinus
300917007,Ischemia of feet
300919005,Digital arterial thrombosis
300921000,Subclavian artery stenosis
300995000,Exercise-induced angina
300996004,Controlled atrial fibrillation
301755001,Ischemic foot
301899003,Dissection of proximal aorta
302131003,Tuberculosis of heart
302233006,Renal artery stenosis
302300004,Femoral popliteal occlusion
302878004,Intracranial septic thrombophlebitis
302879007,Septic thrombophlebitis of cavernous sinus
302880005,Septic thrombophlebitis of sagittal sinus
302881009,Septic thrombophlebitis of lateral sinus
302910002,Atherosclerotic renal artery stenosis
303070000,Pulmonary arteriovenous malformation
30670000,"Anastomosis of thoracic artery to coronary artery, double"
306848006,Occlusion of femoropopliteal bypass graft
306849003,Occlusion of femorofemoral crossover bypass graft
306851004,Occlusion of aortic bifurcation bypass graft
306852006,Occlusion of renal artery bypass graft
306856009,Thrombosis of aortic bifurcation bypass graft
307280005,Implantation of cardiac pacemaker
307403007,Aortojejunal fistula
307404001,Aortocolonic fistula
307406004,Trash foot
307407008,Ischemic hand
307408003,Ischemic toe
307409006,Ischemic finger
307816004,Leriche's syndrome
308065005,History of myocardial infarction in last year
308546005,Dissection of aorta
308805008,Reimplantation of cardiac pacemaker electrode
309405007,Implantation of simple one wire intravenous cardiac pacemaker
309471004,Implantation of temporary intravenous cardiac pacemaker
309735004,Thrombosis of vein of lower limb
309809007,Electromechanical dissociation with successful resuscitation
309814006,Aortocoronary bypass grafting
31019002,Implantation of artificial heart
310415002,Suturing of sinus of Valsalva fistula
310416001,Patching of sinus of Valsalva fistula
31080005,Pericarditis secondary to Mulibrey nanism
31211000119101,Peripheral angiopathy due to type 1 diabetes mellitus
312302004,Plication of ascending aorta
312375001,Upper limb arterial embolus
312377009,Post-radiological embolism of upper limb artery
312378004,Lower limb arterial embolus
312380005,Post-radiological embolism of lower limb artery
312383007,Infective aortitis
312496009,Iliac artery stenosis
312584000,Thrombosis of vein of trunk
312586003,Intracranial thrombophlebitis
312592009,Head and neck arterial embolus
312593004,Trunk arterial embolus
312594005,Head and neck arterial thrombosis
312601003,Thoracic aorta abnormality
31268005,Thrombophlebitis migrans
312822006,Critical ischemia of foot
312825008,Common iliac artery occlusion
312826009,External iliac artery occlusion
312827000,Superficial femoral artery occlusion
312828005,Common femoral artery occlusion
312829002,Common femoral artery stenosis
312997008,Central retinal vein occlusion - ischemic
312998003,Central retinal vein occlusion - non-ischemic
314000002,Branch retinal vein occlusion with no neovascularization
314116003,Post infarct angina
314184006,Ruptured suprarenal aortic aneurysm
314185007,Juxtarenal aortic aneurysm
314186008,Inflammatory abdominal aortic aneurysm
314187004,Iliac artery occlusion
314188009,Femoral artery occlusion
314189001,Popliteal artery occlusion
314208002,Rapid atrial fibrillation
314902007,Peripheral angiopathy due to type 2 diabetes mellitus
315025001,Refractory angina
315026000,Transient myocardial ischemia
31529002,Thrombosis of arteries of upper extremity
315295003,Recurrent abdominal aortic aneurysm
3168002,Thrombophlebitis of intracranial venous sinus
31778009,Replacement of transvenous ventricular pacemaker electrode leads
32194006,Anomalous pulmonary venous drainage to hepatic veins
32413006,Transplantation of heart
32477003,Heart-lung transplant with recipient cardiectomy-pneumonectomy
328511000119109,Saddle embolus of pulmonary artery
33284002,Check artificial pacemaker for amperage threshold
33331003,Insertion of permanent atrial pacemaker with transvenous electrodes
33591000,Thrombosis of arteries of the extremities
33700007,Ruptured sinus of Valsalva into right atrium
33776000,"Insertion of permanent pacemaker with transvenous electrodes, atrio-ventricular sequential"
341751000000103,Congenital dextroposition of heart
343977001,Bundle of His pacing
344994008,Intraventricular pacing
34564005,Creation of shunt of ascending aorta to pulmonary artery
34881000119105,Peripheral vascular disease associated with another disorder
3515001,"Replacement of electronic heart device, pulse generator"
35162007,Ruptured sinus of Valsalva into right ventricle
35386004,Cavernous sinus syndrome
3545003,Diastolic dysfunction
3546002,Aortocoronary artery bypass graft with saphenous vein graft
3589003,Syphilitic pericarditis
35928006,Nocturnal angina
359597003,Single internal mammary-coronary artery bypass
359601003,"Coronary artery bypass with autogenous graft of internal mammary artery, single graft"
359789008,Takayasu's disease
360573001,Post-capillary pulmonary hypertension
360578005,Pulmonary hypertension secondary to raised pulmonary vascular resistance
36110001,Congenital anomaly of pulmonary artery
361278002,Mondor's phlebitis of the penis
36222008,Carcinoid heart disease
363436001,Malignant tumor of endocardium
363437005,Malignant tumor of myocardium
36422005,Transposition of pulmonary veins
36665001,Atrial aneurysm
368009,Heart valve disorder
3681008,Thrombophlebitis of torcular Herophili
37034001,Ligation of arteriovenous fistula of coronary artery
370513009,Fibrosis of cardiac pacemaker electrode
370552002,Dynamic aortic outflow tract obstruction
371037005,Systolic dysfunction
371038000,Terminal aortic occlusion
371039008,Thromboembolic disorder
37104009,Congenital enlargement of coronary sinus
371041009,Embolic stroke
371051005,Traumatic thrombosis of axillary vein
371067004,Hepatopulmonary syndrome
371068009,Myocardial infarction with complication
371807002,Atypical angina
371808007,Recurrent angina status post percutaneous transluminal coronary angioplasty
371809004,Recurrent angina status post coronary stent placement
371810009,Recurrent angina status post coronary artery bypass graft
371811008,Recurrent angina status post rotational atherectomy
371812001,Recurrent angina status post directional coronary atherectomy
371862006,Depression of left ventricular systolic function
371909000,Magnet induced pacing
371910005,Atrioventricular sequential pacing
373135009,Annular abscess of aortic root
373905003,Jervell and Lange-Nielsen syndrome
37943007,Multiple AND bilateral precerebral artery embolism
38208004,Removal of cardiac pacemaker and replacement with single-chamber cardiac device
38230003,Ruptured sinus of Valsalva into left ventricle
38315009,Repair of pacemaker with replacement of pulse generator
38340002,Temporary insertion of pacemaker into atrium by transvenous route
384681005,Patch repair of coronary artery
384683008,Replacement of cardiac pacemaker device with dual-chamber device
384684002,"Removal of cardiac pacemaker with replacement by single-chamber device, rate-responsive"
386815009,Repair of aneurysm of sinus of Valsalva
38739001,Hepatic vein thrombosis
387732009,Becker muscular dystrophy
38877003,Rheumatoid aortitis
39202005,"Coronary artery bypass with autogenous graft, four grafts"
39244004,Pericarditis due to myxedema
39589002,Hypoplasia of right heart
397193006,Percutaneous transluminal coronary angioplasty by rotoablation
39724006,"Anastomosis of internal mammary artery to coronary artery, double vessel"
397431004,"Percutaneous transluminal coronary angioplasty with rotoablation, single vessel"
397829000,Asystole
39785005,Disorder of pulmonary circulation
398220006,Ventricular pacing lead positioned
398274000,Coronary artery thrombosis
399046008,L - transposition of the great vessels
39905002,Scimitar syndrome
399211009,History of myocardial infarction
399216004,D - transposition of the great vessels
39987008,Congenital absence of right pulmonary artery
399957001,Peripheral arterial occlusive disease
400047006,Peripheral vascular disease
400972008,Renewal of intravenous cardiac pacemaker system
40198004,Thrombophlebitis of deep veins of lower extremity
40272001,Congenital absence of coronary sinus
40276003,Embolism of precerebral artery
40283005,Thrombophlebitis of superficial veins of lower extremity
402861007,Ischemic gangrene
404223003,Deep venous thrombosis of lower extremity
404667009,Retinal embolus
404668004,Calcific retinal embolus
404669007,Platelet-fibrin retinal embolus
404670008,Cholesterol retinal embolus
405545007,Mesenteric artery stenosis
405554005,Abscess of aortic root
405556007,Stenosis of lower limb artery
405557003,Occlusion of lower limb artery
405577005,Nontraumatic dissection of thoracic aorta
405580006,Traumatic aortocaval fistula
405585001,Traumatic aorto-enteric fistula
405588004,Upper limb artery stenosis
405598005,Aortocoronary artery bypass graft with two vein grafts
405599002,Aortocoronary artery bypass graft with three vein grafts
405768001,Autotransplantation of heart
40593004,Fibrillation
408665008,Pontine artery thrombosis
408666009,Dissection of abdominal aorta
4090005,Replacement of transvenous atrial and ventricular pacemaker electrode leads
410065004,Congenital anomaly of aortic arch AND/OR descending aorta
410429000,Cardiac arrest
410430005,Cardiorespiratory arrest
412787009,"Intellectual disability, congenital heart disease, blepharophimosis, blepharoptosis and hypoplastic teeth"
41334000,"Angina, class II"
41339005,Coronary angioplasty
413758000,Cardioembolic stroke
413905004,Congenital absence of heart structure
414024009,Disorder of coronary artery
414088005,Emergency coronary artery bypass graft
414089002,Emergency percutaneous coronary intervention
414545008,Ischemic heart disease
415070008,Percutaneous coronary intervention
41514002,Congenital supravalvular mitral stenosis
415991003,Disorder of cardiac ventricle
418461002,Angioplasty of coronary artery using fluoroscopic guidance with contrast
418551006,Laparoscopic coronary artery bypass using robotic assistance
418818005,Brugada syndrome
418824004,Off-pump coronary artery bypass
419132001,Minimally invasive direct coronary artery bypass
420300004,New York Heart Association Classification - Class I
420913000,New York Heart Association Classification - Class III
421365002,Peripheral circulatory disorder due to type 1 diabetes mellitus
421704003,New York Heart Association Classification - Class II
421895002,Peripheral vascular disorder due to diabetes mellitus
422166005,Peripheral circulatory disorder due to type 2 diabetes mellitus
422293003,New York Heart Association Classification - Class IV
422348008,Andersen Tawil syndrome
422967000,Maintenance of permanent cardiac pacemaker settings
422970001,Cardiac arrest due to trauma
423001006,Maintenance of temporary epicardial cardiac pacemaker settings
423168004,Cardiac arrest due to respiratory disorder
423191000,Cardiac arrest due to cardiac disorder
4240001,Rupture of aorta
424265001,Maintenance of temporary cardiac pacemaker system
424571008,Cardiac arrest due to drowning
424727007,Maintenance of temporary cardiac pacemaker settings
425366005,Maintenance of temporary epicardial cardiac pacemaker system
425414000,Bilateral renal artery stenosis
425420004,Thrombosis of internal carotid artery
425453009,Chronic nontraumatic dissection of thoracic aorta
425527003,Atheromatous embolus of lower limb
425771001,Enlarging abdominal aortic aneurysm
425932008,Thrombosis of posterior communicating artery
425963007,Aneurysm of ascending aorta
426104007,Repair of rupture of coronary artery
426270006,Aneurysm of suprarenal aorta
426948001,Aneurysm of descending aorta
427109009,Repair of arteriovenous malformation of coronary artery
427184002,Thrombosis of ulnar artery
427490006,Aneurysm of supraceliac aorta
427567003,Atheromatous embolus of upper limb
427592000,Occlusion of superior mesenteric artery
427665004,Paroxysmal atrial flutter
427775006,Deep venous thrombosis of profunda femoris vein
427776007,Thrombosis of the popliteal vein
427927008,Disorder related to cardiac transplantation
42861008,Thrombophlebitis of iliac vein
428752002,Recent myocardial infarction
42878004,Thrombosis of thoracic aorta
428781001,Deep venous thrombosis associated with coronary artery bypass graft
429064006,Implantation of biventricular cardiac pacemaker system
429243003,Sustained ventricular fibrillation
429434005,Thrombosis of superficial vein of lower limb
429542009,Implantation of intravenous biventricular cardiac pacemaker system
429559004,Typical angina
429575001,Construction of left ventricle to aorta tunnel with right ventricle to pulmonary trunk direct anastomosis
429620002,Construction of left ventricle to aorta tunnel with right ventricle to pulmonary artery valved conduit
429639007,Percutaneous transluminal balloon angioplasty with insertion of stent into coronary artery
42970005,Nonpyogenic thrombosis of intracranial venous sinus
429809004,Percutaneous transluminal angioplasty of coronary artery using fluoroscopic guidance with contrast
42999000,Chronic adhesive pericarditis
430294007,Reposition of permanent cardiac pacemaker using fluoroscopic guidance
431306005,Fluoroscopy of heart for checking of permanent pacemaker position
431702005,Removal of cardiac pacemaker lead using fluoroscopic guidance
431706008,Occlusion of artery of upper extremity
431846007,Replacement of permanent cardiac pacemaker using fluoroscopic guidance
432084000,Management of permanent pacemaker
432113002,Insertion of temporary cardiac pacemaker using fluoroscopic guidance
432953000,Fluoroscopy of heart for checking of cardiac pacemaker electrode position
433068007,Aneurysm of thoracic aorta
433714008,Removal of temporary cardiac pacemaker lead using fluoroscopic guidance
438483005,Thrombophlebitis of subclavian vein
438646004,Thrombophlebitis of axillary vein
438647008,Thrombosis of subclavian vein
438773007,Recurrent pulmonary embolism
438785004,Deep venous thrombosis of tibial vein
43910005,Congenital hypoplasia of aorta
439731006,Septic thrombophlebitis
440028005,Permanent atrial fibrillation
440059007,Persistent atrial fibrillation
441557008,Septic pulmonary embolism
442105001,Septic embolus of artery
442298000,Fracture of stent of coronary artery
442304009,Combined systolic and diastolic dysfunction
44241007,Heart valve stenosis
442439008,Atherosclerosis of bypass graft of limb
442559009,Bundle branch reentrant ventricular tachycardia
442693003,Atherosclerosis of autologous vein bypass graft of limb
442701004,Atherosclerosis of nonautologous biological bypass graft of limb
442735001,Atherosclerosis of nonautologous bypass graft of limb
442907005,Surgical removal of single chamber pacing cardioverter defibrillator electrode by transthoracic approach
442917000,Congenital long QT syndrome
443210003,Deep venous thrombosis of peroneal vein
443355007,Insertion of dual chamber pulse generator and repositioning of cardioverter defibrillation pulse generator lead
443358009,Surgical removal of transvenous electrode of dual chamber pacing cardioverter defibrillator pulse generator by transthoracic approach
443414005,Cor bovinum
443434006,Replacement of dual chamber pulse generator
443477007,Surgical removal of transvenous electrode of dual chamber pacing cardioverter defibrillator pulse generator by transvenous approach
443523006,Insertion of permanent transvenous electrode of dual chamber pulse generator
443622006,Insertion of temporary transvenous electrode of dual chamber cardiac pulse generator
443676006,Surgical removal of transvenous electrode of single chamber pacing cardioverter defibrillator pulse generator by transthoracic approach
443742008,Insertion of transvenous electrode of single chamber pacing cardioverter defibrillator pulse generator
443753002,Insertion of single chamber pacemaker pulse generator
443762000,Hypertrophic cardiomegaly
443816004,Insertion of temporary transvenous electrode of single chamber pacing pulse generator
443852000,Replacement of temporary transvenous electrode of dual chamber pulse generator
443958002,Surgical removal of transvenous electrode of single chamber pacing cardioverter defibrillator pulse generator by transvenous approach
444179007,Insertion of dual chamber pacemaker pulse generator
444325005,Deep vein thrombosis of bilateral lower extremities
444401001,Insertion of single chamber pacing cardioverter defibrillator pulse generator
444437006,Insertion of transvenous electrode of dual chamber pacing cardioverter defibrillator pulse generator
444542000,Insertion of single chamber pacing cardioverter defibrillator pulse generator and transvenous electrode
444566006,Replacement of cardiac pacemaker
444569004,Aneurysm of infrarenal abdominal aorta
444851003,Bifid apex of heart
445027003,Left superior caval vein persisting to coronary sinus
445106006,Congenital dilation of left pulmonary artery
445167000,Congenital dilation of right pulmonary artery
445176007,Congenital dilation of ascending aorta
445208002,Congenital hypoplasia of right pulmonary artery
445209005,Congenital hypoplasia of left pulmonary artery
445237003,Portopulmonary hypertension
445268004,Apex of heart anterior to cardiac base
445284003,Aortic sinus of Valsalva aneurysm from noncoronary sinus
445285002,Aortic sinus of Valsalva aneurysm from left coronary sinus
445286001,Aortic sinus of Valsalva aneurysm from right coronary sinus
445296005,Infracardiac location of anomalous pulmonary venous connections to portal system
445371009,Infracardiac location of anomalous pulmonary venous connections to inferior caval vein
445435009,Apex of heart posterior to cardiac base
445436005,Left superior caval vein persisting to left sided atrium
445543002,Intracardiac location of anomalous pulmonary venous connections to bilateral isomeric atriums
446432002,Pulmonary venous hypoplasia
446657003,Criss-cross heart with rightward rotation
446667008,Two atrioventricular valves in double inlet ventricle
446668003,Obstructed pulmonary venous connection due to extrinsic compression
446813000,Left atrial hypertrophy
446890001,Obstructed pulmonary venous connection at coronary sinus orifice
446909006,Midline apex of heart
446916007,Functionally univentricular heart
447269006,Persistent common pulmonary vein
447274003,Obstructed pulmonary venous connection due to intrinsic narrowing
447275002,Alveolar capillary dysplasia with pulmonary venous misalignment
447289007,Criss-cross heart with leftward rotation
447318008,Obstructed pulmonary venous connection at interatrial communication
447498008,Obstructed pulmonary venous connection due to extrinsic compression between right pulmonary artery and trachea
447528003,Obstructed pulmonary venous connection due to extrinsic compression at diaphragm
447571007,Obstructed pulmonary venous connection due to extrinsic compression between left pulmonary artery and bronchus
447661004,Diverticulum of coronary sinus
447663001,Pulmonary venous confluence remote from left atrium
447664007,Partial anomalous pulmonary venous connection of part of left lung
447666009,Divided left atrium with all pulmonary veins to proximal chamber and then to left atrium
447667000,Divided left atrium with all pulmonary veins to proximal chamber without communication to left atrium
447668005,Discontinuous pulmonary arteries
447691009,Pulmonary venous confluence in direct proximity to left atrium
447700007,Distal aortopulmonary window with minimal superior rim
447701006,Intermediate aortopulmonary window with adequate superior and inferior rim
447702004,Confluent aortopulmonary window with minimal superior and inferior rim
447703009,Double aortic arch with left arch dominant and coarctation of right arch
447772003,Persisting fifth aortic arch with double barrell arch
447773008,Proximal aortopulmonary window with minimal inferior rim
447786004,Creation of anastomosis from ascending aorta to main pulmonary artery
447812003,Left superior vena cava persisting to right atrium and left atrium
447813008,Pulmonary venous confluence in horizontal orientation
447814002,Pulmonary venous confluence in vertical orientation
447817009,Obstruction of aortic arch
447824005,Congenital abnormality of left atrium
447825006,Congenital abnormality of middle cardiac vein
447827003,Partial anomalous pulmonary venous connection of entire right lung
447832002,Total anomalous pulmonary venous connection of supracardiac type
447840008,Stenosis of right pulmonary artery
447846002,Obstruction of ascending aorta
447849009,Double aortic arch with right arch dominant and atresia of left arch
447850009,Double aortic arch with right arch dominant and coarctation of left arch
447860000,Partial anomalous pulmonary venous connection of part of right lung
447861001,Partial anomalous pulmonary venous connection with anomalous veins connecting first to pulmonary venous confluence
447879002,Creation of anastomosis from ascending aorta to right pulmonary artery
447901004,Aortopulmonary window with tubular connection
447902006,Atresia of left superior vena cava
447903001,Coarctation of right pulmonary artery
447913009,Completely unroofed coronary sinus defect in left atrium
447914003,Total anomalous pulmonary venous connection of intracardiac type
447919008,Univentricular atrioventricular connection with absent right sided atrioventricular connection
447925007,Hypoperfusion of left pulmonary artery due to preferential flow to right pulmonary artery
447926008,Hypoperfusion of right pulmonary artery due to preferential flow to left pulmonary artery
447928009,Double aortic arch with balanced arches
447929001,Double aortic arch with left arch dominant
447930006,Double aortic arch with right arch dominant
447932003,Double outlet ventriculoarterial connections
447938004,Congenital abnormality of cardiac vein
447939007,Partial anomalous pulmonary venous connection of entire left lung
447950005,Creation of anastomosis from ascending aorta to left pulmonary artery
447962009,Divided left atrium with restrictive outlet of proximal chamber to left atrium
447968008,Descending aorta anterior and same side as azygos vein with azygos continuity of inferior vena cava
447970004,Double aortic arch with left arch dominant and atresia of right arch
447976005,Removal of cardiac biventricular permanent pacemaker using fluoroscopic guidance
447988007,Common arterial trunk with pulmonary arteries arising from trunk and unobstructed aortic arch
447997006,Vascular ring with retrotracheal right pulmonary artery from ascending aorta
447998001,Single ventricular outlet above right ventricle
447999009,Single ventricular outlet above left ventricle
448000003,Right superior vena cava connecting to left atrium and right atrium
448027004,Supravalvar pulmonary trunk stenosis
448059006,Pulmonary trunk absent with absent left pulmonary artery
448060001,Pulmonary trunk absent with absent right pulmonary artery
448061002,Shelf-like supravalvar aortic stenosis
448063004,Congenital abnormality of posterior cardiac vein of left ventricle
448066007,Divided left atrium with nonrestrictive outlet of proximal chamber to left atrium
448067003,Recoarctation of aorta
448072007,Single inlet ventricle with absent atrioventricular connection
448075009,Uniatrial biventricular connection with absent right sided atrioventricular connection with straddling valve
448078006,Vascular ring with right aortic arch and right arterial ligament with absent left pulmonary artery
448079003,Vascular ring with right aortic arch and right patent arterial duct with absent left pulmonary artery
448080000,Single ventricular outlet above ventricle of indeterminate morphology
448081001,Hepatic vein to coronary sinus
448084009,Absent pulmonary trunk
448086006,Atresia of pulmonary trunk with absent left pulmonary artery
448087002,Atresia of pulmonary trunk with absent right pulmonary artery
448092000,Vascular ring due to aberrant subclavian artery and bilateral arterial ducts
448097006,Abnormal course of aortic arch
448098001,Aneurysm of aortic sinus of Valsalva with protrusion into pulmonary artery
448099009,Aneurysm of aortic sinus of Valsalva with protrusion into right atrium
448100001,Aneurysm of aortic sinus of Valsalva with protrusion into right ventricle
448104005,Localized supravalvar aortic stenosis at sinutubular junction
448105006,Anomalous origin of pulmonary artery from patent arterial duct
448113007,Right superior vena cava connecting to coronary sinus
448115000,Aneurysm of aortic sinus of Valsalva with protrusion into left atrium
448116004,Aneurysm of aortic sinus of Valsalva with protrusion into left ventricle
448117008,Aneurysm of aortic sinus of Valsalva with protrusion into pericardial cavity
448120000,Common arterial trunk with crossed over pulmonary arteries
448150008,Interrogation of cardiac pacemaker
448153005,Vascular ring with left aortic arch and right arterial duct arising from aberrant retroesophageal right subclavian artery
448154004,Vascular ring with left aortic arch and right arterial duct arising from retroesophageal aortic diverticulum
448158001,Abnormality of thoracoabdominal aorta
448181004,Anomalous coronary venous return
448242007,Repositioning of cardiac pacemaker lead using fluoroscopic guidance
448277007,Midline posterior apex of heart
448278002,Coronary sinus drainage cephalad to left superior vena cava
448280008,Malalignment of aortic sinus in relation to pulmonary sinus
448303009,Vascular ring with left aortic arch to right descending aorta and right arterial ligament
448304003,Vascular ring with left aortic arch to right descending aorta and right patent arterial duct
448305002,Vascular ring with malrotation and dextroversion of heart and hypoplasia of right lung and left arterial duct
448320008,Divided left atrium with some pulmonary veins to proximal chamber
448328001,Aneurysm of aortic sinus of Valsalva without rupture
448332007,Left superior vena cava persisting to right sided atrium
448356006,Coronary sinus drainage cephalad to right superior vena cava
448357002,Midline anterior apex of heart
448471006,Congenital abnormality of ascending aorta
448472004,Congenital abnormality of pulmonary trunk
448478000,Systemic to pulmonary collateral artery from coronary artery
448486000,Anomalous pulmonary to systemic collateral vein
448487009,Anomalous pulmonary venous connection of mixed type
448499002,Infracardiac location of anomalous pulmonary venous connection
448500006,Intracardiac location of anomalous pulmonary venous connection
448501005,Interrupted left inferior vena cava
448510002,Stenosis of left pulmonary artery
448517004,Vascular ring with left aortic arch and retroesophageal right descending aorta and right arterial duct arising from aortic diverticulum and aberrant right subclavian artery
448528000,Aneurysm of aortic sinus of Valsalva with rupture to pericardial cavity
448577008,Muscular subvalvar atresia of aorta
448590001,Maintenance of intravenous cardiac pacemaker system
448595006,Scimitar syndrome with additional anomalous pulmonary venous connection
448599000,Total anomalous pulmonary venous connection of infracardiac type
448611005,Vascular ring with left aortic arch and retrotracheal right patent arterial duct
448612003,Single ventricular outlet above both ventricles
448614002,Inferior vena cava anterior and same side as descending aorta
448620001,Azygos continuation of inferior vena cava to right superior vena cava
448624005,Uniatrial biventricular connection with absent left sided atrioventricular connection with straddling valve
448625006,Univentricular atrioventricular connection with absent left sided atrioventricular connection
448627003,Vascular ring with left aortic arch and right arterial duct arising from aberrant retroesophageal brachiocephalic artery
448628008,Vascular ring with left aortic arch and right arterial duct arising from retroesophageal aortic diverticulum and aberrant right subclavian artery
448629000,Vascular ring with left aortic arch and right arterial ligament
448630005,Vascular ring with left aortic arch and right patent arterial duct
448632002,Left inferior vena cava connecting to left atrium and right atrium
448637008,Coarctation of left pulmonary artery
448645003,Aortic arch hypoplasia between subclavian and common carotid arteries
448646002,Aortic arch hypoplasia distal to subclavian artery
448699008,Thoracotomy and removal of cardiac pacemaker electrodes
448721009,Abnormal course of aortic arch and descending aorta
448722002,Abnormality of abdominal aorta
448723007,Aneurysm of aortic sinus of Valsalva with rupture to left atrium
448724001,Aneurysm of aortic sinus of Valsalva with rupture to left ventricle
448725000,Continuity between aortic valve and mitral valve
448727008,Total anomalous pulmonary venous connections of mixed type
448728003,Supracardiac location of anomalous pulmonary venous connection
448742006,Abnormality of aortic arch
448744007,Aneurysm of aortic sinus of Valsalva with rupture to pulmonary artery
448745008,Aneurysm of aortic sinus of Valsalva with rupture to right atrium
448746009,Aneurysm of aortic sinus of Valsalva with rupture to right ventricle
448747000,Common arterial trunk with pulmonary origin from truncal valve sinus
448782004,Interrupted right inferior vena cava
448783009,Pulmonary vein dilatation
448809003,Common arterial trunk with obstruction of aortic arch
448840005,Repair of supravalvar aorta using patch
448869001,Replacement of cardiac biventricular permanent pacemaker using fluoroscopic guidance
448887003,Common arterial trunk with isolated pulmonary artery
448898002,Outflow tract abnormality in solitary indeterminate ventricle
448905005,Dilatation of aortic sinus of Valsalva
448965008,Inferior vena cava connecting to right atrium and left atrium
449009009,Left inferior vena cava connecting to left sided atrium
449010004,Left inferior vena cava connecting to right sided atrium
44902004,Thrombosis of penis
449025004,Vascular ring with left aortic arch and right arterial duct ligament arising from retroesophageal aortic diverticulum with aberrant right subclavian artery
449085001,Pulmonary artery connecting to coronary artery via collateral artery
449119000,Obstruction of aortic outflow
449120006,Obstruction of pulmonary outflow tract
449125001,Congenital stenosis of pulmonary artery
449184004,Dilatation of descending aorta
449185003,Dilatation of aortic sinutubular junction
449188001,Left superior vena cava persisting to coronary sinus and then to right sided atrium
449232001,Aortic arch hypoplasia between carotid arteries
449271003,Residual coarctation of aorta
449350006,Pulmonary artery with absent proximal arterial connection
449397007,Insertion of permanent cardiac pacemaker pulse generator and electrode
449425007,Intracardiac location of anomalous pulmonary venous connection to coronary sinus
449426008,Left sided azygos continuation of inferior vena cava to left superior vena cava
449427004,Double aortic arch with right arch dominant and left arch patent
449428009,Divided left atrium with all pulmonary veins to proximal chamber and then to left atrium with additional pulmonary venous chamber communication
449429001,Divided left atrium with some pulmonary veins to proximal chamber draining to right atrium
449430006,Double aortic arch with left arch dominant and right arch patent
449433008,Diffuse stenosis of left pulmonary artery
449434002,Supracardiac location of anomalous pulmonary venous connection to left superior vena cava
449435001,Infracardiac location of anomalous pulmonary venous connection with two descending veins
449436000,Divided left atrium with some pulmonary veins to proximal chamber draining to left atrium
449440009,Divided left atrium with all pulmonary veins to proximal chamber without communication to left atrium with extracardiac pulmonary venous chamber communication
449441008,Divided left atrium with all pulmonary veins to proximal chamber without communication to left atrium with pulmonary venous chamber communication to right atrium
449442001,Congenital abnormality of great cardiac vein
449443006,Supracardiac location of anomalous pulmonary venous connection to left sided vertical vein
449444000,Infracardiac location of anomalous pulmonary venous connection to hepatic vein
449451009,Supracardiac location of anomalous pulmonary venous connection to hemiazygos vein
449452002,Intracardiac location of anomalous pulmonary venous connection to right atrium
449458003,Right superior vena cava connecting to coronary sinus and then to left sided atrium
449467003,Diffuse stenosis of right pulmonary artery
449492000,Divided left atrium with all pulmonary veins to proximal chamber and then to left atrium with additional pulmonary venous chamber communication to right atrium
449493005,Supracardiac location of anomalous pulmonary venous connection to right sided vertical vein
449494004,Supracardiac location of anomalous pulmonary venous connection to right superior vena cava
449495003,Infracardiac location of anomalous pulmonary venous connection to patent ductus venosus
449513006,Anomalous pulmonary venous connection of mixed type with one pulmonary venous confluence
449514000,Intracardiac location of anomalous pulmonary venous connection to midline with isomeric atria
449521000,Anomalous pulmonary venous connection of mixed type with two pulmonary venous confluences
449523002,Right superior vena cava persisting to coronary sinus and then to right sided atrium
449532000,Congenital abnormality of anterior cardiac vein
449533005,Supracardiac location of anomalous pulmonary venous connection to azygos vein
449536002,Double aortic arch with right arch dominant and atresia of left arch and left ligament to diverticulum
449547009,Right pulmonary artery with absent proximal arterial connection
449551006,Single stenosis of left pulmonary artery
449559008,Multiple stenoses of left pulmonary artery
449560003,Multiple stenoses of right pulmonary artery
449576007,Left pulmonary artery with absent proximal arterial connection
449587004,Divided left atrium with all pulmonary veins to proximal chamber and then to left atrium with additional pulmonary venous chamber extracardiac communication
449589001,Single stenosis of right pulmonary artery
449593007,Divided left atrium with some pulmonary veins to proximal chamber draining to left atrium and others connecting directly to left atrium
449594001,Divided left atrium with some pulmonary veins to proximal chamber draining to left atrium and others connecting anomalously
449595000,Divided left atrium with some pulmonary veins to proximal chamber draining to right atrium and others connecting anomalously
449596004,Divided left atrium with some pulmonary veins to proximal chamber draining to right atrium and others connecting directly to left atrium
449863006,Insertion of pacemaker for control of atrial fibrillation
449873008,Atherosclerotic plaque disruption with thrombosis of artery
449926001,Inflammatory thrombosis of superficial vein of lower leg
450304006,Coarctation of suprarenal abdominal aorta
450305007,Coarctation of infrarenal abdominal aorta
450312003,Coarctation of aorta between subclavian artery and common carotid artery
450313008,Coarctation of aorta between left common carotid artery and right common carotid artery
450314002,Vascular ring with right aortic arch and left patent ductus arteriosus
450315001,Vascular ring with right aortic arch and left ligamentum arteriosum
450811002,Maintenance of battery of cardiac pacemaker system
450816007,Revision of transplantation of heart
450820006,Replacement of pulse generator of permanent cardiac pacemaker using fluoroscopic guidance
450821005,Replacement of pulse generator of implantable cardioverter defibrillator using fluoroscopic guidance
45237002,Congenital dilatation of aorta
45281005,Atherosclerosis of renal artery
45492009,Congenital stenosis of superior vena cava
4557003,Preinfarction syndrome
45669002,Cardio-omentopexy
45720008,"Implantation of electrode into cardiac ventricle, replacement"
458088003,Major systemic to pulmonary collateral artery
45894003,Medionecrosis of aorta
459062008,Fatal congenital nonlysosomal heart glycogenosis
459160003,Abscess at site of aortic coarctation
459163001,Infective endarteritis at site of aortic coarctation
459164007,Systemic to pulmonary collateral artery from descending thoracic aorta
459165008,Systemic to pulmonary collateral artery from abdominal aorta
459173004,Infective endarteritis at site of aortopulmonary window
45921003,Removal of cardiac pacemaker electrodes with replacement
460307002,Systemic to pulmonary collateral artery from right carotid artery
460312001,Systemic to pulmonary collateral artery from left carotid artery
460365008,Systemic to pulmonary collateral artery from right renal artery
460370001,Systemic to pulmonary collateral artery connecting with artery
460375006,Systemic to pulmonary collateral artery from left renal artery
460380002,Systemic to pulmonary collateral artery from right brachiocephalic artery
460387004,Systemic to pulmonary collateral artery from left brachiocephalic artery
460589002,Vascular ring with right aortic arch and left ligamentum arteriosum between left subclavian artery and left common carotid artery
460590006,Vascular ring with right aortic arch and left ligamentum arteriosum with anomalous retroesophageal left subclavian artery
460591005,Vascular ring with right aortic arch and left ductus arteriosus from anomalous retroesophageal left subclavian artery
460592003,Vascular ring with right aortic arch and left ductus arteriosus from retroesophageal diverticulum of aorta and anomalous left subclavian artery
460593008,Vascular ring with right aortic arch and left ductus arteriosus from anomalous retroesophageal brachiocephalic artery
460594002,Vascular ring with right aortic arch and left ductus arteriosus from retroesophageal diverticulum of aorta
460598004,Acquired stenosis of superior vena cava
460609006,Anomalous insertion of ductus arteriosus
460610001,Anomalous insertion of ductus arteriosus into pulmonary trunk
460611002,Anomalous insertion of ductus arteriosus into right pulmonary artery
460612009,Ductus arteriosus dependent pulmonary circulation
46085004,Thrombosis of retinal vein
460906001,Vascular ring with mirror image branching of right aortic arch and left ligamentum arteriosum
461000119108,History of myocardial infarction in last eight weeks
461089003,Cardiac abnormality due to heart abscess
461090007,Right ductus arteriosus
461091006,Patent right ductus arteriosus
461102008,Anomalous insertion of ductus arteriosus into distal left pulmonary artery
461366002,Congenital hypoplasia of descending aorta
461371009,Congenital hypoplasia of abdominal aorta
461376004,Congenital hypoplasia of thoracoabdominal aorta
461386003,Patent ductus arteriosus with normal origin and insertion
461390001,Anomalous insertion of ductus arteriosus into unknown site
461407005,Acquired stenosis of pulmonary venous structure
461408000,Acquired abnormality of pulmonary venous structure
461557000,Congenital atresia of aortic arch
461562004,Atresia of aortic arch with fibrous cord
461567005,Atresia of aortic arch with fibrous cord distal to subclavian artery
461572001,Atresia of aortic arch with fibrous cord between subclavian artery and common carotid artery
461577007,Atresia of aortic arch with fibrous cord between left common carotid artery and right common carotid artery
461587006,Congenital luminal atresia of aortic arch distal to subclavian artery
461592008,Congenital luminal atresia of aortic arch between subclavian artery and common carotid artery
461597002,Congenital luminal atresia of aortic arch between left common carotid artery and right common carotid artery
461602009,Acquired complete obstruction of aortic arch
461609000,Acquired luminal obstruction of aortic arch
461614001,Acquired luminal obstruction of aortic arch distal to subclavian artery
461619006,Acquired luminal obstruction of aortic arch between subclavian artery and common carotid artery
461624009,Acquired luminal obstruction of aortic arch between left common carotid artery and right common carotid artery
461629004,Right aortic arch branching pattern
46253008,Thrombophlebitis of lower extremities
4641009,Myxedema heart disease
46847001,Chronic pulmonary edema
46935006,Stokes-Adams syndrome
47040006,Disorder of aorta
47058000,Heart transplant with recipient cardiectomy
471268000,Middle aortic syndrome
471274000,Systemic to pulmonary collateral artery contributing to dual lung supply
471851005,Disorder of myocardium associated with rejection of cardiac transplant
471863000,Disorder of myocardium due to sickle cell hemoglobinopathy
472101004,Interruption of aortic arch distal to subclavian artery
472102006,Interruption of aortic arch between subclavian artery and common carotid artery
472103001,Interruption of aortic arch between left common carotid artery and right common carotid artery
472702003,Fetal pulmonary outflow tract obstruction due to twin to twin transfusion syndrome
472703008,Pseudoacardia
472750004,Stenosis of superior vena cava as complication of procedure
472756005,Stenosis of anastomosis between pulmonary venous confluence and left atrium after prior repair of anomalous pulmonary venous connection
472757001,Pulmonary venous hypertension as complication of procedure
472758006,Pulmonary venous hypertension due to compression of pulmonary great vein
472759003,Pulmonary venous hypertension due to compression of pulmonary great vein by sclerosing mediastinitis
472760008,Pulmonary venous hypertension due to compression of pulmonary great vein by lymphadenopathy
472761007,Pulmonary venous hypertension due to compression of pulmonary great vein by neoplasm
472762000,Disorder of right atrium
472763005,Disorder of left atrium
472764004,Disorder of right atrium as complication of procedure
472768001,Obstruction of pulmonary great vein due to compression by right atrial dilatation
472789005,Obstruction of surgically constructed pulmonary venous pathway as complication of procedure
472790001,Pulmonary venous hypertension due to disorder of left heart
472791002,Stenosis of pulmonary great vein as complication of procedure
472820000,Abnormal ventriculoarterial connection with usual origin of left coronary artery from aortic sinus to right of nonfacing aortic sinus and usual origin of right coronary artery from aortic sinus to left of nonfacing aortic sinus
473360003,Thrombus of left atrium
473393007,Congenital occlusion of coronary sinus
47780009,Superficial thrombophlebitis complicating pregnancy AND/OR puerperium
47800001,Repair of coronary arteriocardiac chamber fistula
48121000,Congenital cardiomegaly
48248005,Thrombophlebitis of inferior sagittal sinus
48431000,"Anastomosis of thoracic artery to coronary artery, single"
48520006,Congenital atresia of cardiac vein
48601002,Thrombosis of precerebral artery
49436004,Atrial fibrillation
49778009,Idiopathic pulmonary arteriosclerosis
49956009,Antepartum deep phlebothrombosis
50511005,Electronic analysis of dual-chamber internal pacemaker system with reprogramming
50570003,Aneurysm of coronary vessels
50799005,Atrioventricular dissociation
51096002,Legal abortion with pulmonary embolism
51274000,Atherosclerosis of arteries of the extremities
51310003,Electronic analysis of dual-chamber internal pacemaker system without reprogramming
51677000,Atheroembolism of renal arteries
51789008,Congenital malposition of cardiac apex
52156004,Femoral artery thrombosis
52496006,Thrombophlebitis of femoropopliteal vein
52535005,Chronic constrictive pericarditis
52757001,Congenital supravalvular pulmonary stenosis
5370000,Atrial flutter
53741008,Coronary arteriosclerosis
54160000,Congenital aneurysm of sinus of Valsalva
54636000,Cardiomyopexy
54682008,Congenital hypoplasia of pulmonary artery
54687002,Arterial embolism
54866009,Initial implantation of cardiac single-chamber device
54974006,"Insertion of permanent pacemaker with transvenous electrodes, ventricular"
5499009,Pulmonary hypertensive venous disease
55455004,Revision of pacemaker electrode leads
55589000,Illegal abortion with pulmonary embolism
56265001,Heart disease
56272000,Postpartum deep phlebothrombosis
56970000,Central shunt with prosthetic graft
5726007,Removal of epicardial electrodes
57297009,"Implantation of electrode into cardiac atrium and ventricle, replacement"
57809008,Myocardial disease
57834008,Pulmonary artery thrombosis
58123006,Failed attempted abortion with pulmonary embolism
58211007,Removal of electronic heart device battery
58632007,Repair of cardiac pulse generator
58863009,Initial implantation of cardiac dual-chamber device
59021001,Angina decubitus
59047005,Aortointestinal fistula
59218006,Temporary transcutaneous pacing
59282003,Pulmonary embolism
59494005,Congenital septal defect of heart
59631007,Anomalous pulmonary venous drainage
59877000,Congenital anomaly of aorta
60106004,Common arterial trunk and separate origin of pulmonary arteries
60446003,Thyrotoxic heart disease
60787001,Congenital hypoplasia of aortic arch
609480009,Induced termination of pregnancy complicated by pulmonary embolism
60985004,"Implantation of cardiac dual-chamber device, replacement"
61179004,Cardiac beriberi
61490001,"Angina, class I"
61612001,Syphilitic aortic incompetence
61959006,Common truncus arteriosus
62067003,Hypoplastic left heart syndrome
62583006,Puerperal phlegmasia alba dolens
62881002,Removal of cardiac pacemaker
63247009,Williams syndrome
63739005,Coronary occlusion
63795001,Thrombosis of intracranial venous sinus of pregnancy AND/OR puerperium
63934006,Overriding aorta
64156001,Thrombophlebitis
64715009,Hypertensive heart disease
64775002,Vertebral artery thrombosis
64862009,Congenital rhabdomyoma of heart
65084004,Vertebral artery embolism
651000119108,Acute deep vein thrombosis of lower limb
65198009,Arterial thrombosis
65219008,Subcutaneous implantation of cardiac pacemaker
65340007,Aneurysm of heart
65861005,Excision of aneurysm of coronary artery
65936006,Repositioning of cardioverter/defibrillator pulse generator
66189004,Postmyocardial infarction syndrome
66403007,Vascular ring of aorta
66595008,Drug-related myocardial necrosis syndrome
66620003,Hyaline necrosis of aorta
66718009,Check artificial pacemaker by slew rate check
66816004,Implantation of cardiac temporary transvenous pacemaker system during and immediately following cardiac surgery
66858001,Anomalous pulmonary venous drainage to superior vena cava
66877004,Phlegmasia cerulea dolens
66923004,Phlegmasia alba dolens
67166004,Aortocoronary artery bypass graft
67362008,Aortic aneurysm
67486009,Postpartum pelvic thrombophlebitis
67682002,Coronary artery atheroma
677801000119100,Cholesterol retinal embolus of left eye
677811000119102,Cholesterol retinal embolus of right eye
680841000119109,Cholesterol embolus of retinal artery of bilateral eyes
68092007,Anomalous origin of pulmonary artery
682004,Thrombosis complicating pregnancy AND/OR puerperium
68237008,Partial anomalous pulmonary venous connection
68478007,Central retinal vein occlusion
68667005,Insertion of permanent transvenous electrodes
690491000119104,History of cardiomyopathy
690791000119107,Penetrating ulcer of aorta
69158002,Intra-atrial pacing
69357003,Pulmonary thrombosis
697896007,Precapillary pulmonary hypertension
697897003,Heritable pulmonary arterial hypertension
697898008,Idiopathic pulmonary arterial hypertension
697899000,Heritable pulmonary arterial hypertension due to bone morphogenetic protein receptor type II mutation
697900005,Heritable pulmonary arterial hypertension due to activin A receptor type II-like kinase 1 or endoglin mutation
697901009,Pulmonary arterial hypertension caused by toxin
697902002,Associated pulmonary arterial hypertension
697903007,Pulmonary arterial hypertension associated with connective tissue disease
697904001,Pulmonary arterial hypertension associated with human immunodeficiency virus infection
697905000,Pulmonary arterial hypertension associated with congenital heart disease
697906004,Pulmonary arterial hypertension associated with congenital systemic-to-pulmonary shunt
697907008,Pulmonary arterial hypertension associated with schistosomiasis
697908003,Pulmonary arterial hypertension associated with chronic hemolytic anemia
697909006,Pulmonary veno-occlusive disease and/or pulmonary capillary hemangiomatosis
697910001,Pulmonary hypertension due to lung disease and/or hypoxia
697911002,Pulmonary hypertension due to chronic obstructive pulmonary disease
697912009,Pulmonary hypertension due to interstitial lung disease
697913004,Pulmonary hypertension due to pulmonary disease with mixed restrictive and obstructive pattern
697914005,Pulmonary hypertension due to sleep-disordered breathing
697915006,Pulmonary hypertension due to alveolar hypoventilation disorder
697916007,Pulmonary hypertension due to developmental abnormality of the lung
697917003,Pulmonary hypertension due to hematological disorder
697918008,Pulmonary hypertension due to myeloproliferative disorder
697919000,Pulmonary hypertension due to post-splenectomy hematological disorder
697920006,Pulmonary hypertension in systemic disorder
697921005,Pulmonary hypertension in sarcoidosis
697922003,Pulmonary hypertension in Langerhans cell histiocytosis
697923008,Pulmonary hypertension in lymphangioleiomyomatosis
697924002,Pulmonary hypertension in neurofibromatosis
697925001,Pulmonary hypertension due to systolic systemic ventricular dysfunction
697926000,Pulmonary hypertension due to diastolic systemic ventricular dysfunction
697927009,Pulmonary hypertension due to left-sided valvular heart disease
697928004,Pulmonary venous hypertension due to congenital stenosis of pulmonary vein
698270004,Cardiac arrhythmia associated with genetic disorder
698272007,Short QT syndrome
698593009,History of non-ST segment elevation myocardial infarction
698627005,Postoperative phlebitis and thrombophlebitis of intracranial sinuses
698816006,Chronic occlusion of artery of extremity
699123000,Removal of single-chamber cardiac pacemaker with replacement by dual-chamber cardiac pacemaker
699125007,Insertion of programmable cardiac pacemaker
699135001,Implantation of cardiac defibrillator lead
699136000,Insertion of pulse generator of implantable cardioverter defibrillator
699256006,Timothy syndrome type 1
699280005,Repair of aortic root
699297004,Blepharophimosis-intellectual disability syndrome Maat-Kievit-Brunner type
699298009,"Blepharophimosis-mental retardation syndrome, Say-Barber-Biesecker-Young-Simpson type"
699300009,Oculofaciocardiodental syndrome
699352005,Repair of ascending aorta
69954004,Thrombophlebitis of breast
699706000,Embolism of middle cerebral artery
699748007,Cardiorespiratory arrest with successful resuscitation
70195006,Congenital anomaly of superior vena cava
702374000,Neonatal noninfectious cerebral venous sinus thrombosis
703073006,Cardiac pacemaker procedure using fluoroscopic guidance
703158007,Embolism of internal auditory artery
703162001,Bradycardic cardiac arrest
703214003,Silent coronary vasospastic disease
703243006,Acquired aneurysm of pulmonary artery
703244000,Acquired stenosis of left pulmonary artery
703245004,Acquired stenosis of right pulmonary artery
703246003,Acquired pulmonary venous obstruction
703258003,Acquired pulmonary trunk stenosis
703277001,Deep venous thrombosis of femoropopliteal vein
703307003,Acquired abnormality of pulmonary arterial tree
703308008,Acquired dissection of pulmonary artery
703355003,Pulmonary hypertension due to vasculitis
703357006,Acquired discontinuity of pulmonary arteries
703385008,Anomalous origin of pulmonary artery from ascending aorta
703636009,Pulmonary oil microembolism
704115002,Revision of cardiac pacemaker electrode using fluoroscopic guidance
705129007,Thrombosis of middle cerebral artery
70573000,Insertion of pacemaker pulse generator
70589002,Removal of epicardial electrodes with replacement of epicardial lead
70602002,Pseudocoarctation of aorta
70607008,Thrombosis of superior sagittal sinus
706870000,Acute pulmonary embolism
706923002,Longstanding persistent atrial fibrillation
707200002,Descending aorta anterior and same side as azygos vein with absent inferior vena cava
707371002,Congenital stenosis of left pulmonary artery
707372009,Congenital stenosis of right pulmonary artery
707437005,Pulmonary capillaritis
707476006,Stenosis of right pulmonary artery as complication of procedure
707477002,Stenosis of left pulmonary artery as complication of procedure
707478007,Pulmonary trunk stenosis as complication of procedure
707665002,Pulmonary arterial tree abnormality as complication of procedure
707667005,Obstruction of pulmonary vein as complication of procedure
707668000,Pulmonary vein abnormality as complication of procedure
707828002,Percutaneous transluminal cutting balloon angioplasty of coronary artery
708966001,Percutaneous removal of cardiac pacemaker electrode
70933002,Aortitis
709584004,Atherosclerosis of bypass graft of lower limb
709585003,Atherosclerosis of nonautologous biological bypass graft of lower limb
709587006,Atherosclerosis of autologous bypass graft of lower limb
709597002,Acute thrombosis of superficial vein of lower limb
709602009,Chronic thrombosis of superficial vein of lower limb
709687000,Chronic deep vein thrombosis of pelvic vein
70995007,Pulmonary hypertension
710167004,Recurrent deep vein thrombosis
711166001,Removal of implantable cardiac pacemaker
712578006,Aneurysm of aortic arch
712866001,Resting ischemia co-occurrent and due to ischemic heart disease
713029000,Dissection of thoracoabdominal aorta
713030005,Chronic dissection of thoracic aorta
713044004,Removal of cardiac pacemaker using fluoroscopic guidance
713078005,Pulmonary embolism on long-term anticoagulation therapy
713405002,Subacute ischemic heart disease
713419002,Intraoperative cardiorespiratory arrest
713689002,Repair of coronary artery
713825007,Renal artery stenosis of transplanted kidney
71444005,Cerebral arterial thrombosis
715364001,Familial abdominal aortic aneurysm
715395008,Familial atrial fibrillation
715765002,Resection of ascending thoracic aorta using prosthetic graft with cardiopulmonary bypass
715987000,Congenital heart defect with round face and developmental delay syndrome
716050002,Cardiac arrest during surgery
716740009,Potter sequence cleft lip and palate cardiopathy syndrome
7169009,Congenital supravalvular aortic stenosis
71719003,Thrombophlebitis of retinal vein
717859007,"Hydrocephalus, cardiac malformation, dense bone syndrome"
717943008,"Brain malformation, congenital heart disease, postaxial polydactyly syndrome"
718212006,Mitochondrial encephalocardiomyopathy due to transmembrane protein 70 mutation
718216009,Partial defect of atrioventricular canal
718556007,Cranio-cerebello-cardiac dysplasia syndrome
718681002,Oro-facial digital syndrome type 11
71908006,Ventricular fibrillation
71932004,Cardiac dilatation
719379001,Microcephalus with cardiac defect and lung malsegmentation syndrome
719395001,Microcephalus facio-cardio-skeletal syndrome Hadziselimovic type
719400000,Lethal faciocardiomelic dysplasia
719456001,Cleft lip and cleft palate with intestinal malrotation and cardiopathy syndrome
719907006,Timothy syndrome type 2
720448006,Typical atrial flutter
720567008,Bosley Salih Alorainy syndrome
720575002,Braddock syndrome
720605009,Cardiac anomaly and heterotaxy syndrome
720606005,Cardiocranial syndrome Pfeiffer type
720639008,"Coloboma, congenital heart disease, ichthyosiform dermatosis, intellectual disability ear anomaly syndrome"
721009008,Heart defect and limb shortening syndrome
721015008,Hydrocephalus with endocardial fibroelastosis and cataract syndrome
721073008,Short stature with webbed neck and congenital heart disease syndrome
721238001,Acquired anomaly of pulmonary artery
721976003,Lung agenesis with heart defect and thumb anomaly syndrome
722006004,Isotretinoin embryopathy-like syndrome
722027009,Kallman syndrome with heart disease
722051004,"Obesity, colitis, hypothyroidism, cardiac hypertrophy, developmental delay syndrome"
722206009,"Pancreatic hypoplasia, diabetes mellitus, congenital heart disease syndrome"
72242008,Postductal coarctation of aorta
722461004,Meacham syndrome
72252007,Congenital hypoplasia of cardiac vein
722919003,Neonatal cardiac failure due to decreased left ventricular output
722930000,Neonatal thrombosis of cerebral venous sinus
723304001,"Microcephaly, seizure, intellectual disability, heart disease syndrome"
723333000,Faciocardiorenal syndrome
723859005,Pulmonary embolism due to and following acute myocardial infarction
723860000,Arrhythmia due to and following acute myocardial infarction
723866006,Idiopathic ventricular fibrillation not Brugada type
723867002,Coarctation of aortic arch
723871004,Acute occlusion of aortoiliac artery due to thrombosis
723872006,Acute occlusion of artery of lower limb due to thrombosis
723874007,Arterial obstruction due to nonthrombotic embolism from heart
724066002,Polysyndactyly and cardiac malformation syndrome
724208006,Keutel syndrome
724435004,Congenital anomaly of descending thoracic aorta
724436003,Congenital anomaly of abdominal aorta
724437007,Compression of trachea and esophagus co-occurrent and due to congenital anomaly of aortic arch
724440007,Atherosclerosis of artery of lower limb
724441006,Non-atherosclerotic chronic arterial occlusive disease
724442004,Dissection of ascending aorta and aortic arch
724550005,Neonatal cardiac failure due to pulmonary overperfusion
726011000,Placement of stent in coronary artery bypass graft
726083008,Congenital sacral meningocele with conotruncal heart defect syndrome
726571000000105,Absent right sided atrioventricular connection with straddling valve
726581000000107,Absent left sided atrioventricular connection with straddling valve
726704006,"Cataract, congenital heart disease, neural tube defect syndrome"
727151000000108,Right superior vena cava connecting to coronary sinus and right sided atrium
727161000000106,Right superior vena cava connecting to coronary sinus and left sided atrium
727221000000107,Left superior vena cava persisting to coronary sinus and right atrium
727801000000102,Congenital pulmonary venous confluence in vertical orientation
727811000000100,Congenital pulmonary venous confluence in horizontal orientation
727821000000106,Congenital pulmonary venous confluence in direct proximity to left atrium
727831000000108,Congenital pulmonary venous confluence remote from left atrium
728371000000102,Divided left atrium with all pulmonary veins to proximal chamber draining to left atrium
728381000000100,Divided left atrium with all pulmonary veins to proximal chamber draining to left atrium with pulmonary venous chamber communication
728391000000103,Divided left atrium with all pulmonary veins to proximal chamber draining to left atrium with pulmonary venous chamber communication to right atrium
728401000000100,Divided left atrium with all pulmonary veins to proximal chamber draining to left atrium with pulmonary venous chamber extracardiac communication
728851000000102,Retro-aortic brachiocephalic vein
728911000000108,Azygos continuation of inferior vena cava to left superior vena cava
72930009,Superficial migratory thrombophlebitis
7305005,Coarctation of aorta
73067008,Ruptured aortic aneurysm
732230001,Dissection of coronary artery
733127007,Acute occlusion of artery of upper limb caused by thrombus
733325006,Combined occlusion by thrombus of retinal artery and retinal vein
733454004,Long thumb brachydactyly syndrome
733491005,Carney complex
734374000,Thrombosis of left carotid artery
734382000,Thrombosis of right carotid artery
734383005,Thrombosis of left middle cerebral artery
734384004,Thrombosis of right middle cerebral artery
734959006,Embolus of left cerebellar artery
734960001,Embolus of right cerebellar artery
734961002,Embolus of left posterior cerebral artery
734963004,Embolus of right posterior cerebral artery
734964005,Embolus of left middle cerebral artery
734965006,Embolus of right middle cerebral artery
735567001,Perforation of pulmonary artery co-occurrent and due to aneurysm of pulmonary artery
735568006,Rupture of pulmonary artery co-occurrent and due to aneurysm of pulmonary artery
735572005,Acute occlusion of artery of upper limb
735573000,Acute aortoiliac occlusion
735574006,Acute occlusion of artery of lower limb
735575007,Perforation of thoracic aorta co-occurrent and due to aneurysm of thoracic aorta
735576008,Perforation of abdominal aorta co-occurrent and due to aneurysm of abdominal aorta
735577004,Perforation of thoracoabdominal aorta co-occurrent and due to aneurysm of thoracoabdominal aorta
736700005,Revision of internal cardiac defibrillator lead using fluoroscopic guidance
736702002,Revision of biventricular permanent pacemaker lead using fluoroscopic guidance
736962007,Bypass of four or more coronary arteries with prosthesis
736963002,Bypass of one coronary artery with prosthesis
736964008,Bypass of three coronary arteries with prosthesis
736965009,Bypass of two coronary arteries with prosthesis
736966005,Aortocoronary artery bypass of four or more coronary arteries with saphenous vein graft
736967001,Aortocoronary artery bypass of one coronary artery with saphenous vein graft
736968006,Aortocoronary artery bypass of three coronary arteries with saphenous vein graft
736969003,Aortocoronary artery bypass of two coronary arteries with saphenous vein graft
736970002,Allograft bypass of four or more coronary arteries
736971003,Allograft bypass of one coronary artery
736972005,Allograft bypass of three coronary arteries
736973000,Allograft bypass of two coronary arteries
73699003,Common arterial trunk and common origin of pulmonary arteries
737011002,Revision of cardiac biventricular implantable cardioverter defibrillator lead using fluoroscopic guidance
737155005,Congenital anomaly of atrioventricular valve
737157002,False aneurysm of aorta due to and following procedure
737158007,Aneurysm of aorta due to and following procedure
73774007,Subacute bacterial endocarditis
7387004,Thrombophlebitis of tibial vein
739024006,Transplanted heart present
739025007,Transplanted heart-lung present
74034002,Isolated dextrocardia
74315008,Pulmonary microemboli
74371005,"Coronary artery bypass with autogenous graft, two grafts"
7438000,Congenital atresia of aorta
74561007,Kommerell's diverticulum
74883004,Thoracic aortic aneurysm without rupture
74908007,Congenital absence of inferior vena cava
75145007,Stricture of aorta
75403004,Cardiac sarcoidosis
75543006,Cerebral embolism
75761004,Infusion of intra-arterial thrombolytic agent with percutaneous transluminal coronary angioplasty
75878002,Abdominal aortic aneurysm without rupture
762250009,Congenital anomaly of great vessel
762252001,Common arterial trunk with aortic dominance
762253006,Common arterial trunk with pulmonary dominance co-occurrent with interrupted aortic arch
762255004,Thrombus of chamber of heart
762256003,Thrombosis of iliac vein
762433009,Tetralogy of Fallot with pulmonary atresia co-occurrent with systemic-to-pulmonary collateral artery
762629007,Occlusion of right middle cerebral artery by embolus
762630002,Occlusion of left middle cerebral artery by embolus
762632005,Occlusion of left cerebellar artery by embolus
762633000,Occlusion of right cerebellar artery by embolus
762651004,Occlusion of right posterior cerebral artery by embolus
762652006,Occlusion of left posterior cerebral artery by embolus
76267008,Pulmonary valve disorder
763279007,"Facial dysmorphism, conductive hearing loss, heart defect syndrome"
763316006,Congenital patent ductus arteriosus aneurysm
763343001,Intraoperative insertion of cardiac pacemaker
763615003,"Aortic arch anomaly, facial dysmorphism, intellectual disability syndrome"
763725002,Percutaneous transluminal angioplasty of coronary artery using drug eluting balloon catheter
763834000,Oro-facial digital syndrome type 12
763835004,Oro-facial digital syndrome type 13
764452004,Retinal arterial macroaneurysm with supravalvular pulmonic stenosis
764457005,Cardiac arrhythmia ankyrin-B related
764521002,Encircling double aortic arch
764697003,Verloove Vanhorick Brubakk syndrome
764965000,Familial thoracic aortic aneurysm and aortic dissection
76598006,Thrombosis of penile vein
766751007,Neuhauser anomaly
766881008,"Carney complex, trismus, pseudocamptodactyly syndrome"
767309006,Double aortic arch with dominant left arch and hypoplasia of right arch
767311002,Double aortic arch with dominant right arch and hypoplasia of left arch
76846002,Pulmonary endarteritis
770111009,Thrombophlebitis of dorsal venous arch of foot
770432008,Ectasia of left atrial appendage
771348000,Repair of supravalvar aortic stenosis
77326008,Removal of pacemaker electrode leads without replacement
773587008,"X-linked intellectual disability, cardiomegaly, congestive heart failure syndrome"
773749003,Genitopalatocardiac syndrome
77453006,Revision of permanent cardiac pacemaker device
776416004,"Hyperuricemia, pulmonary hypertension, renal failure, alkalosis syndrome"
77788005,Vasomotor acroparesthesia
77892009,Pulmonary venous thrombosis
77978002,Persistent left superior vena cava
77996006,Induction of arrhythmia by electrical pacing
78069008,Chronic rheumatic pericarditis
781065009,Transposition of inferior vena cava
781159007,Congenital levorotation of heart
78250005,Ectopia cordis
782724001,Multisystemic smooth muscle dysfunction syndrome
783738002,"Heart defect, tongue hamartoma, polysyndactyly syndrome"
78381004,"Heart disease in mother complicating pregnancy, childbirth AND/OR puerperium"
784162006,Implantation of permanent cardiac pacemaker using fluoroscopic guidance
784163001,Implantation of cardiac biventricular permanent pacemaker using fluoroscopic guidance
784266000,History of heart-lung transplant recipient
784353002,"Pulmonary valve agenesis, intact ventricular septum, persistent ductus arteriosus syndrome"
78485007,Acyanotic congenital heart disease
789036001,Rheumatic aortitis
789690008,Malignant lymphomatoid granulomatosis of lung
792844003,Limb pain at rest due to atherosclerosis of artery of lower limb
7931000119101,Anterior choroidal artery thrombosis
79439001,Congenital anomaly of aortic arch
7991000119102,Congenital dilatation of aortic root
8001000119106,Atherosclerosis of aortoiliac bypass graft
80235008,Hepatic artery embolism
80383008,Embolism of iliac artery
80606009,Carotid artery embolism
8072003,"Replacement of pacemaker device with single-chamber device, not specified as rate-responsive"
80762004,"Infusion of intra-arterial thrombolytic agent with percutaneous transluminal coronary angioplasty, multiple vessels"
81220003,Artificial pacemaker rate check
81577001,Congenital anomaly of inferior vena cava
8166000,Thrombophlebitis of basilar sinus
81817003,Atherosclerosis of aorta
8186001,Cardiomegaly
82153002,Miscarriage with pulmonary embolism
82247006,"Coronary artery bypass with autogenous graft, five grafts"
822501000000101,Endoscopic robot assisted coronary artery bypass
82367000,Aneurysmectomy of ascending aorta with anastomosis
82385007,Budd-Chiari syndrome
8239009,Primary endocardial fibroelastosis
824031000000109,Leaking thoracic aortic aneurysm
82453008,Thrombosis of iliac artery
8254003,Endomyocardial disease
82608003,Atrial dilatation
827163002,Early postmyocardial infarction pericarditis
827164008,Delayed postmyocardial infarction pericarditis
83333004,Creation of cardiac pacemaker pocket new site in subcutaneous tissue
83393002,Relocation of automatic implantable cardioverter/defibrillator
83799000,Corrected transposition of great vessels
838364007,Aortic aneurysm due to Loeys-Dietz syndrome
83883001,Cardiovascular syphilis
83916000,Postpartum thrombophlebitis
83938003,Thrombosis of vena cava
83940008,Hepatic artery thrombosis
840306007,Mild pulmonary hypertension
840307003,Moderate pulmonary hypertension
840308008,Severe pulmonary hypertension
840580004,Peripheral arterial disease
840713005,Phlebitis and thrombophlebitis of iliac vein
840961000000108,Thrombosis of stent of renal artery
84183007,"Electronic analysis of internal pacemaker system, complete"
842041000000107,Occlusion of radial artery
842061000000108,Occlusion of brachial artery
842081000000104,Occlusion of ulnar artery
842141000000108,Occlusion of dorsalis pedis artery
84216001,Cerebral venous thrombosis of pregnancy AND/OR puerperium
84272007,Thrombosis of abdominal aorta
842721000000102,Occlusion of anterior tibial artery
842741000000109,Occlusion of posterior tibial artery
85053006,"Percutaneous transluminal coronary angioplasty, multiple vessels"
85081000,Common arterial trunk and widely separate origin of pulmonary arteries
85284003,"Angina, class III"
853611000000106,Laser sheath removal of cardiac pacemaker lead using fluoroscopic guidance
854941000000100,Insertion of permanent biventricular pacemaker lead using fluoroscopic guidance
854951000000102,Insertion of biventricular implantable cardioverter defibrillator lead using fluoroscopic guidance
85503007,Grafting of omentum to myocardium
85898001,Cardiomyopathy
86003009,Carotid artery thrombosis
860680001,Pulmonary embolism due to and following ectopic pregnancy
860681002,Pulmonary embolism due to and following molar pregnancy
860699005,Deep vein thrombosis of lower extremity due to intravenous drug use
86252004,Agenesis of pulmonary artery
864191000000104,Thrombosis of internal jugular vein
864211000000100,Thrombosis of external jugular vein
868227005,Coronary artery bypass grafting using radial artery graft
868228000,Coronary artery bypass grafting using gastroepiploic artery graft
868230003,Coronary artery bypass grafting using free right internal thoracic artery graft
868231004,Coronary artery bypass grafting using free left internal thoracic artery graft
868245005,Percutaneous coronary intervention of left coronary artery
868246006,Percutaneous coronary intervention of anterior descending branch of left coronary artery
868247002,Percutaneous coronary intervention of circumflex branch of left coronary artery
868248007,Percutaneous coronary intervention of right coronary artery
86885004,Repair of pacemaker electrodes
870255009,Cardiac resynchronization therapy
870323006,Obstructed anomalous pulmonary venous pathway
870574002,Adaptive-rate cardiac pacing
870743002,Anastomosis of right internal thoracic artery to coronary artery
870744008,Anastomosis of left internal thoracic artery to coronary artery
871496000,Sequential anastomosis of left internal thoracic artery to coronary artery
871497009,Sequential anastomosis of right internal thoracic artery to coronary artery
871498004,Sequential anastomosis of free right internal thoracic artery to coronary artery
871536000,Aneurysm of pararenal aorta
871578006,Arteriovenous fistula of pulmonary vessels following superior cavopulmonary anastomosis
871580000,Arteriovenous malformation of pulmonary vessels following cavopulmonary anastomosis
871596002,Residual patency of arterial duct following patent ductus arteriosus repair
871614007,Abnormal intrapericardial course of great arteries
871637001,Thrombosis of multiple cerebral veins
871647003,Common arterial trunk with pulmonary dominance
871650000,Common arterial trunk with pulmonary dominance and aortic coarctation
871661008,Aneurysm of aorta at coarctation site following procedure
871662001,Dissection of aorta at coarctation site following procedure
871663006,Disorder of aorta due to and following correction of congenital heart anomaly
871664000,Stenosis of aortic arch following procedure
871665004,Acquired dilatation of ascending aorta and aortic root
871667007,Disorder of ascending aorta due to conotruncal malformation
871669005,Acquired abnormality of aorta due to congenital heart anomaly
871671005,Acquired stenosis of supravalvar area
8722008,Aortic valve disorder
87239004,Popliteal artery thrombosis
87394009,Episodic pulmonary hypertension
88174006,Basilar artery thrombosis
88223008,Secondary pulmonary hypertension
88553002,Removal of cardioverter/defibrillator pulse generator without replacement
8876004,Aortocoronary artery bypass graft with prosthesis
88922007,Thrombosis of basilar sinus
89135007,Thromboarteritis
89297009,Replacement of temporary transvenous pacemaker system
89323001,"Angina, class IV"
89420002,Pulmonary veno-occlusive disease
89511008,Check artificial pacemaker for voltage threshold
89980009,Thrombosis of cavernous venous sinus
90154003,Papillary muscle disorder
90205004,Cardiac revascularization with bypass anastomosis
90383006,Congenital absence of aorta
90453003,Chronic rheumatic mediastinopericarditis
90487008,Aortocoronary bypass of two coronary arteries
90543002,"Replacement of electronic heart device, transvenous electrode"
9058002,Duodenoaortic fistula
906071000000100,Insertion of cardiac single chamber permanent pacemaker using fluoroscopic guidance
9061001,Check artificial pacemaker
90958004,Thrombosis of arteries of lower extremity
9106006,Intraoperative cardiac pacing and mapping
91335003,Mural thrombus of heart
91338001,"Infusion of intra-arterial thrombolytic agent with percutaneous transluminal coronary angioplasty, single vessel"
91592003,Closure of fistula of sinus of Valsalva
93031005,Congenital atresia of inferior vena cava
93033008,Congenital atresia of superior vena cava
93050005,Congenital dilatation of aortic arch
93051009,Congenital dilatation of atrium
93055000,Congenital dilatation of ductus arteriosus
93056004,Congenital dilatation of inferior vena cava
93059006,Congenital dilatation of pulmonary artery
93062009,Congenital dilatation of superior vena cava
93064005,Congenital duplication of aorta
93262004,Congenital hypoplasia of heart
93305002,Congenital malposition of aorta
93318005,Congenital malposition of ductus arteriosus
93328001,Congenital malposition of inferior vena cava
93347003,Congenital malposition of pulmonary artery
93354009,Congenital malposition of superior vena cava
93384001,Congenital stenosis of aortic arch
93388003,Congenital stenosis of subclavian artery
936451000000108,Percutaneous transluminal balloon angioplasty and insertion of drug eluting stent into coronary artery
93778001,Primary malignant neoplasm of endocardium
93914000,Primary malignant neoplasm of myocardium
94278009,Secondary malignant neoplasm of endocardium
94433008,Secondary malignant neoplasm of myocardium
94702005,Multiple congenital cardiac defects
94703000,Multiple intracardiac shunts
95234008,Retroesophageal aortic arch
95236005,Retroesophageal pulmonary artery
95242009,Right-sided pulmonary arterial trunk
95437004,Non-cardiogenic pulmonary edema
95440004,Atrial septal aneurysm
95441000,Pulmonary artery stenosis
95445009,Thrombophlebitis of vena cava
95446005,Thrombosis of mesenteric vein
95447001,Thrombophlebitis of mesenteric vein
95448006,Thrombosis of pelvic vein
95449003,Thrombophlebitis of pelvic vein
95450003,Thrombophlebitis of upper extremities
95451004,Thrombophlebitis of superficial veins of upper extremities
95452006,Thrombophlebitis of deep veins of upper extremities
95455008,Thrombosis of cerebral veins
95459002,Cerebellar artery thrombosis
95461006,Thrombophlebitis of cerebral vein
95579008,Thrombosis of renal artery
95580006,Renal artery embolism
95620003,Thrombophlebitis of the newborn
95838002,Pulmonary cyanosis
978421000000101,Unprovoked deep vein thrombosis
978441000000108,Provoked deep vein thrombosis
985961000000104,Isolated aortitis
998008,Chagas' disease with heart involvement"""


c10_df = pd.read_csv(io.StringIO(c10), header=0,delimiter=',').astype(str)
spark.createDataFrame(c10_df).createOrReplaceGlobalTempView("ccu002_06_d17_chd_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_chd_primis

# COMMAND ----------

# MAGIC %md ## ckd15_primis

# COMMAND ----------

c11 = """code,term
117681000119102,Chronic kidney disease stage 1 due to hypertension
129151000119102,Chronic kidney disease stage 4 due to hypertension
129161000119100,Chronic kidney disease stage 5 due to hypertension
129171000119106,Chronic kidney disease stage 3 due to hypertension
129181000119109,Chronic kidney disease stage 2 due to hypertension
140101000119109,Hypertension in chronic kidney disease stage 5 due to type 2 diabetes mellitus
140111000119107,Hypertension in chronic kidney disease stage 4 due to type 2 diabetes mellitus
140121000119100,Hypertension in chronic kidney disease stage 3 due to type 2 diabetes mellitus
140131000119102,Hypertension in chronic kidney disease stage 2 due to type 2 diabetes mellitus
153851000119106,Malignant hypertensive chronic kidney disease stage 5
284971000119100,Chronic kidney disease stage 1 due to benign hypertension
284981000119102,Chronic kidney disease stage 2 due to benign hypertension
284991000119104,Chronic kidney disease stage 3 due to benign hypertension
285001000119105,Chronic kidney disease stage 4 due to benign hypertension
285011000119108,Chronic kidney disease stage 5 due to benign hypertension
285851000119102,Malignant hypertensive chronic kidney disease stage 1
285861000119100,Malignant hypertensive chronic kidney disease stage 2
285871000119106,Malignant hypertensive chronic kidney disease stage 3
285881000119109,Malignant hypertensive chronic kidney disease stage 4
324121000000109,Chronic kidney disease stage 1 with proteinuria
324151000000104,Chronic kidney disease stage 1 without proteinuria
324181000000105,Chronic kidney disease stage 2 with proteinuria
324211000000106,Chronic kidney disease stage 2 without proteinuria
324251000000105,Chronic kidney disease stage 3 with proteinuria
324281000000104,Chronic kidney disease stage 3 without proteinuria
324311000000101,Chronic kidney disease stage 3A with proteinuria
324341000000100,Chronic kidney disease stage 3A without proteinuria
324371000000106,Chronic kidney disease stage 3B with proteinuria
324411000000105,Chronic kidney disease stage 3B without proteinuria
324441000000106,Chronic kidney disease stage 4 with proteinuria
324471000000100,Chronic kidney disease stage 4 without proteinuria
324501000000107,Chronic kidney disease stage 5 with proteinuria
324541000000105,Chronic kidney disease stage 5 without proteinuria
431855005,Chronic kidney disease stage 1
431856006,Chronic kidney disease stage 2
431857002,Chronic kidney disease stage 4
433144002,Chronic kidney disease stage 3
433146000,Chronic kidney disease stage 5
691421000119108,Anemia co-occurrent and due to chronic kidney disease stage 3
700378005,Chronic kidney disease stage 3A
700379002,Chronic kidney disease stage 3B
711000119100,Chronic kidney disease stage 5 due to type 2 diabetes mellitus
714152005,Chronic kidney disease stage 5 on dialysis
714153000,Chronic kidney disease stage 5 with transplant
721000119107,Chronic kidney disease stage 4 due to type 2 diabetes mellitus
731000119105,Chronic kidney disease stage 3 due to type 2 diabetes mellitus
741000119101,Chronic kidney disease stage 2 due to type 2 diabetes mellitus
751000119104,Chronic kidney disease stage 1 due to type 2 diabetes mellitus
90721000119101,Chronic kidney disease stage 1 due to type 1 diabetes mellitus
90731000119103,Chronic kidney disease stage 2 due to type 1 diabetes mellitus
90741000119107,Chronic kidney disease stage 3 due to type 1 diabetes mellitus
90751000119109,Chronic kidney disease stage 4 due to type 1 diabetes mellitus
90761000119106,Chronic kidney disease stage 5 due to type 1 diabetes mellitus
949401000000103,Chronic kidney disease with glomerular filtration rate category G1 and albuminuria category A1
949421000000107,Chronic kidney disease with glomerular filtration rate category G1 and albuminuria category A2
949481000000108,Chronic kidney disease with glomerular filtration rate category G1 and albuminuria category A3
949521000000108,Chronic kidney disease with glomerular filtration rate category G2 and albuminuria category A1
949561000000100,Chronic kidney disease with glomerular filtration rate category G2 and albuminuria category A2
949621000000109,Chronic kidney disease with glomerular filtration rate category G2 and albuminuria category A3
949881000000106,Chronic kidney disease with glomerular filtration rate category G3a and albuminuria category A1
949901000000109,Chronic kidney disease with glomerular filtration rate category G3a and albuminuria category A2
949921000000100,Chronic kidney disease with glomerular filtration rate category G3a and albuminuria category A3
950061000000103,Chronic kidney disease with glomerular filtration rate category G3b and albuminuria category A1
950081000000107,Chronic kidney disease with glomerular filtration rate category G3b and albuminuria category A2
950101000000101,Chronic kidney disease with glomerular filtration rate category G3b and albuminuria category A3
950181000000106,Chronic kidney disease with glomerular filtration rate category G4 and albuminuria category A1
950211000000107,Chronic kidney disease with glomerular filtration rate category G4 and albuminuria category A2
950231000000104,Chronic kidney disease with glomerular filtration rate category G4 and albuminuria category A3
950251000000106,Chronic kidney disease with glomerular filtration rate category G5 and albuminuria category A1
950291000000103,Chronic kidney disease with glomerular filtration rate category G5 and albuminuria category A2
950311000000102,Chronic kidney disease with glomerular filtration rate category G5 and albuminuria category A3
96711000119105,Hypertensive heart AND chronic kidney disease stage 5
96721000119103,Hypertensive heart AND chronic kidney disease stage 4
96731000119100,Hypertensive heart AND chronic kidney disease stage 3
96741000119109,Hypertensive heart AND chronic kidney disease stage 2
96751000119106,Hypertensive heart AND chronic kidney disease stage 1"""


c11_df = pd.read_csv(io.StringIO(c11), header=0,delimiter=',').astype(str)
spark.createDataFrame(c11_df).createOrReplaceGlobalTempView("ccu002_06_d17_ckd15_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_ckd15_primis

# COMMAND ----------

# MAGIC %md ## ckd35_primis

# COMMAND ----------

c12 = """code,term
129151000119102,Chronic kidney disease stage 4 due to hypertension
129161000119100,Chronic kidney disease stage 5 due to hypertension
129171000119106,Chronic kidney disease stage 3 due to hypertension
140101000119109,Hypertension in chronic kidney disease stage 5 due to type 2 diabetes mellitus
140111000119107,Hypertension in chronic kidney disease stage 4 due to type 2 diabetes mellitus
140121000119100,Hypertension in chronic kidney disease stage 3 due to type 2 diabetes mellitus
153851000119106,Malignant hypertensive chronic kidney disease stage 5
284991000119104,Chronic kidney disease stage 3 due to benign hypertension
285001000119105,Chronic kidney disease stage 4 due to benign hypertension
285011000119108,Chronic kidney disease stage 5 due to benign hypertension
285871000119106,Malignant hypertensive chronic kidney disease stage 3
285881000119109,Malignant hypertensive chronic kidney disease stage 4
324251000000105,Chronic kidney disease stage 3 with proteinuria
324281000000104,Chronic kidney disease stage 3 without proteinuria
324311000000101,Chronic kidney disease stage 3A with proteinuria
324341000000100,Chronic kidney disease stage 3A without proteinuria
324371000000106,Chronic kidney disease stage 3B with proteinuria
324411000000105,Chronic kidney disease stage 3B without proteinuria
324441000000106,Chronic kidney disease stage 4 with proteinuria
324471000000100,Chronic kidney disease stage 4 without proteinuria
324501000000107,Chronic kidney disease stage 5 with proteinuria
324541000000105,Chronic kidney disease stage 5 without proteinuria
431857002,Chronic kidney disease stage 4
433144002,Chronic kidney disease stage 3
433146000,Chronic kidney disease stage 5
691421000119108,Anemia co-occurrent and due to chronic kidney disease stage 3
700378005,Chronic kidney disease stage 3A
700379002,Chronic kidney disease stage 3B
711000119100,Chronic kidney disease stage 5 due to type 2 diabetes mellitus
714152005,Chronic kidney disease stage 5 on dialysis
714153000,Chronic kidney disease stage 5 with transplant
721000119107,Chronic kidney disease stage 4 due to type 2 diabetes mellitus
731000119105,Chronic kidney disease stage 3 due to type 2 diabetes mellitus
90741000119107,Chronic kidney disease stage 3 due to type 1 diabetes mellitus
90751000119109,Chronic kidney disease stage 4 due to type 1 diabetes mellitus
90761000119106,Chronic kidney disease stage 5 due to type 1 diabetes mellitus
949881000000106,Chronic kidney disease with glomerular filtration rate category G3a and albuminuria category A1
949901000000109,Chronic kidney disease with glomerular filtration rate category G3a and albuminuria category A2
949921000000100,Chronic kidney disease with glomerular filtration rate category G3a and albuminuria category A3
950061000000103,Chronic kidney disease with glomerular filtration rate category G3b and albuminuria category A1
950081000000107,Chronic kidney disease with glomerular filtration rate category G3b and albuminuria category A2
950101000000101,Chronic kidney disease with glomerular filtration rate category G3b and albuminuria category A3
950181000000106,Chronic kidney disease with glomerular filtration rate category G4 and albuminuria category A1
950211000000107,Chronic kidney disease with glomerular filtration rate category G4 and albuminuria category A2
950231000000104,Chronic kidney disease with glomerular filtration rate category G4 and albuminuria category A3
950251000000106,Chronic kidney disease with glomerular filtration rate category G5 and albuminuria category A1
950291000000103,Chronic kidney disease with glomerular filtration rate category G5 and albuminuria category A2
950311000000102,Chronic kidney disease with glomerular filtration rate category G5 and albuminuria category A3
96711000119105,Hypertensive heart AND chronic kidney disease stage 5
96721000119103,Hypertensive heart AND chronic kidney disease stage 4
96731000119100,Hypertensive heart AND chronic kidney disease stage 3"""


c12_df = pd.read_csv(io.StringIO(c12), header=0,delimiter=',').astype(str)
spark.createDataFrame(c12_df).createOrReplaceGlobalTempView("ccu002_06_d17_ckd35_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_ckd35_primis

# COMMAND ----------

# MAGIC %md ## ckd_primis

# COMMAND ----------

c13 = """code,term
1035471000000100,Dialysis therapy started by renal service
104931000119100,Chronic kidney disease due to hypertension
105502003,Dependence on renal dialysis
10757401000119104,Pre-existing hypertensive heart and chronic kidney disease in mother complicating childbirth
10757481000119107,Pre-existing hypertensive heart and chronic kidney disease in mother complicating pregnancy
1081801000112104,Acute nephrotic syndrome
1082321000119100,Nephroblastoma of left kidney
1082331000119102,Nephroblastoma of right kidney
108241001,Dialysis procedure
10848006,Removal of peritoneal dialysis catheter
109477002,Enamel-renal syndrome
11000731000119102,Dependence on continuous ambulatory peritoneal dialysis
11000771000119104,Dependence on continuous cycling peritoneal dialysis
111411000119103,End stage renal disease due to hypertension
112066009,Absent renal function
118781000119108,Pre-existing hypertensive chronic kidney disease in mother complicating pregnancy
120241000119100,Glomerulonephritis due to hepatitis C
123752003,Immune-complex glomerulonephritis
127991000119101,Hypertension concurrent and due to end stage renal disease on dialysis due to type 2 diabetes mellitus
128001000119105,Hypertension concurrent and due to end stage renal disease on dialysis due to type 1 diabetes mellitus
12963004,Dialysis-associated ascites
133031000119106,Thrombosis of arteriovenous graft caused by hemodialysis arteriovenous access device
13335004,Sclerosing glomerulonephritis
13889008,Methyl lomustine nephropathy
1426004,Necrotizing glomerulonephritis
15123008,Familial amyloid nephropathy with urticaria AND deafness
153891000119101,End stage renal disease on dialysis due to hypertension
15859004,Chronic hemodialysis diet
161665007,History of renal transplant
16320631000119104,Dependence on continuous ambulatory peritoneal dialysis due to end stage renal disease
16652001,Fabry's disease
175899003,Autotransplantation of kidney
175901007,Live donor renal transplant
175902000,Cadaveric renal transplant
175948009,Exploration of renal transplant
17901006,Primary hyperoxaluria
1801000119106,"Anemia, pre-end stage renal disease on erythropoietin protocol"
180272001,Insertion of chronic ambulatory peritoneal dialysis catheter
180273006,Removal of chronic ambulatory peritoneal dialysis catheter
180277007,Insertion of temporary peritoneal dialysis catheter
183985008,Renal transplant planned
1866009,Bilateral total nephrectomy
195791000119101,Chronic proliferative glomerulonephritis
197589005,Nephrotic syndrome with proliferative glomerulonephritis
197590001,Nephrotic syndrome with membranous glomerulonephritis
197591002,Nephrotic syndrome with membranoproliferative glomerulonephritis
197592009,Nephrotic syndrome (& [minimal change glomerulonephritis] or [steroid sensitive])
197593004,"Nephrotic syndrome, minor glomerular abnormality"
197594005,"Nephrotic syndrome, focal and segmental glomerular lesions"
197595006,"Nephrotic syndrome, diffuse membranous glomerulonephritis"
197596007,"Nephrotic syndrome, diffuse mesangial proliferative glomerulonephritis"
197597003,"Nephrotic syndrome, diffuse endocapillary proliferative glomerulonephritis"
197598008,"Nephrotic syndrome, diffuse mesangiocapillary glomerulonephritis"
197599000,"Nephrotic syndrome, dense deposit disease"
197600002,"Nephrotic syndrome, diffuse crescentic glomerulonephritis"
197601003,Finnish congenital nephrotic syndrome
197603000,Nephrotic syndrome associated with another disorder
197604006,Nephrotic syndrome in amyloidosis
197605007,Nephrotic syndrome due to diabetes mellitus
197606008,Nephrotic syndrome in malaria
197607004,Nephrotic syndrome in polyarteritis nodosa
197613008,Chronic mesangial proliferative glomerulonephritis
197614002,Chronic rapidly progressive glomerulonephritis
197616000,Chronic glomerulonephritis associated with another disorder
197617009,Chronic exudative glomerulonephritis
197618004,Chronic focal glomerulonephritis
197619007,Chronic diffuse glomerulonephritis
197626007,Focal membranoproliferative glomerulonephritis
197632002,Berger's immunoglobulin A or immunoglobulin G nephropathy
19765000,Complication of dialysis
197654000,Renal failure: [chronic] or [end stage]
197688006,"Acute nephritic syndrome, diffuse crescentic glomerulonephritis"
197689003,Rapidly progressive nephritic syndrome
197690007,"Rapidly progressive nephritic syndrome, minor glomerular abnormality"
197691006,"Rapidly progressive nephritic syndrome, focal and segmental glomerular lesions"
197692004,"Rapidly progressive nephritic syndrome, diffuse membranous glomerulonephritis"
197693009,"Rapidly progressive nephritic syndrome, diffuse mesangial proliferative glomerulonephritis"
197694003,"Rapidly progressive nephritic syndrome, diffuse endocapillary proliferative glomerulonephritis"
197695002,"Rapidly progressive nephritic syndrome, diffuse mesangiocapillary glomerulonephritis"
197696001,"Rapidly progressive nephritic syndrome, dense deposit disease"
197697005,"Rapidly progressive nephritic syndrome, diffuse crescentic glomerulonephritis"
197709005,"Chronic nephritic syndrome, focal and segmental glomerular lesions"
197712008,"Chronic nephritic syndrome, diffuse endocapillary proliferative glomerulonephritis"
197713003,"Chronic nephritic syndrome, diffuse mesangiocapillary glomerulonephritis"
197714009,"Chronic nephritic syndrome, dense deposit disease"
197715005,"Chronic nephritic syndrome, diffuse crescentic glomerulonephritis"
197738008,Glomerular disorders in neoplastic diseases
20917003,Chronic glomerulonephritis
213150003,Kidney transplant failure and rejection
21764004,Renal carnitine transport defect
224967001,Revision of cannula for dialysis
225892009,Revision of arteriovenous shunt for renal dialysis
233766001,Dialysis-associated hypoxia
234046009,Transplant renal vein thrombosis
234348004,Anemia of renal disease
234485006,Epstein syndrome
236138007,Xenograft renal transplant
236380004,Steroid-sensitive nephrotic syndrome
236381000,Steroid-resistant nephrotic syndrome
236382007,Steroid-dependent nephrotic syndrome
236383002,Familial mesangial sclerosis
236384008,Congenital nephrotic syndrome with focal glomerulosclerosis
236385009,Drash syndrome
236392004,Rapidly progressive glomerulonephritis
236393009,Endocapillary glomerulonephritis
236394003,Idiopathic endocapillary glomerulonephritis
236398000,Crescentic glomerulonephritis
236399008,Steroid-sensitive minimal change glomerulonephritis
236400001,Steroid-resistant minimal change glomerulonephritis
236401002,Steroid-dependent minimal change glomerulonephritis
236407003,Immunoglobulin A nephropathy
236409000,Mesangiocapillary glomerulonephritis type III
236410005,Mesangiocapillary glomerulonephritis type IV
236411009,Immunoglobulin M nephropathy
236412002,C1q nephropathy
236413007,Membranous glomerulonephritis - stage I
236414001,Membranous glomerulonephritis - stage II
236415000,Membranous glomerulonephritis - stage III
236416004,Membranous glomerulonephritis - stage IV
236417008,Membranous glomerulonephritis stage V
236418003,Thin basement membrane disease
236419006,Progressive hereditary glomerulonephritis without deafness
236420000,Alport syndrome-like hereditary nephritis
236422008,Fechtner syndrome
236433006,Acute-on-chronic renal failure
236434000,End stage renal failure untreated by renal replacement therapy
236435004,End stage renal failure on dialysis
236436003,End stage renal failure with renal transplant
236441006,Acquired renal cyst with neoplastic change
236452000,Chronic drug-induced tubulointerstitial nephritis
236466005,Congenital Fanconi syndrome
236482006,Inherited renal tubule insufficiency with cholestatic jaundice
236506009,Goodpasture's disease
236508005,Malignancy-associated glomerulonephritis
236519008,Chronic drug-induced renal disease
236520002,Gold nephropathy
236521003,Penicillamine nephropathy
236522005,Chronic cyclosporin A nephrotoxicity
236525007,Chronic radiation nephritis
236528009,Diffuse mesangial sclerosis with ocular abnormalities
236530006,Pulmonic stenosis and congenital nephrosis
236531005,Renal dysplasia and retinal aplasia
236532003,Renal tubular acidosis with progressive nerve deafness
236535001,Glomerulopathy with giant fibrillar deposits
236538004,Acute disorder of hemodialysis
236539007,First use syndrome of dialysis
236540009,Anaphylactoid reaction to dialysis
236541008,Hyperchloremic acidosis associated with dialysis
236542001,Long-term disorder of dialysis
236544000,Matrix stone formation of dialysis
236550005,Polyserositis syndrome of dialysis
236551009,Underdialysis
236552002,Adynamic bone disease
236554001,Pain during inflow of dialysate
236555000,Pain during outflow of dialysate
236556004,Bloodstained peritoneal dialysis effluent
236557008,Peritoneal dialysis catheter exit site infection
236559006,Loss of ultrafiltration
236560001,Loss of solute clearance
236569000,Primary non-function of renal transplant
236570004,Renal transplant rejection
236571000,Hyperacute rejection of renal transplant
236572007,Accelerated rejection of renal transplant
236573002,Very mild acute rejection of renal transplant
236574008,Acute rejection of renal transplant
236575009,Acute rejection of renal transplant - grade I
236576005,Acute rejection of renal transplant - grade II
236577001,Acute rejection of renal transplant - grade III
236578006,Chronic rejection of renal transplant
236579003,Chronic rejection of renal transplant - grade I
236580000,Chronic rejection of renal transplant - grade II
236581001,Chronic rejection of renal transplant - grade III
236582008,Acute-on-chronic rejection of renal transplant
236583003,Failed renal transplant
236584009,Perfusion injury of renal transplant
236587002,Transplant glomerulopathy
236588007,Transplant glomerulopathy - early form
236589004,Transplant glomerulopathy - late form
236614007,Perirenal and periureteric post-transplant lymphocele
236713006,X-linked recessive nephrolithiasis with renal failure
237612000,"Photomyoclonus, diabetes mellitus, deafness, nephropathy and cerebral dysfunction"
238251000000109,Pre-transplantation of kidney work-up of recipient
238314006,Renewal of chronic ambulatory peritoneal dialysis catheter
238315007,Adjustment of chronic ambulatory peritoneal dialysis catheter
238316008,Aspiration of chronic ambulatory peritoneal dialysis catheter
238317004,Flushing of chronic ambulatory peritoneal dialysis catheter
239101000000109,Pre-transplantation of kidney work-up of live donor
239932005,Primary pauci-immune necrotizing and crescentic glomerulonephritis
241951000,Dialysis membrane-induced anaphylactoid reaction
253878003,Adult type polycystic kidney disease type 1
253879006,Adult type polycystic kidney disease type 2
253880009,Autosomal dominant polycystic kidney disease in childhood
254092004,Saldino-Mainzer dysplasia
265550007,Transplant nephrectomy
265763003,Compensation for renal failure
265764009,Renal dialysis
266549004,Nephrotic syndrome with minimal change glomerulonephritis
268234004,Fibrocystic kidney disease
268854008,Congenital renal failure
26944003,Acute megaloblastic anemia due to dialysis
271418008,Chronic ambulatory peritoneal dialysis catheter procedure
276883000,Peritoneal dialysis-associated peritonitis
277010001,Unexplained episode of renal transplant dysfunction
277011002,Pre-existing disease in renal transplant
278905001,Continuous ambulatory peritoneal dialysis diet
28191000119109,Chronic nephritic syndrome with membranous glomerulonephritis
282364005,Immunoglobulin A nephropathy associated with liver disease
284348003,Excision of rejected transplanted kidney
284961000119106,Chronic kidney disease due to benign hypertension
285831000119108,Malignant hypertensive chronic kidney disease
285841000119104,Malignant hypertensive end stage renal disease
286371000119107,Malignant hypertensive end stage renal disease on dialysis
28770003,"Polycystic kidney disease, infantile type"
290006,Melnick-Fraser syndrome
292760002,Dialysis fluid adverse reaction
292761003,Peritoneal dialysis solution adverse reaction
292762005,Hemodialysis fluid adverse reaction
292763000,Hemofiltration solution adverse reaction
295101000119105,Nephropathy co-occurrent and due to systemic lupus erythematosus
295121000119101,Nephrosis co-occurrent and due to systemic lupus erythematosus
302849000,Nephroblastoma
308751000119106,Glomerular disease due to systemic lupus erythematosus
310647000,Anemia secondary to renal failure
313030004,Donor renal transplantation
32599008,Hemodialysis-associated amyloidosis
33461007,Complication of peritoneal dialysis
33603003,Complication of renal dialysis
35546006,Mesangial proliferative glomerulonephritis
359694003,"Idiopathic crescentic glomerulonephritis, type II"
363233007,Nephrotic syndrome secondary to glomerulonephritis
363234001,Nephrotic syndrome secondary to systemic disease
365001000000107,Peritoneal dialysis associated encapsulating peritoneal sclerosis
365061000000106,Active on kidney transplant waiting list
365071000000104,Active on kidney transplant waiting list while waiting live donor work-up
365081000000102,Active on kidney and pancreas transplant waiting list
365111000000105,Active on kidney and other organ transplant waiting list
365131000000102,Active on paired exchange kidney transplant waiting list
365151000000109,Active on kidney transplant waiting list with failing graft
365161000000107,Active on urgent kidney transplant waiting list
367051000119105,Morphologic change of kidney due to chronic nephritic syndrome
367511000119101,"Hereditary mesangiocapillary glomerulonephritis, type 2"
367521000119108,Hereditary diffuse crescentic glomerulonephritis
367531000119106,Hereditary diffuse endocapillary proliferative glomerulonephritis
367541000119102,Hereditary diffuse membranous glomerulonephritis
367551000119100,Hereditary diffuse mesangial proliferative glomerulonephritis
367561000119103,Hereditary diffuse mesangiocapillary glomerulonephritis
367571000119109,Hereditary focal and segmental glomerular lesions
367591000119105,Hereditary nephropathy
368871000119106,Acute nephritic syndrome co-occurrent and due to membranoproliferative glomerulonephritis type III
368881000119109,Rapidly progressive nephritic syndrome co-occurrent and due to membranoproliferative glomerulonephritis type III
368901000119106,Chronic nephritic syndrome co-occurrent and due to membranoproliferative glomerulonephritis type III
368911000119109,Nephrotic syndrome co-occurrent and due to membranoproliferative glomerulonephritis type III
368921000119102,Nephritic syndrome co-occurrent and due to membranoproliferative glomerulonephritis type III
368931000119104,Isolated proteinuria co-occurrent and due to membranoproliferative glomerulonephritis type III
368941000119108,Hereditary nephropathy co-occurrent with membranoproliferative glomerulonephritis type III
3704008,Diffuse endocapillary proliferative glomerulonephritis
37061001,Granulomatous sarcoid nephropathy
37183000,"Cystinuria, type 1"
385971003,Dialysis care
398471000000102,[V]Aftercare involving intermittent dialysis
398887003,Renal replacement
399340005,Hereditary nephritis
40233000,Nephrotic-nephritic syndrome
402458002,Hemodialysis-associated secondary amyloidosis of skin
402762007,Skin lesion associated with hemodialysis
403732009,Hemodialysis-associated pseudoporphyria
404813001,Peritoneal dialysis leakage
406168002,Dialysis access maintenance
408667000,Hemodialysis-associated hypotension
40951006,"Primary hyperoxaluria, type II"
41962002,Oligohydramnios sequence
423062001,Stenosis of arteriovenous dialysis fistula
425369003,Chronic progressive renal failure
425384007,Sarcoidosis with glomerulonephritis
425879009,Amyloid A nephropathy
426136000,Delayed renal graft function
426340003,Creation of graft fistula for dialysis
426598005,Amyloid light-chain nephropathy
427555000,Glomerulonephritis due to granulomatosis with polyangiitis
428118009,Procedure involving peritoneal dialysis catheter
428575007,Hypertension secondary to kidney transplant
428645009,Examination of recipient after kidney transplant
428937001,Dependence on peritoneal dialysis due to end stage renal disease
428982002,Dependence on hemodialysis due to end stage renal disease
429075005,Dependence on dialysis due to end stage renal disease
429451003,Disorder related to renal transplantation
430333000,Hematoma of dialysis access site
431873008,Peritonitis due to infected peritoneal dialysis catheter
432018009,Replacement of dialysis catheter using fluoroscopic guidance
432654009,Insertion of peritoneal dialysis catheter using fluoroscopy guidance
438341004,Laparoscopic insertion of peritoneal dialysis catheter
438342006,Replacement of peritoneal dialysis catheter
4390004,Lithium nephropathy
439534001,Shaving of peritoneal dialysis catheter cuff
440084005,Assessment of adequacy of dialysis
440228000,Leakage of peritoneal dialysate into subcutaneous tissue of abdominal wall
440310004,Leakage of peritoneal dialysate into pleural cavity
440663004,Encapsulating peritoneal sclerosis associated with peritoneal dialysis
441815006,Proliferative glomerulonephritis
443143006,Dependence on hemodialysis
443596009,Dependence on peritoneal dialysis
444645005,Dent's disease
445119005,Steroid sensitive nephrotic syndrome of childhood
445258009,Idiopathic rapidly progressive glomerulonephritis
445404003,Familial immunoglobulin A nephropathy
446449009,Renal coloboma syndrome
446923008,Lipoprotein glomerulopathy
44785005,Minimal change disease
448591002,Repositioning of Tenckhoff catheter
449288005,Infection of arteriovenous fistula for hemodialysis
449408005,Disorder of kidney due to kappa light chain disease
449409002,Disorder of kidney due to lambda light chain disease
449820008,Steroid resistant nephrotic syndrome of childhood
46177005,End-stage renal disease
473195006,Normal renal function of transplanted kidney
48713002,Amyloid nephropathy
48796009,Congenital nephrotic syndrome
49708008,Anemia of chronic renal failure
52213001,Renal homotransplantation excluding donor and recipient nephrectomy
52254009,Nephrotic syndrome
53556002,Cis-platinum nephropathy
55652009,"Idiopathic crescentic glomerulonephritis, type III"
57557005,Chronic milk alkali syndrome
58797008,Complication of transplanted kidney
59400006,Analgesic nephropathy
59479006,"Mesangiocapillary glomerulonephritis, type II"
61165007,Hereditary nephrogenic diabetes insipidus
61598006,Glycogenosis with glucoaminophosphaturia
62216007,Familial arthrogryposis-cholestatic hepatorenal syndrome
62332007,Infantile nephropathic cystinosis
64168005,"Idiopathic crescentic glomerulonephritis, type I"
64212008,Diffuse crescentic glomerulonephritis
6471000179103,Transplantation of kidney and pancreas
65520001,"Primary hyperoxaluria, type I"
66451004,"Familial visceral amyloidosis, Ostertag type"
68779003,Primary immunoglobulin A nephropathy
698306007,Awaiting transplantation of kidney
698869007,Laparoscopic bilateral total nephrectomy
699235009,Continuous ambulatory peritoneal dialysis associated peritonitis
700107006,Bartter syndrome antenatal type 1
700109009,Bartter syndrome antenatal type 2
700111000,Bartter syndrome type 3
700112007,Bartter syndrome type 4
702397002,Renal tubular dysgenesis
702634004,Inadequate peritoneal dialysis
702635003,Inadequate hemodialysis
703048006,Vesicoureteric reflux after renal transplant
703094009,Peritoneal dialysis catheter procedure using fluoroscopic guidance
703102004,Dialysis catheter procedure using fluoroscopic guidance
703310005,Autosomal dominant progressive nephropathy with hypertension
704667004,Hypertension concurrent and due to end stage renal disease on dialysis
705065000,Childhood nephrotic syndrome
70536003,Transplant of kidney
707090004,Spondyloarthropathy due to hemodialysis-associated amyloidosis
707148007,Recurrent post-transplant renal disease
707324008,Anemia co-occurrent and due to end stage renal disease
707332000,Recurrent proliferative glomerulonephritis
707742001,Bartter syndrome
708988001,Laparoscopic repositioning of Tenckhoff catheter
709044004,Chronic kidney disease
710071003,Management of peritoneal dialysis
711411006,Allotransplantation of kidney from beating heart cadaver
711413009,Allotransplantation of kidney from non-beating heart cadaver
711446003,Transplantation of kidney regime
711531007,Focal mesangial proliferative glomerulonephritis
712487000,End stage renal disease due to benign hypertension
713313000,Chronic kidney disease mineral and bone disorder
713695001,Nephrotic syndrome co-occurrent with human immunodeficiency virus infection
713720009,Sclerosing peritonitis as complication of peritoneal dialysis
713721008,Hydrothorax as complication of peritoneal dialysis
713724000,Abdominal hernia as complication of peritoneal dialysis
713727007,Hemoperitoneum as complication of peritoneal dialysis
713825007,Renal artery stenosis of transplanted kidney
713887002,Focal segmental glomerulosclerosis co-occurrent with human immunodeficiency virus infection
71421000119105,Hypertension in chronic kidney disease due to type 2 diabetes mellitus
71441000119104,Nephrotic syndrome due to type 2 diabetes mellitus
714813000,Recurrent hematuria co-occurrent and due to dense deposit disease
714814006,Persistent hematuria co-occurrent and due to dense deposit disease
714815007,Recurrent hematuria co-occurrent and due to diffuse crescentic glomerulonephritis
714816008,Persistent hematuria co-occurrent and due to diffuse crescentic glomerulonephritis
714817004,Recurrent hematuria co-occurrent and due to diffuse endocapillary proliferative glomerulonephritis
714818009,Persistent hematuria co-occurrent and due to diffuse endocapillary proliferative glomerulonephritis
716094008,Fibulo-ulnar hypoplasia and renal anomalies syndrome
716657000,Familial papillary thyroid carcinoma with renal papillary neoplasia syndrome
716999001,Joubert syndrome with renal defect
71701000119105,Hypertension in chronic kidney disease due to type 1 diabetes mellitus
717187000,Nephronophthisis hepatic fibrosis syndrome
717191005,Sporadic idiopathic steroid-resistant nephrotic syndrome
71721000119101,Nephrotic syndrome due to type 1 diabetes mellitus
717736007,Familial renal cell carcinoma
717760006,Multi-drug resistant nephrotic syndrome
717766000,Alport syndrome autosomal dominant
717767009,Alport syndrome autosomal recessive
717768004,Alport syndrome X-linked
717789008,Dent disease type 1
717790004,Dent disease type 2
717791000,Bartter syndrome type 4a
718141008,Familial idiopathic steroid-resistant nephrotic syndrome
718192000,Non-amyloid fibrillary glomerulonephritis
718308002,Peritoneal dialysis care
718330001,Hemodialysis care
719501003,Ultrafiltration failure
719839000,Tubular renal disease with cardiomyopathy syndrome
719840003,Renal dysplasia with limb defect syndrome
720414005,Acrorenal mandibular syndrome
720415006,Acrorenoocular syndrome
720458005,Acrorenal syndrome
720519003,"Atherosclerosis, deafness, diabetes, epilepsy, nephropathy syndrome"
720982007,"Alport syndrome, intellectual disability, midface hypoplasia, elliptocytosis syndrome"
721173005,Hypotonia cystinuria syndrome
721207002,"Seizure, sensorineural deafness, ataxia, intellectual disability, electrolyte imbalance syndrome"
721297008,Galloway Mowat syndrome
721840000,"Hyperuricemia, anemia, renal failure syndrome"
721862000,Joubert syndrome with oculorenal defect
721970009,Persistent Mullerian derivative with lymphangiectasia and polydactyly syndrome
722086002,Membranous glomerulonephritis due to malignant neoplastic disease
722098007,Chronic kidney disease following donor nephrectomy
722118005,Congenital nephrotic syndrome due to congenital infection
722119002,Idiopathic membranous glomerulonephritis
722120008,Membranous glomerulonephritis caused by drug
722149000,Chronic kidney disease following excision of renal neoplasm
722150000,Chronic kidney disease due to systemic infection
722168002,Membranous glomerulonephritis co-occurrent with infectious disease
722231005,Perlman syndrome
722294004,Autosomal dominant intermediate Charcot-Marie-Tooth disease type E
722369003,Congenital nephrotic syndrome due to diffuse mesangial sclerosis
722381004,"Congenital cataract, nephropathy, encephalopathy syndrome"
722433005,Dyschondrosteosis and nephritis syndrome
722457005,"Juvenile cataract, microcornea, renal glucosuria syndrome"
722467000,Chronic kidney disease due to traumatic loss of kidney
722758004,Complement component 3 glomerulopathy
722759007,Glomerulopathy with fibronectin deposits 2
722760002,Dense deposit disease
722761003,Complement component 3 glomerulonephritis
722948009,Glomerular disorder due to non-neuropathic heredofamilial amyloidosis
723190009,Chronic renal insufficiency
723333000,Faciocardiorenal syndrome
723363009,"Hypotrichosis, lymphedema, telangiectasia, renal defect syndrome"
723373006,Uromodulin related autosomal dominant tubulointerstitial kidney disease
723409007,"Multinodular goiter, cystic kidney, polydactyly syndrome"
723440000,Nephrogenic syndrome of inappropriate antidiuresis
723449004,Pierson syndrome
723555007,"Thymic, renal, anal, lung dysplasia syndrome"
723720008,"Sex reversion, kidney, adrenal and lung dysgenesis syndrome"
723995003,Schimke immuno-osseous dysplasia
723999009,"Retinitis pigmentosa, hypopituitarism, nephronophthisis, skeletal dysplasia syndrome"
724094005,"Neonatal diabetes, congenital hypothyroidism, congenital glaucoma, hepatic fibrosis, polycystic kidney syndrome"
724282009,"Hypoparathyroidism, deafness, renal disease syndrome"
724612006,Osteonecrosis due to and following renal dialysis
725033008,Familial primary hypomagnesemia with hypercalciuria and nephrocalcinosis without severe ocular involvement
725905005,Infundibulopelvic stenosis multicystic kidney syndrome
725908007,Neurofaciodigitorenal syndrome
726017001,Mucin 1 related autosomal dominant tubulointerstitial kidney disease
726018006,Autosomal dominant tubulointerstitial kidney disease
726082003,Immunotactoid glomerulonephritis
726106004,X-linked diffuse leiomyomatosis with Alport syndrome
73305009,Fibrillary glomerulonephritis
733089005,"Spastic paraplegia, nephritis, deafness syndrome"
733096007,Thyrocerebrorenal syndrome
733097003,"Ichthyosis, intellectual disability, dwarfism, renal impairment syndrome"
733116005,"Aniridia, renal agenesis, psychomotor retardation syndrome"
733453005,"Congenital nephrotic syndrome, interstitial lung disease, epidermolysis bullosa syndrome"
733472005,"Microcephalus, glomerulonephritis, marfanoid habitus syndrome"
734990008,Primary hyperoxaluria type III
737295003,Transplanted kidney present
75652008,Familial renal iminoglycinuria
75888001,"Mesangiocapillary glomerulonephritis, type I"
763891005,Renal hepatic pancreatic dysplasia
764961009,Hereditary clear cell renal cell carcinoma
765330003,Autosomal dominant polycystic kidney disease
765331004,Autosomal dominant polycystic kidney disease type 1 with tuberous sclerosis
765478004,Allotransplantation of left kidney
765479007,Allotransplantation of right kidney
766765009,Radio-renal syndrome
770414008,Alport syndrome
771000119108,Chronic kidney disease due to type 2 diabetes mellitus
771266007,"Torticollis, keloids, cryptorchidism, renal dysplasia syndrome"
771447009,Laminin subunit beta 2 related infantile-onset nephrotic syndrome
77182004,Membranous glomerulonephritis
773647007,"Nephrotic syndrome, deafness, pretibial epidermolysis bullosa syndrome"
773737004,Nephrocystin 3-related Meckel-like syndrome
775909002,"Congenital neutropenia, myelofibrosis, nephromegaly syndrome"
776416004,"Hyperuricemia, pulmonary hypertension, renal failure, alkalosis syndrome"
778025006,Atypical hypotonia cystinuria syndrome
782655004,Laparoscopic transplant of kidney using robotic assistance
782722002,"Global developmental delay, lung cysts, overgrowth, Wilms tumor syndrome"
782738008,Karyomegalic interstitial nephritis
782771007,Mitochondrial deoxyribonucleic acid depletion syndrome hepatocerebrorenal form
783157004,Leigh syndrome with nephrotic syndrome
783159001,Holzgreve syndrome
783187005,Aseptic peritoneal eosinophilia due to and following dialysis
783614008,Familial steroid-resistant nephrotic syndrome with sensorineural deafness
783620009,Dominant hypophosphatemia with nephrolithiasis and/or osteoporosis
783787000,Retinal vasculopathy with cerebral leukoencephalopathy and systemic manifestations
78815005,Hereditary tubulointerstitial disorder
79385002,Lowe syndrome
79827002,Arteriovenous anastomosis for renal dialysis
80321008,Mesangiocapillary glomerulonephritis
818952002,Fibronectin glomerulopathy
81896006,Dysmorphic sialidosis with renal involvement
81987005,"Familial hypokalemic alkalosis, Gullner type"
828971000000101,"Primary hyperoxaluria, type III"
83866005,Focal AND segmental proliferative glomerulonephritis
83923004,Familial interstitial nephritis
843691000000100,Urological complication of renal transplant
844661000000109,Vascular complication of renal transplant
846671000000106,Aneurysm of superficialised artery of dialysis arteriovenous fistula
846731000000104,Aneurysm of dialysis arteriovenous fistula
846761000000109,Aneurysm of needle site of dialysis arteriovenous fistula
846801000000104,Aneurysm of anastomotic site of dialysis arteriovenous fistula
847791000000101,Rupture of artery of transplanted kidney
847811000000100,Rupture of vein of transplanted kidney
847881000000107,Stenosis of vein of transplanted kidney
8501000119104,Hypertensive heart and chronic kidney disease
85223007,Complication of hemodialysis
852981000000100,Aneurysm of vein of transplanted kidney
853021000000108,Aneurysm of artery of transplanted kidney
853631000000103,Stenosis of dialysis vascular access
853651000000105,Thrombosis of dialysis vascular access
854161000000102,Anaphylactoid reaction due to haemodialysis
85487008,Renal phosphaturia
863331000000100,Aneurysm of dialysis vascular access
864271000000105,Thrombosis of artery of transplanted kidney
864311000000105,Thrombosis of vein of transplanted kidney
865761000000105,Occlusion of dialysis vascular access
865801000000100,Haemorrhage of dialysis vascular access
865821000000109,Rupture of dialysis vascular access
865841000000102,Stenosis of dialysis arteriovenous graft
865861000000101,Stenosis of dialysis arteriovenous shunt
865981000000103,Thrombosis of dialysis arteriovenous graft
866001000000102,Thrombosis of dialysis arteriovenous fistula
866021000000106,Thrombosis of dialysis arteriovenous shunt
866041000000104,Occlusion of dialysis arteriovenous graft
866061000000103,Occlusion of dialysis arteriovenous fistula
866081000000107,Occlusion of dialysis arteriovenous shunt
866991000000105,Haemorrhage of dialysis arteriovenous graft
867011000000102,Haemorrhage of dialysis arteriovenous fistula
867031000000105,Haemorrhage of dialysis arteriovenous shunt
867051000000103,Rupture of dialysis arteriovenous graft
867071000000107,Rupture of dialysis arteriovenous fistula
867091000000106,Rupture of dialysis arteriovenous shunt
87235005,Dialysis disequilibrium syndrome
872461000000102,Stenosis of arterial side of dialysis arteriovenous shunt
872481000000106,Stenosis of venous side of dialysis arteriovenous shunt
88351001,Hypercalcemia associated with chronic dialysis
89681000119101,Glomerulonephritis co-occurrent and due to scleroderma
90688005,Chronic renal failure syndrome
90771000119100,End stage renal disease on dialysis due to type 1 diabetes mellitus
90791000119104,End stage renal disease on dialysis due to type 2 diabetes mellitus
96441000119101,Chronic kidney disease due to type 1 diabetes mellitus
96701000119107,Hypertensive heart AND chronic kidney disease on dialysis"""


c13_df = pd.read_csv(io.StringIO(c13), header=0,delimiter=',').astype(str)
spark.createDataFrame(c13_df).createOrReplaceGlobalTempView("ccu002_06_d17_ckd_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_ckd_primis

# COMMAND ----------

# MAGIC %md ## cld_primis

# COMMAND ----------

c14 = """code,term
10295004,Chronic viral hepatitis
103611000119102,Cirrhosis of liver due to hepatitis B
10690671000119109,Stage 3 hepatic fibrosis
109819003,Obstructive biliary cirrhosis
1116000,Chronic aggressive type B viral hepatitis
11179002,"Glycogen storage disease, type IV"
111891008,Viral hepatitis B without hepatic coma
123604002,Toxic cirrhosis
123605001,Nutritional cirrhosis
123607009,Septal fibrosis of liver
12368000,Secondary biliary cirrhosis
123716002,Latent cirrhosis
123717006,Advanced cirrhosis
125921000119106,Hepatic coma due to acute hepatitis C
128241005,Inflammatory disease of liver
128302006,Chronic hepatitis C
1287007,Congenital absence of bile duct
146371000119104,Hepatic coma due to chronic hepatitis C
1512006,Congenital stricture of bile duct
153091000119109,Hepatic coma due to chronic hepatitis B with delta agent
154211000119108,Chronic pancreatitis due to chronic alcoholism
15978003,"Glycogen storage disease, muscular form"
15999000,Mixed micro and macronodular cirrhosis
16060001,Hepatic coma due to viral hepatitis A
16070004,Syphilitic cirrhosis
174425003,Orthotopic liver transplant
174426002,Heterotopic liver transplant
174427006,Replacement of previous liver transplant
1761006,Biliary cirrhosis
18027006,Transplantation of liver
186273003,Tuberculosis of liver
186624004,Hepatic coma due to acute hepatitis B with delta agent
186626002,Acute hepatitis B with delta-agent (coinfection) without hepatic coma
186628001,Hepatic coma due to viral hepatitis C
186639003,Chronic viral hepatitis B without delta-agent
190944000,Alpha-1-antitrypsin hepatitis
192008,Congenital syphilitic hepatomegaly
197279005,Cirrhosis and chronic liver disease
197291001,Unilobular portal cirrhosis
197293003,Diffuse nodular cirrhosis
197294009,Fatty portal cirrhosis
197296006,Capsular portal cirrhosis
197299004,Pigmentary portal cirrhosis
197300007,Pipestem portal cirrhosis
197301006,Toxic portal cirrhosis
197303009,Bacterial portal cirrhosis
197305002,Syphilitic portal cirrhosis
197310003,Biliary cirrhosis of children
197316009,Portal fibrosis without cirrhosis
197321007,Steatosis of liver
197324004,Liver abscess and sequelae of chronic liver disease
197348008,Hepatitis in secondary syphilis
197355005,Toxic liver disease with cholestasis
197356006,Toxic liver disease with hepatic necrosis
197359004,Toxic liver disease with chronic persistent hepatitis
197360009,Toxic liver disease with chronic lobular hepatitis
197361008,Toxic liver disease with chronic active hepatitis
197362001,Toxic liver disease with fibrosis and cirrhosis of liver
197367007,Hepatic granulomas in berylliosis
197368002,Hepatic granulomas in sarcoidosis
197441003,Primary sclerosing cholangitis
197442005,Secondary sclerosing cholangitis
19943007,Cirrhosis of liver
204781002,Congenital absence of hepatic ducts
204782009,Atresia of hepatic ducts
204787003,Congenital absence of liver and/or gallbladder
213153001,Liver transplant failure and rejection
213230009,Hepatic failure as a complication of care
213231008,Hepatorenal syndrome as a complication of care
21861000,Micronodular cirrhosis
22508003,Hepatic failure due to a procedure
22846003,Hepatorenal syndrome following delivery
234689009,Relapsing pancreatitis
235458006,Exploration of liver transplant
235494005,Chronic pancreatitis
235865005,Hepatitis D superinfection of hepatitis B carrier
235869004,Chronic viral hepatitis B with hepatitis D
235870003,Chronic non-A non-B hepatitis
235877000,Ischemic hepatitis
235880004,Alcoholic fibrosis and sclerosis of liver
235881000,Alcoholic hepatic failure
235884008,Fulminant hepatic failure
235885009,Subfulminant hepatic failure
235886005,Chronic hepatic failure
235890007,Autoimmune liver disease
235895002,"Laennec's cirrhosis, non-alcoholic"
235896001,Infectious cirrhosis
235897005,Hypoxia-associated cirrhosis
235898000,Pericellular fibrosis of congenital syphilis
235899008,Hepatic sclerosis
235900003,Portal and splenic vein sclerosis
235901004,Hepatic fibrosis with hepatic sclerosis
235902006,Intrahepatic phlebosclerosis and fibrosis
235903001,Metabolic and genetic disorder affecting the liver
235908005,Glycogen storage disease type IX
235909002,Antichymotrypsin deficiency-alpha-1
235910007,Liver transplant disorder
235911006,Liver transplant rejection
235912004,Liver transplant failure
235916001,Ichthyosis congenita with biliary atresia
235917005,Sclerosing cholangitis
235951009,Gallstone chronic pancreatitis
235952002,Alcohol-induced chronic pancreatitis
235953007,Idiopathic chronic pancreatitis
235954001,Obstructive chronic pancreatitis
235955000,Drug-induced chronic pancreatitis
235956004,Familial chronic pancreatitis
237964009,Glycogen synthase deficiency
237965005,Phosphate transport defect
237966006,Glucose transport defect
240792005,Symmer's pipe-stem fibrosis
253807009,Intrahepatic biliary atresia
253808004,Congenital kink of cystic duct
26206000,Hepatic coma due to viral hepatitis B
266468003,Cirrhosis - non-alcoholic
266469006,Multilobular portal cirrhosis
266470007,Cardiac portal cirrhosis
266471006,Juvenile portal cirrhosis
267424007,Generalized glycogenosis
271440004,Cirrhosis secondary to cholestasis
27156006,Posthepatitic cirrhosis
27280000,Liver transplant with recipient hepatectomy
274864009,"Glycogen storage disease, type II"
276668008,Congenital non-A non-B hepatitis infection
276723008,Intrahepatic biliary hypoplasia
278929008,Congenital hepatitis C infection
28009009,Liver transplant without recipient hepatectomy
281095009,Congenital stricture of common bile duct
281388009,Human immunodeficiency virus-related sclerosing cholangitis
29291001,"Glycogen storage disease, type VI"
29633007,Glycogen storage disease
297251003,"Glycogen phosphorylase kinase deficiency, X-linked"
297252005,"Glycogen phosphorylase kinase deficiency, autosomal recessive"
297253000,Cardiac glycogen phosphorylase kinase deficiency
297254006,Hepatic and muscle glycogen phosphorylase kinase deficiency
297255007,Hepatic glycogen phosphorylase kinase deficiency
301009006,Calcific chronic pancreatitis
30102006,Glucose-6-phosphate transport defect
30188007,Alpha-1-antitrypsin deficiency
308129003,Esophageal varices in cirrhosis of the liver
309783001,Esophageal varices in alcoholic cirrhosis of the liver
31005002,Hepatorenal syndrome due to a procedure
314963000,Local recurrence of malignant tumor of liver
31712002,Primary biliary cholangitis
31742004,Arteriohepatic dysplasia
328383001,Chronic liver disease
33144001,Parasitic cirrhosis
33167004,Complication of transplanted liver
34736002,Chronic passive congestion of liver
34742003,Portal hypertension
347891000119103,Chronic hepatitis C with stage 3 fibrosis
3650004,Congenital absence of liver
367406009,"Deficiency of alpha-dextrin endo-1,6-alpha-glucosidase"
36760000,Hepatosplenomegaly
370492003,Copper storage associated hepatitis
371139006,Early cirrhosis
37666005,Glycogen storage disease type X
37688005,Clonorchiasis with biliary cirrhosis
38662009,Chronic persistent type B viral hepatitis
397575003,"Viral hepatitis, type G"
406584008,"Non-A, non-B, non-C hepatitis"
407000,Congenital hepatomegaly
40946000,Hepatic coma due to viral hepatitis
41309000,Alcoholic liver damage
41527003,Glycogen storage disease type VIII
419097006,Danon disease
419728003,Portal cirrhosis
420054005,Alcoholic cirrhosis
424099008,Hepatic coma due to acute hepatitis B
424340000,Hepatic coma due to chronic hepatitis B
425413006,Drug-induced cirrhosis of liver
426356008,Orthotopic transplantation of whole liver
427022004,Liver disease due to cystic fibrosis
427044009,Fulminant hepatitis
428198008,Transplantation of hepatocytes
431222008,Acute rejection of liver transplant
432772009,Hyperacute rejection of liver transplant
432777003,Accelerated rejection of liver transplant
432908002,Chronic rejection of liver transplant
43904005,Macronodular cirrhosis
44047000,Zieve's syndrome
442134007,Hepatitis B associated with Human immunodeficiency virus infection
442191002,Steatohepatitis
442374005,Hepatitis B and hepatitis C
444707001,Glycogen storage disease type Ia
444918006,Sequela of chronic liver disease
44553005,Dubin-Johnson syndrome
446698005,Reactivation of hepatitis B viral hepatitis
450880008,Chronic hepatitis E
45256007,Cruveilhier-Baumgarten syndrome
459062008,Fatal congenital nonlysosomal heart glycogenosis
50167007,Chronic active type B viral hepatitis
50711007,Viral hepatitis type C
51038004,Congenital obstruction of bile duct
51292008,Hepatorenal syndrome
53425008,Anicteric type B viral hepatitis
536002,Glissonian cirrhosis
55912009,"Glycogen storage disease, type V"
5667009,"Hunter's syndrome, mild form"
59927004,Hepatic failure
60037002,Chronic persistent viral hepatitis
60498001,Congenital viral hepatitis B infection
6075009,"Glycogen storage disease, hepatic form"
61598006,Glycogenosis with glucoaminophosphaturia
6183001,Indian childhood cirrhosis
61977001,Chronic type B viral hepatitis
62216007,Familial arthrogryposis-cholestatic hepatorenal syndrome
62484002,Hepatic fibrosis
66071002,Viral hepatitis type B
66870002,Chronic active viral hepatitis
66937008,"Glycogen storage disease, type III"
68094008,Congenital hypoplasia of bile duct
698305006,Awaiting transplantation of liver
699189004,North American Indian childhood cirrhosis
702777009,Liver transplant recipient
703866000,Chronic hepatitis C with stage 2 fibrosis
704201006,Liver transplant planned
707341005,Viral hepatitis type D
70737009,Mucopolysaccharidosis type II
707420003,Portal hypertension due to cystic fibrosis
707551007,Pulmonary interstitial glycogenosis
708198006,Chronic active hepatitis C
708248004,End stage liver disease
709561006,Periodontitis co-occurrent with glycogen storage disease
7111000119109,Viral hepatitis type E
713181003,Chronic alcoholic liver disease
713370005,Acute on chronic alcoholic liver disease
713529007,Steatosis of liver caused by retroviral protease inhibitor
713542007,Portal hypertension caused by antiretroviral drug
713965007,Sclerosis of portal vein and splenic vein caused by antiretroviral drug
713966008,Occult chronic type B viral hepatitis
715401008,Primary biliary cirrhosis co-occurrent with systemic scleroderma
715864007,Non-Wilsonian hepatic copper toxicosis of infancy and childhood
716203000,Decompensated cirrhosis of liver
717156002,Biliary atresia with splenic malformation syndrome
717187000,Nephronophthisis hepatic fibrosis syndrome
717821004,Glycogen storage disease with severe cardiomyopathy due to glycogenin deficiency
719452004,Congenital bronchobiliary fistula
720394008,Congenital tracheobiliary fistula
721099001,Adult polyglucosan body disease
721710005,Fibrosis of liver caused by alcohol
721847002,Joubert syndrome with congenital hepatic fibrosis
722302009,Glycogen storage disease type II infantile onset
722343009,Glycogen storage disease type II late onset
722867009,Idiopathic portal hypertension
722870008,Immunoglobulin G4-related sclerosing cholangitis
722871007,Groove pancreatitis
723360007,Familial hypercholanemia
723583009,Steroid dehydrogenase deficiency and dental anomaly syndrome
724278007,"Neonatal sclerosing cholangitis, ichthyosis, hypotrichosis syndrome"
724540009,Tropical calcific chronic pancreatitis
724766009,Chorea co-occurrent and due to Wilson disease
725026008,Hepatic glycogen synthase deficiency
725027004,Muscle and heart glycogen synthase deficiency
725416005,Cardiomyopathy co-occurrent and due to cirrhosis of liver
725938001,Cirrhosis of liver caused by methotrexate
725939009,Cirrhosis of liver caused by amiodarone
725940006,Cirrhosis of liver caused by methyldopa
7265005,"Glycogen storage disease, type I"
72925005,Congenital cystic disease of liver
73146005,"Hunter's syndrome, severe form"
73475009,Hepatogenous chronic copper poisoning
735451005,Chronic infection caused by Hepatitis D virus
735733008,Cirrhosis of liver co-occurrent and due to primary sclerosing cholangitis
737202006,Fibropolycystic disease of liver
737297006,Transplanted liver present
74669004,Cardiac cirrhosis
74973004,Chronic fibrosing pancreatitis
76301009,Florid cirrhosis
764962002,Hepatoencephalopathy due to combined oxidative phosphorylation defect type 1
767291004,Chronic pancreatitis due to acute alcohol intoxication
767809001,Chronic hepatitis C caused by hepatitis C virus genotype 6
767810006,Chronic hepatitis C caused by hepatitis C virus genotype 5
768006009,Chronic hepatitis C caused by Hepatitis C virus genotype 3
768125005,Chronic hepatitis C caused by Hepatitis C virus genotype 2
768126006,Chronic hepatitis C caused by Hepatitis C virus genotype 4
768127002,Chronic hepatitis C caused by Hepatitis C virus genotype 1
768288001,Chronic hepatitis C caused by Hepatitis C virus genotype 1b
768289009,Chronic hepatitis C caused by Hepatitis C virus genotype 1a
771149000,"Hepatic fibrosis, renal cyst, intellectual disability syndrome"
773415005,Contiguous ABCD1 DXS1357E deletion syndrome
773584001,"Muscular hypertrophy, hepatomegaly, polyhydramnios syndrome"
773737004,Nephrocystin 3-related Meckel-like syndrome
774148007,Polyglucosan body myopathy type 1
774151000,Ferro-cerebro-cutaneous syndrome
77480004,Congenital biliary atresia
776981000000103,Cirrhosis associated with cystic fibrosis
78208005,Pigment cirrhosis
782771007,Mitochondrial deoxyribonucleic acid depletion syndrome hepatocerebrorenal form
783734000,"Mitochondrial deoxyribonucleic acid depletion syndrome, hepatocerebral form due to deoxyguanosine kinase deficiency"
784346006,Navajo neurohepatopathy
79607001,Congenital hepatic fibrosis
79720007,Chronic nonalcoholic liver disease
80378000,Neonatal hepatosplenomegaly
80770009,Secondary syphilis of liver
819953000,Glycogen storage disease due to muscle phosphorylase kinase deficiency
824841000000105,Hepatitis C genotype 1
824851000000108,Hepatitis C genotype 2
824871000000104,Hepatitis C genotype 3
824881000000102,Hepatitis C genotype 4
824891000000100,Hepatitis C genotype 5
824901000000104,Hepatitis C genotype 6
82821008,Congenital atresia of extrahepatic bile duct
831000119103,Cirrhosis of liver due to chronic hepatitis C
838305005,Benign intrahepatic cholestasis type 1
838375006,Chronic infectious pancreatitis
838377003,Chronic hepatitis C co-occurrent with human immunodeficiency virus infection
838380002,Chronic hepatitis B co-occurrent with hepatitis C and hepatitis D
853761000000103,Living donor liver transplantation
86028001,Syphilis of liver
860858001,Glycogen storage disease due to muscle pyruvate kinase deficiency
860860004,Glycogen storage disease type IXB
863957008,Chronic necrosis of liver
86454000,Postnecrotic cirrhosis
870517000,Periportal fibrosis
871619002,Cirrhosis of liver due to and following cardiac procedure
88518009,Wilson's disease
89580002,Cryptogenic cirrhosis
89597008,"Glycogen storage disease, type VII"
89789003,Chronic aggressive viral hepatitis
96601000119101,Aftercare for liver transplant done"""


c14_df = pd.read_csv(io.StringIO(c14), header=0,delimiter=',').astype(str)
spark.createDataFrame(c14_df).createOrReplaceGlobalTempView("ccu002_06_d17_cld_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_cld_primis

# COMMAND ----------

# MAGIC %md ## immdx_primis

# COMMAND ----------

c15 = """code,term
103075007,Humoral immune defect
103682005,Subcutaneous panniculitic T-cell lymphoma
103685007,Hepatosplenic gamma-delta cell lymphoma
103686008,Intestinal T-cell lymphoma
103688009,Acute myeloid leukemia with abnormal marrow eosinophils and inv(16)(p13q22) or t(16;16)(p13;q22)
103689001,"Acute myeloid leukemia, minimal differentiation"
103690005,Acute myeloid leukemia without maturation
103691009,Acute myeloid leukemia with maturation
105601003,Quantitative disorder of neutrophils
10639003,Solitary plasmacytoma of bone
10755671000119100,Human immunodeficiency virus in mother complicating childbirth
1090241000000107,Angioimmunoblastic T-cell lymphoma with dysproteinaemia
1091861000000100,"Follicular lymphoma, cutaneous follicle centre"
1091891000000106,B-cell Hodgkin's lymphoma
1091921000000103,B-cell non-Hodgkin's lymphoma
109391009,Kaposi's sarcoma of lymph nodes
109958007,Hematologic neoplasm of uncertain behavior
109962001,Diffuse non-Hodgkin's lymphoma
109964000,"Diffuse non-Hodgkin's lymphoma, undifferentiated"
109965004,"Diffuse non-Hodgkin's lymphoma, lymphoblastic"
109966003,"Diffuse non-Hodgkin's lymphoma, immunoblastic"
109967007,"Diffuse non-Hodgkin's lymphoma, small cleaved cell"
109968002,"Diffuse non-Hodgkin's lymphoma, small cell"
109969005,"Diffuse non-Hodgkin's lymphoma, large cell"
109970006,"Follicular non-Hodgkin's lymphoma, small cleaved cell"
109971005,"Follicular non-Hodgkin's lymphoma, mixed small cleaved cell and large cell"
109972003,"Follicular non-Hodgkin's lymphoma, large cell"
109975001,T-zone lymphoma
109976000,Lymphoepithelioid lymphoma
109977009,Peripheral T-cell lymphoma
109978004,T-cell lymphoma
109979007,B-cell lymphoma
109980005,Malignant immunoproliferative disease
109985000,Immunoproliferative small intestinal disease
109988003,Histiocytic sarcoma
109989006,Multiple myeloma
109991003,Acute myelofibrosis
109993000,Chronic myeloproliferative disorder (clinical)
109994006,Essential thrombocythemia
109995007,Myelodysplastic syndrome
109996008,"Myelodysplastic syndrome: Refractory anemia, without ringed sideroblasts, without excess blasts"
109998009,Refractory anemia with ringed sideroblasts
110000005,Refractory anemia with excess blasts in transformation
110002002,Mast cell leukemia
110004001,"Acute promyelocytic leukemia, FAB M3"
110005000,"Acute myelomonocytic leukemia, FAB M4"
110006004,Prolymphocytic leukemia
110007008,Adult T-cell leukemia/lymphoma
110459008,"Malignant lymphoma, metastatic"
111001004,Gammopathy
111037009,Basophilic hyperplasia
111585004,Neutropenia associated with autoimmune disease
111880001,Acute human immunodeficiency virus infection
112687003,"Hodgkin lymphoma, lymphocyte depletion"
115244002,Malignant lymphoma - category
115245001,"Malignant lymphoma, follicular AND/OR nodular"
115246000,Specified cutaneous AND/OR peripheral T cell lymphoma
116691000119101,Marginal zone lymphoma of spleen
116811000119106,Non-Hodgkin lymphoma of central nervous system metastatic to lymph node of lower limb
116821000119104,Non-Hodgkin lymphoma of central nervous system metastatic to lymph node of upper limb
116841000119105,Marginal zone lymphoma of lymph nodes of multiple sites
116871000119103,Mantle cell lymphoma of lymph nodes of multiple sites
117211000119105,Peripheral T-cell lymphoma of lymph nodes of multiple sites
118599009,Hodgkin's disease
118600007,Malignant lymphoma
118601006,Non-Hodgkin's lymphoma
118602004,Hodgkin's granuloma
118605002,"Hodgkin lymphoma, nodular lymphocyte predominance"
118606001,Hodgkin's sarcoma
118607005,"Hodgkin lymphoma, lymphocyte-rich"
118608000,"Hodgkin's disease, nodular sclerosis"
118609008,"Hodgkin's disease, mixed cellularity"
118610003,"Hodgkin's disease, lymphocytic depletion"
118611004,Sézary's disease
118612006,Malignant histiocytosis
118613001,Hairy cell leukemia
118614007,"Langerhans cell histiocytosis, disseminated"
118615008,Malignant mast cell tumor
118617000,Burkitt's lymphoma
118618005,Mycosis fungoides
118791000119106,Aplastic anemia caused by antineoplastic agent
119249001,Agammaglobulinemia
119250001,Hypogammaglobulinemia
121131000119109,Chronic graft versus host disease after transplantation of bone marrow
12281000132104,Relapsing acute myeloid leukemia
12291000132102,Refractory acute myeloid leukemia
12301000132103,Acute lymphoid leukemia relapse
12311000132101,Refractory acute lymphoid leukemia
12341000132100,"B-cell lymphoma, unclassifiable, with features intermediate between diffuse large B-cell lymphoma and Burkitt lymphoma"
12351000132102,"B-cell lymphoma, unclassifiable, with features intermediate between diffuse large B-cell lymphoma and Hodgkin lymphoma"
123777002,Autoimmune leukopenia
124950009,Deficiency of immunoglobulin
127034005,Pancytopenia
127069007,Hemophagocytic syndrome
127070008,Malignant histiocytic disorder
127220001,Malignant lymphoma of lymph nodes
127225006,Chronic myelomonocytic leukemia
127388009,Hypergammaglobulinemia
128623006,Myelodysplastic syndrome
128798004,Composite Hodgkin and non-Hodgkin lymphoma
128799007,"Hodgkin lymphoma, lymphocyte-rich"
128800006,Primary effusion lymphoma
128801005,Mediastinal large B-cell lymphoma
128802003,Splenic marginal zone B-cell lymphoma
128803008,Marginal zone B-cell lymphoma
128805001,"Natural killer-/T-cell lymphoma, nasal and nasal-type"
128806000,Precursor cell lymphoblastic lymphoma
128807009,Precursor B-cell lymphoblastic lymphoma
128808004,Precursor T-cell lymphoblastic lymphoma
128809007,"Langerhans cell histiocytosis, no International Classification of Diseases for Oncology subtype"
128812005,"Langerhans cell histiocytosis, disseminated"
128813000,Histiocytic sarcoma
128814006,Langerhans cell sarcoma
128815007,Interdigitating dendritic cell sarcoma
128816008,Follicular dendritic cell sarcoma
128818009,Acute biphenotypic leukemia
128819001,T-cell large granular lymphocytic leukemia
128820007,"Prolymphocytic leukemia, B-cell type"
128821006,"Prolymphocytic leukemia, T-cell type"
128822004,Precursor cell lymphoblastic leukemia
128823009,Precursor B-cell lymphoblastic leukemia
128824003,Precursor T-cell lymphoblastic leukemia
128825002,"Chronic myelogenous leukemia, BCR/ABL positive"
128826001,"Atypical chronic myeloid leukemia, BCR/ABL negative"
128827005,Acute myeloid leukemia with multilineage dysplasia
128828000,"Acute myeloid leukemia, t(8;21) (q22;q22)"
128829008,"Acute myeloid leukemia, 11q23 abnormalities"
128830003,Therapy-related acute myeloid leukemia and myelodysplastic syndrome
128832006,Juvenile myelomonocytic leukemia
128833001,Aggressive natural killer-cell leukemia
128834007,Chronic neutrophilic leukemia
128836009,Refractory cytopenia with multilineage dysplasia
128837000,Myelodysplastic syndrome with 5q- syndrome
128838005,Therapy-related myelodysplastic syndrome
128843003,Myelosclerosis with myeloid metaplasia
128845005,Refractory anemia
128846006,Refractory anemia with sideroblasts
128847002,Refractory anemia with excess blasts
128848007,Refractory anemia with excess blasts in transformation
128875000,Primary cutaneous CD30 antigen positive large T-cell lymphoma
128920006,Malignant histiocytosis
128921005,"Plasmacytoma, extramedullary (not occurring in bone)"
128922003,"Plasma cell leukemia, morphology"
128923008,Prolymphocytic leukemia
128924002,Mast cell leukemia
128929007,Non-Hodgkin lymphoma - category
128930002,Hodgkin lymphoma - category
128931003,Leukemia - category
128932005,Acute leukemia - category
128933000,Chronic leukemia - category
128934006,Myeloid leukemia - category
128935007,Lymphoid leukemia - category
129641006,Chronic benign neutropenia of childhood
129642004,Chronic idiopathic immunoneutropenia in adults
129643009,Chronic hypoplastic neutropenia
129648000,Hypoalphaglobulinemia
129649008,Hypobetaglobulinemia
13048006,Orbital lymphoma
133751000119102,Lymphoma of colon
14024008,Humoral immunologic aplastic anemia
14317002,"Acute myeloid leukemia, M6 type"
14537002,"Hodgkin lymphoma, no International Classification of Diseases for Oncology subtype"
15928141000119107,Cognitive impairment co-occurrent and due to human immunodeficiency virus infection
165816005,Human immunodeficiency virus positive
16623961000119100,Pancytopenia caused by immunosuppressant
16893006,"Hodgkin lymphoma, lymphocyte depletion, diffuse fibrosis"
17182001,Agranulocytosis
17788007,"Acute myeloid leukemia, no International Classification of Diseases for Oncology subtype"
183005,Autoimmune pancytopenia
186706006,Human immunodeficiency virus infection constitutional disease
186707002,Human immunodeficiency virus infection with neurological disease
186708007,Human immunodeficiency virus infection with secondary clinical infectious disease
188487008,Lymphosarcoma and reticulosarcoma
188489006,"Reticulosarcoma of lymph nodes of head, face and neck"
188492005,Reticulosarcoma of lymph nodes of axilla and upper limb
188493000,Reticulosarcoma of lymph nodes of inguinal region and lower limb
188498009,Lymphosarcoma
188500005,"Lymphosarcoma of lymph nodes of head, face and neck"
188501009,Lymphosarcoma of intrathoracic lymph nodes
188502002,Lymphosarcoma of intra-abdominal lymph nodes
188503007,Lymphosarcoma of lymph nodes of axilla and upper limb
188504001,Lymphosarcoma of lymph nodes of inguinal region and lower limb
188505000,Lymphosarcoma of intrapelvic lymph nodes
188506004,Lymphosarcoma of spleen
188507008,Lymphosarcoma of lymph nodes of multiple sites
188510001,"Burkitt's lymphoma of lymph nodes of head, face and neck"
188511002,Burkitt's lymphoma of intrathoracic lymph nodes
188512009,Burkitt's lymphoma of intra-abdominal lymph nodes
188513004,Burkitt's lymphoma of lymph nodes of axilla and upper limb
188514005,Burkitt's lymphoma of lymph nodes of inguinal region and lower limb
188515006,Burkitt's lymphoma of intrapelvic lymph nodes
188516007,Burkitt's lymphoma of spleen
188517003,Burkitt's lymphoma of lymph nodes of multiple sites
188524002,Hodgkin's paragranuloma of intrathoracic lymph nodes
188529007,Hodgkin's paragranuloma of intrapelvic lymph nodes
188531003,Hodgkin's paragranuloma of lymph nodes of multiple sites
188534006,"Hodgkin's granuloma of lymph nodes of head, face and neck"
188536008,Hodgkin's granuloma of intra-abdominal lymph nodes
188537004,Hodgkin's granuloma of lymph nodes of axilla and upper limb
188538009,Hodgkin's granuloma of lymph nodes of inguinal region and lower limb
188541000,Hodgkin's granuloma of lymph nodes of multiple sites
188544008,"Hodgkin's sarcoma of lymph nodes of head, face and neck"
188547001,Hodgkin's sarcoma of lymph nodes of axilla and upper limb
188548006,Hodgkin's sarcoma of lymph nodes of inguinal region and lower limb
188551004,Hodgkin's sarcoma of lymph nodes of multiple sites
188554007,"Hodgkin's disease, lymphocytic-histiocytic predominance of lymph nodes of head, face and neck"
188558005,"Hodgkin's disease, lymphocytic-histiocytic predominance of lymph nodes of axilla and upper limb"
188559002,"Hodgkin's disease, lymphocytic-histiocytic predominance of lymph nodes of inguinal region and lower limb"
188562004,"Hodgkin's disease, lymphocytic-histiocytic predominance of lymph nodes of multiple sites"
188565002,"Hodgkin's disease, nodular sclerosis of lymph nodes of head, face and neck"
188566001,"Hodgkin's disease, nodular sclerosis of intrathoracic lymph nodes"
188567005,"Hodgkin's disease, nodular sclerosis of intra-abdominal lymph nodes"
188568000,"Hodgkin's disease, nodular sclerosis of lymph nodes of axilla and upper limb"
188569008,"Hodgkin's disease, nodular sclerosis of lymph nodes of inguinal region and lower limb"
188570009,"Hodgkin's disease, nodular sclerosis of intrapelvic lymph nodes"
188572001,"Hodgkin's disease, nodular sclerosis of lymph nodes of multiple sites"
188575004,"Hodgkin's disease, mixed cellularity of lymph nodes of head, face and neck"
188576003,"Hodgkin's disease, mixed cellularity of intrathoracic lymph nodes"
188577007,"Hodgkin's disease, mixed cellularity of intra-abdominal lymph nodes"
188578002,"Hodgkin's disease, mixed cellularity of lymph nodes of axilla and upper limb"
188579005,"Hodgkin's disease, mixed cellularity of lymph nodes of inguinal region and lower limb"
188580008,"Hodgkin's disease, mixed cellularity of intrapelvic lymph nodes"
188582000,"Hodgkin's disease, mixed cellularity of lymph nodes of multiple sites"
188585003,"Hodgkin's disease, lymphocytic depletion of lymph nodes of head, face and neck"
188586002,"Hodgkin's disease, lymphocytic depletion of intrathoracic lymph nodes"
188587006,"Hodgkin's disease, lymphocytic depletion of intra-abdominal lymph nodes"
188589009,"Hodgkin's disease, lymphocytic depletion of lymph nodes of axilla and upper limb"
188590000,"Hodgkin's disease, lymphocytic depletion of lymph nodes of inguinal region and lower limb"
188591001,"Hodgkin's disease, lymphocytic depletion of intrapelvic lymph nodes"
188592008,"Hodgkin's disease, lymphocytic depletion of spleen"
188593003,"Hodgkin's disease, lymphocytic depletion of lymph nodes of multiple sites"
188609000,"Nodular lymphoma of lymph nodes of head, face and neck"
188612002,Nodular lymphoma of lymph nodes of axilla and upper limb
188613007,Nodular lymphoma of lymph nodes of inguinal region and lower limb
188627002,Mycosis fungoides of lymph nodes of multiple sites
188630009,"Sézary's disease of lymph nodes of head, face and neck"
188631008,Sézary's disease of intrathoracic lymph nodes
188632001,Sézary's disease of intra-abdominal lymph nodes
188633006,Sézary's disease of lymph nodes of axilla and upper limb
188634000,Sézary's disease of lymph nodes of inguinal region and lower limb
188635004,Sézary's disease of intrapelvic lymph nodes
188637007,Sézary's disease of lymph nodes of multiple sites
188640007,"Malignant histiocytosis of lymph nodes of head, face and neck"
188641006,Malignant histiocytosis of lymph nodes of axilla and upper limb
188642004,Malignant histiocytosis of lymph nodes of inguinal region and lower limb
188645002,"Leukemic reticuloendotheliosis of lymph nodes of head, face and neck"
188648000,Leukemic reticuloendotheliosis of lymph nodes of axilla and upper limb
188649008,Leukemic reticuloendotheliosis of lymph nodes of inguinal region and lower limb
188660004,Malignant mast cell tumors
188662007,"Mast cell malignancy of lymph nodes of head, face and neck"
188663002,Mast cell malignancy of intrathoracic lymph nodes
188664008,Mast cell malignancy of intra-abdominal lymph nodes
188665009,Mast cell malignancy of lymph nodes of axilla and upper limb
188666005,Mast cell malignancy of lymph nodes of inguinal region and lower limb
188667001,Mast cell malignancy of intrapelvic lymph nodes
188668006,Mast cell malignancy of spleen
188669003,Mast cell malignancy of lymph nodes of multiple sites
188672005,Follicular non-Hodgkin's mixed small cleaved and large cell lymphoma
188674006,Diffuse malignant lymphoma - small non-cleaved cell
188675007,Malignant lymphoma - small cleaved cell
188676008,Malignant lymphoma - mixed small and large cell
188679001,Diffuse non-Hodgkin's lymphoma undifferentiated (diffuse)
188691005,Malignant immunoproliferative small intestinal disease
188718006,"Malignant plasma cell neoplasm, extramedullary plasmacytoma"
188725004,Lymphoid leukemia
188726003,Subacute lymphoid leukemia
188728002,Aleukemic lymphoid leukemia
188729005,Adult T-cell leukemia
188732008,Myeloid leukemia
188733003,Chronic eosinophilic leukemia
188734009,Chronic neutrophilic leukemia
188736006,Subacute myeloid leukemia
188737002,Chloroma
188738007,Granulocytic sarcoma
188741003,Aleukemic myeloid leukemia
188744006,Monocytic leukemia
188745007,Chronic monocytic leukemia
188746008,Subacute monocytic leukemia
188748009,Aleukemic monocytic leukemia
188754005,Megakaryocytic leukemia
188768003,Myelomonocytic leukemia
188770007,Subacute myelomonocytic leukemia
189509003,"Refractory anemia without sideroblasts, so stated"
189962004,"Malignant lymphoma, stem cell type"
189982000,Reticulosarcoma morphology
189984004,"Reticulosarcoma, pleomorphic cell type"
189985003,"Reticulosarcoma, nodular"
190030009,Compound leukemias
190055003,Eosinophilic leukemia
190955000,Histiocytosis X syndrome
190986006,Antibody deficiency with near-normal immunoglobulins or with hyperimmunoglobulinemia
191244003,Aplastic anemia due to chronic disease
191246001,Aplastic anemia due to infection
191247005,Aplastic anemia caused by radiation
191248000,Aplastic anemia caused by toxic cause
191255003,Transient acquired pure red cell aplasia
191256002,Idiopathic aplastic anemia
191338000,Primary splenic neutropenia
191345000,Acquired neutropenia in newborn
191347008,Cyclical neutropenia
191358004,Hereditary eosinophilia
191360002,Drug-induced eosinophilia
1929004,"Non-Hodgkin lymphoma, no International Classification of Diseases for Oncology subtype"
193206003,Persistent neonatal myasthenia gravis
193207007,Juvenile or adult myasthenia gravis
19340000,"Malignant lymphoma, lymphoplasmacytic"
19944001,Autologous bone marrow transplant without purging
20447006,Plasma cell dyscrasia with polyneuropathy
209962000,Myeloma-associated amyloidosis
213148006,Transplanted organ rejection
21964009,"Malignant lymphoma, no International Classification of Diseases for Oncology subtype"
22098000,Chronic idiopathic autoimmune hemolytic anemia
22197008,Burkitt cell leukemia
22331004,"Acute monocytic leukemia, morphology"
228311000000103,Allograft of bone marrow from haploidentical donor
230180003,Human immunodeficiency virus leukoencephalopathy
230202002,Vacuolar myelopathy
230598008,Neuropathy caused by human immunodeficiency virus
230683002,Transient neonatal myasthenia
230684008,Ocular myasthenia
230685009,Myasthenia gravis associated with thymoma
230686005,Generalized myasthenia
230687001,Myopathy in myasthenia gravis
232075002,Lymphoma of retina
234331007,Syngeneic bone marrow transplant
234332000,T-cell depleted allogeneic bone marrow graft
234333005,Imperfect T-cell depleted allogeneic bone marrow graft
234334004,Allogeneic related bone marrow transplant
234335003,Allogeneic unrelated bone marrow transplant
234336002,Hemopoietic stem cell transplant
234367000,Pancytopenia with pancreatitis
234370001,"Pure red cell aplasia, acquired"
234376007,Acquired red cell aplasia
234416002,X-linked hypogammaglobulinemia
234423001,Chronic benign neutropenia
234424007,Metabolic neutropenia
234425008,Autoimmune neutropenia
234513007,Post-splenectomy leukocytosis
234519006,Bone marrow transplant rejection
234520000,Bone marrow transplant failure
234532001,Immunodeficiency disorder
234535004,Selective immunoglobulin dysfunction
234557006,Anti-polysaccharide antibody deficiency
234562007,Anti-protein antibody deficiency
234563002,Anti-staphylococcal antibody deficiency
234576008,Chronic familial neutropenia
234603007,Complement 3 deficiency
234646005,Graft-versus-host disease
235009000,Human immunodeficiency virus-associated periodontitis
235726002,Human immunodeficiency virus enteropathy
236406007,Acquired immune deficiency syndrome-related nephropathy
236512004,Leukemic infiltrate of kidney
236513009,Lymphoma of kidney
236585005,De novo transplant disease
23719005,Transplantation of bone marrow
238931006,Eosinophilic cellulitis
239297008,Lymphomatoid granulomatosis of lung
239910001,Toxic oil syndrome
239940004,Lymphomatoid granulomatosis
240103002,Human immunodeficiency virus myopathy
240486003,Parvoviral aplastic crisis
240531002,African Burkitt's lymphoma
24072005,"Acute leukemia, morphology, including blast cell OR undifferentiated leukemia"
247860002,Familial neutropenia
248693006,Chronic idiopathic neutropenia
24974008,Myelokathexis
25109007,Lymphopenic agammaglobulinemia - short-limbed dwarfism syndrome
254792006,Proliferating angioendotheliomatosis
25502009,Episodic lymphocytopenia
255048006,"Tumor of lymphoid, hemopoietic and related tissue"
255101006,Sézary disease of skin
255102004,Angioendotheliomatosis
255191003,Localized malignant reticulohistiocytoma
267459007,Deficiencies of humoral immunity
267460002,Congenital hypogammaglobulinemia
267524009,Constitutional aplastic anemia with malformation
267527002,Aplastic anemia due to drugs
267540007,Neutropenia caused by irradiation
269295009,Transplanted organ failure
269475001,"Malignant tumor of lymphoid, hemopoietic AND/OR related tissue"
269476000,Nodular lymphoma
274905008,"Malignant lymphoma - lymphocytic, intermediate differentiation"
275523003,Pancytopenia-dysmelia
275524009,Immunoproliferative neoplasm
276628009,Chloramphenicol-induced neutropenia
276665006,Congenital acquired immune deficiency syndrome
276666007,Congenital human immunodeficiency virus positive status syndrome
276811008,Gastric lymphoma
276815004,Lymphoma of intestine
276836002,Primary cerebral lymphoma
277473004,B-cell chronic lymphocytic leukemia
277474005,B-cell chronic lymphocytic leukemia variant
277545003,T-cell chronic lymphocytic leukemia
277549009,Chronic lymphocytic prolymphocytic leukemia syndrome
277550009,Richter's syndrome
277551008,Splenic lymphoma with villous lymphocytes
277567002,T-cell prolymphocytic leukemia
277568007,Hairy cell leukemia variant
277569004,Large granular lymphocytic leukemia
277570003,Lymphoma with spill
277571004,B-cell acute lymphoblastic leukemia
277572006,Precursor B-cell acute lymphoblastic leukemia
277573001,Common acute lymphoblastic leukemia
277574007,Null cell acute lymphoblastic leukemia
277575008,T-cell acute lymphoblastic leukemia
277579002,Light chain myeloma
277580004,Non-secretory myeloma
277587001,Juvenile chronic myeloid leukemia
277589003,Atypical chronic myeloid leukemia
277597005,Myelodysplastic syndrome with isolated del(5q)
277601005,Acute monoblastic leukemia
277602003,Acute megakaryoblastic leukemia
277604002,Acute eosinophilic leukemia
277606000,Lymphoreticular tumor
277609007,"Hodgkin's disease, lymphocytic predominance - diffuse"
277610002,"Hodgkin's disease, nodular sclerosis - lymphocytic predominance"
277611003,"Hodgkin's disease, nodular sclerosis - mixed cellularity"
277612005,"Hodgkin's disease, nodular sclerosis - lymphocytic depletion"
277613000,Cutaneous/peripheral T-cell lymphoma
277614006,Prethymic and thymic T-cell lymphoma/leukemia
277615007,Low grade B-cell lymphoma
277616008,Diffuse low grade B-cell lymphoma
277617004,High grade B-cell lymphoma
277618009,Follicular low grade B-cell lymphoma
277619001,B-cell prolymphocytic leukemia
277622004,Mucosa-associated lymphoma
277623009,Monocytoid B-cell lymphoma
277624003,Follicular malignant lymphoma - mixed cell type
277625002,Follicular malignant lymphoma - small cleaved cell
277626001,Diffuse high grade B-cell lymphoma
277627005,Nodular high grade B-cell lymphoma
277628000,Diffuse malignant lymphoma - large cleaved cell
277629008,Diffuse malignant lymphoma - large non-cleaved cell
277632006,Diffuse malignant lymphoma - centroblastic polymorphic
277637000,Large cell anaplastic lymphoma
277641001,Follicular malignant lymphoma - large cell
277642008,Low grade T-cell lymphoma
277643003,High grade T-cell lymphoma
277651000,Peripheral T-cell lymphoma - pleomorphic small cell
277653002,Peripheral T-cell lymphoma - pleomorphic medium and large cell
277654008,Enteropathy-associated T-cell lymphoma
277664004,Malignant lymphoma of testis
278051002,Malignant lymphoma of thyroid gland
278052009,Malignant lymphoma of breast
278189009,Hypergranular promyelocytic leukemia
278256002,Cord cell transfusion
278257006,Peripheral blood stem cell graft
278453007,Acute biphenotypic leukemia
28054005,"Cutaneous T-cell lymphoma, no International Classification of Diseases for Oncology subtype"
281388009,Human immunodeficiency virus-related sclerosing cholangitis
284681000000100,Syngeneic peripheral blood stem cell transplant
285420006,Immunoglobulin A myeloma
285421005,Immunoglobulin G myeloma
285422003,Immunoglobulin D myeloma
285581000000102,Transplantation of stem cells
285769009,Acute promyelocytic leukemia - hypogranular variant
285776004,Intermediate grade B-cell lymphoma
285839005,Acute myelomonocytic leukemia - eosinophilic variant
28950004,"Acute promyelocytic leukemia, t(15;17)(q22;q11-12)"
28975000,Constitutional aplastic anemia
29120000,Eosinophilic colitis
302841002,Malignant lymphoma - small lymphocytic
302842009,Diffuse malignant lymphoma - centroblastic
302845006,"Nodular malignant lymphoma, lymphocytic - well differentiated"
302848008,"Nodular malignant lymphoma, lymphocytic - intermediate differentiation"
302855005,Subacute leukemia
302856006,Aleukemic leukemia
303011007,Neutropenic disorder
303017006,"Malignant lymphoma, convoluted cell type"
303055001,"Malignant lymphoma, follicular center cell"
303056000,"Malignant lymphoma, follicular center cell, cleaved"
303057009,"Malignant lymphoma, follicular center cell, non-cleaved"
306058006,Aplastic anemia
307340003,Monosomy 7 syndrome
307341004,Atypical hairy cell leukemia
307592006,Basophilic leukemia
307617006,Neutrophilic leukemia
307622006,Prolymphocytic lymphosarcoma
307623001,Malignant lymphoma - lymphoplasmacytic
307624007,Diffuse malignant lymphoma - centroblastic-centrocytic
307625008,Malignant lymphoma - centrocytic
307633009,"Hodgkin's disease, lymphocytic depletion, diffuse fibrosis"
307634003,"Hodgkin's disease, lymphocytic depletion, reticular type"
307635002,"Hodgkin's disease, nodular sclerosis - cellular phase"
307636001,"Malignant lymphoma, mixed lymphocytic-histiocytic, nodular"
307637005,"Malignant lymphoma, centroblastic-centrocytic, follicular"
307646004,"Malignant lymphoma, lymphocytic, poorly differentiated, nodular"
307647008,"Malignant lymphoma, centroblastic type, follicular"
307649006,Microglioma
307650006,Histiocytic medullary reticulosis
307651005,Myelosclerosis with myeloid metaplasia
308121000,Follicular non-Hodgkin's lymphoma
30962008,Acute myelomonocytic leukemia
30981000,Secondary eosinophilia
313427003,Lambda light chain myeloma
314922006,B-cell lymphoma morphology
314923001,Low grade B-cell lymphoma morphology
314924007,Follicular low grade B-cell lymphoma morphology
314925008,High grade B-cell lymphoma morphology
314926009,T-cell lymphoma morphology
314927000,High grade T-cell lymphoma morphology
314929002,Diffuse low grade B-cell lymphoma morphology
314930007,Low grade T-cell lymphoma morphology
314931006,Nodular high grade B-cell lymphoma morphology
314934003,Diffuse high grade B-cell lymphoma morphology
315019000,Human immunodeficiency virus infection with aseptic meningitis
3172003,"Peripheral T-cell lymphoma, no International Classification of Diseases for Oncology subtype"
31839002,"Myasthenia gravis, adult form"
320150004,Idiopathic eosinophilia
32092008,Toxic neutropenia
32280000,"Lymphoid leukemia, no International Classification of Diseases for Oncology subtype"
328301000119102,Pancytopenia due to antineoplastic chemotherapy
328611000119105,Adult pulmonary Langerhans cell histiocytosis
350951000119101,B-cell lymphoma of intra-abdominal lymph nodes
351211000119104,B-cell lymphoma of lymph nodes of multiple sites
352251000119109,Small lymphocytic B-cell lymphoma of lymph nodes of multiple sites
352411000119109,Small lymphocytic B-cell lymphoma of intra-abdominal lymph nodes
352791000119108,Non-Hodgkin's lymphoma of lymph nodes of multiple sites
35287006,"Myeloid sarcoma, morphology"
354851000119101,Follicular non-Hodgkin's lymphoma of lymph nodes of multiple sites
359631009,"Acute myeloid leukemia, minimal differentiation, FAB M0"
359640008,"Acute myeloid leukemia without maturation, FAB M1"
359648001,"Acute myeloid leukemia with maturation, FAB M2"
363138005,Hereditary disorder of immune system
363153002,Immune system transplantation
367542003,Pulmonary eosinophilia
370388006,Patient immunocompromised
370391006,Patient immunosuppressed
371012000,"Acute lymphoblastic leukemia, transitional pre-B-cell"
371134001,"Malignant lymphoma, large cell, polymorphous, immunoblastic"
373168002,Reticulosarcoma
373381004,"Myelodysplastic syndrome, no International Classification of Diseases for Oncology subtype"
37810007,"Myeloid leukemia, no International Classification of Diseases for Oncology subtype"
378841000000102,Allograft of bone marrow from unmatched unrelated donor
38970002,Doan-Wright syndrome
3902000,Non dose-related drug-induced neutropenia
39086001,"Hodgkin lymphoma, nodular sclerosis, cellular phase"
393573009,Hypereosinophilic syndrome
397009000,Mast cell malignancy
397011009,Mast cell malignancy of lymph nodes
397338009,Refractory anemia with excess blasts I
397339001,Refractory anemia with excess blasts II
397340004,Acute myeloid leukemia with recurrent genetic abnormality
397341000,Acute myeloid leukemia with multilineage dysplasia following a myelodysplastic syndrome or myelodysplastic syndrome/myeloproliferative disorder
397342007,Acute myeloid leukemia with multilineage dysplasia without antecedent myelodysplastic syndrome
397343002,"Therapy-related acute myeloid leukemia and myelodysplastic syndrome, alkylating agent-related type"
397344008,"Therapy-related acute myeloid leukemia and myelodysplastic syndrome, topoisomerase type II inhibitor-related type"
397345009,Acute leukemia of ambiguous lineage
397349003,Nodal marginal zone B-cell lymphoma
397350003,Extranodal marginal zone B-cell lymphoma of mucosa-associated lymphoid tissue
397352006,"Primary cutaneous anaplastic large T-cell lymphoma, CD30-positive"
397355008,"Dendritic cell sarcoma, no International Classification of Diseases for Oncology subtype"
397400006,Burkitt lymphoma/leukemia
397467006,"Follicular lymphoma, cutaneous follicle center sub-type"
397468001,"Follicular lymphoma, diffuse follicle center sub-type, grade 1"
397469009,"Follicular lymphoma, diffuse follicle center cell sub-type, grade 2"
397763006,Human immunodeficiency virus encephalopathy
39795003,Hand-Schüller-Christian disease
398055000,T-lymphocyte deficiency
398271008,Predominantly T-cell defect
398293003,Cellular immune defect
398329009,Human immunodeficiency virus encephalitis
398623004,Refractory anemia with excess blasts
399648005,Intravascular large B-cell lymphoma
400001003,Primary cutaneous lymphoma
400122007,Primary cutaneous T-cell lymphoma
402355000,Acute graft-versus-host disease
402356004,Chronic graft-versus-host disease
402404006,Episodic angioedema with eosinophilia
402879006,T-cell leukemic infiltration of skin
402880009,Primary cutaneous large T-cell lymphoma
402881008,Primary cutaneous B-cell lymphoma
402882001,Hodgkin's disease affecting skin
404106004,Lymphomatoid papulosis with Hodgkin's disease
404107008,Patch/plaque stage mycosis fungoides
404108003,Poikilodermatous mycosis fungoides
404109006,Follicular mucinosis type mycosis fungoides
40411000,"Follicular lymphoma, grade 3"
404110001,Hypomelanotic mycosis fungoides
404111002,Lymphomatoid papulosis-associated mycosis fungoides
404112009,Granulomatous mycosis fungoides
404113004,Tumor stage mycosis fungoides
404114005,Erythrodermic mycosis fungoides
404115006,Bullous mycosis fungoides
404116007,Mycosis fungoides with systemic infiltration
404117003,Spongiotic mycosis fungoides
404118008,Syringotropic mycosis fungoides
404119000,Pagetoid reticulosis
404120006,Localized pagetoid reticulosis
404121005,Generalized pagetoid reticulosis
404122003,Leukemic infiltration of skin (chronic T-cell lymphocytic leukemia)
404123008,Leukemic infiltration of skin (T-cell prolymphocytic leukemia)
404124002,Leukemic infiltration of skin (T-cell lymphoblastic leukemia)
404126000,CD-30 positive pleomorphic large T-cell cutaneous lymphoma
404127009,CD-30 positive T-immunoblastic cutaneous lymphoma
404128004,CD-30 negative cutaneous T-cell lymphoma
404129007,CD-30 negative anaplastic large T-cell cutaneous lymphoma
404130002,CD-30 negative pleomorphic large T-cell cutaneous lymphoma
404131003,CD-30 negative T-immunoblastic cutaneous lymphoma
404133000,Subcutaneous panniculitic cutaneous T-cell lymphoma
404134006,Anaplastic large T-cell systemic malignant lymphoma
404135007,Angiocentric natural killer/T-cell malignant lymphoma involving skin
404136008,Aggressive natural killer-cell leukemia involving skin
404137004,Precursor B-cell lymphoblastic lymphoma involving skin
404138009,Small lymphocytic B-cell lymphoma involving skin
404139001,Leukemic infiltration of skin in hairy-cell leukemia
404140004,Primary cutaneous marginal zone B-cell lymphoma
404141000,Primary cutaneous immunocytoma
404142007,Primary cutaneous plasmacytoma
404143002,Primary cutaneous follicular center B-cell lymphoma
404144008,Primary cutaneous diffuse large cell B-cell lymphoma
404145009,Primary cutaneous anaplastic large cell B-cell lymphoma
404147001,Follicular center B-cell lymphoma (nodal/systemic with skin involvement)
404148006,Diffuse large B-cell lymphoma (nodal/systemic with skin involvement)
404149003,"Lymphoplasmacytic B-cell lymphoma, nodal/systemic with skin involvement"
404150003,Mantle cell B-cell lymphoma (nodal/systemic with skin involvement)
404151004,Leukemic infiltration of skin in myeloid leukemia
404152006,Leukemic infiltration of skin in acute myeloid leukemia
404153001,Leukemic infiltration of skin in chronic myeloid leukemia
404154007,Leukemic infiltration of skin in monocytic leukemia
404155008,Granulocytic sarcoma affecting skin
404156009,Leukemic infiltration of skin
404157000,Specific skin infiltration in Hodgkin's disease
404160007,Langerhans cell histiocytosis - Hashimoto-Pritzker type
404169008,Malignant histiocytosis involving skin
404171008,Mastocytoma
404172001,Mast cell leukemia affecting skin
405631006,Pediatric human immunodeficiency virus infection
40780007,Human immunodeficiency virus I infection
409089005,Febrile neutropenia
413389003,Accelerated phase chronic myeloid leukemia
413440007,Acute lymphoblastic leukemia - category
413441006,"Acute monocytic leukemia, FAB M5b"
413442004,Acute monocytic/monoblastic leukemia
413443009,Acute myeloid leukemia - category
413527004,"Anaplastic large cell lymphoma, T/Null cell, primary systemic type"
413537009,Angioimmunoblastic T-cell lymphoma
413565006,Aplastic anemia associated with metabolic alteration
413566007,Aplastic anemia associated with pancreatitis
413567003,Aplastic anemia associated with pregnancy
413587002,Smoldering myeloma
413656006,Blastic phase chronic myeloid leukemia
413834006,Chronic disease of immune function
413836008,Chronic eosinophilic leukemia
413840004,Chronic lymphoid leukemia - category
413841000,Chronic myeloid leukemia - category
413842007,Chronic myeloid leukemia in lymphoid blast crisis
413843002,Chronic myeloid leukemia in myeloid blast crisis
413847001,Chronic phase chronic myeloid leukemia
413990004,Diffuse large B-cell lymphoma - category
414029004,Disorder of immune function
414166008,"Extranodal natural killer/T-cell lymphoma, nasal type"
414553000,Kappa light chain myeloma
414644002,Malignant hematopoietic neoplasm
414645001,Malignant histiocytic neoplasm - category
414653009,Mast cell neoplasm
414780005,Mucosa-associated lymphoid tissue lymphoma of orbit
414785000,Multiple solitary plasmacytomas
414825006,Neoplasm of hematopoietic cell type
414850009,Neutrophilia
414927004,Ocular myasthenia with strabismus
415005004,Panleukopenia
415110002,Plasma cell myeloma/plasmacytoma
415111003,Plasma cell neoplasm
415112005,Plasmacytoma
415113000,Plasmacytoma - category
415283002,Refractory anemia with excess blasts-1
415284008,Refractory anemia with excess blasts-2
415285009,Refractory cytopenia with multilineage dysplasia
415286005,Refractory cytopenia with multilineage dysplasia and ringed sideroblasts
415287001,Relapsing chronic myeloid leukemia
41529000,"Hodgkin lymphoma, mixed cellularity"
416729007,Neutropenia associated with acquired immunodeficiency syndrome
417152008,Langerhans cell histiocytosis of lung
417672002,Granulocytopenic disorder
41814009,Neutropenia with dysgranulopoiesis
418265009,Primary cutaneous B-cell lymphoma - category
418628003,Follicular mycosis fungoides
418789003,Primary cutaneous plasmacytoma
419018000,Primary cutaneous large T-cell lymphoma - category
419094004,Immunodeficiency-associated Burkitt's lymphoma
419283005,Primary cutaneous T-cell lymphoma - category
419386004,Pagetoid reticulosis
419392005,Primary cutaneous lymphoma
419455006,Disorder characterized by eosinophilia
419586003,"Primary cutaneous T-cell lymphoma, large cell, CD30-negative"
419662008,Primary cutaneous follicle center cell lymphoma
419770008,Endemic Burkitt's lymphoma
419879004,Atypical Burkitt's lymphoma
420028002,Primary cutaneous marginal zone B-cell lymphoma
420063007,Sporadic Burkitt's lymphoma
420244003,Encephalitis associated with acquired immunodeficiency syndrome
420281004,Skin rash associated with acquired immunodeficiency syndrome
420302007,Reticulosarcoma associated with acquired immunodeficiency syndrome
420308006,Retinal vascular changes associated with acquired immunodeficiency syndrome
420321004,Intestinal malabsorption associated with acquired immunodeficiency syndrome
420384005,Hematopoietic system disease associated with acquired immunodeficiency syndrome
420395004,Acute endocarditis associated with acquired immunodeficiency syndrome
420403001,Pneumocystosis associated with acquired immunodeficiency syndrome
420452002,Myelopathy associated with acquired immunodeficiency syndrome
420519005,Malignant lymphoma of the eye region
420524008,Kaposi's sarcoma associated with acquired immunodeficiency syndrome
420543008,Anemia associated with acquired immunodeficiency syndrome
420544002,Bacterial pneumonia associated with acquired immunodeficiency syndrome
420549007,Salivary gland disease associated with acquired immunodeficiency syndrome
420554003,Progressive multifocal leukoencephalopathy associated with acquired immunodeficiency syndrome
420614009,Organic dementia associated with acquired immunodeficiency syndrome
420658009,Radiculitis associated with acquired immunodeficiency syndrome
420687005,Ill-defined intestinal infection associated with acquired immunodeficiency syndrome
420691000,Nutritional deficiency associated with acquired immunodeficiency syndrome
420718004,Central nervous system demyelinating disease associated with acquired immunodeficiency syndrome
420721002,Acquired immunodeficiency syndrome-associated disorder
420764009,Salmonella infection associated with acquired immunodeficiency syndrome
420774007,Organic brain syndrome associated with acquired immunodeficiency syndrome
420787001,Pneumococcal pneumonia associated with acquired immunodeficiency syndrome
420788006,Intraocular non-Hodgkin malignant lymphoma
420801006,Malaise associated with acquired immunodeficiency syndrome
420818005,Mycobacteriosis associated with acquired immunodeficiency syndrome
420877009,Dermatomycosis associated with acquired immunodeficiency syndrome
420890002,Precursor T cell lymphoblastic leukemia/lymphoblastic lymphoma
420900006,Fatigue associated with acquired immunodeficiency syndrome
420938005,Subacute endocarditis associated with acquired immunodeficiency syndrome
420945005,Histoplasmosis associated with acquired immunodeficiency syndrome
421020000,Microsporidiosis associated with acquired immunodeficiency syndrome
421023003,Presenile dementia associated with acquired immunodeficiency syndrome
421047005,Candidiasis of lung associated with acquired immunodeficiency syndrome
421077004,Disseminated candidiasis associated with acquired immunodeficiency syndrome
421102007,Aplastic anemia associated with acquired immunodeficiency syndrome
421230000,Hepatomegaly associated with acquired immunodeficiency syndrome
421246008,Precursor T-cell lymphoblastic lymphoma
421272004,Subacute myocarditis associated with acquired immunodeficiency syndrome
421283008,Primary lymphoma of brain associated with acquired immunodeficiency syndrome
421312009,Agranulocytosis associated with acquired immunodeficiency syndrome
421315006,Myelitis associated with acquired immunodeficiency syndrome
421394009,Skin disorder associated with acquired immunodeficiency syndrome
421403008,Cryptococcosis associated with acquired immunodeficiency syndrome
421415007,Subacute adenoviral encephalitis associated with acquired immunodeficiency syndrome
421418009,Mature T-cell AND/OR natural killer cell neoplasm
421431004,Nocardiosis associated with acquired immunodeficiency syndrome
421454008,Infectious gastroenteritis associated with acquired immunodeficiency syndrome
421460008,Retinopathy associated with acquired immunodeficiency syndrome
421508002,Viral pneumonia associated with acquired immunodeficiency syndrome
421529006,Dementia associated with acquired immunodeficiency syndrome
421571007,Tuberculosis associated with acquired immunodeficiency syndrome
421597001,Polyneuropathy associated with acquired immunodeficiency syndrome
421660003,Failure to thrive in infant associated with acquired immunodeficiency syndrome
421671002,Pneumonia associated with acquired immunodeficiency syndrome
421695000,Abnormal weight loss associated with acquired immunodeficiency syndrome
421696004,Precursor T-cell neoplasm
421706001,Blindness associated with acquired immunodeficiency syndrome
421708000,Infective arthritis associated with acquired immunodeficiency syndrome
421710003,Candidiasis of mouth associated with acquired immunodeficiency syndrome
421766003,Thrombocytopenia associated with acquired immunodeficiency syndrome
421827003,Encephalopathy associated with acquired immunodeficiency syndrome
421851008,Acquired hemolytic anemia associated with acquired immunodeficiency syndrome
421874007,Respiratory disorder associated with acquired immunodeficiency syndrome
421883002,Strongyloidiasis associated with acquired immunodeficiency syndrome
421929001,Myocarditis associated with acquired immunodeficiency syndrome
421983003,Noninfectious gastroenteritis associated with acquired immunodeficiency syndrome
421998001,Central nervous disorder associated with acquired immunodeficiency syndrome
422003001,Cachexia associated with acquired immunodeficiency syndrome
422012004,Neuritis associated with acquired immunodeficiency syndrome
422089004,Encephalomyelitis associated with acquired immunodeficiency syndrome
422127002,Herpes zoster associated with acquired immunodeficiency syndrome
422136003,Neuralgia associated with acquired immunodeficiency syndrome
422172005,T-cell AND/OR natural killer-cell neoplasm
422177004,Dyspnea associated with acquired immunodeficiency syndrome
422189002,Low vision associated with acquired immunodeficiency syndrome
422194002,Hyperhidrosis associated with acquired immunodeficiency syndrome
422282000,Malignant neoplasm associated with acquired immunodeficiency syndrome
422337001,Coccidioidomycosis associated with acquired immunodeficiency syndrome
422853008,Lymphoma of retroperitoneal space
423294001,Idiopathic hypereosinophilic syndrome
423486005,Disseminated eosinophilic collagen disease
425333006,Myeloproliferative disorder
425563003,Grafting of cord blood to bone marrow
425657001,Osteosclerotic myeloma
425688002,Philadelphia chromosome-positive acute lymphoblastic leukemia
425749006,Subacute myeloid leukemia in remission
425835006,Disorder of immune reconstitution
425843001,Allogeneic peripheral blood stem cell transplant
425869007,"Acute promyelocytic leukemia, FAB M3, in remission"
425941003,Precursor B-cell acute lymphoblastic leukemia in remission
425983008,Autologous peripheral blood stem cell transplant
426071002,Hodgkin's disease in remission
426124006,"Acute myeloid leukemia with maturation, FAB M2, in remission"
426217000,Aleukemic leukemia in remission
426248008,Aleukemic lymphoid leukemia in remission
426336007,Solitary osseous myeloma
426370008,Subacute lymphoid leukemia in remission
426425001,Allograft of bone marrow from sibling donor
426642002,"Erythroleukemia, FAB M6 in remission"
426800001,Febrile granulocytopenia
426885008,"Hodgkin's disease, lymphocytic depletion of lymph nodes of head"
426955004,Philadelphia chromosome-positive acute lymphoblastic leukemia
427056005,Subacute leukemia in remission
427141003,Malignant lymphoma in remission
427245000,Febrile leukopenia
427374007,Immunoproliferative neoplasm in remission
427423003,Allograft of bone marrow from matched unrelated donor
427615008,Allograft of cord blood to bone marrow
427642009,T-cell acute lymphoblastic leukemia in remission
427658007,"Acute myelomonocytic leukemia, FAB M4, in remission"
428103008,Disorder of transplanted bone marrow
429054002,Disorder related to transplantation
429450002,Disorder related to bone marrow transplantation
429490004,Disorder affecting transplanted structure
430338009,Smoldering chronic lymphocytic leukemia
43355006,Eosinopenia
43858000,Secondary aplastic anemia
43985008,"Hodgkin lymphoma, nodular sclerosis, grade 2"
440422002,Asymptomatic multiple myeloma
441313008,Indolent multiple myeloma
441559006,Mantle cell lymphoma of spleen
441962003,Large cell lymphoma of intrapelvic lymph nodes
442134007,Hepatitis B associated with Human immunodeficiency virus infection
442537007,Non-Hodgkin lymphoma associated with Human immunodeficiency virus infection
442557006,Grafting of bone marrow using allograft from unmatched unrelated donor
443487006,Mantle cell lymphoma
444597005,Extranodal marginal zone lymphoma of mucosa-associated lymphoid tissue of stomach
444910004,Primary mediastinal (thymic) large B-cell lymphoma
444911000,Acute myeloid leukemia with t(9:11)(p22;q23); MLLT3-MLL
445105005,Blastic plasmacytoid dendritic cell neoplasm
445227008,Juvenile myelomonocytic leukemia
445269007,Extranodal marginal zone B-cell lymphoma of mucosa-associated lymphoid tissue
445406001,Hepatosplenic T-cell lymphoma
445448008,Acute myeloid leukemia with myelodysplasia-related changes
445738007,Myelodysplastic/myeloproliferative disease
445757003,Allogeneic bone marrow transplantation without purging
445925008,Lymphomatous infiltration
445945000,Infectious disease associated with acquired immune deficiency syndrome
446253009,Allogeneic bone marrow transplantation with purging
446643000,Sarcoma of dendritic cells (accessory cells)
446688004,Leukemic infiltration
447100004,Marginal zone lymphoma
447596005,"Myelodysplastic/myeloproliferative neoplasm, unclassifiable"
447656001,Lymphoma of pylorus of stomach
447658000,Lymphoma of fundus of stomach
447766003,Lymphoma of pyloric antrum of stomach
447805007,Lymphoma of greater curvature of stomach
447806008,Lymphoma of cardia of stomach
447989004,Non-Hodgkin's lymphoma of extranodal site
448212009,Anaplastic lymphoma kinase negative anaplastic large cell lymphoma
448213004,Diffuse non-Hodgkin's lymphoma of prostate
448217003,Follicular non-Hodgkin's lymphoma of prostate
448220006,Non-Hodgkin's lymphoma of bone
448231003,Follicular non-Hodgkin's lymphoma of nose
448254007,Non-Hodgkin's lymphoma of central nervous system
448269008,Lymphoma of lesser curvature of stomach
448317000,Follicular non-Hodgkin's lymphoma of soft tissue
448319002,Diffuse non-Hodgkin's lymphoma of nasopharynx
448354009,Non-Hodgkin's lymphoma of intestine
448371005,Non-Hodgkin's lymphoma of nasopharynx
448372003,Non-Hodgkin's lymphoma of lung
448376000,Non-Hodgkin's lymphoma of ovary
448384001,Non-Hodgkin's lymphoma of nose
448386004,Non-Hodgkin's lymphoma of oral cavity
448387008,Non-Hodgkin's lymphoma of testis
448447004,Non-Hodgkin's lymphoma of skin
448465000,Diffuse non-Hodgkin's lymphoma of testis
448468003,Diffuse non-Hodgkin's lymphoma of oral cavity
448553002,Lymphoma of pelvis
448555009,Lymphoma of body of stomach
448560008,Diffuse non-Hodgkin's lymphoma of extranodal site
448561007,Follicular non-Hodgkin's lymphoma of extranodal site
448607004,Diffuse non-Hodgkin's lymphoma of uterine cervix
448609001,Diffuse non-Hodgkin's lymphoma of ovary
448663003,Diffuse non-Hodgkin's lymphoma of stomach
448666006,Follicular non-Hodgkin's lymphoma of bone
448672006,Follicular non-Hodgkin's lymphoma of lung
448709005,Non-Hodgkin's lymphoma of stomach
448738008,Non-Hodgkin's lymphoma of soft tissue
448774004,Non-Hodgkin's lymphoma of uterine cervix
448865007,Follicular non-Hodgkin's lymphoma of skin
448867004,Diffuse non-Hodgkin's lymphoma of lung
448995000,Follicular non-Hodgkin's lymphoma of central nervous system
449053004,Lymphoma of lower esophagus
449058008,Follicular non-Hodgkin's lymphoma of tonsil
449059000,Follicular non-Hodgkin's lymphoma of uterine cervix
449063007,Follicular non-Hodgkin's lymphoma of oral cavity
449065000,Diffuse non-Hodgkin's lymphoma of nose
449072004,Lymphoma of gastrointestinal tract
449074003,Lymphoma of small intestine
449075002,Lymphoma of cardioesophageal junction
449108003,Philadelphia chromosome positive chronic myelogenous leukemia
449173006,Diffuse non-Hodgkin's lymphoma of tonsil
449176003,Diffuse non-Hodgkin's lymphoma of intestine
449177007,Diffuse non-Hodgkin's lymphoma of bone
449216004,Diffuse non-Hodgkin's lymphoma of soft tissue
449217008,Diffuse non-Hodgkin's lymphoma of skin
449218003,Lymphoma of sigmoid colon
449219006,Follicular non-Hodgkin's lymphoma of nasopharynx
449220000,Diffuse follicle center lymphoma
449221001,Diffuse non-Hodgkin's lymphoma of central nervous system
449222008,Follicular non-Hodgkin's lymphoma of stomach
449292003,Non-Hodgkin's lymphoma of tonsil
449307001,Follicular non-Hodgkin's lymphoma of ovary
449318001,Non-Hodgkin's lymphoma of prostate
449386007,Philadelphia chromosome negative chronic myelogenous leukemia
449418000,Follicular non-Hodgkin's lymphoma of testis
449419008,Follicular non-Hodgkin's lymphoma of intestine
450907007,Hydroa vacciniforme-like lymphoma
450908002,Primary cutaneous gamma-delta T-cell lymphoma
450909005,Plasmablastic lymphoma
450910000,Anaplastic lymphoma kinase positive large B-cell lymphoma
450911001,Large B-cell lymphoma arising in human herpesvirus type 8 associated multicentric Castleman disease
450912008,Fibroblastic reticular cell tumor
450913003,Mixed phenotype acute leukemia
450914009,Mixed phenotype acute leukemia with t(9;22)(q34;q11.2); BCR-ABL1
450915005,Mixed phenotype acute leukemia with t(v;11q23); MLL rearranged
450916006,Mixed phenotype acute leukemia with myeloid and B-cell lymphoid phenotypes
450917002,Mixed phenotype acute leukemia with myeloid and T-cell lymphoid phenotypes
450920005,B lymphoblastic leukemia / lymphoma - category
450928003,Acute myeloid leukemia with t(6;9)(p23;q34); DEK-NUP214
450929006,Acute myeloid leukemia with inv(3)(q21q26.2) or t(3;3)(q21;q26.2); RPN1-EVI1
450935006,Myeloid leukemia associated with Down Syndrome
450937003,Acute myeloid leukemia (megakaryoblastic) with t(1;22)(p13;q13); RBM15-MKL1
450940003,Myeloid or lymphoid neoplasm with alpha-type platelet-derived growth factor receptor gene rearrangement
450945008,Refractory cytopenia with unilineage dysplasia
450946009,Refractory neutropenia
450947000,Refractory thrombocytopenia
450949002,"B lymphoblastic leukemia lymphoma, no International Classification of Diseases for Oncology subtype"
450950002,B lymphoblastic leukemia lymphoma with t(9;22)(q34;q11.2); BCR-ABL1
450951003,B lymphoblastic leukemia lymphoma with t(v;11q23); MLL rearranged
450952005,B lymphoblastic leukemia lymphoma with t(12;21)(p13;q22); TEL-AML1 (ETV6-RUNX1)
450953000,B lymphoblastic leukemia lymphoma with hyperdiploidy
450954006,B lymphoblastic leukemia lymphoma with hypodiploidy (Hypodiploid ALL)
450955007,B lymphoblastic leukemia lymphoma with t(5;14)(q31;q32); IL3-IGH
450956008,B lymphoblastic leukemia lymphoma with t(1;19)(q23;p13.3); E2A-PBX1 (TCF3-PBX1)
450958009,"Malignant lymphoma, diffuse large B-cell, immunoblastic"
450959001,T-cell/histiocyte rich large B-cell lymphoma
45572000,"Hodgkin lymphoma, nodular sclerosis, grade 1"
46280001,Autologous bone marrow transplant with purging
46359005,Neutropenia associated with infectious disease
46732000,"Malignant lymphoma, large B-cell, diffuse, no International Classification of Diseases for Oncology subtype"
46744002,"Follicular lymphoma, grade 1"
46923007,Hodgkin sarcoma [obs]
47318007,Drug-induced neutropenia
48794007,Human immunodeficiency virus infection with infectious mononucleosis-like syndrome
48813009,Lymphocytopenia
4950009,Sézary's disease
50102004,"Malignant lymphoma, mixed small and large cell, diffuse"
50220002,Cellular immunologic aplastic anemia
51092000,B-cell chronic lymphocytic leukemia/small lymphocytic lymphoma
52079000,Congenital human immunodeficiency virus infection
52220008,"Acute megakaryoblastic leukemia, morphology"
52248008,"Hodgkin lymphoma, nodular sclerosis"
52967002,Myelofibrosis
53237008,"Anaplastic large cell lymphoma, T cell and Null cell type"
54087003,Hairy cell leukemia
54097007,White blood cell disorder
55020008,"Follicular lymphoma, grade 2"
55051001,"Myasthenia gravis, juvenile form"
55150002,Follicular lymphoma
55444004,Transient neonatal neutropenia
55907008,Acquired aplastic anemia
55921005,"Multiple myeloma, no International Classification of Diseases for Oncology subtype"
56478004,Leukemoid reaction
56918001,Dose-related drug-induced neutropenia
58390007,Allogeneic bone marrow transplantation
5876000,Acquired pancytopenia
58776007,Autologous bone marrow transplant
58961005,Lethal midline granuloma
61291000119103,Disorder of central nervous system co-occurrent and due to acute lymphoid leukemia in remission
61301000119102,Disorder of central nervous system co-occurrent and due to acute lymphoid leukemia
63364005,"Chronic myelogenous leukemia, no International Classification of Diseases for Oncology subtype"
64249002,Allergic eosinophilia
64575004,"Malignant lymphoma, small lymphocytic"
65399007,Langerhans cell histiocytosis
65623009,Immune neutropenia
67023009,Lymphocytosis
69077002,Acute basophilic leukemia
697922003,Pulmonary hypertension in Langerhans cell histiocytosis
697965002,Cholangitis associated with acquired immunodeficiency syndrome
698075004,Syngeneic peripheral blood stem cell transplantation
698646006,Acute monoblastic leukemia in remission
699293000,Ischemic myelofibrosis
699537002,Polyostotic sclerosing histiocytosis
699657009,Hepatosplenic gamma-delta cell lymphoma
699818003,T-cell large granular lymphocytic leukemia
702446006,Core binding factor acute myeloid leukemia
702476004,Therapy-related myelodysplastic syndrome
702785000,Large cell anaplastic lymphoma T cell and Null cell type
702786004,Follicular non-Hodgkin's lymphoma diffuse follicle center sub-type grade 1
702977001,Follicular non-Hodgkin's lymphoma diffuse follicle center cell sub-type grade 2
703387000,Acute myeloid leukemia with normal karyotype
70349007,Pseudoneutrophilia
703626001,"Anaplastic large cell lymphoma, T/Null cell, primary systemic type"
703817002,Refractory anemia with ring sideroblasts associated with marked thrombocytosis
703818007,Acute monoblastic and monocytic leukemia
703819004,Acute myeloid leukemia with mutation of CCAAT enhancer binding protein alpha gene
703820005,Acute myeloid leukemia with mutated NPM1
703821009,T lymphoblastic leukemia/lymphoma
703822002,Indeterminate dendritic cell tumor
705061009,Childhood myelodysplastic syndrome
70600005,"Hodgkin lymphoma, nodular lymphocyte predominance"
707431006,Langerhans cell histiocytosis of diaper area
707432004,Langerhans cell histiocytosis of skin
709115004,Transplantation of autologous hematopoietic stem cell
709471005,Periodontitis co-occurrent with leukemia
709535007,Periodontitis co-occurrent with infantile genetic agranulocytosis
709608008,Periodontitis co-occurrent with acquired neutropenia
710926008,Periodontitis co-occurrent with familial neutropenia
710927004,Periodontitis co-occurrent with cyclical neutropenia
71109004,"Hodgkin lymphoma, lymphocyte depletion, reticular"
711429001,Transplantation of autologous progenitor cell
713260006,Subacute adenoviral encephalitis co-occurrent with human immunodeficiency virus infection
713275003,Splenomegaly co-occurrent with human immunodeficiency virus infection
713278001,Neuralgia co-occurrent with human immunodeficiency virus infection
713297001,Candidiasis of esophagus co-occurrent with human immunodeficiency virus infection
713298006,Heart disease co-occurrent with human immunodeficiency virus infection
713299003,Disorder of eye proper co-occurrent with human immunodeficiency virus infection
713300006,Disorder of gastrointestinal tract co-occurrent with human immunodeficiency virus infection
713316008,Eruption of skin co-occurrent with human immunodeficiency virus infection
713318009,Myocarditis co-occurrent with human immunodeficiency virus infection
713320007,Radiculitis co-occurrent with human immunodeficiency virus infection
713325002,Primary cerebral lymphoma co-occurrent with human immunodeficiency virus infection
713339002,Infection caused by Strongyloides co-occurrent with human immunodeficiency virus infection
713340000,Disorder of skin co-occurrent with human immunodeficiency virus infection
713341001,Myelitis co-occurrent with human immunodeficiency virus infection
713342008,Infection caused by Salmonella co-occurrent with human immunodeficiency virus infection
713349004,Anemia co-occurrent with human immunodeficiency virus infection
713445006,Disseminated infection caused by Strongyloides co-occurrent with human immunodeficiency virus infection
713446007,Chronic infection caused by herpes simplex virus co-occurrent with human immunodeficiency virus infection
713483007,Reticulosarcoma co-occurrent with human immunodeficiency virus infection
713484001,Disorder of respiratory system co-occurrent with human immunodeficiency virus infection
713487008,Progressive multifocal leukoencephalopathy co-occurrent with human immunodeficiency virus infection
713488003,Presenile dementia co-occurrent with human immunodeficiency virus infection
713489006,Polyneuropathy co-occurrent with human immunodeficiency virus infection
713490002,Infection caused by Pneumocystis co-occurrent with human immunodeficiency virus infection
713491003,Organic brain syndrome co-occurrent with human immunodeficiency virus infection
713497004,Candidiasis of mouth co-occurrent with human immunodeficiency virus infection
713503007,Disorder of spinal cord co-occurrent with human immunodeficiency virus infection
713504001,Disorder of kidney co-occurrent with human immunodeficiency virus infection
713505000,Gastrointestinal malabsorption syndrome co-occurrent with human immunodeficiency virus infection
713506004,Neuritis co-occurrent with human immunodeficiency virus infection
713507008,Lymphadenopathy co-occurrent with human immunodeficiency virus infection
713508003,Aplastic anemia co-occurrent with human immunodeficiency virus infection
713510001,Enlargement of liver co-occurrent with human immunodeficiency virus infection
713511002,Acute endocarditis co-occurrent with human immunodeficiency virus infection
713516007,Primary effusion lymphoma
713523008,Cardiomyopathy co-occurrent with human immunodeficiency virus infection
713526000,Recurrent bacterial pneumonia co-occurrent with human immunodeficiency virus infection
713527009,Disorder of peripheral nervous system co-occurrent with human immunodeficiency virus infection
713530002,Agranulocytosis co-occurrent with human immunodeficiency virus infection
713531003,Visual impairment co-occurrent with human immunodeficiency virus infection
713532005,Infective arthritis co-occurrent with human immunodeficiency virus infection
713533000,Acquired hemolytic anemia co-occurrent with human immunodeficiency virus infection
713543002,Demyelinating disease of central nervous system co-occurrent with human immunodeficiency virus infection
713544008,Bacterial pneumonia co-occurrent with human immunodeficiency virus infection
713545009,Infection caused by Nocardia co-occurrent with human immunodeficiency virus infection
713546005,Isosporiasis co-occurrent with human immunodeficiency virus infection
713570009,Infectious gastroenteritis co-occurrent with human immunodeficiency virus infection
713571008,Disorder of central nervous system co-occurrent with human immunodeficiency virus infection
713572001,Malignant neoplastic disease co-occurrent with human immunodeficiency virus infection
713695001,Nephrotic syndrome co-occurrent with human immunodeficiency virus infection
713696000,Renal failure syndrome co-occurrent with human immunodeficiency virus infection
713718006,Diffuse non-Hodgkin immunoblastic lymphoma co-occurrent with human immunodeficiency virus infection
713722001,Infection caused by Cytomegalovirus co-occurrent with human immunodeficiency virus infection
713729005,Infection caused by Coccidia co-occurrent with human immunodeficiency virus infection
713730000,Infection caused by herpes simplex virus co-occurrent with human immunodeficiency virus infection
713731001,Pyrexia of unknown origin co-occurrent with human immunodeficiency virus infection
713732008,Infection caused by Aspergillus co-occurrent with human immunodeficiency virus infection
713733003,Infection caused by herpes zoster virus co-occurrent with human immunodeficiency virus infection
713734009,Infection caused by Dermatophyte co-occurrent with human immunodeficiency virus infection
713742005,Human immunodeficiency virus antibody positive
713844000,Dementia co-occurrent with human immunodeficiency virus infection
713845004,Infection caused by Cryptosporidium co-occurrent with human immunodeficiency virus infection
713880000,Opportunistic mycosis co-occurrent with human immunodeficiency virus infection
713881001,Infection caused by Microsporidia co-occurrent with human immunodeficiency virus infection
713887002,Focal segmental glomerulosclerosis co-occurrent with human immunodeficiency virus infection
713897006,Burkitt lymphoma co-occurrent with human immunodeficiency virus infection
713910008,Antibody mediated acquired pure red cell aplasia caused by erythropoiesis stimulating agent
713964006,Multidermatomal infection caused by Herpes zoster co-occurrent with human immunodeficiency virus infection
713967004,Disseminated atypical infection caused by Mycobacterium co-occurrent with human immunodeficiency virus infection
714251006,Philadelphia chromosome-negative precursor B-cell acute lymphoblastic leukemia
714463003,Primary effusion lymphoma co-occurrent with infection caused by Human herpesvirus 8
714464009,Immune reconstitution inflammatory syndrome caused by human immunodeficiency virus infection
715664005,Interdigitating dendritic cell sarcoma
715950008,Anaplastic lymphoma kinase positive large B-cell lymphoma
716788007,Epstein-Barr virus positive diffuse large B-cell lymphoma of elderly
716789004,Epstein-Barr virus positive diffuse large B-cell lymphoma of elderly
71692003,Leukoerythroblastotic reaction
718200007,Primary pulmonary lymphoma
718882006,X-linked severe congenital neutropenia
719156006,X-linked intellectual disability with hypogammaglobulinemia and progressive neurological deterioration syndrome
71922006,Immune defect
719522009,Infection of upper respiratory tract caused by Candida co-occurrent with human immunodeficiency virus infection
719789000,Human immunodeficiency virus 2 antibody positive and Human immunodeficiency virus 1 antibody cross-reactivity
721166000,Human immunodeficiency virus complicating pregnancy childbirth and the puerperium
721301004,Myeloid and lymphoid neoplasm with fibroblast growth factor receptor 1 abnormality
721302006,Refractory anemia with ringed sideroblasts associated with marked thrombocytosis
721303001,Refractory neutropenia
721304007,Refractory thrombocytopenia
721305008,Acute myeloid leukemia due to recurrent genetic abnormality
721306009,Therapy related acute myeloid leukemia and myelodysplastic syndrome
721308005,Acute leukemia of ambiguous lineage
721310007,Aggressive natural killer-cell leukemia
721311006,Systemic Epstein-Barr virus positive T-cell lymphoproliferative disease of childhood
721313009,Indeterminate dendritic cell neoplasm
721314003,Fibroblastic reticular cell neoplasm
721555001,Follicular lymphoma of small intestine
721762007,Adult T-cell leukemia/lymphoma of skin
722067005,Severe combined immunodeficiency with hypereosinophilia
722557007,Parkinsonism due to human immunodeficiency virus infection
722795004,Meningeal leukemia
722953004,B-cell lymphoma unclassifiable with features intermediate between Burkitt lymphoma and diffuse large B-cell lymphoma
722954005,B-cell lymphoma unclassifiable with features intermediate between classical Hodgkin lymphoma and diffuse large B-cell lymphoma
722955006,Chronic lymphoproliferative disorder of natural killer cells
722957003,Reactive plasmacytic hyperplasia post-transplant lymphoproliferative disorder
722958008,Infectious mononucleosis-like post-transplant lymphoproliferative disorder
723889003,B lymphoblastic leukemia lymphoma with t(9:22) (q34;q11.2); BCR-ABL 1
724642009,Myeloid neoplasm associated with beta-type platelet-derived growth factor receptor gene rearrangement
724644005,Myeloid leukemia co-occurrent with Down syndrome
724645006,T-cell histiocyte rich large B-cell lymphoma
724647003,Diffuse large B-cell lymphoma co-occurrent with chronic inflammation caused by Epstein-Barr virus
724648008,Plasmablastic lymphoma
724649000,Langerhans cell sarcoma
724650000,Primary follicular dendritic cell sarcoma
725137007,"Neutropenia, monocytopenia, deafness syndrome"
725390002,Acute myeloid leukemia with t(8;16)(p11;p13) translocation
725391003,Acute myeloid leukemia with t(8;16)(p11;p13) translocation
725437002,Chronic lymphocytic leukemia genetic mutation variant
72621000119104,Human immunodeficiency virus (HIV) II infection category B1
72631000119101,Human immunodeficiency virus (HIV) II infection category B2
726721002,Nodal marginal zone B-cell lymphoma
733598001,Acute myeloid leukemia with t(6;9)(p23;q34) translocation
733627006,Primary cutaneous gamma-delta-positive T-cell lymphoma
733834006,Invasive carcinoma of uterine cervix co-occurrent with human immunodeficiency virus infection
733835007,Extrapulmonary tuberculosis co-occurrent with human immunodeficiency virus infection
733860007,Pediatric nodal marginal zone lymphoma
733895005,Primary cutaneous CD8 positive aggressive epidermotropic cytotoxic T-cell lymphoma
733917002,Pediatric follicular lymphoma
734066005,Diffuse large B-cell lymphoma of central nervous system
734067001,Splenic diffuse red pulp small B-cell lymphoma
734076008,Diffuse large B-cell lymphoma associated with chronic inflammation
734141009,Splenic B-cell lymphoma
734142002,B-cell lymphoma with features intermediate between diffuse large B-cell lymphoma and Burkitt lymphoma
734522002,Acute myeloid leukemia with FMS-like tyrosine kinase-3 mutation
734524001,Acute myeloid leukemia with FMS-like tyrosine kinase-3 mutation
735332000,Primary cutaneous diffuse large cell B-cell lymphoma of lower extremity
735439008,Constitutional eosinopenia
735440005,Acquired eosinopenia
735442002,Acquired eosinophilia
735443007,Acquired lymphocytopenia
735521001,Human immunodeficiency virus World Health Organization 2007 stage 1 co-occurrent with tuberculosis
735522008,Human immunodeficiency virus World Health Organization 2007 stage 1 co-occurrent with malaria
735523003,Human immunodeficiency virus World Health Organization 2007 stage 2 co-occurrent with tuberculosis
735524009,Human immunodeficiency virus World Health Organization 2007 stage 2 co-occurrent with malaria
735525005,Human immunodeficiency virus World Health Organization 2007 stage 3 co-occurrent with tuberculosis
735526006,Human immunodeficiency virus World Health Organization 2007 stage 3 co-occurrent with malaria
735527002,Human immunodeficiency virus World Health Organization 2007 stage 4 co-occurrent with tuberculosis
735528007,Human immunodeficiency virus World Health Organization 2007 stage 4 co-occurrent with malaria
736024007,Pancytopenia caused by medication
736322001,Pediatric follicular lymphoma
737223000,Dendritic cell neoplasm
737224006,Histiocytic neoplasm
738527001,Myeloid and/or lymphoid neoplasm associated with platelet derived growth factor receptor alpha rearrangement
738770003,Anaplastic lymphoma kinase positive anaplastic large cell lymphoma
739301006,Osteoporosis co-occurrent and due to multiple myeloma
74189002,Hodgkin granuloma [obs]
74654000,Mantle cell lymphoma
762315004,Therapy related acute myeloid leukemia due to and following administration of antineoplastic agent
762690000,Classical Hodgkin lymphoma
762691001,Classical Hodgkin lymphoma
763309005,Acute myeloid leukemia with nucleophosmin 1 somatic mutation
763477007,Primary lymphoma of conjunctiva
763666008,Splenic marginal zone B-cell lymphoma
763719001,Hydroa vacciniforme-like lymphoma
763796007,Megakaryoblastic acute myeloid leukemia with t(1;22)(p13;q13)
763884007,Splenic diffuse red pulp small B-cell lymphoma
764855007,Acute myeloid leukemia with CCAAT/enhancer binding protein alpha somatic mutation
764940002,Inherited acute myeloid leukemia
765136002,Primary cutaneous CD8 positive aggressive epidermotropic cytotoxic T-cell lymphoma
765328000,Classic mycosis fungoides
765748009,Adult pure red cell aplasia
766045006,Acute myeloid leukemia and myelodysplastic syndrome related to alkylating agent
766046007,Acute myeloid leukemia and myelodysplastic syndrome related to topoisomerase type 2 inhibitor
766048008,Acute myeloid leukemia and myelodysplastic syndrome related to radiation
766935007,Primary bone lymphoma
767263007,22q11.2 deletion syndrome
76762001,Eosinophilic myopathy
767658000,Neutropenia due to and following chemotherapy
76981000119106,Human immunodeficiency virus (HIV) infection category B1
76991000119109,Human immunodeficiency virus (HIV) infection category B2
770596007,Rippling muscle disease with myasthenia gravis
77084001,Immunologic aplastic anemia
770942003,Kostmann syndrome
770947009,Autosomal dominant severe congenital neutropenia
771119002,Infection caused by Coccidia co-occurrent with acquired immunodeficiency syndrome
771126002,Infection caused by Toxoplasma gondii co-occurrent with acquired immunodeficiency syndrome
771127006,Infection caused by Isospora co-occurrent with acquired immunodeficiency syndrome
772126000,Poikiloderma with neutropenia
773537001,Differentiation syndrome due to and following chemotherapy co-occurrent with acute promyelocytic leukemia
773646003,Phospholipase C gamma 2 associated antibody deficiency and immune dysregulation
773730002,Osteopetrosis hypogammaglobulinemia syndrome
77381001,Burkitt lymphoma
773995001,Primary cutaneous anaplastic large cell lymphoma
77430005,Adult T-cell leukemia/lymphoma
77461000119109,Myasthenia gravis with exacerbation
77471000119103,Myasthenia gravis without exacerbation
778004006,Autoinflammation phospholipase C gamma 2 associated antibody deficiency and immune dysregulation
780817000,Undifferentiated myeloproliferative disease
780844005,Acute myeloid leukemia with inv(3)(q21q26.2) or t(3;3)(q21;q26.2); RPN1-EVI1
783017000,Acute myeloid leukemia with BCR-ABL1
783058007,Autosomal recessive severe congenital neutropenia due to glucose-6-phosphatase catalytic subunit 3 deficiency
783199003,Autosomal recessive severe congenital neutropenia due to jagunal homolog 1 deficiency
783200000,Autosomal recessive severe congenital neutropenia due to C-X-C motif chemokine receptor 2 deficiency
783201001,Autosomal recessive severe congenital neutropenia due to colony stimulating factor 3 receptor deficiency
783205005,Alopecia antibody deficiency
783220004,Burkitt-like lymphoma with 11q aberration
783263001,Acute myeloid leukemia with mutated RUNX1
783541009,Breast implant?associated anaplastic large-cell lymphoma
783565007,Indolent T-cell lymphoproliferative disorder of gastrointestinal tract
783615009,Erythropoietic uroporphyria associated with myeloid malignancy
783744003,B-lymphoblastic leukemia lymphoma BCR-ABL1-like
78378009,Isoimmune neutropenia
784551004,Follicular T-cell lymphoma
785825000,B lymphoblastic leukemia lymphoma with intrachromosomal amplification of chromosome 21
786909001,High grade B-cell lymphoma with MYC and BCL2 and/or BCL6 rearrangements
786960000,Large B-cell lymphoma with interferon regulatory factor 4 rearrangement
787036009,Monomorphic epitheliotropic intestinal T-cell lymphoma
787198005,Primary cutaneous acral CD8 positive T-cell lymphoma
787565006,Diffuse large B-cell lymphoma activated B-cell subtype
787594004,Diffuse large B-cell lymphoma germinal centre B-cell subtype
787941004,Myeloid and/or lymphoid neoplasm with pericentriolar material 1-janus kinase 2
788674000,Primary cutaneous CD4 positive small/medium T-cell lymphoproliferative disorder
788740009,Acute myeloid leukemia with biallelic mutation of CCAAT enhancer binding protein alpha gene
788874003,B-cell prolymphocytic leukemia in remission
788972003,Juvenile myelomonocytic leukemia in remission
789435006,Myelodysplastic syndrome with ring sideroblasts and multilineage dysplasia
789689004,Malignant lymphomatoid granulomatosis
789690008,Malignant lymphomatoid granulomatosis of lung
79019005,Human immunodeficiency virus II infection
79336007,Familial eosinophilia
79369007,Complication of transplanted pancreas
80191000119101,Symptomatic human immunodeficiency virus I infection
80570006,Acute panmyelosis with myelofibrosis
80976008,Myasthenic crisis
81000119104,Symptomatic human immunodeficiency virus infection
815121000000102,Follicular lymphoma grade 3a
815131000000100,Follicular lymphoma grade 3b
815361000000107,Acute myeloid leukaemia with 11q23 abnormality
820601000000103,Refractory anaemia with multilineage dysplasia
82178003,Neonatal myasthenia gravis
830057003,Relapsing classical Hodgkin lymphoma
835009,Angioimmunoblastic T-cell lymphoma
836276000,Hodgkin sarcoma
836277009,Hodgkin granuloma
836486002,Lymphomatous infiltrate of kidney
838340006,B lymphoblastic leukemia lymphoma with t(5;14)(q31;q32); IL3-IGH
838341005,B lymphoblastic leukemia lymphoma with t(v;11q23); MLL rearranged
838342003,B lymphoblastic leukemia lymphoma with t(12;21) (p13;q22); TEL/AML1 (ETV6-RUNX1)
838343008,B lymphoblastic leukemia lymphoma with t(1;19)(Q23;P13.3); E2A-PBX1 (TCF3/PBX1)
838344002,B lymphoblastic leukemia lymphoma with hypodiploidy
838346000,B lymphoblastic leukemia lymphoma with hyperdiploidy
838355002,Acute myeloid leukemia with inv(16)(p13.1q22) or t(16;16)(p13.1;q22) CBFB-MYH11
838377003,Chronic hepatitis C co-occurrent with human immunodeficiency virus infection
83980004,Impaired phagocytosis
840423002,Diffuse large B-cell lymphoma of small intestine
840424008,Diffuse large B-cell lymphoma of stomach
840442003,Encephalitis caused by human immunodeficiency virus type 2
840498003,Encephalitis caused by human immunodeficiency virus type 1
847481000000109,Follicular lymphoma grade 1
847631000000107,Follicular lymphoma grade 2
847651000000100,Follicular lymphoma grade 3
847691000000108,Follicular lymphoma grade 3a
847701000000108,Follicular lymphoma grade 3b
847741000000106,Diffuse large B-cell lymphoma
860824009,Eosinophilia due to infectious disease
860827002,Eosinopenia due to infectious disease
863741000000108,Clinical stage A chronic lymphocytic leukaemia
863761000000109,Clinical stage B chronic lymphocytic leukaemia
863781000000100,Clinical stage C chronic lymphocytic leukaemia
86406008,Human immunodeficiency virus infection
866084002,Lymphopenia due to infection
866098005,Large B-cell lymphoma arising in HHV8-associated multicentric Castleman disease
866109006,Lymphocytic hypereosinophilic syndrome
866901000000103,Eosinophilic bronchitis
87117006,Human immunodeficiency virus infection with acute lymphadenitis
871540009,Myelofibrosis due to and following polycythemia vera
871541008,Myelofibrosis due to and following essential thrombocythemia
87163000,"Leukemia, no International Classification of Diseases for Oncology subtype"
89655007,Congenital neutropenia
90120004,Mycosis fungoides
90681000119107,Asymptomatic human immunodeficiency virus A1 infection
90691000119105,Asymptomatic human immunodeficiency virus A2 infection
91637004,Myasthenia gravis
91854005,Acute leukemia in remission
91855006,"Acute leukemia, disease"
91856007,Acute lymphoid leukemia in remission
91857003,"Acute lymphoid leukemia, disease"
91858008,Acute monocytic leukemia in remission
91860005,Acute myeloid leukemia in remission
91861009,"Acute myeloid leukemia, disease"
91947003,Asymptomatic human immunodeficiency virus infection
91948008,Asymptomatic human immunodeficiency virus infection in pregnancy
92511007,Burkitt's tumor of lymph nodes of axilla AND/OR upper limb
92512000,"Burkitt's tumor of lymph nodes of head, face AND/OR neck"
92513005,Burkitt's tumor of lymph nodes of inguinal region AND/OR lower limb
92516002,Burkitt's tumor of extranodal AND/OR solid organ site
92811003,Chronic leukemia in remission
92812005,"Chronic leukemia, disease"
92813000,Chronic lymphoid leukemia in remission
92814006,"Chronic lymphoid leukemia, disease"
92817004,Chronic myeloid leukemia in remission
92818009,"Chronic myeloid leukemia, disease"
93133006,Letterer-Siwe disease of intra-abdominal lymph nodes
93134000,Letterer-Siwe disease of intrapelvic lymph nodes
93135004,Letterer-Siwe disease of intrathoracic lymph nodes
93136003,Letterer-Siwe disease of lymph nodes of axilla AND/OR upper limb
93137007,"Letterer-Siwe disease of lymph nodes of head, face AND/OR neck"
93138002,Letterer-Siwe disease of lymph nodes of inguinal region AND/OR lower limb
93139005,Letterer-Siwe disease of lymph nodes of multiple sites
93140007,Letterer-Siwe disease of spleen
93141006,Letterer-Siwe disease of extranodal AND/OR solid organ site
93142004,Leukemia in remission
93143009,"Leukemia, disease"
93144003,Leukemic reticuloendotheliosis of intra-abdominal lymph nodes
93145002,Leukemic reticuloendotheliosis of intrapelvic lymph nodes
93146001,Leukemic reticuloendotheliosis of intrathoracic lymph nodes
93150008,Leukemic reticuloendotheliosis of lymph nodes of multiple sites
93151007,Hairy cell leukemia of spleen
93152000,Leukemic reticuloendotheliosis of extranodal AND/OR solid organ site
93169003,Lymphoid leukemia in remission
93182006,Malignant histiocytosis of intra-abdominal lymph nodes
93183001,Malignant histiocytosis of intrapelvic lymph nodes
93184007,Malignant histiocytosis of intrathoracic lymph nodes
93185008,Malignant histiocytosis of lymph nodes of axilla AND/OR upper limb
93186009,"Malignant histiocytosis of lymph nodes of head, face AND/OR neck"
93187000,Malignant histiocytosis of lymph nodes of inguinal region AND/OR lower limb
93188005,Malignant histiocytosis of lymph nodes of multiple sites
93189002,Malignant histiocytosis of spleen
93190006,Malignant histiocytosis of extranodal AND/OR solid organ site
93191005,Malignant lymphoma of intra-abdominal lymph nodes
93192003,Malignant lymphoma of intrapelvic lymph nodes
93193008,Malignant lymphoma of intrathoracic lymph nodes
93194002,Malignant lymphoma of lymph nodes of axilla AND/OR upper limb
93195001,"Malignant lymphoma of lymph nodes of head, face AND/OR neck"
93196000,Malignant lymphoma of lymph nodes of inguinal region AND/OR lower limb
93197009,Malignant lymphoma of lymph nodes of multiple sites
93198004,Malignant lymphoma of spleen
93199007,Malignant lymphoma of extranodal AND/OR solid organ site
93200005,Malignant mast cell tumor of intra-abdominal lymph nodes
93201009,Malignant mast cell tumor of intrapelvic lymph nodes
93202002,Malignant mast cell tumor of intrathoracic lymph nodes
93203007,Malignant mast cell tumor of lymph nodes of axilla AND/OR upper limb
93204001,"Malignant mast cell tumor of lymph nodes of head, face AND/OR neck"
93205000,Malignant mast cell tumor of lymph nodes of inguinal region AND/OR lower limb
93451002,"Erythroleukemia, FAB M6"
93487009,"Hodgkin's disease, lymphocytic depletion of lymph nodes of axilla AND/OR upper limb"
93488004,"Hodgkin's disease, lymphocytic depletion of lymph nodes of head, face AND/OR neck"
93489007,"Hodgkin's disease, lymphocytic depletion of lymph nodes of inguinal region AND/OR lower limb"
93492006,"Hodgkin's disease, lymphocytic depletion of extranodal AND/OR solid organ site"
93493001,"Hodgkin's disease, lymphocytic-histiocytic predominance of intra-abdominal lymph nodes"
93494007,"Hodgkin's disease, lymphocytic-histiocytic predominance of intrapelvic lymph nodes"
93495008,"Hodgkin's disease, lymphocytic-histiocytic predominance of intrathoracic lymph nodes"
93496009,"Hodgkin's disease, lymphocytic-histiocytic predominance of lymph nodes of axilla AND/OR upper limb"
93497000,"Hodgkin's disease, lymphocytic-histiocytic predominance of lymph nodes of head, face AND/OR neck"
93498005,"Hodgkin's disease, lymphocytic-histiocytic predominance of lymph nodes of inguinal region AND/OR lower limb"
93500006,"Hodgkin's disease, lymphocytic-histiocytic predominance of spleen"
93501005,"Hodgkin's disease, lymphocytic-histiocytic predominance of extranodal AND/OR solid organ site"
93505001,"Hodgkin's disease, mixed cellularity of lymph nodes of axilla AND/OR upper limb"
93506000,"Hodgkin's disease, mixed cellularity of lymph nodes of head, face AND/OR neck"
93507009,"Hodgkin's disease, mixed cellularity of lymph nodes of inguinal region AND/OR lower limb"
93509007,"Hodgkin's disease, mixed cellularity of spleen"
93510002,"Hodgkin's disease, mixed cellularity of extranodal AND/OR solid organ site"
93514006,"Hodgkin's disease, nodular sclerosis of lymph nodes of axilla AND/OR upper limb"
93515007,"Hodgkin's disease, nodular sclerosis of lymph nodes of head, face AND/OR neck"
93516008,"Hodgkin's disease, nodular sclerosis of lymph nodes of inguinal region AND/OR lower limb"
93518009,"Hodgkin's disease, nodular sclerosis of spleen"
93519001,"Hodgkin's disease, nodular sclerosis of extranodal AND/OR solid organ site"
93520007,Hodgkin's disease of intra-abdominal lymph nodes
93521006,Hodgkin's disease of intrapelvic lymph nodes
93522004,Hodgkin's disease of intrathoracic lymph nodes
93523009,Hodgkin's disease of lymph nodes of axilla AND/OR upper limb
93524003,"Hodgkin's disease of lymph nodes of head, face AND/OR neck"
93525002,Hodgkin's disease of lymph nodes of inguinal region AND/OR lower limb
93526001,Hodgkin's disease of lymph nodes of multiple sites
93527005,Hodgkin's disease of spleen
93528000,Hodgkin's disease of extranodal AND/OR solid organ site
93530003,Hodgkin's granuloma of intrapelvic lymph nodes
93531004,Hodgkin's granuloma of intrathoracic lymph nodes
93532006,Hodgkin's granuloma of lymph nodes of axilla AND/OR upper limb
93533001,"Hodgkin's granuloma of lymph nodes of head, face AND/OR neck"
93534007,Hodgkin's granuloma of lymph nodes of inguinal region AND/OR lower limb
93536009,Hodgkin's granuloma of spleen
93537000,Hodgkin's granuloma of extranodal AND/OR solid organ site
93541001,Hodgkin's paragranuloma of lymph nodes of axilla AND/OR upper limb
93542008,"Hodgkin's paragranuloma of lymph nodes of head, face AND/OR neck"
93543003,Hodgkin's paragranuloma of lymph nodes of inguinal region AND/OR lower limb
93546006,Hodgkin's paragranuloma of extranodal AND/OR solid organ site
93547002,Hodgkin's sarcoma of intra-abdominal lymph nodes
93548007,Hodgkin's sarcoma of intrapelvic lymph nodes
93549004,Hodgkin's sarcoma of intrathoracic lymph nodes
93550004,Hodgkin's sarcoma of lymph nodes of axilla AND/OR upper limb
93551000,"Hodgkin's sarcoma of lymph nodes of head, face AND/OR neck"
93552007,Hodgkin's sarcoma of lymph nodes of inguinal region AND/OR lower limb
93554008,Hodgkin's sarcoma of spleen
93555009,Hodgkin's sarcoma of extranodal AND/OR solid organ site
94148006,Megakaryocytic leukemia in remission
943041000000105,Human immunodeficiency virus disease resulting in haematological and immunological abnormalities
94686001,Mixed cell type lymphosarcoma of intra-abdominal lymph nodes
94687005,Mixed cell type lymphosarcoma of intrapelvic lymph nodes
94688000,Mixed cell type lymphosarcoma of intrathoracic lymph nodes
94690004,"Mixed cell type lymphosarcoma of lymph nodes of head, face, and neck"
94704006,Multiple myeloma in remission
94707004,Mycosis fungoides of intra-abdominal lymph nodes
94708009,Mycosis fungoides of intrapelvic lymph nodes
94709001,Mycosis fungoides of intrathoracic lymph nodes
94710006,Mycosis fungoides of lymph nodes of axilla AND/OR upper limb
94711005,"Mycosis fungoides of lymph nodes of head, face AND/OR neck"
94712003,Mycosis fungoides of lymph nodes of inguinal region AND/OR lower limb
94714002,Mycosis fungoides of spleen
94715001,Mycosis fungoides of extranodal AND/OR solid organ site
94716000,Myeloid leukemia in remission
94718004,Myeloid sarcoma in remission
94719007,"Myeloid sarcoma, disease"
95186006,Nodular lymphoma of intra-abdominal lymph nodes
95187002,Nodular lymphoma of intrapelvic lymph nodes
95188007,Nodular lymphoma of intrathoracic lymph nodes
95192000,Nodular lymphoma of lymph nodes of multiple sites
95193005,Nodular lymphoma of spleen
95194004,Nodular lymphoma of extranodal AND/OR solid organ site
95209008,Plasma cell leukemia in remission
95210003,"Plasma cell leukemia, disease"
95224004,Reticulosarcoma of intra-abdominal lymph nodes
95225003,Reticulosarcoma of intrapelvic lymph nodes
95226002,Reticulosarcoma of intrathoracic lymph nodes
95230004,Reticulosarcoma of lymph nodes of multiple sites
95231000,Reticulosarcoma of spleen
95260009,"Sézary's disease of lymph nodes of head, face AND/OR neck"
95261008,Sézary's disease of lymph nodes of inguinal region AND/OR lower limb
95263006,Sézary's disease of spleen
95264000,Sézary's disease of extranodal AND/OR solid organ site
95416007,Eosinophilia myalgia syndrome
95733001,Eosinophilic keratitis
95892003,Persistent generalized lymphadenopathy"""


c15_df = pd.read_csv(io.StringIO(c15), header=0,delimiter=',').astype(str)
spark.createDataFrame(c15_df).createOrReplaceGlobalTempView("ccu002_06_d17_immdx_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_immdx_primis

# COMMAND ----------

# MAGIC %md ## immrx_primis

# COMMAND ----------

c16 = """code,term
10053811000001103,Fluorouracil 250mg/10ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
10060111000001109,Vinblastine 10mg/10ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
10072211000001108,Temodal 5mg capsules (Schering-Plough Ltd) (product)
10246911000001106,Oxaliplatin 50mg/10ml solution for injection vials (product)
10247111000001106,Eloxatin 50mg/10ml solution for injection vials (sanofi-aventis) (product)
10247311000001108,Oxaliplatin 100mg/20ml solution for injection vials (product)
10247511000001102,Eloxatin 100mg/20ml solution for injection vials (sanofi-aventis) (product)
10277911000001108,Dacarbazine 200mg powder for solution for injection vials (Medac GMBH) (product)
10288111000001102,Azathioprine 50mg tablets (Focus Pharmaceuticals Ltd) (product)
10354511000001104,Antithymocyte immunoglobulin (rabbit) 25mg powder and solvent for solution for injection vials (product)
10354711000001109,Thymoglobulin 25mg powder and solvent for solution for injection vials (Genzyme Therapeutics) (product)
10356411000001106,Vinorelbine 50mg/5ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
10445811000001105,Fluorouracil 2.5g/100ml solution for injection vials (Mayne Pharma Plc) (product)
10448111000001108,Cladribine 10mg/5ml solution for injection vials (product)
10448311000001105,Litak 10 solution for injection vials (Lipomed Ltd) (product)
10454511000001108,Cytoxan 25mg tablets (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
10455611000001108,Droxia 300mg capsules (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
10478811000001100,CellCept 250mg capsules (PI) (Dowelhurst Ltd) (product)
10480711000001104,CellCept 500mg tablets (PI) (Dowelhurst Ltd) (product)
10485011000001107,Arava 10mg tablets (PI) (Waymade Ltd) (product)
10485511000001104,Arava 20mg tablets (PI) (Waymade Ltd) (product)
10524411000001104,Carboplatin 50mg/5ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
10524611000001101,Carboplatin 150mg/15ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
10525111000001108,Carboplatin 450mg/45ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
10525511000001104,Carboplatin 600mg/60ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
10528511000001107,Cisplatin 10mg/10ml solution for injection vials (Teva UK Ltd) (product)
10528811000001105,Cisplatin 50mg/50ml solution for injection vials (Teva UK Ltd) (product)
10529311000001107,Cisplatin 100mg/100ml solution for injection vials (Teva UK Ltd) (product)
10531511000001104,Doxorubicin 10mg/5ml solution for injection vials (Teva UK Ltd) (product)
10531811000001101,Doxorubicin 50mg/25ml solution for injection vials (Teva UK Ltd) (product)
10532111000001103,Doxorubicin 200mg/100ml solution for injection vials (Teva UK Ltd) (product)
10532811000001105,Etoposide 100mg/5ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
10533011000001108,Etoposide 500mg/25ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
10533211000001103,Paclitaxel 30mg/5ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
10533411000001104,Paclitaxel 100mg/16.7ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
10533611000001101,Paclitaxel 150mg/25ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
10533811000001102,Paclitaxel 300mg/50ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
10538811000001107,Mercaptopurine 50mg tablets (PI) (Waymade Ltd) (product)
10615511000001104,Fluorouracil 2.5g/100ml solution for injection vials (medac UK) (product)
10615711000001109,Hydroxycarbamide 500mg capsules (medac UK) (product)
10619911000001108,Doxorubin 10mg powder for solution for injection vials (medac UK) (product)
10620211000001100,Doxorubin 50mg powder for solution for injection vials (medac UK) (product)
10620411000001101,Doxorubin 10mg/5ml solution for injection vials (medac UK) (product)
10620611000001103,Doxorubin 50mg/25ml solution for injection vials (medac UK) (product)
10620811000001104,Doxorubin 200mg/100ml solution for injection vials (medac UK) (product)
10626311000001106,Tysabri 300mg/15ml concentrate for solution for infusion vials (Biogen Ltd) (product)
10638811000001104,CeeNU 100mg capsules (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
10639111000001104,CeeNU 10mg capsules (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
10640911000001106,Paclitaxel 30mg/5ml concentrate for solution for infusion vials (Wockhardt UK Ltd) (product)
10641111000001102,Paclitaxel 100mg/16.7ml concentrate for solution for infusion vials (Wockhardt UK Ltd) (product)
10641511000001106,Paclitaxel 150mg/25ml concentrate for solution for infusion vials (Wockhardt UK Ltd) (product)
10641711000001101,Paclitaxel 300mg/50ml concentrate for solution for infusion vials (Wockhardt UK Ltd) (product)
10642011000001106,Vinorelbine 10mg/1ml concentrate for solution for injection vials (Wockhardt UK Ltd) (product)
10642411000001102,Vinorelbine 50mg/5ml concentrate for solution for injection vials (Wockhardt UK Ltd) (product)
10672611000001103,Metoject 7.5mg/0.75ml solution for injection pre-filled syringes (medac UK) (product)
10672911000001109,Metoject 10mg/1ml solution for injection pre-filled syringes (medac UK) (product)
10673211000001106,Metoject 15mg/1.5ml solution for injection pre-filled syringes (medac UK) (product)
10673511000001109,Metoject 20mg/2ml solution for injection pre-filled syringes (medac UK) (product)
10674011000001104,Metoject 25mg/2.5ml solution for injection pre-filled syringes (medac UK) (product)
10675611000001107,Methotrexate 10mg/1ml solution for injection pre-filled syringes (product)
10675711000001103,Methotrexate 15mg/1.5ml solution for injection pre-filled syringes (product)
10675811000001106,Methotrexate 20mg/2ml solution for injection pre-filled syringes (product)
10675911000001101,Methotrexate 25mg/2.5ml solution for injection pre-filled syringes (product)
10676011000001109,Methotrexate 7.5mg/0.75ml solution for injection pre-filled syringes (product)
10676411000001100,Vinorelbine 10mg/1ml concentrate for solution for infusion vials (medac UK) (product)
10676611000001102,Vinorelbine 50mg/5ml concentrate for solution for infusion vials (medac UK) (product)
10685111000001105,Nexavar 200mg tablets (Bayer Plc) (product)
10685411000001100,Evoltra 20mg/20ml concentrate for solution for infusion vials (Bioenvision Ltd) (product)
10688011000001101,Clofarabine 20mg/20ml solution for injection vials (product)
10688111000001100,Sorafenib 200mg tablets (product)
10816811000001103,Sutent 50mg capsules (Pfizer Ltd) (product)
10817111000001108,Sutent 25mg capsules (Pfizer Ltd) (product)
10817411000001103,Sutent 12.5mg capsules (Pfizer Ltd) (product)
10818111000001109,Muromonab-CD3 solution for injection 5mg/5ml ampoules (product)
10818811000001102,Orthoclone OKT3 solution for injection 5mg/5ml ampoules (Ortho Biotech) (product)
10831711000001105,Sunitinib 12.5mg capsules (product)
10831811000001102,Sunitinib 25mg capsules (product)
10831911000001107,Sunitinib 50mg capsules (product)
10904711000001109,Epirubicin 10mg/5ml solution for injection vials (Mayne Pharma Plc) (product)
10904911000001106,Epirubicin 50mg/25ml solution for injection vials (Mayne Pharma Plc) (product)
10905611000001104,Epirubicin 100mg/50ml solution for injection vials (Mayne Pharma Plc) (product)
10905811000001100,Epirubicin 200mg/100ml solution for injection vials (Mayne Pharma Plc) (product)
10907011000001104,Oxaliplatin 50mg powder for solution for infusion vials (Mayne Pharma Plc) (product)
10907211000001109,Oxaliplatin 100mg powder for solution for infusion vials (Mayne Pharma Plc) (product)
10919611000001103,Epirubicin 100mg/50ml solution for injection vials (product)
10964511000001100,Oxaliplatin 50mg powder for solution for injection vials (A A H Pharmaceuticals Ltd) (product)
10964711000001105,Oxaliplatin 100mg powder for solution for injection vials (A A H Pharmaceuticals Ltd) (product)
10967711000001103,Enbrel 50mg/1ml solution for injection pre-filled syringes (Wyeth Pharmaceuticals) (product)
10969111000001105,Eloxatin 200mg/40ml concentrate for solution for infusion vials (sanofi-aventis) (product)
10970211000001102,Etanercept 50mg/1ml solution for injection pre-filled syringes (product)
10970711000001109,Oxaliplatin 200mg/40ml solution for injection vials (product)
10979611000001106,Lymphoglobuline 100mg/5ml solution for injection vials (Genzyme Therapeutics) (product)
10983911000001108,Antithymocyte immunoglobulin (equine) 100mg/5ml solution for injection vials (product)
10985011000001105,Sprycel 20mg tablets (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
10985511000001102,Sprycel 50mg tablets (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
10985811000001104,Sprycel 70mg tablets (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
10986511000001109,Hydroxycarbamide 500mg capsules (A A H Pharmaceuticals Ltd) (product)
10987511000001106,Dasatinib 20mg tablets (product)
10987611000001105,Dasatinib 50mg tablets (product)
10987711000001101,Dasatinib 70mg tablets (product)
10988011000001102,Methotrexate 50mg/2ml solution for injection vials (Teva UK Ltd) (product)
10988211000001107,Methotrexate 500mg/20ml solution for injection vials (Teva UK Ltd) (product)
110211000001101,Fluorouracil 500mg/20ml solution for injection vials (Unichem Plc) (product)
11023211000001107,Enbrel Paediatric 25mg powder and solvent for solution for injection vials (Wyeth Pharmaceuticals) (product)
11026411000001101,Methotrexate 2.5mg tablets (Wockhardt UK Ltd) (product)
11026611000001103,Methotrexate 10mg tablets (Wockhardt UK Ltd) (product)
11033511000001108,Enbrel 25mg/0.5ml solution for injection pre-filled syringes (Wyeth Pharmaceuticals) (product)
11034511000001106,Etanercept 25mg/0.5ml solution for injection pre-filled syringes (product)
11091011000001108,Methotrexate 1g/40ml solution for injection vials (Teva UK Ltd) (product)
11121311000001108,Rapamune 2mg tablets (Waymade Ltd) (product)
11159911000001109,Prograf 500microgram capsules (Waymade Ltd) (product)
11188011000001105,Humira 40mg/0.8ml solution for injection pre-filled pens (AbbVie Ltd) (product)
11236911000001103,Adalimumab 40mg/0.8ml solution for injection pre-filled disposable devices (product)
11248011000001104,Cisplatin 50mg powder for solution for injection vials (Unichem Plc) (product)
11403011000001103,Dacarbazine 100mg powder for solution for injection vials (Pliva Pharma Ltd) (product)
11403511000001106,Dacarbazine 200mg powder for solution for injection vials (Pliva Pharma Ltd) (product)
11422411000001107,Mitoxantrone 20mg/10ml concentrate for solution for infusion vials (Pliva Pharma Ltd) (product)
11423411000001103,Mitoxantrone 25mg/12.5ml concentrate for solution for infusion vials (Pliva Pharma Ltd) (product)
11494311000001100,Cetuximab 100mg/20ml solution for injection vials (product)
11494411000001107,Cetuximab 500mg/100ml solution for injection vials (product)
11495111000001103,Erbitux 100mg/20ml solution for infusion vials (Merck Pharmaceuticals) (product)
11495411000001108,Erbitux 500mg/100ml solution for infusion vials (Merck Pharmaceuticals) (product)
11528811000001100,Doxorubicin 10mg powder for solution for injection vials (UniChem Ltd) (product)
11529011000001101,Doxorubicin 50mg powder for solution for injection vials (UniChem Ltd) (product)
11529511000001109,Doxorubicin 200mg/100ml solution for injection vials (UniChem Ltd) (product)
11556411000001102,Tarceva 25mg tablets (Roche Products Ltd) (product)
11619211000001106,Advagraf 0.5mg modified-release capsules (Astellas Pharma Ltd) (product)
11619611000001108,Advagraf 1mg modified-release capsules (Astellas Pharma Ltd) (product)
11620011000001100,Advagraf 5mg modified-release capsules (Astellas Pharma Ltd) (product)
11649511000001103,Tacrolimus 1mg modified-release capsules (product)
11649611000001104,Tacrolimus 500microgram modified-release capsules (product)
11649711000001108,Tacrolimus 5mg modified-release capsules (product)
11753911000001100,Orencia 250mg powder for concentrate for solution for infusion vials (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
11755211000001108,Revlimid 5mg capsules (Celgene Europe Ltd) (product)
11755711000001101,Revlimid 10mg capsules (Celgene Europe Ltd) (product)
11756011000001107,Revlimid 15mg capsules (Celgene Europe Ltd) (product)
11756511000001104,Revlimid 25mg capsules (Celgene Europe Ltd) (product)
11762011000001101,Abatacept 250mg powder for solution for injection vials (product)
11762911000001102,Lenalidomide 15mg capsules (product)
11763011000001105,Lenalidomide 25mg capsules (product)
11793511000001104,Cyclophosphamide 35mg/5ml oral suspension (Special Order) (product)
11793811000001101,Cyclophosphamide 35mg/5ml oral solution (Special Order) (product)
11794111000001105,Cyclophosphamide 40mg/5ml oral suspension (Special Order) (product)
11794411000001100,Cyclophosphamide 40mg/5ml oral solution (Special Order) (product)
11794711000001106,Cyclophosphamide 75mg/5ml oral suspension (Special Order) (product)
11795011000001108,Cyclophosphamide 75mg/5ml oral solution (Special Order) (product)
11812511000001108,Soliris 300mg/30ml concentrate for solution for infusion vials (Almac Pharma Services Ltd) (product)
11818011000001102,Cyclophosphamide 35mg/5ml oral solution (product)
11818111000001101,Cyclophosphamide 35mg/5ml oral suspension (product)
11818211000001107,Cyclophosphamide 40mg/5ml oral solution (product)
11818311000001104,Cyclophosphamide 40mg/5ml oral suspension (product)
11818411000001106,Cyclophosphamide 75mg/5ml oral solution (product)
11818511000001105,Cyclophosphamide 75mg/5ml oral suspension (product)
12068711000001104,Azathioprine 125mg/5ml oral suspension (Special Order) (product)
12069011000001106,Azathioprine 125mg/5ml oral solution (Special Order) (product)
12070311000001107,Azathioprine 175mg/5ml oral suspension (Special Order) (product)
12070911000001108,Azathioprine 175mg/5ml oral solution (Special Order) (product)
12080411000001105,Azathioprine 125mg/5ml oral solution (product)
12080511000001109,Azathioprine 125mg/5ml oral suspension (product)
12080611000001108,Azathioprine 175mg/5ml oral solution (product)
12080711000001104,Azathioprine 175mg/5ml oral suspension (product)
12092411000001105,Azathioprine 17mg/5ml oral suspension (Special Order) (product)
12092711000001104,Azathioprine 17mg/5ml oral solution (Special Order) (product)
12093011000001105,Azathioprine 200mg/5ml oral suspension (Special Order) (product)
12093311000001108,Azathioprine 200mg/5ml oral solution (Special Order) (product)
12093611000001103,Azathioprine 35mg/5ml oral suspension (Special Order) (product)
12093911000001109,Azathioprine 35mg/5ml oral solution (Special Order) (product)
12096811000001108,Azathioprine 17mg/5ml oral solution (product)
12096911000001103,Azathioprine 17mg/5ml oral suspension (product)
12097011000001104,Azathioprine 200mg/5ml oral solution (product)
12097111000001103,Azathioprine 200mg/5ml oral suspension (product)
12097211000001109,Azathioprine 35mg/5ml oral solution (product)
12097311000001101,Azathioprine 35mg/5ml oral suspension (product)
12207711000001108,Atriance 250mg/50ml solution for infusion vials (GlaxoSmithKline) (product)
12209611000001109,Azathioprine 37.5mg/5ml oral suspension (Special Order) (product)
12210411000001104,Azathioprine 37.5mg/5ml oral solution (Special Order) (product)
12211711000001102,Azathioprine 37.5mg/5ml oral solution (product)
12211811000001105,Azathioprine 37.5mg/5ml oral suspension (product)
12211911000001100,Azathioprine 45mg/5ml oral suspension (product)
12212311000001105,Azathioprine 45mg/5ml oral suspension (Special Order) (product)
12212411000001103,Nelarabine 250mg/50ml solution for injection vials (product)
12213811000001109,Azathioprine 4mg/5ml oral suspension (Special Order) (product)
12214511000001109,Azathioprine 70mg/5ml oral suspension (Special Order) (product)
12214811000001107,Azathioprine 7mg/5ml oral suspension (Special Order) (product)
12215111000001101,Azathioprine 80mg/5ml oral suspension (Special Order) (product)
12215411000001106,Azathioprine 45mg/5ml oral solution (Special Order) (product)
12216011000001106,Azathioprine 4mg/5ml oral solution (Special Order) (product)
12217411000001100,Azathioprine 70mg/5ml oral solution (Special Order) (product)
12217811000001103,Azathioprine 7mg/5ml oral solution (Special Order) (product)
12218111000001106,Azathioprine 80mg/5ml oral solution (Special Order) (product)
12221811000001102,Azathioprine 45mg/5ml oral solution (product)
12221911000001107,Azathioprine 4mg/5ml oral solution (product)
12222011000001100,Azathioprine 4mg/5ml oral suspension (product)
12222111000001104,Azathioprine 70mg/5ml oral solution (product)
12222211000001105,Azathioprine 70mg/5ml oral suspension (product)
12222311000001102,Azathioprine 7mg/5ml oral solution (product)
12222411000001109,Azathioprine 7mg/5ml oral suspension (product)
12222511000001108,Azathioprine 80mg/5ml oral solution (product)
12222611000001107,Azathioprine 80mg/5ml oral suspension (product)
12241211000001101,Busulfan 2mg/5ml oral suspension (Special Order) (product)
12241611000001104,Busulfan 2mg/5ml oral solution (Special Order) (product)
12288011000001108,Busulfan 2mg/5ml oral solution (product)
12288111000001109,Busulfan 2mg/5ml oral suspension (product)
12532811000001101,Fludarabine phosphate 50mg/2ml concentrate for solution for injection vials (Teva UK Ltd) (product)
12533411000001107,Oxaliplatin 50mg/10ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
12533611000001105,Oxaliplatin 100mg/20ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
12540011000001107,Fludarabine phosphate 50mg/2ml solution for injection vials (product)
12557211000001100,Temodal 140mg capsules (Schering-Plough Ltd) (product)
12557511000001102,Temodal 180mg capsules (Schering-Plough Ltd) (product)
12564211000001102,Temozolomide 140mg capsules (product)
12564311000001105,Temozolomide 180mg capsules (product)
12566811000001108,Hydroxycarbamide 500mg/5ml oral solution (Special Order) (product)
12623611000001104,Hydroxycarbamide 500mg/5ml oral solution (product)
12695311000001100,Mercaptopurine 50mg/5ml oral suspension (Special Order) (product)
12695511000001106,Mercaptopurine 5mg/5ml oral suspension (Special Order) (product)
12696211000001102,Mercaptopurine 75mg/5ml oral suspension (Special Order) (product)
12701511000001101,Mercaptopurine 50mg/5ml oral suspension (product)
12701611000001102,Mercaptopurine 5mg/5ml oral suspension (product)
12701711000001106,Mercaptopurine 75mg/5ml oral suspension (product)
12779011000001104,Oxaliplatin 50mg/10ml concentrate for solution for infusion vials (Mayne Pharma Plc) (product)
12779211000001109,Oxaliplatin 100mg/20ml concentrate for solution for infusion vials (Mayne Pharma Plc) (product)
12793711000001105,Methotrexate 12mg/5ml oral suspension (Special Order) (product)
12794011000001105,Methotrexate 12mg/5ml oral solution (Special Order) (product)
12794311000001108,Methotrexate 17.5mg/5ml oral suspension (Special Order) (product)
12794611000001103,Methotrexate 17.5mg/5ml oral solution (Special Order) (product)
12795811000001103,Methotrexate 18mg/5ml oral suspension (Special Order) (product)
12796111000001104,Methotrexate 18mg/5ml oral solution (Special Order) (product)
12796411000001109,Methotrexate 1mg/5ml oral suspension (Special Order) (product)
12796711000001103,Methotrexate 1mg/5ml oral solution (Special Order) (product)
12798211000001106,Methotrexate 20mg/5ml oral suspension (Special Order) (product)
12798611000001108,Methotrexate 20mg/5ml oral solution (Special Order) (product)
12799711000001108,Methotrexate 22.5mg/5ml oral suspension (Special Order) (product)
12800111000001102,Methotrexate 22.5mg/5ml oral solution (Special Order) (product)
12800611000001105,Methotrexate 25mg/5ml oral suspension (Special Order) (product)
12800911000001104,Methotrexate 25mg/5ml oral solution (Special Order) (product)
12801211000001102,Methotrexate 3.75mg/5ml oral suspension (Special Order) (product)
12801511000001104,Methotrexate 3.75mg/5ml oral solution (Special Order) (product)
12801911000001106,Methotrexate 4mg/5ml oral suspension (Special Order) (product)
12802211000001109,Methotrexate 4mg/5ml oral solution (Special Order) (product)
12802611000001106,Methotrexate 50mg/5ml oral suspension (Special Order) (product)
12803011000001108,Methotrexate 50mg/5ml oral solution (Special Order) (product)
12803311000001106,Methotrexate 6mg/5ml oral suspension (Special Order) (product)
12803611000001101,Methotrexate 6mg/5ml oral solution (Special Order) (product)
12804011000001105,Methotrexate 750micrograms/5ml oral suspension (Special Order) (product)
12804611000001103,Methotrexate 750micrograms/5ml oral solution (Special Order) (product)
12805111000001105,Methotrexate 7mg/5ml oral suspension (Special Order) (product)
12805711000001106,Methotrexate 7mg/5ml oral solution (Special Order) (product)
12806311000001102,Methotrexate 8mg/5ml oral suspension (Special Order) (product)
12806611000001107,Methotrexate 8mg/5ml oral solution (Special Order) (product)
12813911000001109,Methotrexate 12mg/5ml oral solution (product)
12814011000001107,Methotrexate 12mg/5ml oral suspension (product)
12814111000001108,Methotrexate 17.5mg/5ml oral solution (product)
12814211000001102,Methotrexate 17.5mg/5ml oral suspension (product)
12814311000001105,Methotrexate 18mg/5ml oral solution (product)
12814411000001103,Methotrexate 18mg/5ml oral suspension (product)
12814511000001104,Methotrexate 1mg/5ml oral solution (product)
12814611000001100,Methotrexate 1mg/5ml oral suspension (product)
12814711000001109,Methotrexate 20mg/5ml oral solution (product)
12814811000001101,Methotrexate 20mg/5ml oral suspension (product)
12814911000001106,Methotrexate 22.5mg/5ml oral solution (product)
12815011000001106,Methotrexate 22.5mg/5ml oral suspension (product)
12815111000001107,Methotrexate 50mg/5ml oral suspension (product)
12815211000001101,Methotrexate 6mg/5ml oral solution (product)
12815311000001109,Methotrexate 6mg/5ml oral suspension (product)
12815411000001102,Methotrexate 750micrograms/5ml oral solution (product)
12815511000001103,Methotrexate 750micrograms/5ml oral suspension (product)
12815611000001104,Methotrexate 7mg/5ml oral solution (product)
12815711000001108,Methotrexate 7mg/5ml oral suspension (product)
12815811000001100,Methotrexate 8mg/5ml oral solution (product)
12815911000001105,Methotrexate 8mg/5ml oral suspension (product)
12816911000001103,Methotrexate 25mg/5ml oral solution (product)
12817011000001104,Methotrexate 25mg/5ml oral suspension (product)
12817111000001103,Methotrexate 3.75mg/5ml oral solution (product)
12817211000001109,Methotrexate 3.75mg/5ml oral suspension (product)
12817311000001101,Methotrexate 4mg/5ml oral solution (product)
12817411000001108,Methotrexate 4mg/5ml oral suspension (product)
12817511000001107,Methotrexate 50mg/5ml oral solution (product)
12984311000001102,Mycophenolate mofetil 100mg/5ml oral suspension (Special Order) (product)
12984911000001101,Mycophenolate mofetil 125mg/5ml oral suspension (Special Order) (product)
12986111000001106,Penicillamine 125mg/5ml oral solution (Special Order) (product)
12986311000001108,Mycophenolate mofetil 250mg/5ml oral suspension (Special Order) (product)
12986711000001107,Penicillamine 250mg/5ml oral solution (Special Order) (product)
12987211000001103,Mycophenolate mofetil 300mg/5ml oral suspension (Special Order) (product)
12987611000001101,Penicillamine 50mg/5ml oral solution (Special Order) (product)
12988111000001105,Mycophenolate mofetil 500mg/5ml oral suspension (Special Order) (product)
13000311000001106,Mycophenolate mofetil 100mg/5ml oral suspension (product)
13000411000001104,Mycophenolate mofetil 125mg/5ml oral suspension (product)
13000511000001100,Mycophenolate mofetil 250mg/5ml oral suspension (product)
13000611000001101,Mycophenolate mofetil 300mg/5ml oral suspension (product)
13000711000001105,Mycophenolate mofetil 500mg/5ml oral suspension (product)
13005011000001102,Penicillamine 125mg/5ml oral solution (product)
13005111000001101,Penicillamine 250mg/5ml oral solution (product)
13005211000001107,Penicillamine 50mg/5ml oral solution (product)
13094411000001107,Vectibix 100mg/5ml concentrate for solution for infusion vials (Amgen Ltd) (product)
13098711000001109,Arava 10mg tablets (Dowelhurst Ltd) (product)
13142811000001103,Cisplatin 50mg/50ml concentrate for solution for infusion vials (Wockhardt UK Ltd) (product)
13235611000001105,Penicillamine 125mg tablets (Dowelhurst Ltd) (product)
13236111000001108,Penicillamine 250mg tablets (Dowelhurst Ltd) (product)
13282011000001100,Tacrolimus 2mg/5ml oral suspension (Special Order) (product)
13303311000001101,Tacrolimus 2mg/5ml oral suspension (product)
13369011000001100,Fludarabine phosphate 50mg/2ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
13379511000001102,Doxorubicin 50mg/25ml concentrate for solution for infusion vials (Wockhardt UK Ltd) (product)
13386711000001105,Azathioprine 50mg tablets (Arrow Generics Ltd) (product)
13410511000001106,Paclitaxel 30mg/5ml concentrate for solution for infusion vials (PLIVA Pharma Ltd) (product)
13410711000001101,Paclitaxel 100mg/16.7ml concentrate for solution for infusion vials (PLIVA Pharma Ltd) (product)
13410911000001104,Paclitaxel 300mg/50ml concentrate for solution for infusion vials (PLIVA Pharma Ltd) (product)
13441711000001103,Doxorubicin 10mg/2ml concentrate for solution for infusion vials (Wockhardt UK Ltd) (product)
13453911000001102,Doxorubicin 10mg/2ml solution for injection vials (product)
134619001,Liposomal doxorubicin hydrochloride 2mg/mL infusion concentrate 25mL vial (product)
134622004,Product containing precisely capecitabine 500 milligram/1 each conventional release oral tablet (clinical drug)
134623009,Product containing precisely capecitabine 150 milligram/1 each conventional release oral tablet (clinical drug)
134627005,Product containing precisely tegafur 100 milligram and uracil 224 milligram/1 each conventional release oral capsule (clinical drug)
134633001,Product containing precisely fludarabine phosphate 10 milligram/1 each conventional release oral tablet (clinical drug)
134636009,Product containing precisely topotecan (as topotecan hydrochloride) 1 milligram/1 vial powder for conventional release solution for injection (clinical drug)
134640000,Product containing precisely sirolimus 1 milligram/1 milliliter conventional release oral solution (clinical drug)
13572011000001100,Tacrolimus 500micrograms/5ml oral suspension (Special Order) (product)
13573411000001100,Tacrolimus 500micrograms/5ml oral suspension (product)
13599311000001102,Tasigna 200mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
13610211000001105,Nilotinib 200mg capsules (product)
136411000001105,Methotrexate 10mg tablets (Unichem Plc) (product)
13643911000001102,Oxaliplatin 100mg powder for solution for infusion vials (PLIVA Pharma Ltd) (product)
13645511000001108,Tacrolimus 25mg/5ml oral solution (Special Order) (product)
13645811000001106,Tacrolimus 25mg/5ml oral suspension (Special Order) (product)
13648411000001104,Tacrolimus 25mg/5ml oral solution (product)
13648511000001100,Tacrolimus 25mg/5ml oral suspension (product)
13667811000001109,Tyverb 250mg tablets (GlaxoSmithKline) (product)
13711000001108,Distamine 250mg tablets (Alliance Pharmaceuticals Ltd) (product)
13740711000001100,Azathioprine 25mg tablets (Tillomed Laboratories Ltd) (product)
13740911000001103,Azathioprine 50mg tablets (Tillomed Laboratories Ltd) (product)
13829111000001105,Arava 10mg tablets (Doncaster Pharmaceuticals Ltd) (product)
13829311000001107,Arava 20mg tablets (Doncaster Pharmaceuticals Ltd) (product)
13848011000001102,CellCept 250mg capsules (Doncaster Pharmaceuticals Ltd) (product)
13848211000001107,CellCept 500mg tablets (Doncaster Pharmaceuticals Ltd) (product)
13947611000001101,Prograf 500microgram capsules (Doncaster Pharmaceuticals Ltd) (product)
13947911000001107,Prograf 1mg capsules (Doncaster Pharmaceuticals Ltd) (product)
13955911000001104,Siklos 1000mg tablets (Masters Pharmaceuticals Ltd) (product)
13961411000001100,Busulfan 25mg capsules (product)
13961611000001102,Busulfan 25mg capsules (Special Order) (product)
13967911000001100,Hydroxycarbamide 1g tablets (product)
14051111000001106,Advagraf 1mg modified-release capsules (Sigma Pharmaceuticals Plc) (product)
14051611000001103,Advagraf 5mg modified-release capsules (Sigma Pharmaceuticals Plc) (product)
14194111000001106,Arava 10mg tablets (Sigma Pharmaceuticals Plc) (product)
14195011000001109,Arava 20mg tablets (Sigma Pharmaceuticals Plc) (product)
14225911000001104,Hycamtin 0.25mg capsules (GlaxoSmithKline) (product)
14226211000001102,Hycamtin 1mg capsules (GlaxoSmithKline) (product)
14251711000001102,Imuran 25mg tablets (Sigma Pharmaceuticals Plc) (product)
14343911000001108,Neoral 100mg/ml oral solution (Sigma Pharmaceuticals Plc) (product)
14344711000001108,Neoral 100mg capsules (Sigma Pharmaceuticals Plc) (product)
14345511000001102,Neoral 25mg capsules (Sigma Pharmaceuticals Plc) (product)
14346111000001100,Neoral 50mg capsules (Sigma Pharmaceuticals Plc) (product)
14592711000001107,Hydrea 500mg capsules (Waymade Healthcare Plc) (product)
14602911000001103,Torisel 30mg/1.2ml concentrate for solution for infusion vials and diluent (Wyeth Pharmaceuticals) (product)
14653611000001108,Ridaura Tiltab 3mg tablets (Sigma Pharmaceuticals Plc) (product)
14675711000001100,Alimta 100mg powder for concentrate for solution for infusion vials (Eli Lilly and Company Ltd) (product)
14680811000001106,Pemetrexed 100mg powder for solution for injection vials (product)
14689011000001108,Vectibix 400mg/20ml concentrate for solution for infusion vials (Amgen Ltd) (product)
14696711000001104,Panitumumab 400mg/20ml solution for injection vials (product)
14709211000001105,Methotrexate 2.5mg tablets (PI) (Sigma Pharmaceuticals Plc) (product)
14728411000001109,Prograf 500microgram capsules (Sigma Pharmaceuticals Plc) (product)
14728611000001107,Prograf 1mg capsules (Sigma Pharmaceuticals Plc) (product)
14751111000001108,Epirubicin 10mg/5ml solution for injection vials (medac UK) (product)
14751311000001105,Epirubicin 50mg/25ml solution for injection vials (medac UK) (product)
14751511000001104,Epirubicin 200mg/100ml solution for injection vials (medac UK) (product)
14752011000001104,Oxaliplatin 50mg powder for solution for infusion vials (medac UK) (product)
14752211000001109,Oxaliplatin 100mg powder for solution for infusion vials (medac UK) (product)
14752511000001107,Oxaliplatin 150mg powder for solution for infusion vials (medac UK) (product)
14779511000001101,Oxaliplatin 150mg powder for solution for injection vials (product)
14781911000001101,Fludarabine phosphate 50mg powder for solution for injection vials (Actavis UK Ltd) (product)
14788211000001101,Epirubicin 10mg powder for solution for injection vials (Actavis UK Ltd) (product)
14788411000001102,Epirubicin 50mg powder for solution for injection vials (Actavis UK Ltd) (product)
14788611000001104,Oxaliplatin 50mg powder for solution for infusion vials (Actavis UK Ltd) (product)
14946711000001105,Methotrexate 2.5mg tablets (PI) (Waymade Healthcare Plc) (product)
14953811000001108,Abraxane 100mg powder for suspension for infusion vials (Abraxis Bioscience Ltd) (product)
14962511000001107,Methotrexate 2.5mg tablets (Orion Pharma (UK) Ltd) (product)
14963911000001107,Methotrexate 10mg tablets (Orion Pharma (UK) Ltd) (product)
14966311000001102,Doxorubicin 200mg/100ml solution for infusion vials (hameln pharma Ltd) (product)
14966611000001107,Methotrexate 25mg/3ml solution for injection pre-filled syringes (Special Order) (product)
14966811000001106,Methotrexate 500mg/20ml solution for injection vials (hameln pharma Ltd) (product)
14967011000001102,Epirubicin 10mg/5ml solution for injection vials (hameln pharma Ltd) (product)
14967911000001103,Methotrexate 25mg/3ml solution for injection pre-filled syringes (product)
15029311000001100,Vincristine 1mg/1ml solution for injection vials (Teva UK Ltd) (product)
15030011000001109,Vincristine 2mg/2ml solution for injection vials (Teva UK Ltd) (product)
15070411000001103,Azathioprine 25mg tablets (Sigma Pharmaceuticals Plc) (product)
15070611000001100,Azathioprine 50mg tablets (Sigma Pharmaceuticals Plc) (product)
15109411000001107,Methotrexate 10mg tablets (Sigma Pharmaceuticals Plc) (product)
15115911000001104,Oxaliplatin 100mg powder for solution for infusion vials (Actavis UK Ltd) (product)
15116111000001108,Vinorelbine 50mg/5ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
15116311000001105,Vinorelbine 10mg/1ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
15117011000001105,Stelara 45mg/0.5ml solution for injection vials (Janssen-Cilag Ltd) (product)
15125511000001103,Ustekinumab 45mg/0.5ml solution for injection vials (product)
15138411000001109,Methotrexate 50mg/2ml solution for injection vials (hameln pharma Ltd) (product)
15148411000001105,Epirubicin 50mg/25ml solution for injection vials (hameln pharma Ltd) (product)
15158011000001104,Epirubicin 10mg/5ml concentrate for solution for injection vials (Wockhardt UK Ltd) (product)
15158211000001109,Epirubicin 50mg/25ml concentrate for solution for injection vials (Wockhardt UK Ltd) (product)
15158411000001108,Fludarabine phosphate 50mg/2ml concentrate for solution for injection vials (Wockhardt UK Ltd) (product)
15161011000001101,Oxaliplatin 50mg powder for solution for infusion vials (Wockhardt UK Ltd) (product)
15161211000001106,Oxaliplatin 100mg powder for solution for infusion vials (Wockhardt UK Ltd) (product)
15165511000001107,Epirubicin 200mg/100ml concentrate for solution for infusion vials (Wockhardt UK Ltd) (product)
15165711000001102,Epirubicin 100mg/50ml concentrate for solution for infusion vials (Wockhardt UK Ltd) (product)
15167211000001101,Paclitaxel 30mg/5ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
15167411000001102,Paclitaxel 100mg/16.7ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
15167611000001104,Paclitaxel 150mg/25ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
15167811000001100,Paclitaxel 300mg/5ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
15236711000001104,Vidaza 100mg powder for suspension for injection vials (Celgene Ltd) (product)
15242511000001109,Azacitidine 100mg powder for suspension for injection vials (product)
15377711000001109,Gemcitabine 200mg powder for solution for infusion vials (Teva UK Ltd) (product)
15377911000001106,Gemcitabine 1g powder for solution for infusion vials (Teva UK Ltd) (product)
15406411000001101,Sprycel 100mg tablets (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
15410411000001101,Dasatinib 100mg tablets (product)
15472211000001106,Gemcitabine 200mg powder for solution for infusion vials (Sun Pharmaceuticals UK Ltd) (product)
15472411000001105,Gemcitabine 1g powder for solution for infusion vials (Sun Pharmaceuticals UK Ltd) (product)
15513111000001105,Metoject 7.5mg/0.15ml solution for injection pre-filled syringes (medac UK) (product)
15513411000001100,Metoject 10mg/0.2ml solution for injection pre-filled syringes (medac UK) (product)
15513711000001106,Metoject 15mg/0.3ml solution for injection pre-filled syringes (medac UK) (product)
15514011000001106,Metoject 25mg/0.5ml solution for injection pre-filled syringes (medac UK) (product)
15514311000001109,Metoject 20mg/0.4ml solution for injection pre-filled syringes (medac UK) (product)
15516411000001105,Gemcitabine 200mg powder for solution for infusion vials (Actavis UK Ltd) (product)
15516611000001108,Gemcitabine 1g powder for solution for infusion vials (Actavis UK Ltd) (product)
15516911000001102,Navelbine 80mg capsules (Pierre Fabre Ltd) (product)
15517911000001104,Methotrexate 10mg/0.2ml solution for injection pre-filled syringes (product)
15518011000001102,Methotrexate 15mg/0.3ml solution for injection pre-filled syringes (product)
15518111000001101,Methotrexate 20mg/0.4ml solution for injection pre-filled syringes (product)
15518211000001107,Methotrexate 25mg/0.5ml solution for injection pre-filled syringes (product)
15518311000001104,Methotrexate 7.5mg/0.15ml solution for injection pre-filled syringes (product)
15518611000001109,Vinorelbine 80mg capsules (product)
15546011000001108,Campto 300mg/15ml concentrate for solution for infusion vials (Pfizer Ltd) (product)
15548111000001108,Yondelis 0.25mg powder for concentrate for solution for infusion vials (Immedica Pharma AB) (product)
15548411000001103,Yondelis 1mg powder for concentrate for solution for infusion vials (Immedica Pharma AB) (product)
15568011000001101,Irinotecan 300mg/15ml solution for infusion vials (product)
15568211000001106,Trabectedin 1mg powder for solution for infusion vials (product)
15568311000001103,Trabectedin 250microgram powder for solution for infusion vials (product)
15597911000001100,Epirubicin 50mg/25ml solution for injection vials (Teva UK Ltd) (product)
15598111000001102,Epirubicin 10mg/5ml solution for injection vials (Teva UK Ltd) (product)
15603811000001106,Advagraf 3mg modified-release capsules (Astellas Pharma Ltd) (product)
15614511000001109,Tacrolimus 3mg modified-release capsules (product)
15861111000001107,Irinotecan 40mg/2ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
15861311000001109,Irinotecan 100mg/5ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
15867011000001101,Cyclophosphamide 25mg tablets (Special Order) (product)
15870711000001105,Hydroxycarbamide 300mg capsules (Special Order) (product)
15874011000001101,Lomustine 100mg capsules (Special Order) (product)
15874311000001103,Lomustine 10mg capsules (Special Order) (product)
15874611000001108,Trabectedin 250microgram powder for solution for infusion vials (Special Order) (product)
15875311000001104,Trabectedin 1mg powder for solution for infusion vials (Special Order) (product)
15884111000001108,Puri-Nethol 50mg tablets (Waymade Healthcare Plc) (product)
15926411000001109,Irinotecan 40mg/2ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
15926611000001107,Irinotecan 100mg/5ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
15933911000001109,Gemcitabine 200mg powder for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
15934111000001108,Gemcitabine 1g powder for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
15978511000001108,Iressa 250mg tablets (AstraZeneca UK Ltd) (product)
15980311000001108,Enbrel 50mg/1ml solution for injection pre-filled MyClic pens (Pfizer Ltd) (product)
15987111000001107,Etanercept 50mg/1ml solution for injection 1ml pre-filled disposable devices (product)
16012511000001109,Azathioprine 250mg/5ml oral solution (Special Order) (product)
16014711000001109,Azathioprine 250mg/5ml oral suspension (Special Order) (product)
16035911000001102,Azathioprine 250mg/5ml oral solution (product)
16036011000001105,Azathioprine 250mg/5ml oral suspension (product)
16055511000001105,Afinitor 5mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
16056111000001107,Afinitor 10mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
16074111000001102,Everolimus 10mg tablets (product)
16074211000001108,Everolimus 5mg tablets (product)
16099111000001105,RoActemra 200mg/10ml concentrate for solution for infusion vials (Roche Products Ltd) (product)
16099411000001100,RoActemra 80mg/4ml concentrate for solution for infusion vials (Roche Products Ltd) (product)
16099711000001106,RoActemra 400mg/20ml concentrate for solution for infusion vials (Roche Products Ltd) (product)
16100511000001101,Oxaliplatin 100mg powder for solution for infusion vials (Generics (UK) Ltd) (product)
16100711000001106,Oxaliplatin 50mg powder for solution for infusion vials (Generics (UK) Ltd) (product)
16101911000001101,Tocilizumab 200mg/10ml solution for infusion vials (product)
16102011000001108,Tocilizumab 400mg/20ml solution for infusion vials (product)
16102111000001109,Tocilizumab 80mg/4ml solution for infusion vials (product)
16135911000001105,Advagraf 1mg modified-release capsules (Lexon (UK) Ltd) (product)
16198211000001103,Leukeran 2mg tablets (Lexon (UK) Ltd) (product)
16231611000001104,Puri-Nethol 50mg tablets (Lexon (UK) Ltd) (product)
16233811000001101,Ridaura Tiltab 3mg tablets (Lexon (UK) Ltd) (product)
16264311000001100,Arava 20mg tablets (Mawdsley-Brooks & Company Ltd) (product)
16306511000001107,Deximune 25mg capsules (Dexcel-Pharma Ltd) (product)
16306711000001102,Deximune 50mg capsules (Dexcel-Pharma Ltd) (product)
16306911000001100,Deximune 100mg capsules (Dexcel-Pharma Ltd) (product)
16444011000001109,Irinotecan 40mg/2ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
16444211000001104,Irinotecan 100mg/5ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
16445311000001106,Epirubicin 10mg/5ml solution for injection vials (Actavis UK Ltd) (product)
16445511000001100,Epirubicin 50mg/25ml solution for injection vials (Actavis UK Ltd) (product)
16445711000001105,Epirubicin 100mg/50ml solution for infusion vials (Actavis UK Ltd) (product)
16446711000001102,Irinotecan 500mg/25ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
16459511000001100,CellCept 250mg capsules (Mawdsley-Brooks & Company Ltd) (product)
16459711000001105,CellCept 500mg tablets (Mawdsley-Brooks & Company Ltd) (product)
16460411000001100,Irinotecan 500mg/25ml solution for infusion vials (product)
16547711000001106,Imuran 25mg tablets (Stephar (U.K.) Ltd) (product)
16550511000001102,Ciclosporin 25mg capsules (A A H Pharmaceuticals Ltd) (product)
16550711000001107,Ciclosporin 50mg capsules (A A H Pharmaceuticals Ltd) (product)
16550911000001109,Ciclosporin 100mg capsules (A A H Pharmaceuticals Ltd) (product)
16561911000001109,Neoral 25mg capsules (Mawdsley-Brooks & Company Ltd) (product)
16562311000001104,Neoral 50mg capsules (Mawdsley-Brooks & Company Ltd) (product)
16562711000001100,Neoral 100mg capsules (Mawdsley-Brooks & Company Ltd) (product)
16591411000001103,Ilaris 150mg powder for solution for injection vials (Novartis Pharmaceuticals UK Ltd) (product)
16592911000001100,Canakinumab 150mg powder for solution for injection vials (product)
16658211000001106,Tacrolimus 200microgram granules sachets (product)
16658411000001105,Modigraf 0.2mg granules sachets (Astellas Pharma Ltd) (product)
16658611000001108,Tacrolimus 1mg granules sachets (product)
16658811000001107,Modigraf 1mg granules sachets (Astellas Pharma Ltd) (product)
16667211000001103,Epirubicin 200mg/100ml solution for infusion vials (Generics (UK) Ltd) (product)
16667411000001104,Epirubicin 50mg/25ml solution for injection vials (Generics (UK) Ltd) (product)
16668111000001105,Epirubicin 10mg/5ml solution for injection vials (Generics (UK) Ltd) (product)
16697811000001100,Vinflunine 250mg/10ml solution for infusion vials (product)
16698011000001107,Javlor 250 mg/10ml concentrate for solution for infusion (Pierre Fabre Ltd) (product)
16698211000001102,Vinflunine 50mg/2ml solution for infusion vials (product)
16698411000001103,Javlor 50 mg/2ml concentrate for solution for infusion (Pierre Fabre Ltd) (product)
16731811000001107,Irinotecan 500mg/25ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
167911000001107,Methotrexate 2.5mg tablets (Kent Pharmaceuticals Ltd) (product)
170511000001109,Fluorouracil 500mg/20ml solution for injection vials (Mayne Pharma Plc) (product)
17053711000001102,Cyclophosphamide 50mg tablets (Baxter Healthcare Ltd) (product)
17053911000001100,Cyclophosphamide 500mg powder for solution for injection vials (Baxter Healthcare Ltd) (product)
17054111000001101,Cyclophosphamide 1g powder for solution for injection vials (Baxter Healthcare Ltd) (product)
17063511000001102,Temozolomide 250mg capsules (Hospira UK Ltd) (product)
17063911000001109,Temozolomide 100mg capsules (Hospira UK Ltd) (product)
17064711000001109,Temozolomide 20mg capsules (Hospira UK Ltd) (product)
17065111000001107,Temozolomide 5mg capsules (Hospira UK Ltd) (product)
17169211000001106,Temozolomide 5mg capsules (Teva UK Ltd) (product)
17169411000001105,Temozolomide 20mg capsules (Teva UK Ltd) (product)
17169611000001108,Temozolomide 100mg capsules (Teva UK Ltd) (product)
17169811000001107,Temozolomide 140mg capsules (Teva UK Ltd) (product)
17170011000001103,Temozolomide 180mg capsules (Teva UK Ltd) (product)
17170211000001108,Temozolomide 250mg capsules (Teva UK Ltd) (product)
17190711000001109,Ofatumumab 100mg/5ml solution for infusion vials (product)
17191011000001103,Arzerra 100mg/5ml concentrate for solution for infusion vials (GlaxoSmithKline UK Ltd) (product)
17220211000001106,Ifosfamide 1g powder for concentrate for solution for injection vials (Baxter Healthcare Ltd) (product)
17220411000001105,Ifosfamide 2g powder for concentrate for solution for injection vials (Baxter Healthcare Ltd) (product)
172611000001109,Sandimmun 100mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
17291511000001108,Temozolomide 5mg capsules (A A H Pharmaceuticals Ltd) (product)
17291711000001103,Temozolomide 20mg capsules (A A H Pharmaceuticals Ltd) (product)
17291911000001101,Temozolomide 100mg capsules (A A H Pharmaceuticals Ltd) (product)
17292111000001109,Temozolomide 140mg capsules (A A H Pharmaceuticals Ltd) (product)
17292311000001106,Temozolomide 180mg capsules (A A H Pharmaceuticals Ltd) (product)
17292511000001100,Temozolomide 250mg capsules (A A H Pharmaceuticals Ltd) (product)
17315811000001100,Certolizumab pegol 200mg/1ml solution for injection pre-filled syringes (product)
17316011000001102,Cimzia 200mg/1ml solution for injection pre-filled syringes (UCB Pharma Ltd) (product)
17400011000001106,Temozolomide 140mg capsules (Hospira UK Ltd) (product)
17401211000001107,Temozolomide 180mg capsules (Hospira UK Ltd) (product)
17421711000001106,Prograf 500microgram capsules (Mawdsley-Brooks & Company Ltd) (product)
17422111000001100,Prograf 1mg capsules (Mawdsley-Brooks & Company Ltd) (product)
17422311000001103,Prograf 5mg capsules (Mawdsley-Brooks & Company Ltd) (product)
17426211000001107,Puri-Nethol 50mg tablets (Mawdsley-Brooks & Company Ltd) (product)
17430511000001105,Taxotere 20mg/1ml concentrate for solution for infusion vials (sanofi-aventis) (product)
17430811000001108,Taxotere 80mg/4ml concentrate for solution for infusion vials (sanofi-aventis) (product)
17431011000001106,Docetaxel 20mg/1ml solution for infusion vials (product)
17431111000001107,Docetaxel 80mg/4ml solution for infusion vials (product)
17462011000001109,Votrient 400mg tablets (GlaxoSmithKline UK Ltd) (product)
17462311000001107,Votrient 200mg tablets (GlaxoSmithKline UK Ltd) (product)
17462711000001106,Stelara 45mg/0.5ml solution for injection pre-filled syringes (Janssen-Cilag Ltd) (product)
17484011000001100,Ustekinumab 45mg/0.5ml solution for injection pre-filled syringes (product)
17489311000001101,Advagraf 1mg modified-release capsules (Mawdsley-Brooks & Company Ltd) (product)
17489511000001107,Advagraf 0.5mg modified-release capsules (Mawdsley-Brooks & Company Ltd) (product)
17520311000001105,Irinotecan 100mg/5ml concentrate for solution for infusion vials (Generics (UK) Ltd) (product)
17520511000001104,Irinotecan 40mg/2ml concentrate for solution for infusion vials (Generics (UK) Ltd) (product)
17523211000001107,Irinotecan 40mg/2ml concentrate for solution for infusion vials (medac UK) (product)
17523311000001104,Irinotecan 100mg/5ml concentrate for solution for infusion vials (medac UK) (product)
17523411000001106,Irinotecan 300mg/15ml concentrate for solution for infusion vials (medac UK) (product)
17558111000001109,Doxorubicin 200mg/100ml solution for injection Cytosafe vials (Pfizer Ltd) (product)
17577911000001108,Advagraf 1mg modified-release capsules (Necessity Supplies Ltd) (product)
17578611000001103,Advagraf 5mg modified-release capsules (Necessity Supplies Ltd) (product)
17586811000001108,Arava 10mg tablets (Necessity Supplies Ltd) (product)
17587211000001109,Arava 20mg tablets (Necessity Supplies Ltd) (product)
17589811000001102,Puri-Nethol 50mg tablets (Sigma Pharmaceuticals Plc) (product)
17593711000001106,Neoral 50mg capsules (Necessity Supplies Ltd) (product)
17594411000001102,Neoral 100mg/ml oral solution (Necessity Supplies Ltd) (product)
17624911000001109,Prograf 500microgram capsules (Necessity Supplies Ltd) (product)
17625111000001105,Prograf 1mg capsules (Necessity Supplies Ltd) (product)
17648911000001100,Paclitaxel 30mg/5ml concentrate for solution for infusion vials (medac UK) (product)
17649111000001105,Paclitaxel 100mg/16.7ml concentrate for solution for infusion vials (medac UK) (product)
17649311000001107,Paclitaxel 300mg/50ml concentrate for solution for infusion vials (medac UK) (product)
17649711000001106,Gemcitabine 1g powder for solution for infusion vials (medac UK) (product)
17649911000001108,Gemcitabine 200mg powder for solution for infusion vials (medac UK) (product)
17650211000001109,Gemcitabine 1.5g powder for solution for infusion vials (medac UK) (product)
17652111000001104,Gemcitabine 1.5g powder for solution for infusion vials (product)
17652411000001109,Temomedac 5mg capsules (medac UK) (product)
17652811000001106,Temomedac 20mg capsules (medac UK) (product)
17653011000001109,Temomedac 100mg capsules (medac UK) (product)
17653211000001104,Temomedac 140mg capsules (medac UK) (product)
17653411000001100,Temomedac 180mg capsules (medac UK) (product)
17653611000001102,Temomedac 250mg capsules (medac UK) (product)
17665211000001107,Gemcitabine 1g powder for solution for infusion vials (Generics (UK) Ltd) (product)
17665411000001106,Gemcitabine 200mg powder for solution for infusion vials (Generics (UK) Ltd) (product)
17665611000001109,Capimune 50mg capsules (Generics (UK) Ltd) (product)
17665811000001108,Capimune 100mg capsules (Generics (UK) Ltd) (product)
17666911000001105,Capimune 25mg capsules (Generics (UK) Ltd) (product)
17789111000001105,Azathioprine 25mg tablets (Phoenix Healthcare Distribution Ltd) (product)
17790011000001100,Azathioprine 50mg tablets (Phoenix Healthcare Distribution Ltd) (product)
17828911000001107,Gemcitabine 2g powder for solution for infusion vials (Actavis UK Ltd) (product)
17844811000001107,Gemcitabine 2g powder for solution for infusion vials (product)
17845911000001103,Irinotecan 40mg/2ml concentrate for solution for infusion vials (Hospira UK Ltd) (product)
17846111000001107,Irinotecan 100mg/5ml concentrate for solution for infusion vials (Hospira UK Ltd) (product)
17846311000001109,Irinotecan 500mg/25ml concentrate for solution for infusion vials (Hospira UK Ltd) (product)
17846511000001103,Gemcitabine 200mg powder for solution for infusion vials (Hospira UK Ltd) (product)
17846711000001108,Gemcitabine 1g powder for solution for infusion vials (Hospira UK Ltd) (product)
17846911000001105,Gemcitabine 2g powder for solution for infusion vials (Hospira UK Ltd) (product)
17847211000001104,Fludarabine phosphate 50mg powder for solution for injection vials (Hospira UK Ltd) (product)
178511000001107,Azathioprine 50mg tablets (IVAX Pharmaceuticals UK Ltd) (product)
17856611000001101,Ciclosporin 25mg capsules (Phoenix Healthcare Distribution Ltd) (product)
17856811000001102,Ciclosporin 50mg capsules (Phoenix Healthcare Distribution Ltd) (product)
17857011000001106,Ciclosporin 100mg capsules (Phoenix Healthcare Distribution Ltd) (product)
17871411000001107,Bendamustine 25mg powder for solution for infusion vials (product)
17871511000001106,Levact 25mg powder for concentrate for solution for infusion vials (Napp Pharmaceuticals Ltd) (product)
17872411000001102,Bendamustine 100mg powder for solution for infusion vials (product)
17872511000001103,Levact 100mg powder for concentrate for solution for infusion vials (Napp Pharmaceuticals Ltd) (product)
17880111000001103,Epirubicin 50mg/25ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
17930811000001105,Hydroxycarbamide 500mg capsules (Phoenix Healthcare Distribution Ltd) (product)
17953911000001107,Penicillamine 125mg tablets (Phoenix Healthcare Distribution Ltd) (product)
17954111000001106,Penicillamine 250mg tablets (Phoenix Healthcare Distribution Ltd) (product)
18032111000001103,Cyclophosphamide 1g powder for solution for injection vials (Alliance Healthcare (Distribution) Ltd) (product)
18035511000001101,Simponi 50mg/0.5ml solution for injection pre-filled syringes (Schering-Plough Ltd) (product)
18035811000001103,Simponi 50mg/0.5ml solution for injection pre-filled pens (Merck Sharp & Dohme Ltd) (product)
18038011000001101,Golimumab 50mg/0.5ml solution for injection pre-filled disposable devices (product)
18038111000001100,Golimumab 50mg/0.5ml solution for injection pre-filled syringes (product)
18044211000001101,Adoport 5mg capsules (Sandoz Ltd) (product)
18044411000001102,Adoport 1mg capsules (Sandoz Ltd) (product)
18044811000001100,Adoport 0.5mg capsules (Sandoz Ltd) (product)
18065711000001103,Prograf 1mg capsules (Lexon (UK) Ltd) (product)
18159111000001102,Arava 10mg tablets (Mawdsley-Brooks & Company Ltd) (product)
18163911000001106,Myfenax 500mg tablets (Teva UK Ltd) (product)
18164111000001105,Myfenax 250mg capsules (Teva UK Ltd) (product)
18164311000001107,Mycophenolate mofetil 250mg capsules (Actavis UK Ltd) (product)
18164511000001101,Mycophenolate Mofetil 500mg tablets (Actavis UK Ltd) (product)
18166711000001102,Arzip 500mg tablets (Winthrop Pharmaceuticals UK Ltd) (product)
18166911000001100,Arzip 250mg capsules (Winthrop Pharmaceuticals UK Ltd) (product)
18172711000001109,Leflunomide 10mg tablets (medac UK) (product)
18172911000001106,Leflunomide 20mg tablets (medac UK) (product)
18179211000001105,Puri-Nethol 50mg tablets (Necessity Supplies Ltd) (product)
18189211000001103,Hydrea 500mg capsules (Mawdsley-Brooks & Company Ltd) (product)
18190611000001106,Glivec 100mg tablets (Mawdsley-Brooks & Company Ltd) (product)
18208411000001106,Metoject 30mg/0.6ml solution for injection pre-filled syringes (medac UK) (product)
18245711000001104,Methotrexate 30mg/0.6ml solution for injection pre-filled syringes (product)
18275811000001106,Gemcitabine 2g powder for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18280311000001100,Azathioprine 50mg tablets (Co-Pharma Ltd) (product)
18298811000001106,Docetaxel 20mg/1ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
18300111000001109,Docetaxel 80mg/4ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
18300411000001104,Docetaxel 140mg/7ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
18300811000001102,Docetaxel 140mg/7ml solution for infusion vials (product)
18304811000001107,Docetaxel 20mg/2ml concentrate for solution for infusion vials (Hospira UK Ltd) (product)
18305511000001105,Docetaxel 80mg/8ml concentrate for solution for infusion vials (Hospira UK Ltd) (product)
18305811000001108,Docetaxel 160mg/16ml concentrate for solution for infusion vials (Hospira UK Ltd) (product)
18305911000001103,Docetaxel 160mg/16ml solution for infusion vials (product)
18306011000001106,Docetaxel 20mg/2ml solution for infusion vials (product)
18306111000001107,Docetaxel 80mg/8ml solution for infusion vials (product)
18309311000001102,Taxotere 160mg/8ml concentrate for solution for infusion vials (sanofi-aventis) (product)
18310411000001102,Mycophenolate mofetil 250mg capsules (A A H Pharmaceuticals Ltd) (product)
18310611000001104,Mycophenolate mofetil 500mg tablets (A A H Pharmaceuticals Ltd) (product)
18342011000001101,Leflunomide 10mg tablets (Alliance Healthcare (Distribution) Ltd) (product)
18342211000001106,Leflunomide 20mg tablets (Alliance Healthcare (Distribution) Ltd) (product)
18342411000001105,Mycophenolate mofetil 250mg capsules (Alliance Healthcare (Distribution) Ltd) (product)
18342611000001108,Mycophenolate mofetil 500mg tablets (Alliance Healthcare (Distribution) Ltd) (product)
18347511000001107,Docetaxel 160mg/8ml solution for infusion vials (product)
18401611000001102,Rapamune 0.5mg tablets (Pfizer Ltd) (product)
18412111000001102,Mycophenolate mofetil 500mg tablets (Generics (UK) Ltd) (product)
18413011000001107,Mercaptopurine 10mg tablets (Special Order) (product)
18430611000001102,Mercaptopurine 10mg tablets (product)
18430811000001103,Sirolimus 500microgram tablets (product)
18431311000001102,Sprycel 140mg tablets (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
18431611000001107,Sprycel 80mg tablets (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
18446611000001104,Hydroxycarbamide 500mg capsules (Alliance Healthcare (Distribution) Ltd) (product)
18448611000001103,Tasigna 150mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
18464211000001103,Mycophenolate mofetil 250mg capsules (Accord Healthcare Ltd) (product)
18464411000001104,Mycophenolate mofetil 500mg tablets (Accord Healthcare Ltd) (product)
18468211000001109,Nilotinib 150mg capsules (product)
18470311000001105,Dasatinib 140mg tablets (product)
18470411000001103,Dasatinib 80mg tablets (product)
18477511000001100,Mycophenolate mofetil 500mg tablets (Dr Reddy's Laboratories (UK) Ltd) (product)
18477711000001105,Mycophenolate mofetil 250mg capsules (Dr Reddy's Laboratories (UK) Ltd) (product)
18497511000001105,Azathioprine 50mg tablets (Almus Pharmaceuticals Ltd) (product)
18499611000001104,Fluorouracil 2.5g/100ml solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18530911000001102,Taxceus 20mg/1ml concentrate for solution for infusion vials (medac UK) (product)
18531911000001109,Taxceus 80mg/4ml concentrate for solution for infusion vials (medac UK) (product)
18533211000001101,Taxceus 140mg/7ml concentrate for solution for infusion vials (medac UK) (product)
18542411000001107,Docetaxel 20mg/1ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18542611000001105,Docetaxel 20mg/2ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18542811000001109,Docetaxel 80mg/4ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18543011000001107,Docetaxel 80mg/8ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18543611000001100,Docetaxel 140mg/7ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18543811000001101,Irinotecan 300mg/15ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18590011000001107,Gemcitabine 200mg concentrate for solution for infusion vials (Hospira UK Ltd) (product)
18590911000001106,Gemcitabine 1g concentrate for solution for infusion vials (Hospira UK Ltd) (product)
18591211000001108,Gemcitabine 2g concentrate for solution for infusion vials (Hospira UK Ltd) (product)
18594811000001106,Gemcitabine 1g solution for infusion vials (product)
18594911000001101,Gemcitabine 200mg solution for infusion vials (product)
18595011000001101,Gemcitabine 2g solution for infusion vials (product)
18603011000001107,Neoral 100mg capsules (Doncaster Pharmaceuticals Ltd) (product)
18607911000001102,Puri-Nethol 50mg tablets (Doncaster Pharmaceuticals Ltd) (product)
18617711000001101,Vivadex 1mg capsules (Dexcel-Pharma Ltd) (product)
18618011000001102,Vivadex 0.5mg capsules (Dexcel-Pharma Ltd) (product)
18618211000001107,Vivadex 5mg capsules (Dexcel-Pharma Ltd) (product)
18622711000001109,Mycophenolate mofetil 250mg capsules (Phoenix Healthcare Distribution Ltd) (product)
18622911000001106,Mycophenolate mofetil 500mg tablets (Phoenix Healthcare Distribution Ltd) (product)
18643411000001109,Tacrolimus 500microgram capsules (A A H Pharmaceuticals Ltd) (product)
18643711000001103,Tacrolimus 1mg capsules (A A H Pharmaceuticals Ltd) (product)
18644711000001101,Tacrolimus 5mg capsules (A A H Pharmaceuticals Ltd) (product)
18677311000001108,Tioguanine 10mg capsules (Special Order) (product)
18684611000001101,Tioguanine 10mg capsules (product)
18728911000001102,Mycophenolate mofetil 250mg capsules (Sigma Pharmaceuticals Plc) (product)
18730111000001104,Mycophenolate mofetil 500mg tablets (Sigma Pharmaceuticals Plc) (product)
18741011000001105,Gilenya 0.5mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
18744111000001109,Epirubicin 200mg/100ml solution for infusion vials (Teva UK Ltd) (product)
18748011000001104,Fingolimod 500microgram capsules (product)
18754511000001103,Carboplatin 50mg/5ml solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18754711000001108,Carboplatin 150mg/15ml solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18754911000001105,Carboplatin 450mg/45ml solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18755311000001108,Carboplatin 600mg/60ml solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18756811000001107,Leflunomide 10mg tablets (A A H Pharmaceuticals Ltd) (product)
18757211000001108,Leflunomide 20mg tablets (A A H Pharmaceuticals Ltd) (product)
18758511000001105,Cyclophosphamide 1g powder for solution for injection vials (A A H Pharmaceuticals Ltd) (product)
18758711000001100,Daunorubicin 20mg powder for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18772311000001100,Halaven 0.88mg/2ml solution for injection vials (Eisai Ltd) (product)
18781111000001100,Eribulin 880micrograms/2ml solution for injection vials (product)
18810411000001100,Leflunomide 10mg tablets (Teva UK Ltd) (product)
18812611000001101,Leflunomide 20mg tablets (Teva UK Ltd) (product)
18870811000001105,Docetaxel 160mg/16ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18871511000001100,Doxorubicin 10mg/5ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
18872211000001105,Doxorubicin 200mg/100ml solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18872811000001106,Doxorubicin 50mg/25ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
18873311000001107,Epirubicin 100mg/50ml solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18873811000001103,Epirubicin 10mg/5ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
18874311000001109,Epirubicin 200mg/100ml solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18875011000001105,Etoposide 100mg/5ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18875311000001108,Etoposide 500mg/25ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
18876211000001106,Fludarabine phosphate 50mg powder for solution for injection vials (A A H Pharmaceuticals Ltd) (product)
191111000001100,Methotrexate 10mg tablets (Mayne Pharma Plc) (product)
19177811000001101,Cabazitaxel 60mg/1.5ml solution for infusion vials (product)
19177911000001106,JEVTANA 60mg/1.5ml concentrate and solvent for solution for infusion vials (Sanofi) (product)
19224611000001108,Metoject 12.5mg/0.25ml solution for injection pre-filled syringes (medac UK) (product)
19225111000001101,Metoject 17.5mg/0.35ml solution for injection pre-filled syringes (medac UK) (product)
19225411000001106,Metoject 22.5mg/0.45ml solution for injection pre-filled syringes (medac UK) (product)
19225811000001108,Metoject 27.5mg/0.55ml solution for injection pre-filled syringes (medac UK) (product)
19231311000001104,Methotrexate 12.5mg/0.25ml solution for injection pre-filled syringes (product)
19231411000001106,Methotrexate 17.5mg/0.35ml solution for injection pre-filled syringes (product)
19231511000001105,Methotrexate 22.5mg/0.45ml solution for injection pre-filled syringes (product)
19231611000001109,Methotrexate 27.5mg/0.55ml solution for injection pre-filled syringes (product)
19265711000001106,Ofatumumab 1g/50ml solution for infusion vials (product)
19265811000001103,Arzerra 1000mg/50ml concentrate for solution for infusion vials (GlaxoSmithKline UK Ltd) (product)
19293811000001104,Tacni 0.5mg capsules (Teva UK Ltd) (product)
19294011000001107,Tacni 1mg capsules (Teva UK Ltd) (product)
19294211000001102,Tacni 5mg capsules (Teva UK Ltd) (product)
19311511000001108,Thiotepa 15mg powder for solution for infusion vials (product)
19311711000001103,Tepadina 15mg powder for concentrate for solution for infusion vials (Adienne S.r.l.) (product)
19311911000001101,Thiotepa 100mg powder for solution for infusion vials (product)
19312111000001109,Tepadina 100mg powder for concentrate for solution for infusion vials (Adienne S.r.l.) (product)
19313611000001106,Siklos 100mg tablets (Masters Pharmaceuticals Ltd) (product)
19345811000001103,Hydroxycarbamide 100mg tablets (product)
19353311000001109,Carboplatin 150mg/15ml concentrate for solution for infusion vials (Sun Pharmaceuticals UK Ltd) (product)
19353511000001103,Carboplatin 450mg/45ml concentrate for solution for infusion vials (Sun Pharmaceuticals UK Ltd) (product)
19353711000001108,Carboplatin 50mg/5ml concentrate for solution for infusion vials (Sun Pharmaceuticals UK Ltd) (product)
19353911000001105,Carboplatin 600mg/60ml concentrate for solution for infusion vials (Sun Pharmaceuticals UK Ltd) (product)
19376911000001102,Capsorin 100mg capsules (Morningside Healthcare Ltd) (product)
19377111000001102,Capsorin 50mg capsules (Morningside Healthcare Ltd) (product)
19377311000001100,Capsorin 25mg capsules (Morningside Healthcare Ltd) (product)
19381511000001106,Yervoy 50mg/10ml concentrate for solution for infusion vials (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
19382711000001108,Yervoy 200mg/40ml concentrate for solution for infusion vials (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
19429811000001107,Mycophenolate motefil 500mg tablets (Wockhardt UK Ltd) (product)
19431511000001106,Amsacrine 75mg/1.5ml solution for infusion ampoules and diluent (product)
19448511000001100,Ipilimumab 200mg/40ml solution for infusion vials (product)
19448611000001101,Ipilimumab 50mg/10ml solution for infusion vials (product)
19463411000001100,Nulojix 250mg powder for concentrate for solution for infusion vials (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
19464711000001108,Belatacept 250mg powder for solution for infusion vials (product)
19473111000001104,Oxaliplatin 50mg/10ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
19473311000001102,Oxaliplatin 100mg/20ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
19480311000001104,Benlysta 400mg powder for concentrate for solution for infusion vials (GlaxoSmithKline UK Ltd) (product)
19480611000001109,Benlysta 120mg powder for concentrate for solution for infusion vials (GlaxoSmithKline UK Ltd) (product)
19482011000001103,Belimumab 120mg powder for solution for infusion vials (product)
19482111000001102,Belimumab 400mg powder for solution for infusion vials (product)
19496811000001109,Capexion 0.5mg capsules (Generics (UK) Ltd) (product)
19497011000001100,Capexion 1mg capsules (Generics (UK) Ltd) (product)
19498011000001104,Capexion 5mg capsules (Generics (UK) Ltd) (product)
19573411000001102,Mitoxantrone 20mg/10ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
19574611000001101,Paclitaxel 30mg/5ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
19574811000001102,Paclitaxel 100mg/16.7ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
19575011000001107,Paclitaxel 150mg/25ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
19575211000001102,Paclitaxel 300mg/50ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
19575811000001101,Vinorelbine 10mg/1ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
19617911000001102,Neoral 25mg capsules (Doncaster Pharmaceuticals Ltd) (product)
19625511000001108,Topotecan 4mg/4ml concentrate for solution for infusion vials (Hospira UK Ltd) (product)
19627511000001104,Topotecan 4mg/4ml solution for infusion vials (product)
19633311000001101,Irinotecan 300mg/15ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
19633511000001107,Topotecan 1mg powder for solution for infusion vials (Actavis UK Ltd) (product)
19633711000001102,Topotecan 4mg powder for solution for infusion vials (Actavis UK Ltd) (product)
19671611000001105,Topotecan 1mg powder for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
19671811000001109,Topotecan 4mg powder for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
19680911000001100,Avastin 1.25mg/0.05ml solution for injection vials (Special Order) (product)
19687311000001100,Humira 40mg/0.8ml solution for injection vials (Abbott Laboratories Ltd) (product)
19697711000001100,Adalimumab 40mg/0.8ml solution for injection vials (product)
19697811000001108,Bevacizumab 1.25mg/0.05ml solution for injection vials (product)
19711011000001101,Votubia 5mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
19716211000001103,Votubia 2.5mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
19744011000001106,Everolimus 2.5mg tablets (product)
19783111000001102,Leflunomide 10mg tablets (Actavis UK Ltd) (product)
19783511000001106,Leflunomide 20mg tablets (Actavis UK Ltd) (product)
19812311000001109,Bevacizumab 1.25mg/0.05ml solution for injection vials (Special Order) (product)
19828211000001106,Temozolomide 100mg capsules (Generics (UK) Ltd) (product)
19828411000001105,Temozolomide 20mg capsules (Generics (UK) Ltd) (product)
19865611000001109,Aminolevulinic acid hydrochloride 30mg/ml oral solution (product)
19866111000001107,Gliolan 30mg/ml oral solution (medac GmbH) (product)
19867411000001100,CellCept 250mg capsules (Lexon (UK) Ltd) (product)
19867611000001102,CellCept 500mg tablets (Lexon (UK) Ltd) (product)
19921411000001107,Enbrel Paediatric 10mg powder and solvent for solution for injection vials (Pfizer Ltd) (product)
19946811000001101,Etanercept 10mg powder and solvent for solution for injection vials (product)
19953911000001102,Ebetrex 7.5mg/0.75ml solution for injection pre-filled syringes (Sandoz Ltd) (product)
19954111000001103,Ebetrex 10mg/1ml solution for injection pre-filled syringes (Sandoz Ltd) (product)
19954411000001108,Ebetrex 15mg/1.5ml solution for injection pre-filled syringes (Sandoz Ltd) (product)
19955711000001103,Ebetrex 25mg/1.25ml solution for injection pre-filled syringes (Sandoz Ltd) (product)
19956011000001109,Ebetrex 20mg/1ml solution for injection pre-filled syringes (Sandoz Ltd) (product)
19972411000001103,Ebetrex 30mg/1.5ml solution for injection pre-filled syringes (Sandoz Ltd) (product)
19976011000001106,Methotrexate 20mg/1ml solution for injection pre-filled syringes (product)
19976111000001107,Methotrexate 25mg/1.25ml solution for injection pre-filled syringes (product)
19976211000001101,Methotrexate 30mg/1.5ml solution for injection pre-filled syringes (product)
20095311000001101,Temozolomide 50mg/5ml oral suspension (product)
20095611000001106,Temozolomide 50mg/5ml oral suspension (Special Order) (product)
20106311000001101,Zelboraf 240mg tablets (Roche Products Ltd) (product)
20114011000001106,Vemurafenib 240mg tablets (product)
20158911000001108,Abraxane 100mg powder for suspension for infusion vials (Celgene Ltd) (product)
20164511000001102,Neoral 50mg capsules (Doncaster Pharmaceuticals Ltd) (product)
20177211000001100,Paclitaxel albumin 100mg powder for suspension for infusion vials (product)
201811000001107,Methotrexate 2.5mg tablets (A A H Pharmaceuticals Ltd) (product)
20204811000001101,Carboplatin 150mg/15ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20205611000001104,Carboplatin 450mg/45ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20206211000001107,Carboplatin 50mg/5ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20206611000001109,Carboplatin 600mg/60ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20208411000001107,Cisplatin 50mg/50ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20208911000001104,Cisplatin 10mg/10ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20209211000001103,Cisplatin 100mg/100ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20210911000001103,Cytarabine 1g/10ml solution for injection vials (Accord Healthcare Ltd) (product)
20211311000001109,Cytarabine 100mg/1ml solution for injection vials (Accord Healthcare Ltd) (product)
20211811000001100,Cytarabine 500mg/5ml solution for injection vials (Accord Healthcare Ltd) (product)
20262711000001100,Doxorubicin 200mg/100ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20262911000001103,Doxorubicin 50mg/25ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20263511000001103,Doxorubicin 10mg/5ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20265411000001103,Epirubicin 200mg/100ml solution for infusion vials (Accord Healthcare Ltd) (product)
20265811000001101,Epirubicin 50mg/25ml solution for injection vials (Accord Healthcare Ltd) (product)
20266211000001108,Epirubicin 10mg/5ml solution for injection vials (Accord Healthcare Ltd) (product)
20268111000001103,Epirubicin 20mg/10ml solution for injection vials (Accord Healthcare Ltd) (product)
20271611000001105,Fluorouracil 5g/100ml solution for infusion vials (Accord Healthcare Ltd) (product)
20272011000001106,Fluorouracil 500mg/10ml solution for injection vials (Accord Healthcare Ltd) (product)
20272211000001101,Fluorouracil 1g/20ml solution for injection vials (Accord Healthcare Ltd) (product)
20272711000001108,Fluorouracil 2.5g/50ml solution for infusion vials (Accord Healthcare Ltd) (product)
20273511000001105,Fluorouracil 250mg/5ml solution for injection vials (Accord Healthcare Ltd) (product)
20274211000001105,Gemcitabine 2g powder for solution for infusion vials (Accord Healthcare Ltd) (product)
20274411000001109,Gemcitabine 1g powder for solution for infusion vials (Accord Healthcare Ltd) (product)
20274611000001107,Gemcitabine 200mg powder for solution for infusion vials (Accord Healthcare Ltd) (product)
20274811000001106,Irinotecan 40mg/2ml concentrate for solution for infusion vial (Accord Healthcare Ltd) (product)
20275011000001101,Irinotecan 100mg/5ml concentrate for solution for infusion vial (Accord Healthcare Ltd) (product)
20275211000001106,Irinotecan 500mg/25ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20278311000001107,Oxaliplatin 50mg/10ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20278511000001101,Paclitaxel 100mg/16.7ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20278711000001106,Paclitaxel 300mg/50ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20278911000001108,Paclitaxel 30mg/5ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
20290211000001108,Leflunomide 10mg tablets (Sandoz Ltd) (product)
20290411000001107,Leflunomide 20mg tablets (Sandoz Ltd) (product)
20293611000001101,Epirubicin 20mg/10ml solution for injection vials (product)
20293711000001105,Fluorouracil 250mg/5ml solution for injection vials (product)
20307311000001108,Removab 10micrograms/0.1ml concentrate for solution for infusion pre-filled syringes (Fresenius Biotech) (product)
20307611000001103,Removab 50micrograms/0.5ml concentrate for solution for infusion pre-filled syringes (Fresenius Biotech) (product)
20310611000001100,Methotrexate 2.5mg tablets (Sandoz Ltd) (product)
20310811000001101,Methotrexate 10mg tablets (Sandoz Ltd) (product)
20312011000001106,Mycophenolate mofetil 250mg capsules (Sandoz Ltd) (product)
20312211000001101,Mycophenolate motefil 500mg tablets (Sandoz Ltd) (product)
20344311000001106,Catumaxomab 10micrograms/0.1ml solution for infusion pre-filled syringes (product)
20344411000001104,Catumaxomab 50micrograms/0.5ml solution for infusion pre-filled syringes (product)
20358611000001109,Caprelsa 100mg tablets (AstraZeneca UK Ltd) (product)
20358911000001103,Caprelsa 300mg tablets (AstraZeneca UK Ltd) (product)
20363411000001107,Vandetanib 100mg tablets (product)
20363511000001106,Vandetanib 300mg tablets (product)
20366511000001103,Teysuno 20mg/5.8mg/15.8mg capsules (Nordic Pharma Ltd) (product)
20367111000001105,Teysuno 15mg/4.35mg/11.8mg capsules (Nordic Pharma Ltd) (product)
20419211000001101,Generic Teysuno 15mg/4.35mg/11.8mg capsules (product)
20419311000001109,Generic Teysuno 20mg/5.8mg/15.8mg capsules (product)
20471811000001105,Caelyx pegylated liposomal 20mg/10ml concentrate for solution for infusion vials (Janssen-Cilag Ltd) (product)
20472311000001105,Caelyx pegylated liposomal 50mg/25ml concentrate for solution for infusion vials (Janssen-Cilag Ltd) (product)
20478211000001100,Doxorubicin liposomal pegylated 20mg/10ml solution for infusion vials (product)
20478311000001108,Doxorubicin liposomal pegylated 50mg/25ml solution for infusion vials (product)
20538611000001107,Mercaptopurine 25mg tablets (Special Order) (product)
20556311000001100,Mercaptopurine 25mg tablets (product)
20839511000001103,Leflunomide 10mg tablets (Aspire Pharma Ltd) (product)
20839811000001100,Leflunomide 20mg tablets (Aspire Pharma Ltd) (product)
20886411000001102,Mercaptopurine 45mg/5ml oral suspension (Special Order) (product)
20914411000001104,Leflunomide 10mg tablets (Zentiva) (product)
20914611000001101,Leflunomide 20mg tablets (Zentiva) (product)
20921111000001100,Mercaptopurine 45mg/5ml oral suspension (product)
209911000001103,Prograf 1mg capsules (Fujisawa Ltd) (product)
21209511000001108,Crizotinib 250mg capsules (product)
21210111000001107,Xalkori 250mg capsules (Imported (United States)) (product)
21263111000001101,Ciclosporin 25mg capsules (Sigma Pharmaceuticals Plc) (product)
21263311000001104,Ciclosporin 50mg capsules (Sigma Pharmaceuticals Plc) (product)
21263511000001105,Ciclosporin 100mg capsules (Sigma Pharmaceuticals Plc) (product)
21274511000001100,Jakavi 20mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
21275011000001107,Jakavi 5mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
21275311000001105,Jakavi 15mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
21290711000001107,Ruxolitinib 15mg tablets (product)
21290811000001104,Ruxolitinib 20mg tablets (product)
21290911000001109,Ruxolitinib 5mg tablets (product)
21293211000001105,Cytarabine 2g/20ml solution for injection vials (Accord Healthcare Ltd) (product)
21293411000001109,Docetaxel 160mg/8ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
21293611000001107,Docetaxel 20mg/1ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
21293811000001106,Docetaxel 80mg/4ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
21294011000001103,Irinotecan 300mg/15ml concentrate for solution for infusion vial (Accord Healthcare Ltd) (product)
21294211000001108,Oxaliplatin 100mg/20ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
21294511000001106,Topotecan 1mg/1ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
21294711000001101,Topotecan 4mg powder for solution for infusion vials (Accord Healthcare Ltd) (product)
21297311000001109,Oxaliplatin 200mg/40ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
21298711000001109,Topotecan 4mg/4ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
21303211000001104,Tacrolimus 800micrograms/5ml oral solution (Special Order) (product)
21305711000001107,Tacrolimus 800micrograms/5ml oral solution (product)
21305811000001104,Topotecan 1mg/1ml solution for infusion vials (product)
21505811000001102,Inlyta 5mg tablets (Pfizer Ltd) (product)
21506111000001103,Inlyta 1mg tablets (Pfizer Ltd) (product)
21510211000001109,Axitinib 1mg tablets (product)
21510311000001101,Axitinib 5mg tablets (product)
21516311000001103,Pixantrone 29mg powder for solution for infusion vials (product)
21516711000001104,Pixuvri 29mg powder for concentrate for solution for infusion vials (CTI Life Sciences Ltd) (product)
21521511000001107,Dacogen 50mg powder for concentrate for solution for infusion vials (Janssen-Cilag Ltd) (product)
21557911000001107,Foscan 1mg/1ml solution for injection vials (Biolitec Pharma Ltd) (product)
21558211000001104,Foscan 3mg/3ml solution for injection vials (Biolitec Pharma Ltd) (product)
21558511000001101,Foscan 6mg/6ml solution for injection vials (Biolitec Pharma Ltd) (product)
21572311000001106,Brentuximab vedotin 50mg powder for solution for infusion vials (product)
21572511000001100,Adcetris 50mg powder for concentrate for solution for infusion vials (Takeda UK Ltd) (product)
21578711000001108,Decitabine 50mg powder for solution for infusion vials (product)
21580111000001100,Temoporfin 1mg/1ml solution for injection vials (product)
21580211000001106,Temoporfin 3mg/3ml solution for injection vials (product)
21580311000001103,Temoporfin 6mg/6ml solution for injection vials (product)
21596111000001101,Xalkori 250mg capsules (Pfizer Ltd) (product)
21597811000001105,Crizotinib 200mg capsules (product)
21598111000001102,Xalkori 200mg capsules (Pfizer Ltd) (product)
21678611000001108,Votubia 10mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
21699611000001106,Orencia 125mg/1ml solution for injection pre-filled syringes (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
21704711000001107,Abatacept 125mg/1ml solution for injection pre-filled syringes (product)
21780411000001106,Azathioprine 25mg tablets (Waymade Healthcare Plc) (product)
21780711000001100,Azathioprine 50mg tablets (Waymade Healthcare Plc) (product)
21785811000001102,Temozolomide 20mg capsules (Waymade Healthcare Plc) (product)
21786011000001104,Temozolomide 100mg capsules (Waymade Healthcare Plc) (product)
21796211000001108,Methotrexate 2.5mg tablets (Waymade Healthcare Plc) (product)
21796511000001106,Methotrexate 10mg tablets (Waymade Healthcare Plc) (product)
21808611000001106,Mycophenolate mofetil 250mg capsules (Waymade Healthcare Plc) (product)
21808811000001105,Mycophenolate mofetil 500mg tablets (Waymade Healthcare Plc) (product)
21835311000001101,Ciclosporin 100mg capsules (Cubic Pharmaceuticals Ltd) (product)
21835511000001107,Ciclosporin 50mg capsules (Cubic Pharmaceuticals Ltd) (product)
21835711000001102,Ciclosporin 25mg capsules (Cubic Pharmaceuticals Ltd) (product)
21842511000001100,Penicillamine 125mg tablets (Waymade Healthcare Plc) (product)
21842611000001101,Mycophenolate mofetil 250mg capsules (Cubic Pharmaceuticals Ltd) (product)
21842911000001107,Penicillamine 250mg tablets (Waymade Healthcare Plc) (product)
21929811000001100,Bevacizumab 1.25mg/0.05ml solution for injection pre-filled syringes (product)
21930511000001108,Bevacizumab 1.25mg/0.05ml solution for injection pre-filled syringes (Special Order) (product)
21969411000001109,Xaluprine 20mg/ml oral suspension (Nova Laboratories Ltd) (product)
22063011000001107,Leflunomide 10mg tablets (Waymade Healthcare Plc) (product)
22063211000001102,Leflunomide 20mg tablets (Waymade Healthcare Plc) (product)
22101211000001108,Mercaptopurine 25mg capsules (Special Order) (product)
22135211000001104,Perjeta 420mg/14ml concentrate for solution for infusion vials (Roche Products Ltd) (product)
22154611000001102,Mercaptopurine 25mg capsules (product)
22154811000001103,Pertuzumab 420mg/14ml solution for infusion vials (product)
22222111000001103,Methotrexate 10mg tablets (Teva UK Ltd) (product)
22222311000001101,Methotrexate 2.5mg tablets (Teva UK Ltd) (product)
22311211000001101,Doxorubicin 20mg/10ml solution for infusion pre-filled syringes (product)
22311811000001100,Doxorubicin 20mg/10ml solution for infusion pre-filled syringes (Special Order) (product)
22312511000001106,Doxorubicin 45mg/22.5ml solution for infusion pre-filled syringes (product)
22313211000001102,Doxorubicin 45mg/22.5ml solution for infusion pre-filled syringes (Special Order) (product)
22313511000001104,Doxorubicin 55mg/27.5ml solution for infusion pre-filled syringes (product)
22313811000001101,Doxorubicin 55mg/27.5ml solution for infusion pre-filled syringes (Special Order) (product)
22314111000001105,Doxorubicin 5mg/2.5ml solution for infusion pre-filled syringes (product)
22314411000001100,Doxorubicin 5mg/2.5ml solution for infusion pre-filled syringes (Special Order) (product)
22333211000001109,Esbriet 267mg capsules (InterMune UK Ltd) (product)
22343011000001103,Pirfenidone 267mg capsules (product)
22352411000001100,Mycophenolate mofetil 250mg capsules (AM Distributions (Yorkshire) Ltd) (product)
22408311000001108,Ciclosporin 25mg capsules (Doncaster Pharmaceuticals Ltd) (product)
22408511000001102,Ciclosporin 50mg capsules (Doncaster Pharmaceuticals Ltd) (product)
22408711000001107,Ciclosporin 100mg capsules (Doncaster Pharmaceuticals Ltd) (product)
22409911000001101,Mycophenolate mofetil 250mg capsules (Doncaster Pharmaceuticals Ltd) (product)
22440211000001105,Epirubicin 100mg/50ml solution for infusion pre-filled syringes (product)
22440511000001108,Epirubicin 100mg/50ml solution for infusion pre-filled syringes (Special Order) (product)
22440811000001106,Epirubicin 20mg/10ml solution for injection pre-filled syringes (product)
22441111000001105,Epirubicin 20mg/10ml solution for injection pre-filled syringes (Special Order) (product)
22441411000001100,Epirubicin 40mg/20ml solution for injection pre-filled syringes (product)
22441711000001106,Epirubicin 40mg/20ml solution for injection pre-filled syringes (Special Order) (product)
22442011000001101,Epirubicin 50mg/25ml solution for injection pre-filled syringes (product)
22442311000001103,Epirubicin 50mg/25ml solution for injection pre-filled syringes (Special Order) (product)
22442711000001104,Epirubicin 60mg/30ml solution for injection pre-filled syringes (product)
22443011000001105,Epirubicin 60mg/30ml solution for injection pre-filled syringes (Special Order) (product)
22443511000001102,Epirubicin 5mg/2.5ml solution for injection pre-filled syringes (product)
22444011000001107,Epirubicin 5mg/2.5ml solution for injection pre-filled syringes (Special Order) (product)
22444511000001104,Epirubicin 90mg/45ml solution for injection pre-filled syringes (product)
22444811000001101,Epirubicin 90mg/45ml solution for injection pre-filled syringes (Special Order) (product)
22449011000001108,Ifosfamide 1g powder for concentrate for solution for injection vials (Alliance Healthcare (Distribution) Ltd) (product)
22449711000001105,Ifosfamide 2g powder for concentrate for solution for injection vials (Alliance Healthcare (Distribution) Ltd) (product)
22459711000001108,Cyclophosphamide 1g/50ml solution for infusion pre-filled syringes (product)
22460011000001107,Cyclophosphamide 1g/50ml solution for infusion pre-filled syringes (Special Order) (product)
22460311000001105,Cyclophosphamide 200mg/10ml solution for injection pre-filled syringes (product)
22460611000001100,Cyclophosphamide 200mg/10ml solution for injection pre-filled syringes (Special Order) (product)
22460911000001106,Cyclophosphamide 500mg/25ml solution for injection pre-filled syringes (product)
22461211000001108,Cyclophosphamide 500mg/25ml solution for injection pre-filled syringes (Special Order) (product)
22461511000001106,Cyclophosphamide 550mg/27.5ml solution for injection pre-filled syringes (product)
22461811000001109,Cyclophosphamide 550mg/27.5ml solution for injection pre-filled syringes (Special Order) (product)
22462111000001107,Cyclophosphamide 600mg/30ml solution for injection pre-filled syringes (product)
22462411000001102,Cyclophosphamide 600mg/30ml solution for injection pre-filled syringes (Special Order) (product)
22462711000001108,Cyclophosphamide 900mg/45ml solution for injection pre-filled syringes (product)
22463011000001102,Cyclophosphamide 900mg/45ml solution for injection pre-filled syringes (Special Order) (product)
22463311000001104,Cyclophosphamide 950mg/47.5ml solution for injection pre-filled syringes (product)
22463611000001109,Cyclophosphamide 950mg/47.5ml solution for injection pre-filled syringes (Special Order) (product)
22464411000001109,Mycophenolate mofetil 500mg tablets (Arrow Generics Ltd) (product)
22475211000001102,Cytarabine 20mg/0.2ml solution for injection pre-filled syringes (product)
22475511000001104,Cytarabine 20mg/0.2ml solution for injection pre-filled syringes (Special Order) (product)
22479811000001103,Temozolomide 5mg capsules (Sun Pharmaceuticals UK Ltd) (product)
22519811000001102,Mercaptopurine 50mg tablets (Aspen Pharma Trading Ltd) (product)
22520911000001108,Tioguanine 40mg tablets (Aspen Pharma Trading Ltd) (product)
22522211000001103,Melphalan 50mg powder and solvent for solution for injection vials (Aspen Pharma Trading Ltd) (product)
22566811000001107,Ifosfamide 1g powder for solution for injection vials (A A H Pharmaceuticals Ltd) (product)
22604011000001104,Ciclosporin 100mg capsules (Colorama Pharmaceuticals Ltd) (product)
22604211000001109,Ciclosporin 25mg capsules (Colorama Pharmaceuticals Ltd) (product)
22604411000001108,Ciclosporin 50mg capsules (Colorama Pharmaceuticals Ltd) (product)
22605811000001106,Mycophenolate mofetil 250mg capsules (Colorama Pharmaceuticals Ltd) (product)
22614111000001101,Azathioprine 25mg tablets (Doncaster Pharmaceuticals Ltd) (product)
22615211000001108,Azathioprine 50mg tablets (Doncaster Pharmaceuticals Ltd) (product)
22641611000001100,Oxaliplatin 100mg/20ml concentrate for solution for infusion vials (Sun Pharmaceuticals UK Ltd) (product)
22643311000001106,Oxaliplatin 50mg/10ml concentrate for solution for infusion vials (Sun Pharmaceuticals UK Ltd) (product)
22649711000001108,Idarubicin 5mg powder for solution for injection vials (Teva UK Ltd) (product)
22649911000001105,Idarubicin 10mg powder for solution for injection vials (Teva UK Ltd) (product)
22673711000001106,Mercaptopurine 50mg tablets (Alliance Healthcare (Distribution) Ltd) (product)
22680611000001100,Melphalan 50mg powder and solvent for solution for injection vials (A A H Pharmaceuticals Ltd) (product)
22697611000001102,Bosulif 100mg tablets (Pfizer Ltd) (product)
22697911000001108,Bosulif 500mg tablets (Pfizer Ltd) (product)
22703911000001108,Bosutinib 100mg tablets (product)
22704011000001106,Bosutinib 500mg tablets (product)
22705211000001100,Idarubicin 10mg/10ml solution for injection vials (Teva UK Ltd) (product)
22705511000001102,Idarubicin 5mg/5ml solution for injection vials (Teva UK Ltd) (product)
22756511000001104,Docetaxel 20mg/0.5ml solution for infusion vials and diluent (Teva UK Ltd) (product)
22756711000001109,Docetaxel 80mg/2ml solution for infusion vials and diluent (Teva UK Ltd) (product)
22764011000001107,Erivedge 150mg capsules (Roche Products Ltd) (product)
22785511000001101,Idarubicin 5mg/5ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
22785711000001106,Idarubicin 10mg/10ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
22787311000001104,Vismodegib 150mg capsules (product)
22831311000001104,Docetaxel 20mg/2ml solution for infusion vials and diluent (Teva UK Ltd) (product)
22831611000001109,Docetaxel 80mg/8ml solution for infusion vials and diluent (Teva UK Ltd) (product)
22836011000001109,Chlorambucil 2mg tablets (Aspen Pharma Trading Ltd) (product)
22857911000001107,Docetaxel 20mg/2ml solution for infusion vials and diluent (product)
22858011000001109,Docetaxel 80mg/8ml solution for infusion vials and diluent (product)
23046711000001104,Topotecan 4mg/4ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
23047011000001103,Topotecan 1mg/1ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
23070511000001108,Tafinlar 50mg capsules (GlaxoSmithKline UK Ltd) (product)
23070811000001106,Tafinlar 75mg capsules (GlaxoSmithKline UK Ltd) (product)
23107511000001108,Dabrafenib 50mg capsules (product)
23107611000001107,Dabrafenib 75mg capsules (product)
23118711000001104,Chlorambucil 2mg tablets (A A H Pharmaceuticals Ltd) (product)
23157311000001105,Herceptin 600mg/5ml solution for injection vials (Roche Products Ltd) (product)
23179111000001104,Melphalan 50mg powder and solvent for solution for injection vials (Alliance Healthcare (Distribution) Ltd) (product)
23204911000001105,Trastuzumab 600mg/5ml solution for injection vials (product)
23218811000001105,Mycophenolate mofetil 250mg capsules (J M McGill Ltd) (product)
23269311000001106,Stivarga 40mg tablets (Bayer Plc) (product)
23285111000001105,Imnovid 1mg capsules (Celgene Ltd) (product)
23285411000001100,Imnovid 2mg capsules (Celgene Ltd) (product)
23285711000001106,Imnovid 3mg capsules (Celgene Ltd) (product)
23286011000001100,Imnovid 4mg capsules (Celgene Ltd) (product)
23305111000001101,Pomalidomide 1mg capsules (product)
23305211000001107,Pomalidomide 2mg capsules (product)
23305311000001104,Pomalidomide 3mg capsules (product)
23305411000001106,Pomalidomide 4mg capsules (product)
23307411000001100,Revlimid 2.5mg capsules (Celgene Ltd) (product)
23326611000001106,Melphalan 2mg tablets (Aspen Pharma Trading Ltd) (product)
23344511000001104,Lenalidomide 2.5mg capsules (product)
23344611000001100,Regorafenib 40mg tablets (product)
23361911000001104,Melphalan 2mg tablets (A A H Pharmaceuticals Ltd) (product)
23410511000001105,Gilotrif 30mg tablets (Imported (United States)) (product)
23410811000001108,Gilotrif 40mg tablets (Imported (United States)) (product)
23411111000001107,Gilotrif 20mg tablets (Imported (United States)) (product)
23416611000001106,Afatinib 20mg tablets (product)
23416711000001102,Afatinib 30mg tablets (product)
23416811000001105,Afatinib 40mg tablets (product)
23428211000001103,Ciclosporin 100mg capsules (J M McGill Ltd) (product)
23428411000001104,Ciclosporin 25mg capsules (J M McGill Ltd) (product)
23428611000001101,Ciclosporin 50mg capsules (J M McGill Ltd) (product)
23472211000001101,Fludarabine phosphate 50mg/2ml concentrate for solution for injection vials (Accord Healthcare Ltd) (product)
23563711000001102,Perixis 0.5mg capsules (Accord Healthcare Ltd) (product)
23564011000001102,Perixis 1mg capsules (Accord Healthcare Ltd) (product)
23564611000001109,Perixis 5mg capsules (Accord Healthcare Ltd) (product)
23564911000001103,Epirubicin 100mg/50ml solution for infusion vials (Accord Healthcare Ltd) (product)
23566911000001106,Gemcitabine 200mg/2ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
23569011000001101,Gemcitabine 1g/10ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
23570911000001104,Gemcitabine 2g/20ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
23576111000001104,Paclitaxel 150mg/25ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
23582311000001108,Iclusig 15mg tablets (Ariad Pharma (UK) Ltd) (product)
23582911000001109,Iclusig 45mg tablets (Ariad Pharma (UK) Ltd) (product)
23603711000001109,Gemcitabine 1g/10ml solution for infusion vials (product)
23603811000001101,Gemcitabine 200mg/2ml solution for infusion vials (product)
23603911000001106,Gemcitabine 2g/20ml solution for infusion vials (product)
23604711000001106,Ponatinib 15mg tablets (product)
23604811000001103,Ponatinib 45mg tablets (product)
23605811000001102,Prograf 5mg capsules (Waymade Healthcare Plc) (product)
23609711000001107,Tacrolimus 900micrograms/5ml oral suspension (Special Order) (product)
23612111000001104,Tacrolimus 900micrograms/5ml oral suspension (product)
23640111000001106,Capecitabine 150mg tablets (A A H Pharmaceuticals Ltd) (product)
23640311000001108,Capecitabine 500mg tablets (A A H Pharmaceuticals Ltd) (product)
23668711000001104,Capecitabine 150mg tablets (Zentiva) (product)
23668911000001102,Capecitabine 500mg tablets (Zentiva) (product)
23673011000001104,Cyclophosphamide 300mg/15ml solution for injection pre-filled syringes (product)
23673311000001101,Cyclophosphamide 300mg/15ml solution for injection pre-filled syringes (Special Order) (product)
23855511000001104,Giotrif 20mg tablets (Boehringer Ingelheim Ltd) (product)
23858411000001108,Giotrif 30mg tablets (Boehringer Ingelheim Ltd) (product)
23859211000001104,Giotrif 40mg tablets (Boehringer Ingelheim Ltd) (product)
23861011000001101,Giotrif 50mg tablets (Boehringer Ingelheim Ltd) (product)
23905211000001104,Afatinib 50mg tablets (product)
23936311000001108,Ciclosporin 100mg capsules (Niche Pharma Ltd) (product)
23936511000001102,Ciclosporin 25mg capsules (Niche Pharma Ltd) (product)
23936711000001107,Ciclosporin 50mg capsules (Niche Pharma Ltd) (product)
23950411000001104,Temozolomide 100mg capsules (Sun Pharmaceuticals UK Ltd) (product)
23950611000001101,Temozolomide 140mg capsules (Sun Pharmaceuticals UK Ltd) (product)
23950811000001102,Temozolomide 180mg capsules (Sun Pharmaceuticals UK Ltd) (product)
23951011000001104,Temozolomide 20mg capsules (Sun Pharmaceuticals UK Ltd) (product)
23951211000001109,Temozolomide 250mg capsules (Sun Pharmaceuticals UK Ltd) (product)
23958811000001104,Mycophenolate mofetil 250mg capsules (Niche Pharma Ltd) (product)
23964811000001100,Kadcyla 100mg powder for concentrate for solution for infusion vials (Roche Products Ltd) (product)
23965111000001106,Kadcyla 160mg powder for concentrate for solution for infusion vials (Roche Products Ltd) (product)
23982811000001109,Simponi 100mg/1ml solution for injection pre-filled pens (Merck Sharp & Dohme Ltd) (product)
23984711000001106,Golimumab 100mg/1ml solution for injection pre-filled disposable devices (product)
23985411000001104,Trastuzumab emtansine 100mg powder for solution for infusion vials (product)
23985511000001100,Trastuzumab emtansine 160mg powder for solution for infusion vials (product)
24028011000001102,Mycophenolate mofetil 250mg capsules (CST Pharma Ltd) (product)
24104211000001101,Afinitor 2.5mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
24113511000001103,Ciclosporin 100mg capsules (Lexon (UK) Ltd) (product)
24116711000001101,Leflunomide 10mg tablets (Morningside Healthcare Ltd) (product)
24116911000001104,Leflunomide 20mg tablets (Morningside Healthcare Ltd) (product)
24135711000001100,Methotrexate 10mg tablets (Morningside Healthcare Ltd) (product)
24136011000001106,Methotrexate 2.5mg tablets (Morningside Healthcare Ltd) (product)
24157711000001107,Ciclosporin 25mg capsules (Ethigen Ltd) (product)
24157911000001109,Ciclosporin 50mg capsules (Ethigen Ltd) (product)
24158111000001107,Ciclosporin 100mg capsules (Ethigen Ltd) (product)
24200211000001107,Capecitabine 150mg tablets (Actavis UK Ltd) (product)
24200411000001106,Capecitabine 500mg tablets (Actavis UK Ltd) (product)
24363111000001104,Leflunomide 10mg tablets (DE Pharmaceuticals) (product)
24363311000001102,Leflunomide 20mg tablets (DE Pharmaceuticals) (product)
24375211000001100,Capecitabine 150mg tablets (medac UK) (product)
24375411000001101,Capecitabine 500mg tablets (medac UK) (product)
24376011000001101,Topotecan 1mg/1ml concentrate for solution for infusion vials (medac UK) (product)
24376211000001106,Topotecan 4mg/4ml concentrate for solution for infusion vials (medac UK) (product)
24376511000001109,Capecitabine 300mg tablets (medac UK) (product)
24376811000001107,Leflunomide 15mg tablets (medac UK) (product)
24377211000001108,Doxorubicin 50mg/25ml solution for infusion vials (medac UK) (product)
24377411000001107,Doxorubicin 200mg/100ml solution for infusion vials (medac UK) (product)
24378411000001106,Doxorubicin 10mg/5ml solution for infusion vials (medac UK) (product)
24381411000001107,Methotrexate 10mg tablets (DE Pharmaceuticals) (product)
24381611000001105,Methotrexate 2.5mg tablets (DE Pharmaceuticals) (product)
24403811000001102,Amsidine 75mg/1.5ml solution for infusion ampoules and diluent (NordMedica A/S) (product)
24405511000001101,Mycophenolate mofetil 500mg tablets (DE Pharmaceuticals) (product)
24405711000001106,Potactasol 1mg powder for concentrate for solution for infusion vials (Actavis UK Ltd) (product)
24405911000001108,Potactasol 4mg powder for concentrate for solution for infusion vials (Actavis UK Ltd) (product)
24407611000001109,Capecitabine 300mg tablets (product)
24408011000001101,Leflunomide 15mg tablets (product)
24436711000001107,Hydroxycarbamide 500mg/5ml oral suspension (Drug Tariff Special Order) (product)
24504611000001108,Aubagio 14mg tablets (Genzyme Therapeutics Ltd) (product)
24504911000001102,Docetaxel 20mg/0.72ml concentrate for solution for infusion vials and diluent (Teva UK Ltd) (product)
24505211000001107,Azathioprine 25mg tablets (Sandoz Ltd) (product)
24505311000001104,Docetaxel 80mg/2.88ml concentrate for solution for infusion vials and diluent (Teva UK Ltd) (product)
24507811000001103,Inlyta 7mg tablets (Pfizer Ltd) (product)
24508111000001106,Inlyta 3mg tablets (Pfizer Ltd) (product)
24509011000001100,Axitinib 3mg tablets (product)
24509111000001104,Axitinib 7mg tablets (product)
24509511000001108,Docetaxel 20mg/0.72ml solution for infusion vials and diluent (product)
24509611000001107,Docetaxel 80mg/2.88ml solution for infusion vials and diluent (product)
24510211000001101,Hydroxycarbamide 500mg/5ml oral suspension (product)
24510811000001100,Teriflunomide 14mg tablets (product)
24519911000001104,Ciclosporin 25mg capsules (Mawdsley-Brooks & Company Ltd) (product)
24520111000001101,Ciclosporin 50mg capsules (Mawdsley-Brooks & Company Ltd) (product)
24520311000001104,Ciclosporin 100mg capsules (Mawdsley-Brooks & Company Ltd) (product)
24559811000001100,Capecitabine 150mg tablets (Generics (UK) Ltd) (product)
24560011000001107,Capecitabine 500mg tablets (Generics (UK) Ltd) (product)
24561811000001109,Lemtrada 12mg/1.2ml concentrate for solution for infusion vials (Genzyme Therapeutics Ltd) (product)
24565711000001104,Alemtuzumab 12mg/1.2ml solution for infusion vials (product)
24571011000001105,Mycophenolate mofetil 250mg capsules (Mawdsley-Brooks & Company Ltd) (product)
24574711000001105,Capecitabine 500mg tablets (Sun Pharmaceuticals UK Ltd) (product)
24588411000001102,Metoject PEN 7.5mg/0.15ml solution for injection pre-filled pens (medac UK) (product)
24588711000001108,Metoject PEN 30mg/0.6ml solution for injection pre-filled pens (medac UK) (product)
24589011000001101,Metoject PEN 27.5mg/0.55ml solution for injection pre-filled pens (medac UK) (product)
24589311000001103,Metoject PEN 25mg/0.5ml solution for injection pre-filled pens (medac UK) (product)
24589611000001108,Metoject PEN 15mg/0.3ml solution for injection pre-filled pens (medac UK) (product)
24589911000001102,Metoject PEN 12.5mg/0.25ml solution for injection pre-filled pens (medac UK) (product)
24590211000001100,Metoject PEN 10mg/0.2ml solution for injection pre-filled pens (medac UK) (product)
24590411000001101,Metoject PEN 22.5mg/0.45ml solution for injection pre-filled pens (medac UK) (product)
24590811000001104,Metoject PEN 20mg/0.4ml solution for injection pre-filled pens (medac UK) (product)
24591111000001100,Metoject PEN 17.5mg/0.35ml solution for injection pre-filled pens (medac UK) (product)
24594311000001100,Methotrexate 10mg/0.2ml solution for injection pre-filled disposable devices (product)
24594411000001107,Methotrexate 12.5mg/0.25ml solution for injection pre-filled disposable devices (product)
24594511000001106,Methotrexate 15mg/0.3ml solution for injection pre-filled disposable devices (product)
24594611000001105,Methotrexate 17.5mg/0.35ml solution for injection pre-filled disposable devices (product)
24594711000001101,Methotrexate 20mg/0.4ml solution for injection pre-filled disposable devices (product)
24594811000001109,Methotrexate 22.5mg/0.45ml solution for injection pre-filled disposable devices (product)
24594911000001104,Methotrexate 25mg/0.5ml solution for injection pre-filled disposable devices (product)
24595011000001104,Methotrexate 27.5mg/0.55ml solution for injection pre-filled disposable devices (product)
24595111000001103,Methotrexate 30mg/0.6ml solution for injection pre-filled disposable devices (product)
24595211000001109,Methotrexate 7.5mg/0.15ml solution for injection pre-filled disposable devices (product)
24656211000001103,Capecitabine 500mg tablets (Dr Reddy's Laboratories (UK) Ltd) (product)
24657811000001100,Entyvio 300mg powder for concentrate for solution for infusion vials (Takeda UK Ltd) (product)
24670211000001102,Vedolizumab 300mg powder for solution for infusion vials (product)
24775211000001101,Leflunomide 15mg tablets (Alliance Healthcare (Distribution) Ltd) (product)
24780211000001103,MabThera 1400mg/11.7ml solution for injection vials (Roche Products Ltd) (product)
24780811000001102,RoActemra 162mg/0.9ml solution for injection pre-filled syringes (Roche Products Ltd) (product)
24796311000001105,Sylvant 400mg powder for concentrate for solution for infusion vials (EUSA Pharma Ltd) (product)
24797411000001101,Sylvant 100mg powder for concentrate for solution for infusion vials (EUSA Pharma Ltd) (product)
24856511000001109,Rituximab 1.4g/11.7ml solution for injection vials (product)
24856911000001102,Tocilizumab 162mg/0.9ml solution for injection pre-filled syringes (product)
25091011000001106,Siltuximab 100mg powder for solution for infusion vials (product)
25091211000001101,Siltuximab 400mg powder for solution for infusion vials (product)
25371411000001105,Zortress 250microgram tablets (Imported (United States)) (product)
25371711000001104,Zortress 750microgram tablets (Imported (United States)) (product)
25444111000001106,Gazyvaro 1000mg/40ml concentrate for solution for infusion vials (Roche Products Ltd) (product)
25503511000001103,Obinutuzumab 1g/40ml solution for infusion vials (product)
25553011000001101,Temozolomide 5mg capsules (Zentiva) (product)
25553511000001109,Temozolomide 20mg capsules (Zentiva) (product)
25553811000001107,Temozolomide 100mg capsules (Zentiva) (product)
25554711000001102,Temozolomide 140mg capsules (Zentiva) (product)
25555011000001100,Temozolomide 180mg capsules (Zentiva) (product)
25555511000001108,Temozolomide 250mg capsules (Zentiva) (product)
25694011000001104,Ciclosporin 25mg capsules (Icarus Pharmaceuticals Ltd) (product)
25694711000001102,Ciclosporin 50mg capsules (Icarus Pharmaceuticals Ltd) (product)
25695111000001104,Ciclosporin 100mg capsules (Icarus Pharmaceuticals Ltd) (product)
25881711000001105,Mycophenolate mofetil 250mg capsules (Icarus Pharmaceuticals Ltd) (product)
25933411000001100,Docetaxel 80mg/4ml concentrate for solution for infusion vials (Dr Reddy's Laboratories (UK) Ltd) (product)
25933611000001102,Docetaxel 20mg/1ml concentrate for solution for infusion vials (Dr Reddy's Laboratories (UK) Ltd) (product)
25964511000001108,Trametinib 2mg tablets (product)
25964911000001101,Mekinist 2mg tablets (Imported (United States)) (product)
26019111000001108,Ciclosporin 100mg capsules (Ennogen Healthcare Ltd) (product)
26021211000001109,Ciclosporin 25mg capsules (Ennogen Healthcare Ltd) (product)
26022211000001102,Ciclosporin 50mg capsules (Ennogen Healthcare Ltd) (product)
26658011000001100,Azapress 50mg tablets (Ennogen Pharma Ltd) (product)
27044711000001102,Capecitabine 300mg tablets (A A H Pharmaceuticals Ltd) (product)
27855611000001105,Capecitabine 150mg tablets (Accord Healthcare Ltd) (product)
27856011000001107,Capecitabine 300mg tablets (Accord Healthcare Ltd) (product)
27856711000001109,Capecitabine 500mg tablets (Accord Healthcare Ltd) (product)
27946711000001104,Idelalisib 100mg tablets (product)
27946811000001107,Zydelig 100mg tablets (Gilead Sciences International Ltd) (product)
27947111000001102,Idelalisib 150mg tablets (product)
27947211000001108,Zydelig 150mg tablets (Gilead Sciences International Ltd) (product)
27950611000001109,Etoposide 100mg/5ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
27951711000001108,Methotrexate 1g/40ml solution for injection vials (Accord Healthcare Ltd) (product)
27952411000001107,Methotrexate 500mg/20ml solution for injection vials (Accord Healthcare Ltd) (product)
27990111000001105,Azathioprine 50mg tablets (Ennogen Healthcare Ltd) (product)
28003411000001105,Capecitabine 150mg tablets (Dr Reddy's Laboratories (UK) Ltd) (product)
28009911000001104,Cometriq 20mg capsules (Swedish Orphan Biovitrum Ltd) (product)
28010411000001100,Cometriq 80mg capsules (Swedish Orphan Biovitrum Ltd) (product)
28010711000001106,Cometriq 20mg capsules and Cometriq 80mg capsules (Swedish Orphan Biovitrum Ltd) (product)
28012311000001106,Cabozantinib 20mg capsules (product)
28012411000001104,Cabozantinib 20mg capsules and Cabozantinib 80mg capsules (product)
28012511000001100,Cabozantinib 80mg capsules (product)
28093711000001101,Chlorambucil 2mg tablets (Alliance Healthcare (Distribution) Ltd) (product)
28094111000001100,Melphalan 2mg tablets (Alliance Healthcare (Distribution) Ltd) (product)
28095411000001106,Tioguanine 40mg tablets (Alliance Healthcare (Distribution) Ltd) (product)
28122211000001100,Ciclosporin 100mg capsules (Pharma-z Ltd) (product)
28122711000001107,Ciclosporin 25mg capsules (Pharma-z Ltd) (product)
28123311000001103,Ciclosporin 50mg capsules (Pharma-z Ltd) (product)
28279111000001101,Mercaptopurine 30mg capsules (Special Order) (product)
28282411000001107,Imbruvica 140mg capsules (Janssen-Cilag Ltd) (product)
28335911000001108,Vanquoral 25mg capsules (Teva UK Ltd) (product)
28337411000001106,Vanquoral 50mg capsules (Teva UK Ltd) (product)
28338911000001102,Vanquoral 100mg capsules (Teva UK Ltd) (product)
28366311000001107,Mercaptopurine 30mg capsules (product)
28395011000001103,Ibrutinib 140mg capsules (product)
28397011000001105,Mercaptopurine 75mg tablets (Special Order) (product)
28415311000001105,Mercaptopurine 75mg tablets (product)
28469211000001103,Cyramza 500mg/50ml concentrate for solution for infusion vials (Eli Lilly and Company Ltd) (product)
284711000001102,Imuran 25mg tablets (GlaxoSmithKline) (product)
28770611000001108,Otezla 30mg tablets (Amgen Ltd) (product)
28770911000001102,Otezla 10mg tablets (Amgen Ltd) (product)
28771211000001100,Otezla 20mg tablets (Amgen Ltd) (product)
28782311000001106,Vargatef 100mg capsules (Boehringer Ingelheim Ltd) (product)
28782611000001101,Vargatef 150mg capsules (Boehringer Ingelheim Ltd) (product)
28789011000001101,Apremilast 10mg tablets (product)
28789111000001100,Apremilast 20mg tablets (product)
28789211000001106,Apremilast 30mg tablets (product)
28790211000001100,Nintedanib 100mg capsules (product)
28790311000001108,Nintedanib 150mg capsules (product)
28790411000001101,Ramucirumab 100mg/10ml solution for infusion vials (product)
28790511000001102,Ramucirumab 500mg/50ml solution for infusion vials (product)
28791311000001103,Cyramza 100mg/10ml concentrate for solution for infusion vials (Eli Lilly and Company Ltd) (product)
28791811000001107,Envarsus 1mg modified-release tablets (Chiesi Ltd) (product)
28792111000001105,Envarsus 750microgram modified-release tablets (Chiesi Ltd) (product)
28792411000001100,Envarsus 4mg modified-release tablets (Chiesi Ltd) (product)
28795911000001100,Temozolomide 5mg capsules (Actavis UK Ltd) (product)
28796111000001109,Temozolomide 20mg capsules (Actavis UK Ltd) (product)
28796311000001106,Temozolomide 100mg capsules (Actavis UK Ltd) (product)
28796511000001100,Temozolomide 140mg capsules (Actavis UK Ltd) (product)
28796711000001105,Temozolomide 180mg capsules (Actavis UK Ltd) (product)
28796911000001107,Temozolomide 250mg capsules (Actavis UK Ltd) (product)
28800611000001103,Adoport 0.75mg capsules (Sandoz Ltd) (product)
28800911000001109,Adoport 2mg capsules (Sandoz Ltd) (product)
28803711000001103,Remsima 100mg powder for concentrate for solution for infusion vials (Celltrion Healthcare UK Ltd) (product)
28808811000001101,Tacrolimus 1mg modified-release tablets (product)
28808911000001106,Tacrolimus 4mg modified-release tablets (product)
28809011000001102,Tacrolimus 750microgram modified-release tablets (product)
28883311000001103,Cyclophosphamide 2g powder for solution for injection vials (Sandoz Ltd) (product)
28926411000001102,Cyclophosphamide 1g powder for solution for injection vials (Sandoz Ltd) (product)
28943211000001105,Inflectra 100mg powder for concentrate for solution for infusion vials (Hospira UK Ltd) (product)
28947611000001104,Tacrolimus 2mg capsules (product)
28947711000001108,Tacrolimus 750microgram capsules (product)
28962711000001102,Fluorouracil 5g/100ml solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
28991611000001102,Methotrexate 50mg/2ml solution for injection vials (Accord Healthcare Ltd) (product)
29211611000001100,Secukinumab 150mg/1ml solution for injection pre-filled disposable devices (product)
29212511000001107,Cosentyx 150mg/1ml solution for injection pre-filled pens (Novartis Pharmaceuticals UK Ltd) (product)
29212711000001102,Secukinumab 150mg/1ml solution for injection pre-filled syringes (product)
29212911000001100,Cosentyx 150mg/1ml solution for injection pre-filled syringes (Novartis Pharmaceuticals UK Ltd) (product)
29224211000001105,Docetaxel 80mg/2.88ml concentrate for solution for infusion vials and diluent (A A H Pharmaceuticals Ltd) (product)
29507211000001103,Jakavi 10mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
29676311000001107,Halaven 1.32mg/3ml solution for injection vials (Eisai Ltd) (product)
29686811000001106,Eribulin 1320micrograms/3ml solution for injection vials (product)
29699211000001100,Certican 0.25mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
29699411000001101,Certican 0.75mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
29699711000001107,Certican 0.5mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
29701811000001108,Gemcitabine 1g/26.3ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
29702011000001105,Gemcitabine 200mg/5.3ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
29743711000001105,Topotecan 1mg/1ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
29743911000001107,Topotecan 4mg/4ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
29747111000001101,Orencia ClickJect 125mg/1ml solution for injection pre-filled pens (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
29747411000001106,Lynparza 50mg capsules (AstraZeneca UK Ltd) (product)
29759911000001108,Auranofin 3mg tablets (Special Order) (product)
29767011000001106,Abatacept 125mg/1ml solution for injection pre-filled disposable devices (product)
29768811000001101,Olaparib 50mg capsules (product)
29865011000001101,Lenvima 4mg capsules (Eisai Ltd) (product)
29865311000001103,Lenvima 10mg capsules (Eisai Ltd) (product)
29884411000001106,Leflunomide 10mg tablets (Sigma Pharmaceuticals Plc) (product)
29884611000001109,Leflunomide 20mg tablets (Sigma Pharmaceuticals Plc) (product)
29887311000001108,Opdivo 40mg/4ml concentrate for solution for infusion vials (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
29887611000001103,Opdivo 100mg/10ml concentrate for solution for infusion vials (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
29888911000001105,Lenvatinib 10mg capsules (product)
29889011000001101,Lenvatinib 4mg capsules (product)
29889111000001100,Nivolumab 100mg/10ml solution for infusion vials (product)
29889211000001106,Nivolumab 40mg/4ml solution for infusion vials (product)
29894911000001104,Revlimid 7.5mg capsules (Celgene Ltd) (product)
29895411000001108,Revlimid 20mg capsules (Celgene Ltd) (product)
29903711000001107,Lenalidomide 20mg capsules (product)
29903811000001104,Lenalidomide 7.5mg capsules (product)
29918911000001101,Methotrexate 2.5mg tablets (Sigma Pharmaceuticals Plc) (product)
29934411000001106,Busulfan 2mg tablets (Aspen Pharma Trading Ltd) (product)
29934611000001109,Vanquoral 10mg capsules (Teva UK Ltd) (product)
29956211000001103,Adoport 1mg capsules (Lexon (UK) Ltd) (product)
29960811000001107,Arava 10mg tablets (Lexon (UK) Ltd) (product)
29961011000001105,Arava 20mg tablets (Lexon (UK) Ltd) (product)
29983111000001105,Penicillamine 125mg tablets (Sigma Pharmaceuticals Plc) (product)
29997811000001108,Azathioprine 25mg tablets (Mawdsley-Brooks & Company Ltd) (product)
29998111000001100,Azathioprine 50mg tablets (Mawdsley-Brooks & Company Ltd) (product)
30005511000001109,Keytruda 50mg powder for concentrate for solution for infusion vials (Merck Sharp & Dohme Ltd) (product)
30033011000001108,Pembrolizumab 50mg powder for solution for infusion vials (product)
30033711000001105,Advagraf 1mg modified-release capsules (Waymade Healthcare Plc) (product)
30040911000001100,Advagraf 3mg modified-release capsules (Waymade Healthcare Plc) (product)
30074711000001109,Penicillamine 125mg tablets (DE Pharmaceuticals) (product)
30074911000001106,Penicillamine 250mg tablets (DE Pharmaceuticals) (product)
30089111000001104,Nivolumab BMS 40mg/4ml concentrate for solution for infusion vials (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
30089411000001109,Nivolumab BMS 100mg/10ml concentrate for solution for infusion vials (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
30108611000001106,Etoposide 100mg/5ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
30219011000001109,Leflunomide 10mg tablets (Mawdsley-Brooks & Company Ltd) (product)
303511000001103,Neoral 10mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
30595111000001100,Methotrexate 2mg/ml oral solution sugar free (Rosemont Pharmaceuticals Ltd) (product)
30758811000001108,Ceritinib 150mg capsules (product)
30759111000001108,Zykadia 150mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
30768311000001108,Ofev 100mg capsules (Boehringer Ingelheim Ltd) (product)
30768811000001104,Ofev 150mg capsules (Boehringer Ingelheim Ltd) (product)
30788811000001101,Temozolomide 5mg capsules (Accord Healthcare Ltd) (product)
30789111000001101,Temozolomide 20mg capsules (Accord Healthcare Ltd) (product)
30789911000001103,Temozolomide 100mg capsules (Accord Healthcare Ltd) (product)
30790111000001107,Temozolomide 140mg capsules (Accord Healthcare Ltd) (product)
30790311000001109,Temozolomide 180mg capsules (Accord Healthcare Ltd) (product)
30790611000001104,Temozolomide 250mg capsules (Accord Healthcare Ltd) (product)
30799911000001104,Methotrexate 10mg/5ml oral solution sugar free (product)
30816311000001105,Stelara 90mg/1ml solution for injection pre-filled syringes (Janssen-Cilag Ltd) (product)
30849511000001103,Mycophenolate mofetil 500mg tablets (Mawdsley-Brooks & Company Ltd) (product)
30920411000001100,Ustekinumab 90mg/1ml solution for injection pre-filled syringes (product)
30985211000001103,Methotrexate 2mg/ml oral solution sugar free (Alliance Healthcare (Distribution) Ltd) (product)
31000011000001104,Azathioprine 65mg/5ml oral suspension (Special Order) (product)
31002111000001104,Azathioprine 65mg/5ml oral suspension (product)
31065011000001106,Methotrexate 2mg/ml oral solution sugar free (A A H Pharmaceuticals Ltd) (product)
31079211000001108,Mekinist 2mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
31079711000001101,Mekinist 0.5mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
31088511000001109,Trametinib 500micrograms tablets (product)
31092211000001108,Cisplatin 100mg/100ml concentrate for solution for infusion vials (Sandoz Ltd) (product)
31092511000001106,Fludarabine phosphate 50mg/2ml concentrate for solution for injection vials (Sandoz Ltd) (product)
31138211000001109,Paclitaxel 100mg/16.7ml concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
31143211000001102,Carfilzomib 60mg powder for solution for infusion vials (product)
31143311000001105,Kyprolis 60mg powder for solution for infusion vials (Amgen Ltd) (product)
31143811000001101,Blinatumomab 38.5micrograms powder and solvent for solution for infusion vials (product)
31143911000001106,Blincyto 38.5micrograms powder and solvent for solution for infusion vials (Amgen Ltd) (product)
31258511000001108,HEXALEN 50mg capsules (Imported (United States)) (product)
31375911000001100,Pemetrexed 100mg/4ml solution for infusion vials (product)
31376011000001108,Pemetrexed 100mg/4ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
31382611000001105,Pemetrexed 500mg/20ml solution for infusion vials (product)
31382711000001101,Pemetrexed 500mg/20ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
31384111000001105,Pemetrexed 1g/40ml solution for infusion vials (product)
31384711000001106,Pemetrexed 1000mg/40ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
31406711000001106,Zlatal 20mg/0.8ml solution for injection pre-filled syringes (Nordic Pharma Ltd) (product)
31407211000001102,Zlatal 22.5mg/0.9ml solution for injection pre-filled syringes (Nordic Pharma Ltd) (product)
31407411000001103,Zlatal 25mg/1ml solution for injection pre-filled syringes (Nordic Pharma Ltd) (product)
31407911000001106,Zlatal 10mg/0.4ml solution for injection pre-filled syringes (Nordic Pharma Ltd) (product)
31408511000001100,Zlatal 7.5mg/0.3ml solution for injection pre-filled syringes (Nordic Pharma Ltd) (product)
31409011000001103,Zlatal 12.5mg/0.5ml solution for injection pre-filled syringes (Nordic Pharma Ltd) (product)
31409611000001105,Zlatal 15mg/0.6ml solution for injection pre-filled syringes (Nordic Pharma Ltd) (product)
31410211000001104,Zlatal 17.5mg/0.7ml solution for injection pre-filled syringes (Nordic Pharma Ltd) (product)
31508511000001107,Mercaptopurine 75mg capsules (Special Order) (product)
31535311000001101,Mercaptopurine 75mg capsules (product)
318611000001108,Immunoprin 50mg tablets (Ashbourne Pharmaceuticals Ltd) (product)
31880111000001103,Busulfan 2mg tablets (Alliance Healthcare (Distribution) Ltd) (product)
319211000001101,Neoral 50mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
32149811000001100,Antithymocyte immunoglobulin (equine) 250mg/5ml solution for infusion ampoules (product)
32150511000001109,Atgam 250mg/5ml solution for infusion ampoules (Imported (United States)) (product)
32189011000001104,Antithymocyte immunoglobulin (rabbit) 100mg/5ml solution for infusion vials (product)
32189711000001102,ATG-Fresenius S 100mg/5ml concentrate for solution for infusion vials (Imported (Germany)) (product)
322011000001106,Maxtrex 10mg tablets (Pfizer Ltd) (product)
32227111000001100,Benepali 50mg/1ml solution for injection pre-filled syringes (Biogen Idec Ltd) (product)
32230111000001103,Benepali 50mg/1ml solution for injection pre-filled pens (Biogen Idec Ltd) (product)
32424411000001104,Mycophenolate mofetil 250mg capsules (Kent Pharmaceuticals Ltd) (product)
32424611000001101,Mycophenolate mofetil 500mg tablets (Kent Pharmaceuticals Ltd) (product)
32642811000001109,Bendamustine 25mg powder for concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
32643011000001107,Bendamustine 100mg powder for concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
326723005,Product containing precisely busulfan 2 milligram/1 each conventional release oral tablet (clinical drug)
326726002,Carmustine 100mg powder and solvent for infusion vial (product)
326729009,Product containing precisely chlorambucil 2 milligram/1 each conventional release oral tablet (clinical drug)
326731000,Product containing precisely cyclophosphamide 50 milligram/1 each conventional release oral tablet (clinical drug)
326733002,Product containing precisely cyclophosphamide (as cyclophosphamide monohydrate) 200 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326734008,Product containing precisely cyclophosphamide (as cyclophosphamide monohydrate) 500 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326735009,Product containing precisely cyclophosphamide (as cyclophosphamide monohydrate) 1 gram/1 vial powder for conventional release solution for injection (clinical drug)
326747003,Product containing precisely estramustine phosphate (as estramustine phosphate sodium) 140 milligram/1 each conventional release oral capsule (clinical drug)
326755005,Product containing precisely ifosfamide 1 gram/1 vial powder for conventional release solution for injection (clinical drug)
326756006,Product containing precisely ifosfamide 2 gram/1 vial powder for conventional release solution for injection (clinical drug)
326760009,Product containing precisely lomustine 40 milligram/1 each conventional release oral capsule (clinical drug)
326765004,Melphalan 50mg powder and solvent for injection solution vial (product)
326766003,Product containing precisely melphalan 2 milligram/1 each conventional release oral tablet (clinical drug)
326773008,Product containing precisely thiotepa 15 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326775001,Product containing precisely treosulfan 250 milligram/1 each conventional release oral capsule (clinical drug)
326776000,Treosulfan 5g infusion (pdr for recon)+diluent+kit (product)
326778004,Product containing precisely treosulfan 1 gram/1 vial powder for conventional release solution for injection (clinical drug)
326781009,Product containing precisely dactinomycin 500 microgram/1 vial powder for conventional release solution for injection (clinical drug)
326788003,Product containing precisely doxorubicin hydrochloride 10 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326789006,Product containing precisely doxorubicin hydrochloride 50 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326790002,Liposomal doxorubicin hydrochloride 2mg/mL infusion concentrate 10mL vial (product)
326802005,Epirubicin hydrochloride 2mg/mL infusion solution 5mL vial (product)
326803000,Epirubicin hydrochloride 50mg/25mL injection (product)
326806008,Product containing precisely epirubicin hydrochloride 10 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326807004,Product containing precisely epirubicin hydrochloride 20 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326808009,Product containing precisely epirubicin hydrochloride 50 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326813008,Mitomycin 40mg powder for intravesical solution vials (product)
326814002,Product containing precisely mitomycin 20 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326815001,Product containing precisely mitomycin 10 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326816000,Product containing precisely mitomycin 2 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326820001,Product containing precisely idarubicin hydrochloride 5 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326821002,Product containing precisely idarubicin hydrochloride 10 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326827003,Product containing precisely idarubicin hydrochloride 5 milligram/1 each conventional release oral capsule (clinical drug)
326828008,Product containing precisely idarubicin hydrochloride 10 milligram/1 each conventional release oral capsule (clinical drug)
326829000,Product containing precisely idarubicin hydrochloride 25 milligram/1 each conventional release oral capsule (clinical drug)
326835000,Product containing precisely daunorubicin (as daunorubicin hydrochloride) 20 milligram/1 vial powder for conventional release solution for injection (clinical drug)
32683711000001104,Bendamustine 25mg powder for concentrate for solution for infusion vials (medac UK) (product)
32684011000001104,Bendamustine 100mg powder for concentrate for solution for infusion vials (medac UK) (product)
326843005,Cytarabine 100mg/mL injection solution 5mL vial (product)
326844004,Cytarabine 100mg/mL injection solution 20mL vial (product)
326849009,Cytarabine 20mg/mL injection solution 25mL vial (product)
326853006,Cytarabine 100mg/mL injection solution 1mL vial (product)
326854000,Cytarabine 100mg/mL injection solution 10mL vial (product)
326861001,Fluorouracil 25mg/mL injection solution 100mL vial (product)
326863003,Fluorouracil 500mg/10mL injection (product)
326866006,Fluorouracil 50mg/mL injection solution 50mL (product)
32686711000001106,Bendamustine 25mg powder for concentrate for solution for infusion vials (Actavis UK Ltd) (product)
326868007,Fluorouracil 25mg/mL injection solution 10mL vial (product)
326869004,Product containing precisely fluorouracil 250 milligram/1 each conventional release oral capsule (clinical drug)
326871004,Fluorouracil 25mg/mL injection solution 20mL vial (product)
32687111000001108,Bendamustine 100mg powder for concentrate for solution for infusion vials (Actavis UK Ltd) (product)
326873001,Product containing precisely mercaptopurine 50 milligram/1 each conventional release oral tablet (clinical drug)
326874007,Product containing precisely methotrexate 2.5 milligram/1 each conventional release oral tablet (clinical drug)
326875008,Product containing precisely methotrexate 10 milligram/1 each conventional release oral tablet (clinical drug)
326877000,Methotrexate 2.5mg/mL injection solution 2mL vial (product)
326879002,Methotrexate 25mg/mL injection solution 2mL vial (product)
326881000,Methotrexate 25mg/mL injection solution 8mL vial (product)
326882007,Methotrexate 25mg/mL injection solution 20mL vial (product)
326883002,Methotrexate 25mg/mL injection solution 40mL vial (product)
326884008,Methotrexate 25mg/mL injection solution 200mL vial (product)
326905008,Methotrexate 100mg/mL injection solution 10mL vial (product)
326906009,Methotrexate 100mg/mL injection solution 50mL vial (product)
326908005,Product containing precisely tioguanine 40 milligram/1 each conventional release oral tablet (clinical drug)
326909002,Product containing precisely gemcitabine (as gemcitabine hydrochloride) 200 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326910007,Product containing precisely gemcitabine (as gemcitabine hydrochloride) 1 gram/1 vial powder for conventional release solution for injection (clinical drug)
326916001,Product containing precisely raltitrexed 2 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326924006,Product containing precisely etoposide (as etoposide phosphate) 100 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326925007,Product containing precisely etoposide 50 milligram/1 each conventional release oral capsule (clinical drug)
326926008,Product containing precisely etoposide 100 milligram/1 each conventional release oral capsule (clinical drug)
326927004,Etoposide 100mg/5mL injection concentrate (product)
326931005,Vinblastine sulfate 10mg injection (pdr for recon)+diluent (product)
326932003,Vinblastine sulfate 10mg/10mL injection (product)
326944000,Vincristine sulfate 5mg/5mL injection (product)
326945004,Vincristine sulfate 1mg/1mL injection (product)
326946003,Vincristine sulfate 2mg/2mL injection (product)
326949005,Product containing precisely vindesine sulfate 5 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326950005,Vinorelbine 10mg/1mL intravenous solution (product)
326951009,Vinorelbine 50mg/5mL intravenous solution (product)
326957008,Amsacrine 5mg/mL infusion concentrate 15mL vial (product)
326989004,Product containing precisely dacarbazine (as dacarbazine citrate) 200 milligram/1 vial powder for conventional release solution for injection (clinical drug)
326991007,Product containing precisely hydroxycarbamide 500 milligram/1 each conventional release oral capsule (clinical drug)
327002004,Product containing precisely procarbazine (as procarbazine hydrochloride) 50 milligram/1 each conventional release oral capsule (clinical drug)
327004003,Product containing precisely razoxane 125 milligram/1 each conventional release oral tablet (clinical drug)
327005002,Product containing precisely asparaginase (as crisantaspase) 10000 unit/1 vial powder for conventional release solution for injection (clinical drug)
327008000,Product containing precisely pentostatin 10 milligram/1 vial powder for conventional release solution for injection (clinical drug)
327016009,Product containing precisely fludarabine phosphate 50 milligram/1 vial powder for conventional release solution for injection (clinical drug)
327017000,Cladribine 1mg/mL infusion concentrate 10mL vial (product)
327023005,Product containing precisely topotecan (as topotecan hydrochloride) 4 milligram/1 vial powder for conventional release solution for injection (clinical drug)
327025003,Irinotecan hydrochloride trihydrate 20mg/mL infusion concentrate 2mL vial (product)
327026002,Irinotecan hydrochloride trihydrate 20mg/mL infusion concentrate 5mL vial (product)
327030004,Product containing precisely altretamine 50 milligram/1 each conventional release oral capsule (clinical drug)
327035009,Product containing precisely oxaliplatin 50 milligram/1 vial powder for conventional release solution for injection (clinical drug)
327036005,Product containing precisely oxaliplatin 100 milligram/1 vial powder for conventional release solution for injection (clinical drug)
327042009,Product containing precisely temozolomide 5 milligram/1 each conventional release oral capsule (clinical drug)
327043004,Product containing precisely temozolomide 20 milligram/1 each conventional release oral capsule (clinical drug)
327044005,Product containing precisely temozolomide 100 milligram/1 each conventional release oral capsule (clinical drug)
327045006,Product containing precisely temozolomide 250 milligram/1 each conventional release oral capsule (clinical drug)
327048008,Product containing precisely verteporfin 15 milligram/1 vial powder for conventional release solution for injection (clinical drug)
327070006,Product containing precisely azathioprine 50 milligram/1 each conventional release oral tablet (clinical drug)
327071005,Product containing precisely azathioprine 25 milligram/1 each conventional release oral tablet (clinical drug)
327072003,Product containing precisely azathioprine 50 milligram/1 vial powder for conventional release solution for injection (clinical drug)
327082002,Product containing precisely ciclosporin 25 milligram/1 each conventional release oral capsule (clinical drug)
327083007,Product containing precisely ciclosporin 100 milligram/1 each conventional release oral capsule (clinical drug)
327085000,Product containing precisely ciclosporin 50 milligram/1 each conventional release oral capsule (clinical drug)
327090002,Product containing precisely ciclosporin 10 milligram/1 each conventional release oral capsule (clinical drug)
327093000,Cyclosporin 100mg/mL s/f oral solution (product)
327094006,Cyclosporin 50mg/1mL oily infusion concentrate (product)
327095007,Cyclosporin 250mg/5mL oily infusion concentrate (product)
327096008,Product containing precisely tacrolimus 1 milligram/1 each conventional release oral capsule (clinical drug)
327097004,Product containing precisely tacrolimus 5 milligram/1 each conventional release oral capsule (clinical drug)
327098009,Tacrolimus 5mg/mL infusion concentrate 1mL ampule (product)
327103006,Product containing precisely tacrolimus 500 microgram/1 each conventional release oral capsule (clinical drug)
327104000,Product containing precisely mycophenolate mofetil 250 milligram/1 each conventional release oral capsule (clinical drug)
327106003,Product containing precisely mycophenolate mofetil 500 milligram/1 each conventional release oral tablet (clinical drug)
327109005,Product containing precisely mycophenolate mofetil (as mycophenolate mofetil hydrochloride) 500 milligram/1 vial powder for conventional release solution for injection (clinical drug)
32711411000001100,Oxaliplatin 200mg/40ml concentrate for solution for infusion vials (Hospira UK Ltd) (product)
327235003,Daclizumab 25mg/5mL infusion concentrate (product)
327393005,Rituximab 10mg/mL injection concentrate 10mL vial (product)
327394004,Rituximab 10mg/mL infusion concentrate 50mL vial (product)
327399009,Product containing precisely trastuzumab 150 milligram/1 vial powder for conventional release solution for injection (clinical drug)
32774711000001101,Gemcitabine 200mg/5ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
32775011000001104,Gemcitabine 1g/25ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
32775311000001101,Gemcitabine 2g/50ml concentrate for solution for infusion vials (Actavis UK Ltd) (product)
32780911000001103,Gemcitabine 1g/25ml solution for infusion vials (product)
32781011000001106,Gemcitabine 200mg/5ml solution for infusion vials (product)
32781111000001107,Gemcitabine 2g/50ml solution for infusion vials (product)
32786611000001106,Bendamustine 25mg powder for concentrate for solution for infusion vials (Dr Reddy's Laboratories (UK) Ltd) (product)
32786911000001100,Bendamustine 100mg powder for concentrate for solution for infusion vials (Dr Reddy's Laboratories (UK) Ltd) (product)
32881711000001106,Humira 40mg/0.4ml solution for injection pre-filled pens (AbbVie Ltd) (product)
32882011000001101,Humira 40 mg/0.4ml solution for injection pre-filled syringes (AbbVie Ltd) (product)
32888111000001102,Adalimumab 40mg/0.4ml solution for injection pre-filled disposable devices (product)
32888211000001108,Adalimumab 40mg/0.4ml solution for injection pre-filled syringes (product)
32903411000001108,Gemcitabine 1g/25ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
32903611000001106,Gemcitabine 2g/50ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
32903811000001105,Gemcitabine 200mg/5ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
330021002,Sodium aurothiomalate 10mg/0.5mL injection (product)
330022009,Sodium aurothiomalate 20mg/0.5mL injection (product)
330023004,Sodium aurothiomalate 50mg/0.5mL injection (product)
330026007,Product containing precisely penicillamine 125 milligram/1 each conventional release oral tablet (clinical drug)
330027003,Product containing precisely penicillamine 250 milligram/1 each conventional release oral tablet (clinical drug)
330041007,Product containing precisely auranofin 3 milligram/1 each conventional release oral tablet (clinical drug)
330057007,Product containing precisely leflunomide 10 milligram/1 each conventional release oral tablet (clinical drug)
330058002,Product containing precisely leflunomide 20 milligram/1 each conventional release oral tablet (clinical drug)
330059005,Product containing precisely leflunomide 100 milligram/1 each conventional release oral tablet (clinical drug)
33087411000001104,Flixabi 100mg powder for concentrate for solution for infusion vials (Biogen Idec Ltd) (product)
33155511000001107,Bendamustine 25mg powder for concentrate for solution for infusion vials (Zentiva) (product)
33156111000001109,Bendamustine 100mg powder for concentrate for solution for infusion vials (Zentiva) (product)
33254711000001104,Pemetrexed 100mg powder for concentrate for solution for infusion vials (Dr Reddy's Laboratories (UK) Ltd) (product)
33255911000001103,Pemetrexed 500mg powder for concentrate for solution for infusion vials (Dr Reddy's Laboratories (UK) Ltd) (product)
33341411000001104,Mycophenolate mofetil 500mg powder for concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
33420911000001109,Oxaliplatin 50mg/10ml concentrate for solution for infusion vials (medac UK) (product)
33421111000001100,Oxaliplatin 100mg/20ml concentrate for solution for infusion vials (medac UK) (product)
33421311000001103,Oxaliplatin 200mg/40ml concentrate for solution for infusion vials (medac UK) (product)
33491311000001109,Gemcitabine 1.2g/120ml infusion bags (Sun Pharmaceuticals UK Ltd) (product)
33491511000001103,Gemcitabine 1.2g/120ml infusion bags (product)
33491611000001104,Gemcitabine 1.6g/160ml infusion bags (product)
33491811000001100,Gemcitabine 1.6g/160ml infusion bags (Sun Pharmaceuticals UK Ltd) (product)
33492011000001103,Gemcitabine 1.8g/180ml infusion bags (product)
33492211000001108,Gemcitabine 1.8g/180ml infusion bags (Sun Pharmaceuticals UK Ltd) (product)
33492511000001106,Gemcitabine 2g/200ml infusion bags (product)
33492811000001109,Gemcitabine 2g/200ml infusion bags (Sun Pharmaceuticals UK Ltd) (product)
33493311000001105,Gemcitabine 2.2g/220ml infusion bags (product)
33493511000001104,Gemcitabine 2.2g/220ml infusion bags (Sun Pharmaceuticals UK Ltd) (product)
33511811000001109,Cimzia 200mg/1ml solution for injection pre-filled pens (UCB Pharma Ltd) (product)
33523711000001105,Certolizumab pegol 200mg/1ml solution for injection pre-filled disposable devices (product)
33529111000001107,Epirubicin 30mg/15ml solution for injection pre-filled syringes (product)
33529311000001109,Epirubicin 30mg/15ml solution for injection pre-filled syringes (Special Order) (product)
33561411000001108,Kisplyx 4mg capsules (Eisai Ltd) (product)
33561611000001106,Kisplyx 10mg capsules (Eisai Ltd) (product)
33579311000001108,Penicillamine 250mg/5ml oral suspension (Special Order) (product)
33592411000001101,Leflunomide 10mg tablets (Mylan Ltd) (product)
33592811000001104,Leflunomide 20mg tablets (Mylan Ltd) (product)
33596211000001104,Penicillamine 250mg/5ml oral suspension (product)
33602811000001108,Fluorouracil 1000mg/40ml solution for injection pre-filled syringes (Special Order) (product)
33603111000001107,Fluorouracil 1.1g/44ml solution for injection pre-filled syringes (Special Order) (product)
33603411000001102,Fluorouracil 1.2g/48ml solution for injection pre-filled syringes (Special Order) (product)
33603711000001108,Fluorouracil 200mg/8ml solution for injection pre-filled syringes (Special Order) (product)
33604111000001109,Fluorouracil 500mg/20ml solution for injection pre-filled syringes (Special Order) (product)
33604511000001100,Fluorouracil 600mg/24ml solution for injection pre-filled syringes (Special Order) (product)
33605011000001107,Fluorouracil 800mg/32ml solution for injection pre-filled syringes (Special Order) (product)
33605511000001104,Fluorouracil 900mg/36ml solution for injection pre-filled syringes (Special Order) (product)
33605911000001106,Fluorouracil 950mg/38ml solution for injection pre-filled syringes (Special Order) (product)
336111000001109,Penicillamine 250mg tablets (A A H Pharmaceuticals Ltd) (product)
33618311000001103,Fluorouracil 1.1g/44ml solution for injection pre-filled syringes (product)
33618411000001105,Fluorouracil 1.2g/48ml solution for injection pre-filled syringes (product)
33618511000001109,Fluorouracil 1000mg/40ml solution for injection pre-filled syringes (product)
33618711000001104,Fluorouracil 200mg/8ml solution for injection pre-filled syringes (product)
33618811000001107,Fluorouracil 500mg/20ml solution for injection pre-filled syringes (product)
33618911000001102,Fluorouracil 600mg/24ml solution for injection pre-filled syringes (product)
33619011000001106,Fluorouracil 800mg/32ml solution for injection pre-filled syringes (product)
33619111000001107,Fluorouracil 900mg/36ml solution for injection pre-filled syringes (product)
33619211000001101,Fluorouracil 950mg/38ml solution for injection pre-filled syringes (product)
33622811000001100,Cabometyx 20mg tablets (Ipsen Ltd) (product)
33623111000001101,Cabometyx 40mg tablets (Ipsen Ltd) (product)
33630911000001109,Cabozantinib 20mg tablets (product)
33631011000001101,Cabozantinib 40mg tablets (product)
33632811000001103,Cabometyx 60mg tablets (Ipsen Ltd) (product)
33655111000001104,Capecitabine 150mg tablets (Morningside Healthcare Ltd) (product)
33655711000001103,Capecitabine 500mg tablets (Morningside Healthcare Ltd) (product)
33657311000001105,Cabozantinib 60mg tablets (product)
33749511000001100,Stelara 130mg/26ml concentrate for solution for infusion vials (Janssen-Cilag Ltd) (product)
33749811000001102,Ustekinumab 130mg/26ml solution for infusion vials (product)
33750211000001108,Imatinib 400mg tablets (Teva UK Ltd) (product)
33750411000001107,Imatinib 100mg tablets (Teva UK Ltd) (product)
33756811000001106,Zinbryta 150mg/1ml solution for injection pre-filled pens (Biogen Idec Ltd) (product)
33757711000001100,Imatinib 100mg tablets (Actavis UK Ltd) (product)
33757911000001103,Imatinib 400mg tablets (Actavis UK Ltd) (product)
33760311000001105,Daclizumab 150mg/1ml solution for injection pre-filled disposable devices (product)
33760511000001104,Imatinib 100mg tablets (Intrapharm Laboratories Ltd) (product)
33760711000001109,Imatinib 400mg tablets (Intrapharm Laboratories Ltd) (product)
338311000001105,Azathioprine 25mg tablets (Kent Pharmaceuticals Ltd) (product)
33866911000001106,Imatinib 100mg tablets (A A H Pharmaceuticals Ltd) (product)
33867211000001100,Imatinib 400mg tablets (A A H Pharmaceuticals Ltd) (product)
33931011000001102,Imatinib 100mg tablets (Wockhardt UK Ltd) (product)
33959611000001106,Imatinib 400mg tablets (Wockhardt UK Ltd) (product)
339911000001103,Azathioprine 50mg tablets (Alpharma Limited) (product)
34006211000001102,Carmustine 100mg powder and solvent for solution for infusion vials (Emcure Pharma UK Ltd) (product)
34024011000001105,Imatinib 100mg capsules (Dr Reddy's Laboratories (UK) Ltd) (product)
34024411000001101,Imatinib 400mg capsules (Dr Reddy's Laboratories (UK) Ltd) (product)
34025211000001104,Imatinib 100mg tablets (Dr Reddy's Laboratories (UK) Ltd) (product)
34025411000001100,Imatinib 400mg tablets (Dr Reddy's Laboratories (UK) Ltd) (product)
34034411000001103,Imatinib 100mg tablets (Accord Healthcare Ltd) (product)
34034611000001100,Imatinib 400mg tablets (Accord Healthcare Ltd) (product)
34103311000001106,Onivyde pegylated liposomal 43mg/10ml concentrate for solution for infusion vials (Servier Laboratories Ltd) (product)
34155811000001108,Irinotecan pegylated liposomal 43mg/10ml solution for infusion vials (product)
34161711000001105,Nordimet 7.5mg/0.3ml solution for injection pre-filled pens (Nordic Pharma Ltd) (product)
34162611000001107,Nordimet 10mg/0.4ml solution for injection pre-filled pens (Nordic Pharma Ltd) (product)
34162911000001101,Nordimet 12.5mg/0.5ml solution for injection pre-filled pens (Nordic Pharma Ltd) (product)
34163211000001104,Nordimet 15mg/0.6ml solution for injection pre-filled pens (Nordic Pharma Ltd) (product)
34163511000001101,Nordimet 17.5mg/0.7ml solution for injection pre-filled pens (Nordic Pharma Ltd) (product)
34163811000001103,Nordimet 20mg/0.8ml solution for injection pre-filled pens (Nordic Pharma Ltd) (product)
34164111000001107,Nordimet 22.5mg/0.9ml solution for injection pre-filled pens (Nordic Pharma Ltd) (product)
34164411000001102,Nordimet 25mg/1ml solution for injection pre-filled pens (Nordic Pharma Ltd) (product)
34164811000001100,Votubia 2mg dispersible tablets (Novartis Pharmaceuticals UK Ltd) (product)
34165111000001106,Votubia 3mg dispersible tablets (Novartis Pharmaceuticals UK Ltd) (product)
34165411000001101,Votubia 5mg dispersible tablet (Novartis Pharmaceuticals UK Ltd) (product)
34165611000001103,Truxima 500mg/50ml concentrate for solution for infusion vials (Napp Pharmaceuticals Ltd) (product)
34166411000001105,Imatinib 100mg tablets (Sandoz Ltd) (product)
34166611000001108,Imatinib 400mg tablets (Sandoz Ltd) (product)
34167311000001100,Everolimus 2mg dispersible tablets sugar free (product)
34167411000001107,Everolimus 3mg dispersible tablets sugar free (product)
34167511000001106,Everolimus 5mg dispersible tablets sugar free (product)
34167711000001101,Methotrexate 10mg/0.4ml solution for injection pre-filled disposable devices (product)
34167811000001109,Methotrexate 12.5mg/0.5ml solution for injection pre-filled disposable devices (product)
34167911000001104,Methotrexate 15mg/0.6ml solution for injection pre-filled disposable devices (product)
34168011000001102,Methotrexate 17.5mg/0.7ml solution for injection pre-filled disposable devices (product)
34168111000001101,Methotrexate 20mg/0.8ml solution for injection pre-filled disposable devices (product)
34168211000001107,Methotrexate 22.5mg/0.9ml solution for injection pre-filled disposable devices (product)
34168311000001104,Methotrexate 25mg/1ml solution for injection pre-filled disposable devices (product)
34168411000001106,Methotrexate 7.5mg/0.3ml solution for injection pre-filled disposable devices (product)
34177311000001109,Cisplatin 50mg/50ml concentrate for solution for infusion vials (Sandoz Ltd) (product)
34177511000001103,Cisplatin 10mg/10ml concentrate for solution for infusion vials (Sandoz Ltd) (product)
34177711000001108,Cyclophosphamide 500mg powder for solution for injection vials (Sandoz Ltd) (product)
34187811000001107,Imatinib 100mg capsules (A A H Pharmaceuticals Ltd) (product)
34191511000001102,Cytarabine 4g/40ml solution for injection vials (Accord Healthcare Ltd) (product)
34191811000001104,Cytarabine 5g/50ml solution for infusion vials (Accord Healthcare Ltd) (product)
34199111000001105,Cytarabine 4g/40ml solution for injection vials (product)
34199211000001104,Cytarabine 5g/50ml solution for infusion vials (product)
34209411000001100,Imatinib 100mg tablets (Mylan Ltd) (product)
34210011000001103,Imatinib 400mg tablets (Mylan Ltd) (product)
34228111000001105,Oxaliplatin 50mg/10ml concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
34228811000001103,Oxaliplatin 100mg/20ml concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
34229511000001107,Etoposide 500mg/25ml concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
34238111000001108,Tioguanine 50mg/5ml oral suspension (product)
34238311000001105,Tioguanine 50mg/5ml oral suspension (Special Order) (product)
34349311000001108,Keytruda 100mg/4ml concentrate for solution for infusion vials (Merck Sharp & Dohme Ltd) (product)
34378411000001105,Pembrolizumab 100mg/4ml solution for infusion vials (product)
34468011000001101,Mercaptopurine 50mg tablets (A A H Pharmaceuticals Ltd) (product)
34497511000001107,Vincristine 2mg/50ml infusion bags (product)
34497711000001102,Vincristine 2mg/50ml infusion bags (Special Order) (product)
34530511000001106,Carfilzomib 10mg powder for solution for infusion vials (product)
34530811000001109,Kyprolis 10mg powder for solution for infusion vials (Amgen Ltd) (product)
34531211000001102,Carfilzomib 30mg powder for solution for infusion vials (product)
34531411000001103,Kyprolis 30mg powder for solution for infusion vials (Amgen Ltd) (product)
34559211000001100,Docetaxel 160mg/8ml concentrate for solution for infusion vials (A A H Pharmaceuticals Ltd) (product)
34575711000001108,Paclitaxel 150mg/25ml concentrate for solution for infusion vials (Alliance Healthcare (Distribution) Ltd) (product)
34576411000001106,Nibix 100mg capsules (Rivopharm (UK) Ltd) (product)
34576611000001109,Nibix 400mg capsules (Rivopharm (UK) Ltd) (product)
34609111000001108,Benepali 25mg/0.5ml solution for injection pre-filled syringes (Biogen Idec Ltd) (product)
34613711000001108,Truxima 100mg/10ml concentrate for solution for infusion vials (Napp Pharmaceuticals Ltd) (product)
34623211000001105,Esbriet 267mg tablets (Roche Products Ltd) (product)
34623711000001103,Esbriet 801mg tablets (Roche Products Ltd) (product)
34625511000001107,Pirfenidone 267mg tablets (product)
34625611000001106,Pirfenidone 801mg tablets (product)
34632811000001101,Mitomycin 20mg powder and solvent for intravesical solution vials (product)
34633111000001102,Mitomycin 20mg powder and solvent for intravesical solution vials (medac UK) (product)
34633311000001100,Mitomycin 40mg powder and solvent for intravesical solution vials (product)
34633511000001106,Mitomycin 40mg powder and solvent for intravesical solution vials (medac UK) (product)
34633711000001101,Erelzi 25mg/0.5ml solution for injection pre-filled syringes (Sandoz Ltd) (product)
34633911000001104,Erelzi 50mg/1ml solution for injection pre-filled syringes (Sandoz Ltd) (product)
34634111000001100,Erelzi 50mg/1ml solution for injection pre-filled pens (Sandoz Ltd) (product)
34634311000001103,Rixathon 100mg/10ml concentrate for solution for infusion vials (Sandoz Ltd) (product)
34634611000001108,Rixathon 500mg/50ml concentrate for solution for infusion vials (Sandoz Ltd) (product)
346418000,Equine anti-human thymocyte immunoglobulin 20mg/mL injection solution 5mL vial (product)
34692611000001105,Anagrelide 0.5mg capsules (Consilient Health Ltd) (product)
34703111000001100,Idarubicin 5mg/5ml solution for injection vials (Accord Healthcare Ltd) (product)
34704011000001104,Idarubicin 10mg/10ml solution for injection vials (Accord Healthcare Ltd) (product)
34705011000001100,Mitoxantrone 20mg/10ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
34709711000001101,Anagrelide 500microgram capsules (Alliance Healthcare (Distribution) Ltd) (product)
34713011000001104,Anagrelide 500microgram capsules (A A H Pharmaceuticals Ltd) (product)
34717811000001104,Zydelig 100mg tablets (Gilead Sciences Ireland UC) (product)
34718311000001109,Zydelig 150mg tablets (Gilead Sciences Ireland UC) (product)
34737911000001102,Mitomycin 2mg powder for solution for injection vials (Accord Healthcare Ltd) (product)
34738111000001104,Mitomycin 10mg powder for solution for injection vials (Accord Healthcare Ltd) (product)
34738311000001102,Mitomycin 20mg powder for solution for injection vials (Accord Healthcare Ltd) (product)
347400007,Epirubicin hydrochloride 2mg/mL infusion solution 100mL vial (product)
34776411000001105,Methofill 7.5mg/0.15ml solution for injection pre-filled injector (Accord Healthcare Ltd) (product)
34776911000001102,Methofill 10mg/0.2ml solution for injection pre-filled injector (Accord Healthcare Ltd) (product)
34777111000001102,Methofill 15mg/0.3ml solution for injection pre-filled injector (Accord Healthcare Ltd) (product)
34777311000001100,Methofill 12.5mg/0.25ml solution for injection pre-filled injector (Accord Healthcare Ltd) (product)
34777611000001105,Methofill 17.5mg/0.35ml solution for injection pre-filled injector (Accord Healthcare Ltd) (product)
34777811000001109,Methofill 20mg/0.4ml solution for injection pre-filled injector (Accord Healthcare Ltd) (product)
34778011000001102,Methofill 22.5mg/0.45ml solution for injection pre-filled injector (Accord Healthcare Ltd) (product)
34778211000001107,Methofill 25mg/0.5ml solution for injection pre-filled injector (Accord Healthcare Ltd) (product)
34778411000001106,Methofill 27.5mg/0.55ml solution for injection pre-filled injector (Accord Healthcare Ltd) (product)
34778611000001109,Methofill 30mg/0.6ml solution for injection pre-filled injector (Accord Healthcare Ltd) (product)
347811000001104,Sandimmun 25mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
34782411000001102,Busulfan 2mg tablets (A A H Pharmaceuticals Ltd) (product)
34791011000001104,Mavenclad 10mg tablets (Merck Serono Ltd) (product)
34794011000001101,Iclusig 30mg tablets (Incyte Biosciences UK Ltd) (product)
34796711000001108,Cladribine 10mg tablets (product)
34809211000001105,Ceptava 180mg gastro-resistant tablets (Sandoz Ltd) (product)
34809411000001109,Ceptava 360mg gastro-resistant tablets (Sandoz Ltd) (product)
34819011000001103,Ponatinib 30mg tablets (product)
34824311000001107,Docetaxel 160mg/8ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
34834011000001106,Enbrel 25mg/0.5ml solution for injection pre-filled MyClic pens (Pfizer Ltd) (product)
34840511000001108,Etanercept 25mg/0.5ml solution for injection pre-filled disposable devices (product)
34871011000001105,Jylamvo 2mg/ml oral solution (Intrapharm Laboratories Ltd) (product)
34871211000001100,Cosentyx 150mg/1ml solution for injection pre-filled syringes (Novartis Pharmaceuticals UK Ltd) (product)
3490411000001109,Neoral 100mg/ml oral solution (Novartis Pharmaceuticals UK Ltd) (product)
3490711000001103,Sandimmun 100mg/ml oral solution (Novartis Pharmaceuticals UK Ltd) (product)
34912911000001104,Anagrelide 500microgram capsules (Teva UK Ltd) (product)
34932711000001105,Mycophenolic acid 180mg gastro-resistant tablets (Accord Healthcare Ltd) (product)
34932911000001107,Mycophenolic acid 360mg gastro-resistant tablets (Accord Healthcare Ltd) (product)
34956611000001101,Methotrexate 2.5mg tablets (Almus Pharmaceuticals Ltd) (product)
35014411000001103,Clofarabine 20mg/20ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
35035511000001109,Ilaris 150mg/1ml solution for injection vials (Novartis Pharmaceuticals UK Ltd) (product)
35057111000001105,5-Aminolevulinic acid 8mg medicated plasters (product)
35057211000001104,Alacare 8mg medicated plasters (medac UK) (product)
35086111000001103,Canakinumab 150mg/1ml solution for injection vials (product)
35201011000001102,Ontruzant 150mg powder for concentrate for solution for infusion vials (Merck Sharp & Dohme Ltd) (product)
35206711000001106,Capsorin 100mg/ml oral solution (Morningside Healthcare Ltd) (product)
35209811000001109,Procarbazine 150mg/5ml oral suspension (product)
35209911000001104,Procarbazine 150mg/5ml oral suspension (Special Order) (product)
35245311000001107,Imatinib 100mg tablets (Milpharm Ltd) (product)
35245511000001101,Imatinib 400mg tablets (Milpharm Ltd) (product)
35314211000001101,Oxaliplatin 225mg/500ml in Glucose 5% infusion bags (product)
35314311000001109,Oxaliplatin 225mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35315311000001108,Humira 20mg/0.2ml solution for injection pre-filled syringes (AbbVie Ltd) (product)
35315711000001107,Oxaliplatin 250mg/500ml in Glucose 5% infusion bags (product)
35315811000001104,Oxaliplatin 250mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35316111000001100,Oxaliplatin 280mg/500ml in Glucose 5% infusion bags (product)
35316211000001106,Oxaliplatin 280mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35317011000001103,Vincristine 1mg/50ml in Sodium chloride 0.9% infusion bags (product)
35317111000001102,Vincristine 1mg/50ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35317711000001101,Carboplatin 270mg/500ml in Glucose 5% infusion bags (product)
35317811000001109,Carboplatin 270mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35318111000001101,Carboplatin 300mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35318411000001106,Carboplatin 300mg/500ml in Glucose 5% infusion bags (product)
35318811000001108,Adalimumab 20mg/0.2ml solution for injection pre-filled syringes (product)
35320211000001103,Vinblastine 10mg/50ml in Sodium chloride 0.9% infusion bags (product)
35320311000001106,Vinblastine 10mg/50ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35320611000001101,Vinblastine 11mg/50ml in Sodium chloride 0.9% infusion bags (product)
35320711000001105,Vinblastine 11mg/50ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35321011000001104,Vinblastine 12mg/50ml in Sodium chloride 0.9% infusion bags (product)
35321111000001103,Vinblastine 12mg/50ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35321711000001102,Vinblastine 8.2mg/50ml in Sodium chloride 0.9% infusion bags (product)
35321811000001105,Vinblastine 8.2mg/50ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35322111000001108,Vinblastine 9mg/50ml in Sodium chloride 0.9% infusion bags (product)
35322211000001102,Vinblastine 9mg/50ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35326711000001108,Herzuma 150mg powder for concentrate for solution for infusion vials (Napp Pharmaceuticals Ltd) (product)
35335811000001106,Mycophenolic acid 180mg gastro-resistant tablets (A A H Pharmaceuticals Ltd) (product)
35336011000001109,Mycophenolic acid 360mg gastro-resistant tablets (A A H Pharmaceuticals Ltd) (product)
35355911000001102,Carboplatin 330mg/500ml in Glucose 5% infusion bags (product)
35356011000001105,Carboplatin 330mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35361411000001103,Carboplatin 360mg/500ml in Glucose 5% infusion bags (product)
35361511000001104,Carboplatin 360mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35362411000001108,Carboplatin 400mg/500ml in Glucose 5% infusion bags (product)
35362511000001107,Carboplatin 400mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35362811000001105,Carboplatin 450mg/500ml in Glucose 5% infusion bags (product)
35362911000001100,Carboplatin 450mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35363511000001100,Carboplatin 500mg/500ml in Glucose 5% infusion bags (product)
35363611000001101,Carboplatin 500mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35363911000001107,Carboplatin 560mg/500ml in Glucose 5% infusion bags (product)
35364011000001105,Carboplatin 560mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35364511000001102,Carboplatin 630mg/500ml in Glucose 5% infusion bags (product)
35364611000001103,Carboplatin 630mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35364911000001109,Carboplatin 700mg/500ml in Glucose 5% infusion bags (product)
35365011000001109,Carboplatin 700mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35365311000001107,Carboplatin 790mg/500ml in Glucose 5% infusion bags (product)
35365411000001100,Carboplatin 790mg/500ml in Glucose 5% infusion bags (Special Order) (product)
35410311000001106,RoActemra 162mg/0.9ml solution for injection pre-filled pens (Roche Products Ltd) (product)
35431611000001103,Tocilizumab 162mg/0.9ml solution for injection pre-filled disposable devices (product)
35478111000001100,Pemetrexed 100mg powder for concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35478511000001109,Pemetrexed 500mg powder for concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35498711000001106,Lynparza 100mg tablets (AstraZeneca UK Ltd) (product)
35499011000001104,Lynparza 150mg tablets (AstraZeneca UK Ltd) (product)
35514811000001103,Olaparib 100mg tablets (product)
35514911000001108,Olaparib 150mg tablets (product)
35541611000001106,Opdivo 240mg/24ml concentrate for solution for infusion vials (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
35541811000001105,Nivolumab 240mg/24ml solution for infusion vials (product)
35544711000001104,Docetaxel 20mg/1ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35544911000001102,Docetaxel 80mg/4ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35545211000001107,Docetaxel 160mg/8ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35545511000001105,Irinotecan 40mg/2ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35545711000001100,Irinotecan 100mg/5ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35545911000001103,Irinotecan 300mg/15ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35546111000001107,Irinotecan 500mg/25ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35552711000001106,Kanjinti 150mg powder for concentrate for solution for infusion vials (Amgen Ltd) (product)
35552911000001108,Cytarabine 100mg/5ml solution for injection Cytosafe vials (Pfizer Ltd) (product)
35553111000001104,Cytarabine 500mg/25ml solution for injection Cytosafe vials (Pfizer Ltd) (product)
35553311000001102,Cytarabine 1g/10ml solution for injection Cytosafe vials (Pfizer Ltd) (product)
35553511000001108,Cytarabine 2g/20ml solution for injection Cytosafe vials (Pfizer Ltd) (product)
35580011000001104,Paclitaxel 108mg/250ml in Sodium chloride 0.9% infusion bags (product)
35580111000001103,Paclitaxel 108mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35580411000001108,Paclitaxel 120mg/250ml in Sodium chloride 0.9% infusion bags (product)
35580511000001107,Paclitaxel 120mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35580811000001105,Paclitaxel 132mg/250ml in Sodium chloride 0.9% infusion bags (product)
35580911000001100,Paclitaxel 132mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35585611000001103,Paclitaxel 144mg/250ml in Sodium chloride 0.9% infusion bags (product)
35585711000001107,Paclitaxel 144mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35586011000001101,Paclitaxel 162mg/500ml in Sodium chloride 0.9% infusion bags (product)
35586111000001100,Paclitaxel 162mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35586411000001105,Paclitaxel 180mg/500ml in Sodium chloride 0.9% infusion bags (product)
35586511000001109,Paclitaxel 180mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35589011000001107,Doxorubicin 10mg/5ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35589211000001102,Doxorubicin 50mg/25ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35589411000001103,Doxorubicin 200mg/100ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35594611000001103,Paclitaxel 198mg/500ml in Sodium chloride 0.9% infusion bags (product)
35595011000001109,Paclitaxel 198mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35595311000001107,Paclitaxel 216mg/500ml in Sodium chloride 0.9% infusion bags (product)
35595511000001101,Paclitaxel 216mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35595711000001106,Paclitaxel 240mg/500ml in Sodium chloride 0.9% infusion bags (product)
35595811000001103,Paclitaxel 240mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35596111000001104,Paclitaxel 270mg/500ml in Sodium chloride 0.9% infusion bags (product)
35596211000001105,Paclitaxel 270mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35596811000001106,Anagrelide 500microgram capsules (Mylan) (product)
35597411000001106,Bosulif 400mg tablets (Pfizer Ltd) (product)
35599711000001108,Bosutinib 400mg tablets (product)
35600111000001109,Paclitaxel 300mg/500ml in Sodium chloride 0.9% infusion bags (product)
35600211000001103,Paclitaxel 300mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35600511000001100,Paclitaxel 336mg/500ml in Sodium chloride 0.9% infusion bags (product)
35600611000001101,Paclitaxel 336mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35601211000001109,Doxorubicin 20mg/10ml solution for infusion vials (product)
35601411000001108,Doxorubicin 20mg/10ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35601611000001106,Doxorubicin 100mg/50ml solution for infusion vials (product)
35601811000001105,Doxorubicin 100mg/50ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
35610011000001106,Etoposide 500mg/25ml concentrate for solution for infusion vials (medac UK) (product)
35610211000001101,Etoposide 100mg/5ml concentrate for solution for infusion vials (medac UK) (product)
35612011000001105,Irinotecan 200mg/250ml in Sodium chloride 0.9% infusion bags (product)
35612111000001106,Irinotecan 200mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35612411000001101,Irinotecan 220mg/250ml in Sodium chloride 0.9% infusion bags (product)
35612511000001102,Irinotecan 220mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35612811000001104,Irinotecan 240mg/250ml in Sodium chloride 0.9% infusion bags (product)
35612911000001109,Irinotecan 240mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35613211000001106,Irinotecan 260mg/250ml in Sodium chloride 0.9% infusion bags (product)
35613411000001105,Irinotecan 260mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35619611000001105,Doxorubicin 100mg/50ml solution for injection pre-filled syringes (product)
35619811000001109,Doxorubicin 100mg/50ml solution for injection pre-filled syringes (Special Order) (product)
35620311000001104,Doxorubicin 50mg/25ml solution for injection pre-filled syringes (product)
35620411000001106,Doxorubicin 50mg/25ml solution for injection pre-filled syringes (Special Order) (product)
35620711000001100,Doxorubicin 60mg/30ml solution for injection pre-filled syringes (product)
35620911000001103,Doxorubicin 60mg/30ml solution for injection pre-filled syringes (Special Order) (product)
35634211000001101,"Bleomycin 15,000unit powder for solution for injection vials (Accord Healthcare Ltd) (product)"
35635311000001108,Irinotecan 280mg/250ml in Sodium chloride 0.9% infusion bags (product)
35635411000001101,Irinotecan 280mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35635711000001107,Irinotecan 300mg/250ml in Sodium chloride 0.9% infusion bags (product)
35635811000001104,Irinotecan 300mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35636311000001103,Irinotecan 320mg/250ml in Sodium chloride 0.9% infusion bags (product)
35636411000001105,Irinotecan 320mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35640711000001103,Irinotecan 360mg/250ml in Sodium chloride 0.9% infusion bags (product)
35640811000001106,Irinotecan 360mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35641111000001105,Irinotecan 400mg/250ml in Sodium chloride 0.9% infusion bags (product)
35641211000001104,Irinotecan 400mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35643211000001100,Docetaxel 108mg/250ml in Sodium chloride 0.9% infusion bags (product)
35643311000001108,Docetaxel 108mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35643611000001103,Docetaxel 120mg/250ml in Sodium chloride 0.9% infusion bags (product)
35643711000001107,Docetaxel 120mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35644011000001107,Docetaxel 132mg/250ml in Sodium chloride 0.9% infusion bags (product)
35644111000001108,Docetaxel 132mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35644411000001103,Docetaxel 148mg/250ml in Sodium chloride 0.9% infusion bags (product)
35644511000001104,Docetaxel 148mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35645811000001100,Docetaxel 200mg/500ml in Sodium chloride 0.9% infusion bags (product)
35645911000001105,Docetaxel 200mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
35725211000001106,Mycophenolate mofetil 500mg tablets (Tillomed Laboratories Ltd) (product)
35778311000001108,Vyxeos liposomal 44mg/100mg powder for concentrate for solution for infusion vials (Jazz Pharmaceuticals UK) (product)
35812911000001103,Daunorubicin 44mg / Cytarabine 100mg powder for concentrate for solution for infusion vials (product)
35837211000001104,Clofarabine 20mg/20ml concentrare for solution for infusion vials (Consilient Health Ltd) (product)
35849311000001101,Irinotecan 40mg/2ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
35849511000001107,Irinotecan 100mg/5ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
35849711000001102,Irinotecan 300mg/15ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
35850011000001109,Busulfan 60mg/10ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
35853711000001102,Busulfan 60mg/10ml solution for infusion vials (product)
35855611000001105,Etoposide 500mg/25ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
358599006,Basiliximab 20mg injection (pdr for recon)+solvent (product)
35873611000001108,Anagrelide 500microgram capsules (Dr Reddy's Laboratories (UK) Ltd) (product)
35890911000001103,Kanjinti 420mg powder for concentrate for solution for infusion vials (Amgen Ltd) (product)
35894411000001100,Adalimumab 40mg/0.8ml solution for injection pre-filled syringes (product)
35903811000001108,Trastuzumab 420mg powder for solution for infusion vials (product)
35906211000001100,Basiliximab 10mg powder and solvent for solution for injection vials (product)
35907511000001100,Basiliximab 20mg powder and solvent for solution for injection vials (product)
35911111000001100,Bevacizumab 100mg/4ml solution for infusion vials (product)
35911211000001106,Bevacizumab 400mg/16ml solution for infusion vials (product)
35914611000001105,Tacrolimus 5mg/1ml solution for infusion ampoules (product)
35915411000001108,Temsirolimus 30mg/1.2ml solution for infusion vials and diluent (product)
35921311000001108,Treosulfan 5g powder for solution for injection vials (product)
35924511000001100,Sodium aurothiomalate 10mg/0.5ml solution for injection ampoules (product)
35924611000001101,Sodium aurothiomalate 20mg/0.5ml solution for injection ampoules (product)
35924711000001105,Sodium aurothiomalate 50mg/0.5ml solution for injection ampoules (product)
359282000,Etanercept 25mg powder and solvent for injection solution vial (product)
35934711000001107,Rituximab 100mg/10ml solution for infusion vials (product)
35934811000001104,Rituximab 500mg/50ml solution for infusion vials (product)
36004911000001107,Amgevita 40mg/0.8ml solution for injection pre-filled syringes (Amgen Ltd) (product)
36005111000001108,Amgevita 40mg/0.8ml solution for injection pre-filled pens (Amgen Ltd) (product)
36023611000001109,Paclitaxel 100mg/16.7ml solution for infusion vials (product)
36023711000001100,Paclitaxel 150mg/25ml solution for infusion vials (product)
36023811000001108,Paclitaxel 300mg/50ml solution for infusion vials (product)
36025311000001103,Panitumumab 100mg/5ml solution for infusion vials (product)
36030311000001108,Natalizumab 300mg/15ml solution for infusion vials (product)
36032911000001108,Methotrexate 1g/10ml solution for injection vials (product)
36033011000001100,Methotrexate 1g/40ml solution for injection vials (product)
36033111000001104,Methotrexate 200mg/8ml solution for injection vials (product)
36033211000001105,Methotrexate 500mg/20ml solution for injection vials (product)
36033311000001102,Methotrexate 50mg/2ml solution for injection vials (product)
36033411000001109,Methotrexate 5g/200ml solution for infusion vials (product)
36033511000001108,Methotrexate 5g/50ml solution for infusion vials (product)
36033611000001107,Methotrexate 5mg/2ml solution for injection vials (product)
36041711000001103,Melphalan 50mg powder and solvent for solution for injection vials (product)
36045511000001106,Idarubicin 10mg/10ml solution for injection vials (product)
36045711000001101,Idarubicin 5mg/5ml solution for injection vials (product)
36049511000001109,Irinotecan 100mg/5ml solution for infusion vials (product)
36049611000001108,Irinotecan 40mg/2ml solution for infusion vials (product)
36065611000001101,Etanercept 25mg powder and solvent for solution for injection vials (product)
36065711000001105,Etanercept 50mg powder and solvent for solution for injection vials (product)
36066111000001103,Etoposide 100mg/5ml solution for infusion vials (product)
36068111000001104,Fluorouracil 2.5g/100ml solution for infusion vials (product)
36068211000001105,Fluorouracil 2.5g/50ml solution for infusion vials (product)
36068311000001102,Fluorouracil 250mg/10ml solution for injection vials (product)
36068411000001109,Fluorouracil 500mg/10ml solution for injection vials (product)
36068511000001108,Fluorouracil 500mg/20ml solution for injection vials (product)
36071311000001101,Doxorubicin 200mg/100ml solution for infusion vials (product)
36071511000001107,Eculizumab 300mg/30ml solution for infusion vials (product)
36072411000001103,Epirubicin 10mg/5ml solution for injection vials (product)
36072511000001104,Epirubicin 200mg/100ml solution for infusion vials (product)
36072611000001100,Epirubicin 50mg/25ml solution for injection vials (product)
36084111000001108,Hulio 40mg/0.8ml solution for injection pre-filled pens (Mylan) (product)
36085111000001107,Hulio 40mg/0.8ml solution for injection pre-filled syringes (Mylan) (product)
36092011000001100,Cytarabine 100mg/1ml solution for injection vials (product)
36092211000001105,Cytarabine 1g/10ml solution for injection vials (product)
36092311000001102,Cytarabine 2g/20ml solution for injection vials (product)
36092511000001108,Cytarabine 500mg/25ml solution for injection vials (product)
36092611000001107,Cytarabine 500mg/5ml solution for injection vials (product)
36092711000001103,Daclizumab 25mg/5ml solution for infusion vials (product)
3610011000001101,Methotrexate 50mg/2ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
36105511000001109,Azathioprine 50mg tablets (Ennogen Pharma Ltd) (product)
3612511000001105,Methotrexate 5mg/2ml solution for injectionl vials (A A H Pharmaceuticals Ltd) (product)
3612811000001108,Methotrexate 50mg/2ml solution for injection vials (Mayne Pharma Plc) (product)
3613311000001109,Methotrexate 50mg/2ml solution for injection vials (Unichem Plc) (product)
36133811000001102,Carmustine 100mg powder and solvent for solution for injection vials (product)
36139311000001109,Ciclosporin 100mg/ml oral solution sugar free (product)
36139511000001103,Ciclosporin 250mg/5ml solution for infusion ampoules (product)
36140311000001101,Ciclosporin 50mg/1ml solution for infusion ampoules (product)
36142411000001109,Cladribine 10mg/10ml solution for infusion vials (product)
3614611000001101,Methotrexate 5mg/2ml solution for injection vials (Mayne Pharma Plc) (product)
3614911000001107,Methotrexate 5mg/2ml solution for injection vials (Unichem Plc) (product)
36149811000001101,Vinblastine 10mg powder for solution for injection vials (product)
36149911000001106,Vinblastine 10mg/10ml solution for injection vials (product)
36150011000001102,Vincristine 1mg/1ml solution for injection vials (product)
36150111000001101,Vincristine 2mg/2ml solution for injection vials (product)
36150311000001104,Vincristine 5mg/5ml solution for injection vials (product)
36150411000001106,Vinorelbine 10mg/1ml solution for infusion vials (product)
36150511000001105,Vinorelbine 50mg/5ml solution for infusion vials (product)
3615611000001100,Methotrexate 50mg/2ml solution for injection vials (Goldshield Healthcare Ltd) (product)
3615811000001101,Methotrexate 5g/50ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
3616411000001107,Methotrexate 5g/50ml solution for injection vials (Mayne Pharma Plc) (product)
3616911000001104,Methotrexate 5g/50ml solution for injection vials (Unichem Plc) (product)
3618611000001106,Methotrexate 1g/10ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
3619211000001104,Methotrexate 1g/10ml solution for injection vials (Mayne Pharma Plc) (product)
3619511000001101,Methotrexate 1g/10ml solution for injection vials (Unichem Plc) (product)
3620611000001103,Methotrexate 5g/200ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
3620811000001104,Methotrexate 5g/200ml solution for injection vials (Unichem Plc) (product)
3621111000001100,Methotrexate 5g/200ml solution for injection vials (Goldshield Healthcare Ltd) (product)
3621611000001108,Methotrexate 200mg/8ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
3621811000001107,Methotrexate 200mg/8ml solution for injection vials (Goldshield Healthcare Ltd) (product)
3622011000001109,Methotrexate 200mg/8ml solution for injection vials (Unichem Plc) (product)
3622611000001102,Methotrexate 500mg/20ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
3622911000001108,Methotrexate 500mg/20ml solution for injection vials (Mayne Pharma Plc) (product)
3623211000001105,Methotrexate 500mg/20ml solution for injection vials (Unichem Plc) (product)
36234311000001105,Hyrimoz 40mg/0.8ml solution for injection pre-filled pens (Sandoz Ltd) (product)
36234511000001104,Hyrimoz 40mg/0.8ml solution for injection pre-filled syringes (Sandoz Ltd) (product)
3623611000001107,Methotrexate 500mg/20ml solution for injection vials (Goldshield Healthcare Ltd) (product)
36243311000001109,Humira 80mg/0.8ml solution for injection pre-filled syringes (AbbVie Ltd) (product)
36243611000001104,Humira 80mg/0.8ml solution for injection pre-filled pens (AbbVie Ltd) (product)
3624511000001106,Methotrexate 1g/40ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
3624711000001101,Methotrexate 1g/40ml solution for injection vials (Unichem Plc) (product)
3625011000001104,Methotrexate 1g/40ml solution for injection vials (Goldshield Healthcare Ltd) (product)
36435611000001103,Amgevita 20mg/0.4ml solution for injection pre-filled syringes (Amgen Ltd) (product)
36441711000001106,Adalimumab 20mg/0.4ml solution for injection pre-filled syringes (product)
36442011000001101,Imraldi 40mg/0.8ml solution for injection pre-filled pens (Biogen Idec Ltd) (product)
36457911000001103,Adalimumab 80mg/0.8ml solution for injection pre-filled disposable devices (product)
36458011000001101,Adalimumab 80mg/0.8ml solution for injection pre-filled syringes (product)
36460211000001102,Imraldi 40mg/0.8ml solution for injection pre-filled syringes (Biogen Idec Ltd) (product)
36464311000001102,Fludarabine phosphate 50mg powder for solution for injection vials (Accord Healthcare Ltd) (product)
36476511000001106,Mercaptopurine 10mg tablets (Imported (Germany)) (product)
36484811000001108,Treosulfan 5g powder for solution for injection vials (Tillomed Laboratories Ltd) (product)
36485511000001106,Carmustine 100mg powder and solvent for solution for infusion vials (Tillomed Laboratories Ltd) (product)
36493611000001107,Melphalan 50mg powder and solvent for solution for injection vials (Tillomed Laboratories Ltd) (product)
36495511000001107,Clofarabine 20mg/20ml concentrate for solution for infusion vials (Tillomed Laboratories Ltd) (product)
36538011000001109,Busulfan 60mg/10ml concentrate for solution for infusion vials (Tillomed Laboratories Ltd) (product)
36582811000001109,Mercaptopurine 20mg capsules (Special Order) (product)
36583811000001101,Tacrolimus 2microgram suppositories (Special Order) (product)
36584011000001109,Zessly 100mg powder for concentrate for solution for infusion vials (Sandoz Ltd) (product)
36589911000001109,Oxaliplatin 200mg/40ml concentrate for solution for infusion vials (Sun Pharmaceutical Industries Europe B.V.) (product)
36590011000001101,Herzuma 420mg powder for concentrate for solution for infusion vials (Napp Pharmaceuticals Ltd) (product)
36595711000001109,Mercaptopurine 20mg capsules (product)
36596211000001108,Tacrolimus 2microgram suppositories (product)
36597411000001109,Paclitaxel 300mg/50ml concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
36597811000001106,Paclitaxel 30mg/5ml concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
36598111000001103,Paclitaxel 150mg/25ml concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
36598611000001106,Oxaliplatin 200mg/40ml concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
36598811000001105,Cytarabine 2g/20ml solution for injection vials (Fresenius Kabi Oncology Plc) (product)
36599011000001109,Cytarabine 1g/10ml solution for injection vials (Fresenius Kabi Oncology Plc) (product)
3659911000001102,CellCept 250mg capsules (Roche Products Ltd) (product)
36600011000001106,Carboplatin 150mg/15ml concentrate for solution for infusion vials (Fresenius Kabi Oncology Plc) (product)
36600211000001101,Carboplatin 450mg/45ml concentrate for solution for infusion vials (Fresenius Kabi Oncology Plc) (product)
36600411000001102,Carboplatin 50mg/5ml concentrate for solution for infusion vials (Fresenius Kabi Oncology Plc) (product)
36600611000001104,Carboplatin 600mg/60ml concentrate for solution for infusion vials (Fresenius Kabi Oncology Plc) (product)
36610111000001105,Anagrelide 500microgram capsules (Sandoz Ltd) (product)
3661611000001102,CellCept 500mg tablets (Roche Products Ltd) (product)
36616911000001106,Tacrolimus 2mg suppositories (Special Order) (product)
36617111000001106,Gemcitabine 2g powder for solution for infusion vials (Fresenius Kabi Oncology Plc) (product)
36627411000001108,Bendamustine 180mg/4ml solution for infusion vials (product)
36627611000001106,Bendamustine 180mg/4ml concentrate for solution for infusion vials (Dr Reddy's Laboratories (UK) Ltd) (product)
36629611000001101,Anagrelide 500microgram capsules (AOP Orphan Ltd) (product)
36630711000001100,Tacrolimus 2mg suppositories (product)
366611000001106,Penicillamine 250mg tablets (Approved Prescription Services) (product)
36666311000001106,Gemcitabine 1g powder for solution for infusion vials (Fresenius Kabi Oncology Plc) (product)
36666511000001100,Gemcitabine 200mg powder for solution for infusion vials (Fresenius Kabi Oncology Plc) (product)
36685311000001103,Docetaxel 20mg/1ml concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
36685511000001109,Docetaxel 80mg/4ml concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
36685811000001107,Docetaxel 160mg/8ml concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
36686311000001108,Pemetrexed 500mg powder for concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
36686511000001102,Pemetrexed 100mg powder for concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
36687011000001108,Etoposide 100mg/5ml concentrate for solution for infusion vials (Fresenius Kabi Oncology Plc) (product)
36687211000001103,Etoposide 200mg/10ml concentrate for solution for infusion vials (Fresenius Kabi Oncology Plc) (product)
36687511000001100,Busulfan 60mg/10ml concentrate for solution for infusion vials (Fresenius Kabi Ltd) (product)
36687811000001102,Gemcitabine 200mg/5.26ml concentrate for solution for infusion vials (Fresenius Kabi Oncology Plc) (product)
36688011000001109,Gemcitabine 1g/26.3ml concentrate for solution for infusion vials (Fresenius Kabi Oncology Plc) (product)
36688211000001104,Gemcitabine 2g/52.6ml concentrate for solution for infusion vials (Fresenius Kabi Oncology Plc) (product)
36753311000001101,Gemcitabine 200mg/5.26ml solution for infusion vials (product)
36756311000001105,Trazimera 150mg powder for concentrate for solution for infusion vials (Pfizer Ltd) (product)
36761211000001104,Irinotecan 500mg/25ml concentrate for solution for infusion vials (Fresenius Kabi Oncology Plc) (product)
36763811000001104,CellCept 250mg capsules (Originalis B.V.) (product)
36783411000001104,Carmustine Obvius 100mg powder and solvent for concentrate for solution for infusion vials (Nexcape Pharmaceuticals Ltd) (product)
36785611000001102,Carboplatin 50mg/5ml solution for infusion vials (Consilient Health Ltd) (product)
36785811000001103,Carboplatin 150mg/15ml solution for infusion vials (Consilient Health Ltd) (product)
36786011000001100,Carboplatin 450mg/45ml solution for infusion vials (Consilient Health Ltd) (product)
36786211000001105,Carboplatin 600mg/60ml solution for infusion vials (Consilient Health Ltd) (product)
36798511000001108,Oxaliplatin 50mg/10ml concentrate for solution for infusion vials (Sandoz Ltd) (product)
36803911000001106,Imnovid 4mg capsules (Originalis B.V.) (product)
36806811000001105,Keytruda 50mg powder for concentrate for solution for infusion vials (Originalis B.V.) (product)
36809311000001108,Prograf 1mg capsules (Pharmaram Ltd) (product)
36810511000001107,Oxaliplatin 100mg/20ml concentrate for solution for infusion vials (Sandoz Ltd) (product)
36815511000001102,Mekinist 2mg tablets (Originalis B.V.) (product)
36818511000001105,Opdivo 100mg/10ml concentrate for solution for infusion vials (Originalis B.V.) (product)
36819311000001105,Perjeta 420mg/14ml concentrate for solution for infusion vials (Originalis B.V.) (product)
36821711000001102,Prograf 1mg capsules (Originalis B.V.) (product)
36824311000001103,Everolimus 2.5mg tablets (A A H Pharmaceuticals Ltd) (product)
36824511000001109,Everolimus 5mg tablets (A A H Pharmaceuticals Ltd) (product)
36824711000001104,Everolimus 10mg tablets (A A H Pharmaceuticals Ltd) (product)
36825811000001108,Everolimus 2.5mg tablets (Accord Healthcare Ltd) (product)
36826011000001106,Everolimus 5mg tablets (Accord Healthcare Ltd) (product)
36826211000001101,Everolimus 10mg tablets (Accord Healthcare Ltd) (product)
36866711000001103,Carmustine 100mg powder and solvent for solution for infusion vials (Nexcape Pharmaceuticals Ltd) (product)
36888011000001104,Anagrelide 500microgram capsules (Torrent Pharma (UK) Ltd) (product)
36897711000001102,Stivarga 40mg tablets (Originalis B.V.) (product)
36898011000001103,Tafinlar 75mg capsules (Originalis B.V.) (product)
36908211000001102,Xagrid 500microgram capsules (Originalis B.V.) (product)
36908611000001100,Yervoy 50mg/10ml concentrate for solution for infusion vials (Originalis B.V.) (product)
36933211000001101,Melphalan 50mg powder and solvent for solution for injection vials (Sun Pharmaceutical Industries Europe B.V.) (product)
36936311000001100,Paclitaxel 100mg/16.7ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
36936511000001106,Paclitaxel 30mg/5ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
36936711000001101,Paclitaxel 300mg/50ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
3693911000001106,Cyclophosphamide 50mg tablets (A A H Pharmaceuticals Ltd) (product)
3694111000001105,Endoxana 50mg tablets (Baxter Healthcare Ltd) (product)
3694311000001107,Cyclophosphamide 50mg tablets (Pfizer Ltd) (product)
3694511000001101,Cyclophosphamide 50mg tablets (Unichem Plc) (product)
3695011000001108,Azathioprine 25mg tablets (IVAX Pharmaceuticals UK Ltd) (product)
36959911000001107,Mercaptopurine 12.5mg capsules (Special Order) (product)
36979111000001107,Mercaptopurine 12.5mg capsules (product)
37061411000001103,Bendamustine 25mg powder for concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
37065311000001107,Bendamustine 100mg powder for concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
37077111000001106,Azathioprine 50mg tablets (Relonchem Ltd) (product)
37102011000001107,Bortezomib 3.5mg powder for solution for injection vials (Aspire Pharma Ltd) (product)
37106111000001107,Anagrelide 500microgram capsules (DE Pharmaceuticals) (product)
37129511000001102,Anagrelide 500microgram capsules (Zentiva) (product)
37141811000001103,Tasigna 50mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
37143311000001108,Gilenya 0.25mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
37171911000001109,Nilotinib 50mg capsules (product)
37192411000001100,Tioguanine 40mg tablets (A A H Pharmaceuticals Ltd) (product)
37216911000001105,Orencia 87.5mg/0.7ml solution for injection pre-filled syringes (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
37217211000001104,Orencia 50mg/0.4ml solution for injection pre-filled syringes (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
37221911000001107,Sprycel 10mg/ml oral suspension (Bristol-Myers Squibb Pharmaceuticals Ltd) (product)
37223011000001109,Abatacept 50mg/0.4ml solution for injection pre-filled syringes (product)
37223111000001105,Abatacept 87.5mg/0.7ml solution for injection pre-filled syringes (product)
37223211000001104,Dasatinib 10mg/ml oral suspension (product)
37224911000001105,Gefitinib 250mg tablets (Mylan) (product)
37234111000001109,Arsenic 10mg/10ml concentrate for solution for infusion vials (Flexipharm Austrading Ltd) (product)
37236211000001108,Fingolimod 250microgram capsules (product)
37238611000001106,Arsenic 10mg/10ml solution for infusion vials (product)
37262611000001101,Mitocin 20mg powder and solvent for intravesical solution vials (Vygoris Ltd) (product)
37263811000001105,Mitocin 20mg powder for solution for injection vials (Vygoris Ltd) (product)
37267811000001104,Gemcitabine 1.4g/140ml infusion bags (Sun Pharmaceutical Industries Europe B.V.) (product)
37270111000001102,Metalcaptase gastro-resistant 150mg tablets (Imported (Germany)) (product)
37270911000001104,Metalcaptase gastro-resistant 300mg tablets (Imported (Germany)) (product)
37273211000001103,Methotrexate 2.5mg tablets (Mawdsley-Brooks & Company Ltd) (product)
37280611000001104,Gefitinib 250mg tablets (Sandoz Ltd) (product)
37280911000001105,Gemcitabine 1.4g/140ml infusion bags (product)
37281111000001101,Penicillamine gastro-resistant 150mg tablets (product)
37281511000001105,Penicillamine gastro-resistant 300mg tablets (product)
37342511000001100,Advagraf 3mg modified-release capsules (Mawdsley-Brooks & Company Ltd) (product)
37344311000001104,Prograf 500microgram capsules (CST Pharma Ltd) (product)
37345711000001101,Neoral 25mg capsules (CST Pharma Ltd) (product)
37346011000001107,Neoral 50mg capsules (CST Pharma Ltd) (product)
37346411000001103,Neoral 100mg capsules (CST Pharma Ltd) (product)
37347311000001108,Prograf 1mg capsules (CST Pharma Ltd) (product)
37382611000001108,Gefitinib 250mg tablets (Genus Pharmaceuticals Ltd) (product)
37397611000001105,Metoject PEN 7.5mg/0.15ml solution for injection pre-filled pens (CST Pharma Ltd) (product)
37397811000001109,Metoject PEN 10mg/0.2ml solution for injection pre-filled pens (CST Pharma Ltd) (product)
37398011000001102,Metoject PEN 12.5mg/0.25ml solution for injection pre-filled pens (CST Pharma Ltd) (product)
374106009,Idarubicin hydrochloride 1mg/mL injection solution 10mL vial (product)
374192000,Doxorubicin hydrochloride 2mg/mL injection solution 100mL vial (product)
374202004,Idarubicin hydrochloride 1mg/mL injection solution 5mL vial (product)
37427211000001107,Gefitinib 250mg tablets (Accord Healthcare Ltd) (product)
374287008,Product containing precisely cyclophosphamide 25 milligram/1 each conventional release oral tablet (clinical drug)
37429611000001104,Arava 10mg tablets (CST Pharma Ltd) (product)
37429811000001100,Arava 20mg tablets (CST Pharma Ltd) (product)
37432811000001107,CellCept 250mg capsules (CST Pharma Ltd) (product)
37433011000001105,CellCept 500mg tablets (CST Pharma Ltd) (product)
374336007,Product containing precisely lomustine 10 milligram/1 each conventional release oral capsule (clinical drug)
374342006,Product containing precisely lomustine 100 milligram/1 each conventional release oral capsule (clinical drug)
374369007,Product containing precisely mitotane 500 milligram/1 each conventional release oral tablet (clinical drug)
37450711000001102,Methotrexate 2mg/ml oral solution sugar free (DE Pharmaceuticals) (product)
374572004,Product containing precisely anagrelide hydrochloride 500 microgram/1 each conventional release oral capsule (clinical drug)
37476311000001101,Bortezomib 3.5mg/1.4ml solution for injection vials (Thornton & Ross Ltd) (product)
374872005,Product containing precisely bexarotene 75 milligram/1 each conventional release oral capsule (clinical drug)
37490911000001105,Gefitinib 250mg tablets (Glenmark Pharmaceuticals Europe Ltd) (product)
37491411000001106,Bortezomib 3.5mg/1.4ml solution for injection vials (product)
37492311000001108,Imbruvica 420mg tablets (Janssen-Cilag Ltd) (product)
37492611000001103,Imbruvica 560mg tablets (Janssen-Cilag Ltd) (product)
37492911000001109,Imbruvica 140mg tablets (Janssen-Cilag Ltd) (product)
37493211000001106,Imbruvica 280mg tablets (Janssen-Cilag Ltd) (product)
37493411000001105,Ibrutinib 140mg tablets (product)
37493511000001109,Ibrutinib 280mg tablets (product)
37493611000001108,Ibrutinib 420mg tablets (product)
37493711000001104,Ibrutinib 560mg tablets (product)
37511311000001108,Imuran 50mg tablets (Mawdsley-Brooks & Company Ltd) (product)
37538311000001108,Xagrid 500microgram capsules (CST Pharma Ltd) (product)
375449005,Product containing precisely hydroxycarbamide 300 milligram/1 each conventional release oral capsule (clinical drug)
37560311000001102,Bortezomib 1mg powder for solution for injection vials (Aspire Pharma Ltd) (product)
37561211000001104,Gefitinib 250mg tablets (A A H Pharmaceuticals Ltd) (product)
37564111000001108,Bortezomib 1mg powder for solution for injection vials (product)
37569311000001106,Xromi 100mg/ml oral solution (Nova Laboratories Ltd) (product)
37571111000001101,Methofill 7.5mg/0.15ml solution for injection pre-filled syringes (Accord Healthcare Ltd) (product)
37571311000001104,Methofill 10mg/0.2ml solution for injection pre-filled syringes (Accord Healthcare Ltd) (product)
37571511000001105,Methofill 12.5mg/0.25ml solution for injection pre-filled syringes (Accord Healthcare Ltd) (product)
37571711000001100,Methofill 15mg/0.3ml solution for injection pre-filled syringes (Accord Healthcare Ltd) (product)
37571911000001103,Methofill 17.5mg/0.35ml solution for injection pre-filled syringes (Accord Healthcare Ltd) (product)
37572111000001106,Hanixol 50mg tablets (Fontus Health Ltd) (product)
37572311000001108,Methofill 20mg/0.4ml solution for injection pre-filled syringes (Accord Healthcare Ltd) (product)
37572511000001102,Methofill 22.5mg/0.45ml solution for injection pre-filled syringes (Accord Healthcare Ltd) (product)
37572711000001107,Methofill 25mg/0.5ml solution for injection pre-filled syringes (Accord Healthcare Ltd) (product)
37572911000001109,Methofill 27.5mg/0.55ml solution for injection pre-filled syringes (Accord Healthcare Ltd) (product)
37573111000001100,Methofill 30mg/0.6ml solution for injection pre-filled syringes (Accord Healthcare Ltd) (product)
37574311000001101,Leflunomide 10mg tablets (Relonchem Ltd) (product)
37574511000001107,Leflunomide 20mg tablets (Relonchem Ltd) (product)
37579211000001108,Bortezomib 2.5mg powder for solution for injection vials (Aspire Pharma Ltd) (product)
37600311000001105,Bortezomib 2.5mg powder for solution for injection vials (product)
37600411000001103,Hydroxycarbamide 500mg/5ml oral solution sugar free (product)
37603711000001100,Imatinib 100mg tablets (Zentiva) (product)
37603911000001103,Imatinib 400mg tablets (Zentiva) (product)
37616311000001106,Trazimera 420mg powder for concentrate for solution for infusion vials (Pfizer Ltd) (product)
37623911000001105,CellCept 250mg capsules (Ethigen Ltd) (product)
37624111000001109,CellCept 500mg tablets (Ethigen Ltd) (product)
37689211000001105,Metoject PEN 10mg/0.2ml solution for injection pre-filled pens (Pilsco Ltd) (product)
37689511000001108,Metoject PEN 12.5mg/0.25ml solution for injection pre-filled pens (Pilsco Ltd) (product)
37689811000001106,Metoject PEN 7.5mg/0.15ml solution for injection pre-filled pens (Pilsco Ltd) (product)
37694111000001101,Cyclophosphamide 50mg tablets (CST Pharma Ltd) (product)
37698511000001103,Prograf 500microgram capsules (Pilsco Ltd) (product)
37698711000001108,Prograf 1mg capsules (Pilsco Ltd) (product)
37699511000001109,Puri-Nethol 50mg tablets (Pilsco Ltd) (product)
37723611000001108,Metoject PEN 15mg/0.3ml solution for injection pre-filled pens (Pilsco Ltd) (product)
37723811000001107,Metoject PEN 17.5mg/0.35ml solution for injection pre-filled pens (Pilsco Ltd) (product)
37724011000001104,Metoject PEN 20mg/0.4ml solution for injection pre-filled pens (Pilsco Ltd) (product)
37724211000001109,Metoject PEN 22.5mg/0.45ml solution for injection pre-filled pens (Pilsco Ltd) (product)
37725411000001109,Dasatinib 20mg tablets (Zentiva) (product)
37725611000001107,Dasatinib 50mg tablets (Zentiva) (product)
37726211000001104,Dasatinib 140mg tablets (Zentiva) (product)
37726511000001101,Dasatinib 80mg tablets (Zentiva) (product)
37726811000001103,Dasatinib 100mg tablets (Zentiva) (product)
37733011000001104,Methotrexate 1g/10ml solution for injection vials (medac UK) (product)
37733211000001109,Methotrexate 5g/50ml solution for infusion vials (medac UK) (product)
37753911000001101,Gefitinib 250mg tablets (Zentiva) (product)
37755211000001109,Bortezomib 3.5mg powder for solution for injection vials (Dr Reddy's Laboratories (UK) Ltd) (product)
37758411000001103,Chlorambucil 2mg tablets (CST Pharma Ltd) (product)
37776211000001100,Keytruda 100mg/4ml concentrate for solution for infusion vials (Originalis B.V.) (product)
37776611000001103,Yervoy 200mg/40ml concentrate for solution for infusion vials (Originalis B.V.) (product)
37807111000001101,Rituximab (MabThera) 1000mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37809311000001109,Rituximab (Truxima) 1000mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37809611000001104,Rituximab (Rixathon) 1000mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37817011000001104,Rituximab (MabThera) 500mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37817311000001101,Rituximab (Rixathon) 500mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37817711000001102,Rituximab (Truxima) 500mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37819111000001109,Rituximab (MabThera) 600mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37819311000001106,Rituximab (Rixathon) 600mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37819511000001100,Rituximab (Truxima) 600mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37820011000001109,Rituximab (MabThera) 700mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37820311000001107,Rituximab (Rixathon) 700mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37820511000001101,Rituximab (Truxima) 700mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37821311000001102,Rituximab (MabThera) 800mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37821511000001108,Rituximab (Rixathon) 800mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37821711000001103,Rituximab (Truxima) 800mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37824411000001106,Rituximab (MabThera) 900mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37824811000001108,Rituximab (Rixathon) 900mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37825011000001103,Rituximab (Truxima) 900mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37829011000001101,Rituximab 1000mg/500ml in Sodium chloride 0.9% infusion bags (product)
37829111000001100,Rituximab 500mg/500ml in Sodium chloride 0.9% infusion bags (product)
37829211000001106,Rituximab 600mg/500ml in Sodium chloride 0.9% infusion bags (product)
37829311000001103,Rituximab 700mg/500ml in Sodium chloride 0.9% infusion bags (product)
37829511000001109,Rituximab 800mg/500ml in Sodium chloride 0.9% infusion bags (product)
37829611000001108,Rituximab 900mg/500ml in Sodium chloride 0.9% infusion bags (product)
37834311000001102,Cisplatin 100mg/1000ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37834611000001107,Cisplatin 113mg/1000ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37834911000001101,Cisplatin 128mg/1000ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37835211000001106,Cisplatin 145mg/1000ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37835511000001109,Cisplatin 164mg/1000ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37835811000001107,Cisplatin 185mg/1000ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37836111000001106,Cisplatin 33mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37836411000001101,Cisplatin 36mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37836711000001107,Cisplatin 40mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37837011000001108,Cisplatin 45mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37838711000001106,Cyclophosphamide 1000mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37839011000001104,Cyclophosphamide 1120mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37839311000001101,Cyclophosphamide 1260mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37839611000001106,Cyclophosphamide 2000mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37839911000001100,Cyclophosphamide 4180mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37840511000001103,Cyclophosphamide 480mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37840911000001105,Cisplatin 50mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37841211000001107,Cisplatin 70mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37841511000001105,Cisplatin 89mg/500ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37842711000001107,Anagrelide 500microgram capsules (Kent Pharmaceuticals Ltd) (product)
37843111000001100,Cisplatin 100mg/1000ml in Sodium chloride 0.9% infusion bags (product)
37843211000001106,Cisplatin 113mg/1000ml in Sodium chloride 0.9% infusion bags (product)
37843311000001103,Cisplatin 128mg/1000ml in Sodium chloride 0.9% infusion bags (product)
37843411000001105,Cisplatin 145mg/1000ml in Sodium chloride 0.9% infusion bags (product)
37843511000001109,Cisplatin 164mg/1000ml in Sodium chloride 0.9% infusion bags (product)
37843611000001108,Cisplatin 185mg/1000ml in Sodium chloride 0.9% infusion bags (product)
37843711000001104,Cisplatin 33mg/250ml in Sodium chloride 0.9% infusion bags (product)
37843811000001107,Cisplatin 36mg/250ml in Sodium chloride 0.9% infusion bags (product)
37843911000001102,Cisplatin 40mg/250ml in Sodium chloride 0.9% infusion bags (product)
37844011000001104,Cisplatin 45mg/250ml in Sodium chloride 0.9% infusion bags (product)
37844111000001103,Cisplatin 50mg/500ml in Sodium chloride 0.9% infusion bags (product)
37844211000001109,Cisplatin 70mg/500ml in Sodium chloride 0.9% infusion bags (product)
37844311000001101,Cisplatin 89mg/500ml in Sodium chloride 0.9% infusion bags (product)
37844411000001108,Cyclophosphamide 1000mg/250ml in Sodium chloride 0.9% infusion bags (product)
37844511000001107,Cyclophosphamide 1120mg/250ml in Sodium chloride 0.9% infusion bags (product)
37844611000001106,Cyclophosphamide 1260mg/250ml in Sodium chloride 0.9% infusion bags (product)
37844711000001102,Cyclophosphamide 2000mg/250ml in Sodium chloride 0.9% infusion bags (product)
37844811000001105,Cyclophosphamide 4180mg/250ml in Sodium chloride 0.9% infusion bags (product)
37844911000001100,Cyclophosphamide 480mg/250ml in Sodium chloride 0.9% infusion bags (product)
37847011000001107,Cimzia 200mg/1ml solution for injection in a dose-dispenser cartridge (UCB Pharma Ltd) (product)
37854811000001107,Certolizumab pegol 200mg/1ml solution for injection cartridges (product)
37878911000001106,Vinorelbine 20mg capsules (Consilient Health Ltd) (product)
37879311000001104,Vinorelbine 30mg capsules (Consilient Health Ltd) (product)
37880111000001101,Vinorelbine 80mg capsules (Consilient Health Ltd) (product)
37894311000001106,Bortezomib 1.6mg/0.64ml in Sodium chloride 0.9% solution for injection pre-filled syringes (Special Order) (product)
37894611000001101,Bortezomib 1.8mg/0.72ml in Sodium chloride 0.9% solution for injection pre-filled syringes (Special Order) (product)
37895211000001102,Bortezomib 2.25mg/0.9ml in Sodium chloride 0.9% solution for injection pre-filled syringes (Special Order) (product)
37895511000001104,Bortezomib 2.5mg/1ml in Sodium chloride 0.9% solution for injection pre-filled syringes (Special Order) (product)
37895811000001101,Bortezomib 2.75mg/1.1ml in Sodium chloride 0.9% solution for injection pre-filled syringes (Special Order) (product)
37896111000001102,Bortezomib 2mg/0.8ml in Sodium chloride 0.9% solution for injection pre-filled syringes (Special Order) (product)
37896411000001107,Bortezomib 3mg/1.2ml in Sodium chloride 0.9% solution for injection pre-filled syringes (Special Order) (product)
37898511000001107,Bortezomib 1.6mg/0.64ml in Sodium chloride 0.9% solution for injection pre-filled syringes (product)
37898611000001106,Bortezomib 1.8mg/0.72ml in Sodium chloride 0.9% solution for injection pre-filled syringes (product)
37898711000001102,Bortezomib 2.25mg/0.9ml in Sodium chloride 0.9% solution for injection pre-filled syringes (product)
37898811000001105,Bortezomib 2.5mg/1ml in Sodium chloride 0.9% solution for injection pre-filled syringes (product)
37898911000001100,Bortezomib 2.75mg/1.1ml in Sodium chloride 0.9% solution for injection pre-filled syringes (product)
37899011000001109,Bortezomib 2mg/0.8ml in Sodium chloride 0.9% solution for injection pre-filled syringes (product)
37899111000001105,Bortezomib 3mg/1.2ml in Sodium chloride 0.9% solution for injection pre-filled syringes (product)
37913711000001102,Fluorouracil 1350mg/1000ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37913911000001100,Fluorouracil 1350mg/1000ml in Sodium chloride 0.9% infusion bags (product)
37914211000001107,Fluorouracil 1500mg/1000ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37914411000001106,Fluorouracil 1500mg/1000ml in Sodium chloride 0.9% infusion bags (product)
37916311000001105,Gemcitabine 1026mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37916611000001100,Gemcitabine 1100mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37916911000001106,Gemcitabine 1140mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37917211000001100,Gemcitabine 1254mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37917511000001102,Gemcitabine 1300mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37917811000001104,Gemcitabine 1368mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37918111000001107,Gemcitabine 1400mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37918411000001102,Gemcitabine 1500mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37918711000001108,Gemcitabine 1520mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37919011000001101,Gemcitabine 1710mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37919311000001103,Gemcitabine 1900mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37919611000001108,Gemcitabine 2128mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37919911000001102,Gemcitabine 2394mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37920211000001105,Gemcitabine 2400mg/250ml in Sodium chloride 0.9% infusion bags (Special Order) (product)
37922011000001101,Methotrexate 100mg/4ml solution for injection pre-filled syringes (Special Order) (product)
37922311000001103,Methotrexate 40mg/1.6ml solution for injection pre-filled syringes (Special Order) (product)
37922611000001108,Methotrexate 45mg/1.8ml solution for injection pre-filled syringes (Special Order) (product)
37922911000001102,Methotrexate 60mg/2.4ml solution for injection pre-filled syringes (Special Order) (product)
37923211000001100,Methotrexate 80mg/3.2ml solution for injection pre-filled syringes (Special Order) (product)
37923511000001102,Methotrexate 85mg/3.4ml solution for injection pre-filled syringes (Special Order) (product)
37923811000001104,Methotrexate 90mg/3.6ml solution for injection pre-filled syringes (Special Order) (product)
37924011000001107,Gemcitabine 1026mg/250ml in Sodium chloride 0.9% infusion bags (product)
37924111000001108,Gemcitabine 1100mg/250ml in Sodium chloride 0.9% infusion bags (product)
37924211000001102,Gemcitabine 1140mg/250ml in Sodium chloride 0.9% infusion bags (product)
37924311000001105,Gemcitabine 1254mg/250ml in Sodium chloride 0.9% infusion bags (product)
37924411000001103,Gemcitabine 1300mg/250ml in Sodium chloride 0.9% infusion bags (product)
37924511000001104,Gemcitabine 1368mg/250ml in Sodium chloride 0.9% infusion bags (product)
37924611000001100,Gemcitabine 1400mg/250ml in Sodium chloride 0.9% infusion bags (product)
37924711000001109,Gemcitabine 1500mg/250ml in Sodium chloride 0.9% infusion bags (product)
37924811000001101,Gemcitabine 1520mg/250ml in Sodium chloride 0.9% infusion bags (product)
37924911000001106,Gemcitabine 1710mg/250ml in Sodium chloride 0.9% infusion bags (product)
37925011000001106,Gemcitabine 1900mg/250ml in Sodium chloride 0.9% infusion bags (product)
37925111000001107,Gemcitabine 2128mg/250ml in Sodium chloride 0.9% infusion bags (product)
37925211000001101,Gemcitabine 2394mg/250ml in Sodium chloride 0.9% infusion bags (product)
37925311000001109,Gemcitabine 2400mg/250ml in Sodium chloride 0.9% infusion bags (product)
37925611000001104,Methotrexate 100mg/4ml solution for injection pre-filled syringes (product)
37925711000001108,Methotrexate 40mg/1.6ml solution for injection pre-filled syringes (product)
37925811000001100,Methotrexate 45mg/1.8ml solution for injection pre-filled syringes (product)
37925911000001105,Methotrexate 60mg/2.4ml solution for injection pre-filled syringes (product)
37926011000001102,Methotrexate 80mg/3.2ml solution for injection pre-filled syringes (product)
37926111000001101,Methotrexate 85mg/3.4ml solution for injection pre-filled syringes (product)
37926211000001107,Methotrexate 90mg/3.6ml solution for injection pre-filled syringes (product)
37939711000001107,Dailiport 0.5mg modified-release capsules (Sandoz Ltd) (product)
37939911000001109,Dailiport 1mg modified-release capsules (Sandoz Ltd) (product)
37940211000001108,Dailiport 3mg modified-release capsules (Sandoz Ltd) (product)
37940411000001107,Dailiport 5mg modified-release capsules (Sandoz Ltd) (product)
37941011000001107,Dailiport 2mg modified-release capsules (Sandoz Ltd) (product)
37949111000001107,Tacrolimus 2mg modified-release capsules (product)
37977511000001106,Gefitinib 250mg tablets (Wockhardt UK Ltd) (product)
37992311000001105,Zykadia 150mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
37993511000001106,Prograf 500microgram capsules (Pharmaram Ltd) (product)
37993711000001101,Prograf 5mg capsules (Pharmaram Ltd) (product)
38000111000001106,Fluorouracil 3150mg/120ml (2.5ml/hour) in Sodium chloride 0.9% infusion AutoFuser elastomeric devices (Special Order) (product)
38000411000001101,Fluorouracil 3500mg/120ml (2.5ml/hour) in Sodium chloride 0.9% infusion AutoFuser elastomeric devices (Special Order) (product)
38000711000001107,Fluorouracil 3950mg/120ml (2.5ml/hour) in Sodium chloride 0.9% infusion AutoFuser elastomeric devices (Special Order) (product)
38001011000001101,Fluorouracil 4450mg/120ml (2.5ml/hour) in Sodium chloride 0.9% infusion AutoFuser elastomeric devices (Special Order) (product)
38001311000001103,Fluorouracil 5000mg/120ml (2.5ml/hour) in Sodium chloride 0.9% infusion AutoFuser elastomeric devices (Special Order) (product)
38002411000001100,Fluorouracil 3150mg/120ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38002511000001101,Fluorouracil 3500mg/120ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38002611000001102,Fluorouracil 3950mg/120ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38002711000001106,Fluorouracil 4450mg/120ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38002811000001103,Fluorouracil 5000mg/120ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38004511000001106,Remsima 120mg/1ml solution for injection pre-filled syringes (Celltrion Healthcare UK Ltd) (product)
38004811000001109,Remsima 120mg/1ml solution for injection pre-filled pens (Celltrion Healthcare UK Ltd) (product)
38005111000001103,Fluorouracil 5650mg/200ml (2ml/hour) in Sodium chloride 0.9% infusion AutoFuser elastomeric devices (Special Order) (product)
38005411000001108,Fluorouracil 6400mg/200ml (2ml/hour) in Sodium chloride 0.9% infusion AutoFuser elastomeric devices (Special Order) (product)
38005711000001102,Fluorouracil 7250mg/200ml (2ml/hour) in Sodium chloride 0.9% infusion AutoFuser elastomeric devices (Special Order) (product)
38006011000001108,Fluorouracil 8200mg/200ml (2ml/hour) in Sodium chloride 0.9% infusion AutoFuser elastomeric devices (Special Order) (product)
38006211000001103,Fluorouracil 5650mg/200ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38006311000001106,Fluorouracil 6400mg/200ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38006411000001104,Fluorouracil 7250mg/200ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38006511000001100,Fluorouracil 8200mg/200ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38007711000001108,Ceritinib 150mg tablets (product)
3801811000001105,Ridaura Tiltab 3mg tablets (Yamanouchi Pharmaceuticals) (product)
38023511000001101,Fluorouracil 1350mg/105ml (0.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV0.5 elastomeric devices (Special Order) (product)
38024711000001108,Fluorouracil 1650mg/105ml (0.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV0.5 elastomeric devices (Special Order) (product)
38025011000001105,Fluorouracil 1800mg/105ml (0.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV0.5 elastomeric devices (Special Order) (product)
38025311000001108,Fluorouracil 2000mg/105ml (0.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV0.5 elastomeric devices (Special Order) (product)
38025611000001103,Fluorouracil 2250mg/105ml (0.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV0.5 elastomeric devices (Special Order) (product)
38025911000001109,Fluorouracil 2500mg/105ml (0.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV0.5 elastomeric devices (Special Order) (product)
38026211000001106,Fluorouracil 2800mg/105ml (0.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV0.5 elastomeric devices (Special Order) (product)
38026511000001109,Fluorouracil 3150mg/105ml (0.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV0.5 elastomeric devices (Special Order) (product)
38026811000001107,Fluorouracil 3500mg/105ml (0.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV0.5 elastomeric devices (Special Order) (product)
38027111000001102,Fluorouracil 3950mg/105ml (0.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV0.5 elastomeric devices (Special Order) (product)
38028011000001102,Fluorouracil 1350mg/105ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38028111000001101,Fluorouracil 1650mg/105ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38028211000001107,Fluorouracil 1800mg/105ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38028311000001104,Fluorouracil 2000mg/105ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38028411000001106,Fluorouracil 2250mg/105ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38028511000001105,Fluorouracil 2500mg/105ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38028611000001109,Fluorouracil 2800mg/105ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38028711000001100,Fluorouracil 3150mg/105ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38028811000001108,Fluorouracil 3500mg/105ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38028911000001103,Fluorouracil 3950mg/105ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38043011000001107,Fluorouracil 2000mg/130ml (2.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV2.5 elastomeric devices (Special Order) (product)
38043711000001109,Fluorouracil 2250mg/130ml (2.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV2.5 elastomeric devices (Special Order) (product)
38044711000001106,Fluorouracil 2500mg/130ml (2.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV2.5 elastomeric devices (Special Order) (product)
38045711000001105,Fluorouracil 2800mg/130ml (2.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV2.5 elastomeric devices (Special Order) (product)
38047211000001106,Fluorouracil 3150mg/130ml (2.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV2.5 elastomeric devices (Special Order) (product)
38047511000001109,Fluorouracil 3500mg/130ml (2.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV2.5 elastomeric devices (Special Order) (product)
38048111000001104,Fluorouracil 3950mg/130ml (2.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV2.5 elastomeric devices (Special Order) (product)
38049311000001108,Fluorouracil 4450mg/130ml (2.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV2.5 elastomeric devices (Special Order) (product)
38054011000001107,Fluorouracil 5000mg/130ml (2.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV2.5 elastomeric devices (Special Order) (product)
38054311000001105,Fluorouracil 5650mg/130ml (2.5ml/hour) in Sodium chloride 0.9% infusion FOLFusor SV2.5 elastomeric devices (Special Order) (product)
38054811000001101,Fluorouracil 2800mg/300ml (5ml/hour) in Sodium chloride 0.9% infusion FOLFusor LV5 elastomeric devices (Special Order) (product)
38055111000001107,Fluorouracil 3150mg/300ml (5ml/hour) in Sodium chloride 0.9% infusion FOLFusor LV5 elastomeric devices (Special Order) (product)
38055411000001102,Fluorouracil 3500mg/300ml (5ml/hour) in Sodium chloride 0.9% infusion FOLFusor LV5 elastomeric devices (Special Order) (product)
38057811000001105,Fluorouracil 3950mg/300ml (5ml/hour) in Sodium chloride 0.9% infusion FOLFusor LV5 elastomeric devices (Special Order) (product)
38058111000001102,Fluorouracil 4450mg/300ml (5ml/hour) in Sodium chloride 0.9% infusion FOLFusor LV5 elastomeric devices (Special Order) (product)
38058811000001109,Fluorouracil 5000mg/300ml (5ml/hour) in Sodium chloride 0.9% infusion FOLFusor LV5 elastomeric devices (Special Order) (product)
38059111000001109,Fluorouracil 5650mg/300ml (5ml/hour) in Sodium chloride 0.9% infusion FOLFusor LV5 elastomeric devices (Special Order) (product)
38059411000001104,Fluorouracil 6400mg/300ml (5ml/hour) in Sodium chloride 0.9% infusion FOLFusor LV5 elastomeric devices (Special Order) (product)
38059711000001105,Fluorouracil 7250mg/300ml (5ml/hour) in Sodium chloride 0.9% infusion FOLFusor LV5 elastomeric devices (Special Order) (product)
38060211000001104,Erlotinib 25mg tablets (Zentiva) (product)
38064011000001102,Fluorouracil 2000mg/130ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38064111000001101,Fluorouracil 2250mg/130ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38064211000001107,Fluorouracil 2500mg/130ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38064311000001104,Fluorouracil 2800mg/130ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38064411000001106,Fluorouracil 2800mg/300ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38064511000001105,Fluorouracil 3150mg/130ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38064611000001109,Fluorouracil 3150mg/300ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38064711000001100,Fluorouracil 3500mg/130ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38064811000001108,Fluorouracil 3500mg/300ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38064911000001103,Fluorouracil 3950mg/130ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38065011000001103,Fluorouracil 3950mg/300ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38065111000001102,Fluorouracil 4450mg/130ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38065211000001108,Fluorouracil 4450mg/300ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38065311000001100,Fluorouracil 5000mg/130ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38065411000001107,Fluorouracil 5000mg/300ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38065511000001106,Fluorouracil 5650mg/130ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38065611000001105,Fluorouracil 5650mg/300ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38065711000001101,Fluorouracil 6400mg/300ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38065811000001109,Fluorouracil 7250mg/300ml in Sodium chloride 0.9% infusion elastomeric devices (product)
38066111000001108,Erlotinib 100mg tablets (Zentiva) (product)
38066311000001105,Erlotinib 150mg tablets (Zentiva) (product)
38082211000001100,Bortezomib 3.5mg powder for solution for injection vials (Mylan) (product)
38094411000001109,Erlotinib 25mg tablets (Mylan) (product)
38094711000001103,Erlotinib 100mg tablets (Mylan) (product)
38094911000001101,Erlotinib 150mg tablets (Mylan) (product)
38106911000001102,Cytarabine 20mg/1ml solution for injection pre-filled syringes (Special Order) (product)
38108911000001103,Cytarabine 20mg/1ml solution for injection pre-filled syringes (product)
3813911000001102,Leukeran 2mg tablets (GlaxoSmithKline) (product)
38140311000001105,Imuran 50mg tablets (DE Pharmaceuticals) (product)
38150711000001106,Mercaptopurine 50mg tablets (DE Pharmaceuticals) (product)
38150911000001108,Metoject PEN 7.5mg/0.15ml solution for injection pre-filled pens (DE Pharmaceuticals) (product)
38151111000001104,Metoject PEN 10mg/0.2ml solution for injection pre-filled pens (DE Pharmaceuticals) (product)
38151311000001102,Metoject PEN 12.5mg/0.25ml solution for injection pre-filled pens (DE Pharmaceuticals) (product)
38151511000001108,Metoject PEN 15mg/0.3ml solution for injection pre-filled pens (DE Pharmaceuticals) (product)
38153711000001102,Oxaliplatin 100mg/20ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
38160011000001100,Oxaliplatin 50mg/10ml concentrate for solution for infusion vials (Seacross Pharmaceuticals Ltd) (product)
38176011000001109,Xagrid 500microgram capsules (DE Pharmaceuticals) (product)
38178211000001103,Erlotinib 25mg tablets (Sandoz Ltd) (product)
38178411000001104,Erlotinib 100mg tablets (Sandoz Ltd) (product)
38178611000001101,Erlotinib 150mg tablets (Sandoz Ltd) (product)
38196011000001104,Infliximab 120mg/1ml solution for injection pre-filled disposable devices (product)
38196111000001103,Infliximab 120mg/1ml solution for injection pre-filled syringes (product)
38231011000001102,Fluorouracil 10mg/0.2ml solution for injection pre-filled syringes (Special Order) (product)
38234711000001102,Fluorouracil 10mg/0.2ml solution for injection pre-filled syringes (product)
38237411000001103,Azacitidine 100mg powder for suspension for injection vials (Accord Healthcare Ltd) (product)
38237611000001100,Arsenic 10mg/10ml concentrate for solution for infusion vials (Accord Healthcare Ltd) (product)
38239611000001105,Erlotinib 100mg tablets (Teva UK Ltd) (product)
38239811000001109,Erlotinib 150mg tablets (Teva UK Ltd) (product)
38242211000001104,Trecondi 1g powder for solution for infusion (medac UK) (product)
38242411000001100,Trecondi 5g powder for solution for infusion (medac UK) (product)
38251511000001106,Bortezomib 3.5mg powder for solution for injection vials (Actavis UK Ltd) (product)
38289211000001104,Entyvio 108mg/0.68ml solution for injection pre-filled syringes (Takeda UK Ltd) (product)
38289811000001103,Entyvio 108mg/0.68ml solution for injection pre-filled pens (Takeda UK Ltd) (product)
38301811000001108,Azacitidine 100mg powder for suspension for injection vials (Zentiva) (product)
3832911000001101,Puri-Nethol 50mg tablets (GlaxoSmithKline) (product)
38362011000001109,Vedolizumab 108mg/0.68ml solution for injection pre-filled disposable devices (product)
38362211000001104,Vedolizumab 108mg/0.68ml solution for injection pre-filled syringes (product)
38364311000001100,Idacio 40mg/0.8ml solution for injection pre-filled syringes (Fresenius Kabi Ltd) (product)
38366311000001106,Idacio 40mg/0.8ml solution for injection vials (Fresenius Kabi Ltd) (product)
38367611000001104,Idacio 40mg/0.8ml solution for injection pre-filled pens (Fresenius Kabi Ltd) (product)
383711000001107,Methotrexate 2.5mg tablets (Mayne Pharma Plc) (product)
38371911000001107,Cyramza 500mg/50ml concentrate for solution for infusion vials (Originalis B.V.) (product)
38372611000001107,Gazyvaro 1000mg/40ml concentrate for solution for infusion vials (Originalis B.V.) (product)
38372811000001106,Iressa 250mg tablets (Originalis B.V.) (product)
38373411000001100,Kadcyla 100mg powder for concentrate for solution for infusion vials (Originalis B.V.) (product)
38373611000001102,Kadcyla 160mg powder for concentrate for solution for infusion vials (Originalis B.V.) (product)
38373811000001103,Mekinist 0.5mg tablets (Originalis B.V.) (product)
38375311000001108,JEVTANA 60mg/1.5ml concentrate and solvent for solution for infusion vials (Originalis B.V.) (product)
38383211000001107,Erlotinib 25mg tablets (Accord Healthcare Ltd) (product)
38384211000001105,Erlotinib 100mg tablets (Accord Healthcare Ltd) (product)
38384411000001109,Erlotinib 150mg tablets (Accord Healthcare Ltd) (product)
38484211000001104,Zirabev 100mg/4ml solution for infusion vials (Pfizer Ltd) (product)
38485411000001104,Zirabev 400mg/16ml solution for infusion vials (Pfizer Ltd) (product)
38498711000001102,Azacitidine 100mg powder for suspension for injection vials (Seacross Pharmaceuticals Ltd) (product)
38517411000001103,Bortezomib 3.5mg powder for solution for injection vials (Zentiva) (product)
38523011000001107,Mycophenolate mofetil 250mg capsules (Tillomed Laboratories Ltd) (product)
38562011000001106,Erlotinib 150mg tablets (A A H Pharmaceuticals Ltd) (product)
38588911000001105,Ruxience 500mg/50ml concentrate for solution for infusion vials (Pfizer Ltd) (product)
38591311000001103,Trisenox 12mg/6ml concentrate for solution for infusion vials (Teva UK Ltd) (product)
38591611000001108,Arsenic 12mg/6ml solution for infusion vials (product)
38591811000001107,Ruxience 100mg/10ml concentrate for solution for infusion vials (Pfizer Ltd) (product)
38662811000001108,Mitomycin 40mg powder for solution for injection vials (Accord Healthcare Ltd) (product)
38688311000001104,Azacitidine 100mg powder for suspension for injection vials (Mylan) (product)
38696611000001107,Mitomycin 40mg powder for solution for injection vials (product)
38706111000001106,Arsenic 10mg/10ml concentrate for solution for infusion ampoules (Thornton & Ross Ltd) (product)
38707611000001101,Erlotinib 25mg tablets (Teva UK Ltd) (product)
38740411000001108,Arsenic 10mg/10ml solution for infusion ampoules (A A H Pharmaceuticals Ltd) (product)
38788911000001109,Anagrelide 500microgram capsules (Medihealth (Northern) Ltd) (product)
38801911000001101,Azathioprine 25mg tablets (Medihealth (Northern) Ltd) (product)
38802211000001103,Azathioprine 50mg tablets (Medihealth (Northern) Ltd) (product)
38961711000001108,Penicillamine 250mg tablets (Imported) (product)
3929011000001103,Myleran 2mg tablets (GlaxoSmithKline) (product)
395278001,Product containing precisely sirolimus 1 milligram/1 each conventional release oral tablet (clinical drug)
3965111000001108,Estracyt 140mg capsules (Pfizer Ltd) (product)
400231002,Paclitaxel 6mg/mL injection solution 50mL vial (product)
400565002,Product containing precisely cyclophosphamide (as cyclophosphamide monohydrate) 2 gram/1 vial powder for conventional release solution for injection (clinical drug)
400687000,Product containing precisely infliximab 100 milligram/1 vial powder for conventional release solution for injection (clinical drug)
400756007,Paclitaxel 6mg/mL injection solution 16.7mL vial (product)
400857008,Paclitaxel 6mg/mL injection solution 25mL vial (product)
4038811000001107,Alkeran 2mg tablets (GlaxoSmithKline) (product)
404111000001101,Arava 100mg tablets (Aventis Pharma) (product)
407101003,Product containing precisely gefitinib 250 milligram/1 each conventional release oral tablet (clinical drug)
407797002,Product containing precisely imatinib 100 milligram/1 each conventional release oral capsule (clinical drug)
408133009,Basiliximab 10mg injection (pdr for recon)+solvent (product)
408154002,Adalimumab 40mg injection solution 0.8mL prefilled syringe (product)
408155001,Product containing precisely sirolimus 2 milligram/1 each conventional release oral tablet (clinical drug)
4091011000001100,Rapamune 1mg/ml oral solution (Wyeth Laboratories) (product)
4091411000001109,Rapamune 1mg tablets (Wyeth Laboratories) (product)
409409000,Bevacizumab 25mg/mL injection solution 4mL vial (product)
409410005,Bevacizumab 25mg/mL injection solution 16mL vial (product)
4105311000001105,Sirolimus 1mg tablets (product)
410950003,Product containing precisely imatinib 400 milligram/1 each conventional release oral tablet (clinical drug)
41411000001107,Penicillamine 250mg tablets (Generics (UK) Ltd) (product)
414124007,Product containing precisely erlotinib (as erlotinib hydrochloride) 100 milligram/1 each conventional release oral tablet (clinical drug)
414125008,Product containing precisely erlotinib (as erlotinib hydrochloride) 150 milligram/1 each conventional release oral tablet (clinical drug)
414126009,Product containing precisely erlotinib (as erlotinib hydrochloride) 25 milligram/1 each conventional release oral tablet (clinical drug)
414461007,Product containing precisely imatinib 100 milligram/1 each conventional release oral tablet (clinical drug)
414462000,Product containing precisely imatinib 400 milligram/1 each conventional release oral capsule (clinical drug)
414806008,Natalizumab 300mg injection solution 15mL vial (product)
4156611000001102,Enbrel 25mg powder and solvent for solution for injection vials (Wyeth Laboratories) (product)
416803003,Product containing precisely paclitaxel 100 milligram/1 vial powder for conventional release suspension for injection (clinical drug)
41911000001104,Azathioprine 50mg tablets (A A H Pharmaceuticals Ltd) (product)
4200711000001102,Lanvis 40mg tablets (GlaxoSmithKline) (product)
420238002,Etanercept 50mg powder and solvent for injection solution vial (product)
420637003,Product containing precisely sunitinib (as sunitinib malate) 25 milligram/1 each conventional release oral capsule (clinical drug)
420897004,Product containing precisely sunitinib (as sunitinib malate) 12.5 milligram/1 each conventional release oral capsule (clinical drug)
420966002,Product containing precisely lenalidomide 10 milligram/1 each conventional release oral capsule (clinical drug)
420994005,Product containing precisely sorafenib (as sorafenib tosylate) 200 milligram/1 each conventional release oral tablet (clinical drug)
421398007,Product containing precisely sunitinib (as sunitinib malate) 50 milligram/1 each conventional release oral capsule (clinical drug)
422330004,Product containing precisely lenalidomide 5 milligram/1 each conventional release oral capsule (clinical drug)
424058002,Product containing precisely dasatinib 20 milligram/1 each conventional release oral tablet (clinical drug)
424254006,Product containing precisely dasatinib 50 milligram/1 each conventional release oral tablet (clinical drug)
424939008,Panitumumab 20mg/mL injection solution 5mL vial (product)
425166003,Product containing precisely dasatinib 70 milligram/1 each conventional release oral tablet (clinical drug)
426040006,Eculizumab 10mg/mL injection solution 30mL vial (product)
426269005,Product containing precisely lapatinib ditosylate 250 milligram/1 each conventional release oral tablet (clinical drug)
426944004,Temsirolimus 25mg/mL injection solution vial + diluent (product)
427960006,Product containing precisely topotecan 1 milligram/1 each conventional release oral capsule (clinical drug)
427962003,Product containing precisely nilotinib (as nilotinib hydrochloride monohydrate) 200 milligram/1 each conventional release oral capsule (clinical drug)
428011000001101,Azathioprine 50mg tablets (Sandoz Ltd) (product)
428403002,Product containing precisely topotecan 250 microgram/1 each conventional release oral capsule (clinical drug)
4329311000001108,Targretin 75mg capsules (Medeus Pharma) (product)
4332011000001100,Glivec 100mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
4337611000001105,Bexarotene 75mg capsules (product)
4337811000001109,Imatinib 100mg capsules (product)
4346311000001104,CellCept 500mg powder for solution for injection vials (Roche Products Ltd) (product)
4355111000001105,Fludara 10mg tablets (Schering Health Care Ltd) (product)
4367011000001108,Lomustine 40mg capsules (Medac GMBH) (product)
4391311000001103,Prograf 5mg/1ml solution for injection ampoules (Fujisawa Ltd) (product)
4398011000001107,Remicade 100mg powder for solution for injection vials (Schering-Plough Ltd) (product)
441726005,Product containing precisely everolimus 5 milligram/1 each conventional release oral tablet (clinical drug)
441953000,Product containing precisely everolimus 10 milligram/1 each conventional release oral tablet (clinical drug)
4419711000001107,Treosulfan 250mg capsules (A A H Pharmaceuticals Ltd) (product)
4419911000001109,Treosulfan 250mg capsules (Unichem Plc) (product)
4420211000001101,Temodal 20mg capsules (Schering-Plough Ltd) (product)
4420511000001103,Temodal 100mg capsules (Schering-Plough Ltd) (product)
4420811000001100,Temodal 250mg capsules (Schering-Plough Ltd) (product)
4427711000001109,Infliximab 100mg powder for solution for injection vials (product)
4430311000001107,Vepesid 50mg capsules (Cheplapharm Arzneimittel GmbH) (product)
4430611000001102,Vepesid 100mg capsules (Cheplapharm Arzneimittel GmbH) (product)
4430911000001108,Vepesid 100mg/5ml solution for injection vials (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
443785004,Product containing precisely pazopanib 200 milligram/1 each conventional release oral tablet (clinical drug)
443997005,Product containing precisely pazopanib 400 milligram/1 each conventional release oral tablet (clinical drug)
4445211000001107,Xeloda 150mg tablets (Roche Products Ltd) (product)
4445511000001105,Xeloda 500mg tablets (Roche Products Ltd) (product)
4453011000001100,Uftoral capsules (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
4454611000001105,Zavedos 5mg capsules (Pfizer Ltd) (product)
4455011000001104,Zavedos 10mg capsules (Pfizer Ltd) (product)
4455411000001108,Zavedos 25mg capsules (Pfizer Ltd) (product)
4455911000001100,Zavedos 5mg powder for solution for injection vials (Pfizer Ltd) (product)
4456211000001103,Zavedos 10mg powder for solution for injection vials (Pfizer Ltd) (product)
446482007,Product containing precisely everolimus 500 microgram/1 each conventional release oral tablet (clinical drug)
446483002,Product containing precisely everolimus 750 microgram/1 each conventional release oral tablet (clinical drug)
4465211000001102,Mitoxantrone 20mg/10ml solution for injection vials (Mayne Pharma Plc) (product)
4465811000001101,Novantrone 20mg/10ml solution for injection vials (Wyeth Laboratories) (product)
4466011000001103,Onkotrone 20mg/10ml solution for injection vials (ASTA Medica Ltd) (product)
4467411000001109,Onkotrone 25mg/12.5ml solution for injection vials (ASTA Medica Ltd) (product)
4469711000001106,Novantrone 25mg/12.5ml solution for injection vials (Wyeth Laboratories) (product)
447132004,Product containing precisely everolimus 250 microgram/1 each conventional release oral tablet (clinical drug)
4471911000001104,Novantrone 30mg/15ml solution for injection vials (Wyeth Laboratories) (product)
4474711000001103,Onkotrone 30mg/15ml solution for injection vials (ASTA Medica Ltd) (product)
4475511000001109,Cisplatin 10mg/10ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4475811000001107,Cisplatin 10mg/10ml solution for injection vials (Mayne Pharma Plc) (product)
4476011000001105,Cisplatin 10mg/10ml solution for injection vials (Unichem Plc) (product)
4476611000001103,Cisplatin 50mg/50ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4476911000001109,Cisplatin 50mg/50ml solution for injection vials (Mayne Pharma Plc) (product)
4477311000001106,Cisplatin 50mg/50ml solution for injection vials (Unichem Plc) (product)
4477811000001102,Cisplatin 100mg/100ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4478011000001109,Cisplatin 100mg/100ml solution for injection vials (C P Pharmaceuticals Ltd) (product)
4478311000001107,Cisplatin 100mg/100ml solution for injection vials (Mayne Pharma Plc) (product)
4478711000001106,Cisplatin 100mg/100ml solution for injection vials (Unichem Plc) (product)
4483411000001100,Mitoxantrone 20mg/10ml solution for injection vials (product)
4483511000001101,Mitoxantrone 25mg/12.5ml solution for injection vials (product)
4483611000001102,Mitoxantrone 30mg/15ml solution for injection vials (product)
4488611000001109,Cisplatin 100mg/100ml solution for injection vials (product)
4488711000001100,Cisplatin 10mg/10ml solution for injection vials (product)
4488811000001108,Cisplatin 50mg/50ml solution for injection vials (product)
4489611000001100,Pharmorubicin Rapid Dissolution 20mg powder for solution for injection vials (Pfizer Ltd) (product)
4494511000001102,Pharmorubicin Rapid Dissolution 50mg powder for solution for injection vials (Pfizer Ltd) (product)
4496611000001107,Cosmegen Lyovac 500microgram powder for solution for injection vials (Recordati Rare Diseases UK Ltd) (product)
4511211000001109,Razoxane 125mg tablets (A A H Pharmaceuticals Ltd) (product)
4511411000001108,Razoxane 125mg tablets (Cambridge Laboratories) (product)
4511611000001106,Razoxane 125mg tablets (Unichem Plc) (product)
4564711000001100,Rapamune 2mg tablets (Wyeth Laboratories) (product)
456811000001107,Neoral 100mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
4595211000001106,DTIC-DOME 200mg powder for solution for injection vials (Bayer Plc) (product)
4595711000001104,Dacarbazine 200mg powder for solution for injection vials (Mayne Pharma Plc) (product)
4601411000001102,Sirolimus 2mg tablets (product)
4619811000001101,Alkeran 50mg powder and solvent for solution for injection vials (GlaxoSmithKline) (product)
4625511000001105,Leukeran 5mg tablets (GlaxoSmithKline) (product)
4626011000001106,Taxotere 20mg/0.5ml solution for injection vials and diluent (Aventis Pharma) (product)
4629111000001104,Taxol 30mg/5ml solution for injection vials (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
4629411000001109,Taxol 100mg/16.7ml solution for injection vials (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
4630011000001106,Taxotere 80mg/2ml solution for injection vials and diluent (Aventis Pharma) (product)
4630811000001100,Docetaxel 20mg/0.5ml solution for injection vials and diluent (product)
4630911000001105,Docetaxel 80mg/2ml solution for injection vials and diluent (product)
4633411000001105,Paraplatin 150mg/15ml solution for injection vials (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
4634511000001107,Paraplatin 450mg/45ml solution for injection vials (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
4634911000001100,Nipent 10mg powder for solution for injection vials (Wyeth Laboratories) (product)
4635311000001102,Carboplatin 450mg/45ml solution for injection vials (Mayne Pharma Plc) (product)
4635611000001107,Carboplatin 150mg/15ml solution for injection vials (Mayne Pharma Plc) (product)
4638011000001108,Paclitaxel 30mg/5ml solution for injection vials (product)
4639311000001100,Carboplatin 150mg/15ml solution for injection vials (product)
4639411000001107,Carboplatin 450mg/45ml solution for injection vials (product)
4642211000001104,Paraplatin 50mg/5ml solution for injection vials (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
4642411000001100,Carboplatin 50mg/5ml solution for injection vials (Mayne Pharma Plc) (product)
4643411000001109,Paraplatin 600mg/60ml solution for injection vials (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
4644511000001106,Carboplatin 600mg/60ml solution for injection vials (Mayne Pharma Plc) (product)
4651711000001101,Chlorambucil 5mg tablets (product)
4651811000001109,Carboplatin 50mg/5ml solution for injection vials (product)
4651911000001104,Carboplatin 600mg/60ml solution for injection vials (product)
4673411000001108,Cisplatin 50mg powder for solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4673611000001106,Cisplatin 50mg powder for solution for injection vials (Pfizer Ltd) (product)
4676911000001106,Cytarabine 1g/10ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4677511000001102,Cytarabine 1g/10ml solution for injection vials (Mayne Pharma Plc) (product)
4677711000001107,Cytarabine 1g/10ml solution for injection vials (Pfizer Ltd) (product)
4678011000001106,Cytarabine 500mg/5ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4678211000001101,Cytarabine 500mg/5ml solution for injection vials (Mayne Pharma Plc) (product)
4678511000001103,Cytarabine 2g/20ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4678711000001108,Cytarabine 2g/20ml solution for injection vials (Mayne Pharma Plc) (product)
4678911000001105,Cytarabine 2g/20ml solution for injection vials (Pfizer Ltd) (product)
4679211000001106,Cytarabine 100mg/1ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4679411000001105,Cytarabine 100mg/1ml solution for injection vials (Mayne Pharma Plc) (product)
4679811000001107,Cytarabine 100mg/5ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4680011000001101,Cytarabine 100mg/5ml solution for injection vials (Mayne Pharma Plc) (product)
4680211000001106,Cytarabine 20mg/ml solution for injection vials (Pfizer Ltd) (product)
4680511000001109,Cytarabine 500mg/25ml solution for injection vials (Pfizer Ltd) (product)
4680811000001107,"Bleo-Kyowa 15,000unit powder for solution for injection vials (Kyowa Hakko) (product)"
4683211000001101,Doxorubicin 10mg/5ml solution for injection vials (Pfizer Ltd) (product)
4683411000001102,Doxorubicin 10mg/5ml solution for injection vials (Unichem Plc) (product)
4683611000001104,Doxorubicin Cytosafe 10mg/5ml solution for injection vials (Pfizer Ltd) (product)
4684511000001100,Doxorubicin 50mg/25ml solution for injection vials (Unichem Plc) (product)
4684811000001102,Doxorubicin 50mg/25ml solution for injection vials (Pfizer Ltd) (product)
4685211000001102,Doxorubicin Cytosafe 50mg/25ml solution for injection vials (Pfizer Ltd) (product)
4685511000001104,Doxorubicin 200mg/100ml solution for injection vials (Pfizer Ltd) (product)
4686511000001106,Doxorubicin 10mg powder for solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4686811000001109,Doxorubicin 10mg powder for solution for injection vials (Mayne Pharma Plc) (product)
4687011000001100,Doxorubicin Rapid Dissolution 10mg powder for solution for injection vials (Pfizer Ltd) (product)
4688311000001101,Doxorubicin 50mg powder for solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4688511000001107,Doxorubicin 50mg powder for solution for injection vials (Mayne Pharma Plc) (product)
4688911000001100,Doxorubicin Rapid Dissolution 50mg powder for solution for injection vials (Pfizer Ltd) (product)
4690811000001106,DaunoXome 50mg emulsion for injection vials (Gilead Sciences) (product)
4691711000001106,Daunorubicin 20mg powder for solution for injection vials (Beacon Pharmaceuticals Ltd) (product)
4694211000001102,Daunorubicin (liposomal) 50mg emulsion for injection vials (product)
4694311000001105,"Bleomycin 15,000unit powder for solution for injection vials (product)"
4696711000001100,Campto 100mg/5ml solution for injection vials (Pfizer Ltd) (product)
4699111000001109,Cytarabine 100mg/5ml solution for injection vials (product)
4700511000001101,Doxorubicin 50mg/25ml solution for injection vials (product)
4700611000001102,Doxorubicin 10mg/5ml solution for injection vials (product)
4701011000001100,Cisplatin 50mg powder for solution for injection vials (product)
4742011000001102,Etoposide 200mg/10ml solution for injection vials (Mayne Pharma Plc) (product)
4747011000001100,Etoposide 200mg/10ml solution for injection vials (product)
4748711000001102,Kineret 100mg/0.67ml solution for injection pre-filled syringes (Amgen Ltd) (product)
4751711000001105,Anakinra 100mg/0.67ml solution for injection pre-filled syringes (product)
4753111000001105,Leustat 10mg/10ml solution for injection vials (Janssen-Cilag Ltd) (product)
4756511000001109,Gemzar 1g powder for solution for injection vials (Eli Lilly & Co Ltd) (product)
4762311000001105,Platinex 50mg/50ml solution for injection vials (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
4762511000001104,Platinex 100mg/100ml solution for injection vials (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
4762811000001101,"Erwinase 10,000unit powder for solution for injection vials (Ipsen Ltd) (product)"
4767011000001109,Pharmorubicin Rapid Dissolution 10mg powder for solution for injection vials (Pfizer Ltd) (product)
4771111000001107,Gemzar 200mg powder for solution for injection vials (Eli Lilly & Co Ltd) (product)
4773411000001103,Simulect 20mg powder and solvent for solution for injection vials (Novartis Pharmaceuticals UK Ltd) (product)
4780911000001109,Zenapax 25mg/5ml solution for injection vials (Roche Products Ltd) (product)
4785711000001102,Etopophos 100mg powder for solution for injection vials (Cheplapharm Arzneimittel GmbH) (product)
4800711000001108,Navelbine 10mg/1ml solution for injection vials (Pierre Fabre Ltd) (product)
4802711000001107,Hycamtin 4mg powder for solution for injection vials (GlaxoSmithKline) (product)
4803011000001101,Herceptin 150mg powder for solution for injection vials (Roche Products Ltd) (product)
4803311000001103,Treosulfan 1g powder for solution for injection vials (Medac GMBH) (product)
4803611000001108,Treosulfan 5g powder for solution for injection vials (Medac GMBH) (product)
4804211000001109,Navelbine 50mg/5ml solution for injection vials (Pierre Fabre Ltd) (product)
4811811000001106,Visudyne 15mg powder for solution for infusion vials (Cheplapharm Arzneimittel GmbH) (product)
4812011000001108,Trastuzumab 150mg powder for solution for injection vials (product)
4812711000001105,Velbe 10mg powder for solution for injection vials (Eli Lilly & Co Ltd) (product)
4813011000001104,Vinblastine 10mg/10ml solution for injection vials (Mayne Pharma Plc) (product)
4813511000001107,Vincristine 1mg/1ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4813911000001100,Oncovin 1mg/1ml solution for injection vials (Eli Lilly & Co Ltd) (product)
4814411000001106,Vincristine 1mg/1ml solution for injection vials (Mayne Pharma Plc) (product)
4815211000001108,Vincristine 2mg/2ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4815511000001106,Vincristine 2mg/2ml solution for injection vials (Mayne Pharma Plc) (product)
4815711000001101,Vincristine 2mg/2ml solution for injection vials (Unichem Plc) (product)
4816311000001105,Vincristine 5mg/5ml solution for injection vials (Mayne Pharma Plc) (product)
4821411000001100,Cytarabine 100mg/5ml solution for injection vials (Unichem Plc) (product)
4821811000001103,Cytarabine 500mg/25ml solution for injection vials (Unichem Plc) (product)
4822211000001106,Cytarabine 1g/10ml solution for injection vials (Unichem Plc) (product)
4822411000001105,Cytarabine 2g/20ml solution for injection vials (Unichem Plc) (product)
4830011000001102,Taxol 300mg/50ml solution for injection vials (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
483011000001100,Penicillamine 125mg tablets (Unichem Plc) (product)
4840911000001104,Alkeran 5mg tablets (GlaxoSmithKline) (product)
4843711000001105,Melphalan 5mg tablets (product)
4844711000001107,BiCNU 100mg powder and solvent for solution for injection vials (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
4846111000001104,Fludara 50mg powder for solution for injection vials (Schering Health Care Ltd) (product)
4849111000001107,Caelyx 20mg/10ml solution for injection vials (Schering-Plough Ltd) (product)
4849211000001101,Treosulfan 250mg capsules (Medac GMBH) (product)
4849611000001104,Caelyx 50mg/25ml solution for injection vials (Schering-Plough Ltd) (product)
4853111000001107,Pharmorubicin 10mg/5ml solution for injection vials (Pfizer Ltd) (product)
4853411000001102,Pharmorubicin 50mg/25ml solution for injection vials (Pfizer Ltd) (product)
4881311000001100,CellCept 1g/5ml oral suspension (Roche Products Ltd) (product)
4897811000001103,Mycophenolate mofetil 1g/5ml oral suspension sugar free (product)
494311000001101,Myocrisin 20mg/0.5ml solution for injection ampoules (JHC Healthcare Ltd) (product)
4943611000001108,Dacarbazine 600mg powder for solution for injection vials (Mayne Pharma Plc) (product)
4948711000001105,Fluorouracil 250mg capsules (Cambridge Laboratories) (product)
4950411000001104,Fluorouracil 500mg/10ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4951111000001103,Fluorouracil 500mg/10ml solution for injection vials (Mayne Pharma Plc) (product)
4951311000001101,Fluorouracil 500mg/10ml solution for injection vials (Medac GMBH) (product)
4954711000001104,Fluorouracil 1g/20ml solution for injection vials (Mayne Pharma Plc) (product)
4954911000001102,Fluorouracil 1g/20ml solution for injection vials (Medac GMBH) (product)
4956811000001100,Dacarbazine 600mg powder for solution for injection vials (product)
4957011000001109,Fluorouracil 1g/20ml solution for injection vials (product)
4958811000001104,Fluorouracil 2.5g/50ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
4959011000001100,Fluorouracil 2.5g/50ml solution for injection vials (Mayne Pharma Plc) (product)
4959311000001102,Fluorouracil 2.5g/50ml solution for injection vials (Medac GMBH) (product)
4962711000001103,Fluorouracil 5g/100ml solution for injection vials (Mayne Pharma Plc) (product)
4963311000001107,Fluorouracil 5g/100ml solution for injection vials (Medac GMBH) (product)
4969811000001101,Fluorouracil 5g/100ml solution for injection vials (product)
498611000001101,Penicillamine 125mg tablets (Kent Pharmaceuticals Ltd) (product)
499111000001102,Arava 10mg tablets (Aventis Pharma) (product)
4998511000001107,Procarbazine 50mg capsules (A A H Pharmaceuticals Ltd) (product)
4998711000001102,Procarbazine 50mg capsules (Cambridge Laboratories) (product)
4998911000001100,Procarbazine 50mg capsules (Unichem Plc) (product)
5007511000001108,Humira 40mg/0.8ml solution for injection pre-filled syringes (Abbott Laboratories Ltd) (product)
5007811000001106,Simulect 10mg powder and solvent for solution for injection vials (Novartis Pharmaceuticals UK Ltd) (product)
5009111000001105,Cyclophosphamide 500mg powder for solution for injection vials (A A H Pharmaceuticals Ltd) (product)
5009611000001102,Endoxana 500mg powder for solution for injection vials (Baxter Healthcare Ltd) (product)
5009911000001108,Cyclophosphamide 500mg powder for solution for injection vials (Pfizer Ltd) (product)
5010211000001108,Cyclophosphamide 500mg powder for solution for injection vials (Unichem Plc) (product)
5051611000001109,Cytarabine 500mg/25ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
5305411000001102,Neoral 100mg/ml oral solution (PI) (Dowelhurst Ltd) (product)
5347111000001105,CellCept 250mg capsules (PI) (Waymade Ltd) (product)
5347711000001106,CellCept 500mg tablets (PI) (Waymade Ltd) (product)
5375011000001101,Imuran 25mg tablets (PI) (Waymade Ltd) (product)
5393711000001105,Neoral 25mg capsules (PI) (Waymade Ltd) (product)
5394111000001106,Neoral 50mg capsules (PI) (Waymade Ltd) (product)
5394311000001108,Neoral 100mg capsules (PI) (Waymade Ltd) (product)
5397211000001107,Neoral 100mg/ml oral solution (PI) (Waymade Ltd) (product)
544611000001107,Azathioprine 25mg tablets (Generics (UK) Ltd) (product)
5491311000001103,Prograf 1mg capsules (PI) (Waymade Ltd) (product)
5493011000001100,Azathioprine 25mg tablets (PI) (Dowelhurst Ltd) (product)
5494911000001104,Azathioprine 50mg tablets (PI) (Dowelhurst Ltd) (product)
5552111000001108,Imuran 25mg tablets (PI) (Dowelhurst Ltd) (product)
5552411000001103,Imuran 50mg tablets (PI) (Dowelhurst Ltd) (product)
5570811000001104,Prograf 1mg capsules (PI) (Dowelhurst Ltd) (product)
5571711000001104,Neoral 100mg capsules (PI) (Dowelhurst Ltd) (product)
5572411000001100,Neoral 25mg capsules (PI) (Dowelhurst Ltd) (product)
5574011000001103,Neoral 50mg capsules (PI) (Dowelhurst Ltd) (product)
5866911000001101,Azathioprine 25mg tablets (Alpharma Limited) (product)
611111000001100,Azathioprine 25mg tablets (Unichem Plc) (product)
62411000001105,Arava 20mg tablets (Aventis Pharma) (product)
638611000001108,Sandimmun 50mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
644711000001108,Maxtrex 2.5mg tablets (Pfizer Ltd) (product)
655811000001102,Fluorouracil 500mg/20ml solution for injection vials (A A H Pharmaceuticals Ltd) (product)
656111000001103,Prograf 500microgram capsules (Fujisawa Ltd) (product)
660811000001100,Neoral 25mg capsules (Novartis Pharmaceuticals UK Ltd) (product)
675711000001108,Imuran 50mg tablets (GlaxoSmithKline) (product)
679611000001101,Myocrisin 10mg/0.5ml solution for injection ampoules (JHC Healthcare Ltd) (product)
683611000001105,Methotrexate 2.5mg tablets (Wyeth Laboratories) (product)
690211000001104,Penicillamine 125mg tablets (Approved Prescription Services) (product)
703581000,Product containing precisely afatinib dimaleate 20 milligram/1 each conventional release oral tablet (clinical drug)
703583002,Product containing precisely afatinib dimaleate 30 milligram/1 each conventional release oral tablet (clinical drug)
703584008,Product containing precisely afatinib dimaleate 40 milligram/1 each conventional release oral tablet (clinical drug)
703587001,Product containing precisely bosutinib monohydrate 100 milligram/1 each conventional release oral tablet (clinical drug)
703588006,Product containing precisely bosutinib monohydrate 500 milligram/1 each conventional release oral tablet (clinical drug)
703639002,Product containing precisely crizotinib 200 milligram/1 each conventional release oral capsule (clinical drug)
703640000,Product containing precisely crizotinib 250 milligram/1 each conventional release oral capsule (clinical drug)
703647002,Product containing precisely dabrafenib (as dabrafenib mesilate) 50 milligram/1 each conventional release oral capsule (clinical drug)
703648007,Product containing precisely dabrafenib (as dabrafenib mesilate) 75 milligram/1 each conventional release oral capsule (clinical drug)
703780001,Product containing precisely ruxolitinib 5 milligram/1 each conventional release oral tablet (clinical drug)
703781002,Product containing precisely ruxolitinib 10 milligram/1 each conventional release oral tablet (clinical drug)
703788008,Product containing precisely teriflunomide 14 milligram/1 each conventional release oral tablet (clinical drug)
703791008,Product containing precisely pomalidomide 1 milligram/1 each conventional release oral capsule (clinical drug)
703792001,Product containing precisely pomalidomide 2 milligram/1 each conventional release oral capsule (clinical drug)
703793006,Product containing precisely pomalidomide 3 milligram/1 each conventional release oral capsule (clinical drug)
703794000,Product containing precisely pomalidomide 4 milligram/1 each conventional release oral capsule (clinical drug)
703799005,Product containing precisely ponatinib (as ponatinib hydrochloride) 15 milligram/1 each conventional release oral tablet (clinical drug)
703800009,Product containing precisely ponatinib (as ponatinib hydrochloride) 45 milligram/1 each conventional release oral tablet (clinical drug)
703809005,Product containing precisely regorafenib 40 milligram/1 each conventional release oral tablet (clinical drug)
703814009,Product containing precisely vismodegib 150 milligram/1 each conventional release oral capsule (clinical drug)
706911000001103,Methotrexate 2.5mg tablets (Unichem Plc) (product)
708911000001104,Hydrea 500mg capsules (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
715511000001100,Azathioprine 50mg tablets (Approved Prescription Services) (product)
7258211000001106,Endoxana 1g powder for solution for injection vials (Baxter Healthcare Ltd) (product)
7258311000001103,Cyclophosphamide 1g powder for solution for injection vials (Pfizer Ltd) (product)
7262611000001104,Endoxana 200mg powder for solution for injection vials (Baxter Healthcare Ltd) (product)
7267211000001103,Mitoxana 2g powder for solution for injection vials (Baxter Healthcare Ltd) (product)
7268711000001106,Mitoxana 1g powder for solution for injection vials (Baxter Healthcare Ltd) (product)
7274311000001106,Thiotepa 15mg powder for solution for injection vials (Cyanamid UK) (product)
7275711000001109,Mitomycin-C Kyowa 40mg powder for intravesical solution vials (Kyowa Kirin Ltd) (product)
7275911000001106,Mitomycin-C Kyowa 10mg powder for solution for injection vials (Kyowa Hakko) (product)
7276211000001108,Mitomycin-C Kyowa 20mg powder for solution for injection vials (Kyowa Hakko) (product)
7276411000001107,Mitomycin-C Kyowa 2mg powder for solution for injection vials (Kyowa Hakko) (product)
7309311000001105,Tomudex 2mg powder for solution for injection vials (AstraZeneca) (product)
7309811000001101,Eloxatin 50mg powder for solution for injection vials (Sanofi-Synthelabo Ltd) (product)
7310011000001101,Eloxatin 100mg powder for solution for injection vials (Sanofi-Synthelabo Ltd) (product)
7315711000001109,Hycamtin 1mg powder for solution for injection vials (SmithKline Beecham Pharmaceuticals) (product)
7319811000001103,Glivec 400mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
7321111000001100,Pharmorubicin 200mg/100ml solution for injection vials (Pfizer Ltd) (product)
7322611000001102,Imatinib 400mg tablets (product)
7322711000001106,Dacarbazine 100mg powder for solution for injection vials (product)
7322811000001103,Dacarbazine 500mg powder for solution for injection vials (product)
7322911000001108,Dacarbazine 1g powder for solution for injection vials (product)
7323311000001102,Dacarbazine 1g powder for solution for injection vials (Medac GMBH) (product)
7323411000001109,Dacarbazine 100mg powder for injection vials (Medac GMBH) (product)
7323511000001108,Dacarbazine 500mg powder for solution for injection vials (Medac GMBH) (product)
744711000001104,Azathioprine 25mg tablets (A A H Pharmaceuticals Ltd) (product)
745811000001108,Penicillamine 125mg tablets (Generics (UK) Ltd) (product)
7466111000001105,Carboplatin 50mg/5ml solution for injection vials (C P Pharmaceuticals Ltd) (product)
7466511000001101,Carboplatin 150mg/15ml solution for injection vials (C P Pharmaceuticals Ltd) (product)
7467111000001108,Carboplatin 450mg/45ml solution for injection vials (C P Pharmaceuticals Ltd) (product)
7501011000001106,Eldisine 5mg powder for solution for injection vials (Clonmel Healthcare Ltd) (product)
7513011000001109,Velcade 3.5mg powder for solution for injection vials (Ortho Biotech) (product)
752211000001104,Prograf 5mg capsules (Fujisawa Ltd) (product)
7525711000001100,Bortezomib 3.5mg powder for solution for injection vials (product)
7533111000001100,Busulfan 60mg/10ml solution for injection ampoules (product)
7533311000001103,Busilvex 60mg/10ml solution for injection ampoules (Pierre Fabre Ltd) (product)
7542511000001101,Arsenic 10mg/10ml solution for injection ampoules (product)
7553411000001106,Carmustine 7.7mg implant (product)
7553611000001109,Gliadel 7.7mg implant (Link Pharmaceuticals Ltd) (product)
7553911000001103,Paxene 100mg/16.7ml solution for injection vials (Mayne Pharma Plc) (product)
7554611000001107,Paxene 30mg/5ml solution for injection vials (Mayne Pharma Plc) (product)
7554911000001101,Paxene 300mg/50ml solution for injection vials (Mayne Pharma Plc) (product)
7556411000001101,Paxene 150mg/25ml solution for injection vials (Mayne Pharma Plc) (product)
7591711000001106,Cytarabine 50mg/5ml intrathecal suspension for injection vials (product)
7591911000001108,DepoCyte 50mg/5ml intrathecal suspension for injection vials (Napp Pharmaceuticals Ltd) (product)
7602611000001102,Trisenox 10mg/10ml solution for injection (Cell Therapeutics (UK) Ltd) (product)
764611000001101,Penicillamine 250mg tablets (Unichem Plc) (product)
7654211000001102,Etoposide 500mg/25ml solution for injection vials (product)
7654411000001103,Eposin 500mg/25ml solution for injection vials (Medac GMBH) (product)
7655711000001108,Amsidine 75mg/1.5ml solution for injection vials and diluent (Goldshield Healthcare Ltd) (product)
7659211000001103,Eposin 100mg/5ml solution for injection vials (Medac GMBH) (product)
7693411000001106,Alemtuzumab 30mg/3ml solution for injection ampoules (product)
7694211000001105,Mabcampath 30mg/3ml solution for injection ampoules (Schering Health Care Ltd) (product)
7695711000001104,MabThera 100mg/10ml solution for injection vials (Roche Products Ltd) (product)
7697011000001108,MabThera 500mg/50ml solution for injection vials (Roche Products Ltd) (product)
7714811000001101,Cetuximab 100mg/50ml solution for injection vials (product)
7715011000001106,Erbitux 100mg/50ml solution for injection vials (Merck Pharmaceuticals) (product)
7815711000001106,Temoporfin 20mg/5ml solution for injection vials (product)
7816311000001102,Foscan 20mg/5ml solution for injection vials (Biolitec Pharma) (product)
786611000001108,Myocrisin 50mg/0.5ml solution for injection ampoules (JHC Healthcare Ltd) (product)
795511000001101,Penicillamine 250mg tablets (Alpharma Limited) (product)
8076911000001104,Mycophenolic acid 180mg gastro-resistant tablets (product)
8077011000001100,Mycophenolic acid 360mg gastro-resistant tablets (product)
8077511000001108,Myfortic 180mg gastro-resistant tablets (Novartis Pharmaceuticals UK Ltd) (product)
8077811000001106,Myfortic 360mg gastro-resistant tablets (Novartis Pharmaceuticals UK Ltd) (product)
8089311000001103,Campto 40mg/2ml solution for injection vials (Pfizer Ltd) (product)
8089611000001108,Glivec 100mg tablets (Novartis Pharmaceuticals UK Ltd) (product)
8100311000001104,Imatinib 100mg tablets (product)
8170311000001107,Lomustine 40mg capsules (Unichem Plc) (product)
8246011000001106,Raptiva 125mg powder and solvent for solution for injection vials (Serono Laboratories (UK) Ltd) (product)
8259811000001108,Azathioprine 100mg/5ml oral solution (Special Order) (product)
8260111000001100,Azathioprine 100mg/5ml oral suspension (Special Order) (product)
8260411000001105,Azathioprine 120mg/5ml oral solution (Special Order) (product)
8260811000001107,Azathioprine 120mg/5ml oral suspension (Special Order) (product)
8261211000001100,Azathioprine 150mg/5ml oral solution (Special Order) (product)
8262111000001101,Azathioprine 13mg/5ml oral solution (Special Order) (product)
8262811000001108,Azathioprine 10mg/5ml oral solution (Special Order) (product)
8262911000001103,Azathioprine 150mg/5ml oral suspension (Special Order) (product)
8263111000001107,Azathioprine 15mg/5ml oral solution (Special Order) (product)
8263511000001103,Azathioprine 13mg/5ml oral suspension (Special Order) (product)
8264111000001109,Azathioprine 10mg/5ml oral suspension (Special Order) (product)
8264311000001106,Azathioprine 15mg/5ml oral suspension (Special Order) (product)
8264611000001101,Azathioprine 17.5mg/5ml oral solution (Special Order) (product)
8265411000001103,Azathioprine 12mg/5ml oral solution (Special Order) (product)
8265911000001106,Azathioprine 2.5mg/5ml oral solution (Special Order) (product)
8266011000001103,Azathioprine 17.5mg/5ml oral suspension (Special Order) (product)
8266211000001108,Azathioprine 12mg/5ml oral suspension (Special Order) (product)
8267211000001105,Azathioprine 20mg/5ml oral solution (Special Order) (product)
8267811000001106,Azathioprine 2.5mg/5ml oral suspension (Special Order) (product)
8268111000001103,Azathioprine 20mg/5ml oral suspension (Special Order) (product)
8268511000001107,Azathioprine 30mg/5ml oral solution (Special Order) (product)
8268711000001102,Azathioprine 25mg/5ml oral solution (Special Order) (product)
8269111000001105,Azathioprine 30mg/5ml oral suspension (Special Order) (product)
8269711000001106,Azathioprine 25mg/5ml oral suspension (Special Order) (product)
8272311000001109,Azathioprine 40mg/5ml oral solution (Special Order) (product)
8273411000001106,Azathioprine 5mg/5ml oral solution (Special Order) (product)
8274811000001106,Azathioprine 50mg/5ml oral solution (Special Order) (product)
8275911000001102,Azathioprine 5mg/5ml oral suspension (Special Order) (product)
8277711000001105,Azathioprine 40mg/5ml oral suspension (Special Order) (product)
8278511000001101,Azathioprine 50mg/5ml oral suspension (Special Order) (product)
8279411000001108,Azathioprine 75mg/5ml oral solution (Special Order) (product)
8280411000001108,Azathioprine 75mg/5ml oral suspension (Special Order) (product)
8281911000001107,Azathioprine 100mg/5ml oral solution (product)
8282011000001100,Azathioprine 100mg/5ml oral suspension (product)
8282111000001104,Azathioprine 10mg/5ml oral solution (product)
8282211000001105,Azathioprine 10mg/5ml oral suspension (product)
8282311000001102,Azathioprine 120mg/5ml oral solution (product)
8282411000001109,Azathioprine 120mg/5ml oral suspension (product)
8282511000001108,Azathioprine 12mg/5ml oral solution (product)
8282611000001107,Azathioprine 12mg/5ml oral suspension (product)
8282711000001103,Azathioprine 13mg/5ml oral solution (product)
8282811000001106,Azathioprine 13mg/5ml oral suspension (product)
8282911000001101,Azathioprine 150mg/5ml oral solution (product)
8283011000001109,Azathioprine 150mg/5ml oral suspension (product)
8283111000001105,Azathioprine 15mg/5ml oral solution (product)
8283211000001104,Azathioprine 15mg/5ml oral suspension (product)
8283311000001107,Azathioprine 17.5mg/5ml oral solution (product)
8283411000001100,Azathioprine 17.5mg/5ml oral suspension (product)
8283511000001101,Azathioprine 2.5mg/5ml oral solution (product)
8283611000001102,Azathioprine 2.5mg/5ml oral suspension (product)
8283811000001103,Azathioprine 20mg/5ml oral solution (product)
8283911000001108,Azathioprine 20mg/5ml oral suspension (product)
8284011000001106,Azathioprine 25mg/5ml oral solution (product)
8284111000001107,Azathioprine 25mg/5ml oral suspension (product)
8284211000001101,Azathioprine 30mg/5ml oral solution (product)
8285111000001106,Efalizumab 125mg powder and solvent for solution for injection vials (product)
8288511000001105,Azathioprine 60mg/5ml oral solution (Special Order) (product)
8290111000001102,Azathioprine 60mg/5ml oral suspension (Special Order) (product)
8291411000001103,Azathioprine 90mg/5ml oral solution (Special Order) (product)
8292211000001109,Azathioprine 90mg/5ml oral suspension (Special Order) (product)
8307511000001102,Azathioprine 90mg/5ml oral suspension (product)
8307711000001107,Azathioprine 90mg/5ml oral solution (product)
8307811000001104,Azathioprine 75mg/5ml oral suspension (product)
8307911000001109,Azathioprine 75mg/5ml oral solution (product)
8308011000001106,Azathioprine 60mg/5ml oral suspension (product)
8308111000001107,Azathioprine 60mg/5ml oral solution (product)
8308211000001101,Azathioprine 5mg/5ml oral suspension (product)
8308311000001109,Azathioprine 5mg/5ml oral solution (product)
8308411000001102,Azathioprine 50mg/5ml oral suspension (product)
8308511000001103,Azathioprine 50mg/5ml oral solution (product)
8308611000001104,Azathioprine 40mg/5ml oral suspension (product)
8308711000001108,Azathioprine 40mg/5ml oral solution (product)
8308811000001100,Azathioprine 30mg/5ml oral suspension (product)
8388611000001100,Azathioprine 25mg tablets (Approved Prescription Services) (product)
8409011000001109,Cyclophosphamide 25mg/5ml oral solution (Special Order) (product)
8409411000001100,Cyclophosphamide 50mg/5ml oral solution (Special Order) (product)
8409711000001106,Cyclophosphamide 25mg/5ml oral suspension (Special Order) (product)
841011000001102,Penicillamine 125mg tablets (Alpharma Limited) (product)
8410111000001102,Cyclophosphamide 100mg/5ml oral solution (Special Order) (product)
8410311000001100,Cyclophosphamide 50mg/5ml oral suspension (Special Order) (product)
8410911000001104,Cyclophosphamide 100mg/5ml oral suspension (Special Order) (product)
843311000001103,Azathioprine 50mg tablets (Generics (UK) Ltd) (product)
8450911000001105,Cyclophosphamide 100mg/5ml oral solution (product)
8451011000001102,Cyclophosphamide 100mg/5ml oral suspension (product)
8451111000001101,Cyclophosphamide 25mg/5ml oral solution (product)
8451211000001107,Cyclophosphamide 25mg/5ml oral suspension (product)
8451311000001104,Cyclophosphamide 50mg/5ml oral solution (product)
8451411000001106,Cyclophosphamide 50mg/5ml oral suspension (product)
8612811000001107,Mercaptopurine 100mg/5ml oral suspension (Special Order) (product)
8613411000001101,Mercaptopurine 25mg/5ml oral suspension (Special Order) (product)
8618111000001102,Methotrexate 10mg/5ml oral solution (Special Order) (product)
8618811000001109,Methotrexate 10mg/5ml oral suspension (Special Order) (product)
8619311000001106,Methotrexate 12.5mg/5ml oral solution (Special Order) (product)
8619611000001101,Methotrexate 12.5mg/5ml oral suspension (Special Order) (product)
8619911000001107,Methotrexate 15mg/5ml oral solution (Special Order) (product)
8620311000001107,Methotrexate 15mg/5ml oral suspension (Special Order) (product)
8622711000001105,Methotrexate 2.5mg/5ml oral solution (Special Order) (product)
8624211000001107,Methotrexate 2.5mg/5ml oral suspension (Special Order) (product)
8625811000001109,Methotrexate 7.5mg/5ml oral solution (Special Order) (product)
8625911000001104,Methotrexate 5mg/5ml oral solution (Special Order) (product)
8626411000001103,Methotrexate 7.5mg/5ml oral suspension (Special Order) (product)
8626511000001104,Methotrexate 5mg/5ml oral suspension (Special Order) (product)
863111000001105,Azathioprine 50mg tablets (Kent Pharmaceuticals Ltd) (product)
8663611000001102,Mercaptopurine 100mg/5ml oral suspension (product)
8663711000001106,Mercaptopurine 25mg/5ml oral suspension (product)
8664911000001105,Methotrexate 10mg/5ml oral solution (product)
8665011000001105,Methotrexate 10mg/5ml oral suspension (product)
8665111000001106,Methotrexate 12.5mg/5ml oral solution (product)
8665211000001100,Methotrexate 12.5mg/5ml oral suspension (product)
8665311000001108,Methotrexate 15mg/5ml oral solution (product)
8665411000001101,Methotrexate 15mg/5ml oral suspension (product)
8665611000001103,Methotrexate 2.5mg/5ml oral solution (product)
8665711000001107,Methotrexate 2.5mg/5ml oral suspension (product)
8665811000001104,Methotrexate 5mg/5ml oral solution (product)
8665911000001109,Methotrexate 5mg/5ml oral suspension (product)
8666011000001101,Methotrexate 7.5mg/5ml oral solution (product)
8666111000001100,Methotrexate 7.5mg/5ml oral suspension (product)
8708211000001102,Tacrolimus 2.5mg/5ml oral solution (Special Order) (product)
8708811000001101,Tacrolimus 2.5mg/5ml oral suspension (Special Order) (product)
8726011000001101,Tacrolimus 2.5mg/5ml oral suspension (product)
8726211000001106,Tacrolimus 2.5mg/5ml oral solution (product)
8733511000001103,Azathioprine 10mg capsules (Special Order) (product)
8742911000001104,Azathioprine 5mg capsules (Special Order) (product)
8743211000001102,Azathioprine 30mg capsules (Special Order) (product)
8759711000001105,Mercaptopurine 10mg capsules (Special Order) (product)
8791311000001100,Azathioprine 10mg capsules (product)
8791411000001107,Azathioprine 30mg capsules (product)
8791511000001106,Azathioprine 5mg capsules (product)
8796611000001103,Mercaptopurine 10mg capsules (product)
8822711000001100,Tacrolimus 5mg/5ml oral suspension (Special Order) (product)
8823011000001106,Tacrolimus 5mg/5ml oral suspension (product)
88611000001108,Sandimmun 250mg/5ml solution for injection ampoules (Novartis Pharmaceuticals UK Ltd) (product)
888811000001106,Azathioprine 50mg tablets (Unichem Plc) (product)
8993211000001102,Pemetrexed 500mg powder for solution for injection vials (product)
8993411000001103,Alimta 500mg powder for solution for injection vials (Eli Lilly & Co Ltd) (product)
900111000001107,Penicillamine 125mg tablets (A A H Pharmaceuticals Ltd) (product)
9040511000001106,Xagrid 500microgram capsules (Shire Pharmaceuticals Ltd) (product)
9042711000001102,Anagrelide 500microgram capsules (product)
906711000001106,Imuran 50mg powder for solution for injection vials (GlaxoSmithKline) (product)
9098211000001100,Taxol 150mg/25ml solution for injection vials (Bristol-Myers Squibb Pharmaceuticals Limited) (product)
9104711000001109,Carboplatin 150mg/15ml solution for injection vials (Pliva Pharma Ltd) (product)
9104911000001106,Carboplatin 450mg/45ml solution for injection vials (Pliva Pharma Ltd) (product)
9118411000001109,Fluorouracil 250mg/10ml solution for injection vials (Mayne Pharma Plc) (product)
911911000001101,Sandimmun 50mg/1ml solution for injection ampoules (Novartis Pharmaceuticals UK Ltd) (product)
9152611000001102,Avastin 400mg/16ml solution for injection vials (Roche Products Ltd) (product)
9152911000001108,Avastin 100mg/4ml solution for injection vials (Roche Products Ltd) (product)
9163211000001101,Paclitaxel 30mg/5ml solution for injection vials (Mayne Pharma Plc) (product)
9163411000001102,Paclitaxel 100mg/16.7ml solution for injection vials (Mayne Pharma Plc) (product)
9163611000001104,Paclitaxel 150mg/25ml solution for injection vials (Mayne Pharma Plc) (product)
9163811000001100,Paclitaxel 300mg/50ml solution for injection vials (Mayne Pharma Plc) (product)
9188011000001102,Alemtuzumab 30mg/1ml solution for injection vials (product)
9188211000001107,MabCampath Concentrate 30mg/1ml solution for injection vials (Schering Health Care Ltd) (product)
928011000001103,Methotrexate 10mg tablets (A A H Pharmaceuticals Ltd) (product)
9309311000001101,Enbrel 50mg powder and solvent for solution for injection vials (Wyeth Laboratories) (product)
939011000001105,Penicillamine 250mg tablets (Kent Pharmaceuticals Ltd) (product)
9448011000001109,Methotrexate 50mg/2ml solution for injection pre-filled syringes (Special Order) (product)
9448511000001101,Methotrexate 35mg/1.4ml solution for injection pre-filled syringes (Special Order) (product)
9449511000001107,Methotrexate 32.5mg/1.3ml solution for injection pre-filled syringes (Special Order) (product)
9450111000001105,Methotrexate 30mg/1.2ml solution for injection pre-filled syringes (Special Order) (product)
9451611000001107,Methotrexate 27.5mg/1.1ml solution for injection pre-filled syringes (Special Order) (product)
9452311000001106,Methotrexate 25mg/1ml solution for injection pre-filled syringes (Special Order) (product)
9452811000001102,Methotrexate 22.5mg/0.9ml solution for injection pre-filled syringes (Special Order) (product)
9453111000001103,Methotrexate 20mg/0.8ml solution for injection pre-filled syringes (Special Order) (product)
9453611000001106,Methotrexate 17.5mg/0.7ml solution for injection pre-filled syringes (Special Order) (product)
9454211000001107,Methotrexate 15mg/0.6ml solution for injection pre-filled syringes (Special Order) (product)
9455211000001108,Methotrexate 12.5mg/0.5ml solution for injection pre-filled syringes (Special Order) (product)
9455911000001104,Methotrexate 10mg/0.4ml solution for injection pre-filled syringes (Special Order) (product)
9456611000001100,Methotrexate 7.5mg/0.3ml solution for injection pre-filled syringes (Special Order) (product)
9457411000001101,Methotrexate 5mg/0.2ml solution for injection pre-filled syringes (Special Order) (product)
9467311000001101,Lysodren 500mg tablets (Laboratoire HRA Pharma) (product)
9468211000001108,Methotrexate 10mg/0.4ml solution for injection pre-filled syringes (product)
9468311000001100,Methotrexate 12.5mg/0.5ml solution for injection pre-filled syringes (product)
9468411000001107,Methotrexate 15mg/0.6ml solution for injection pre-filled syringes (product)
9468511000001106,Methotrexate 17.5mg/0.7ml solution for injection pre-filled syringes (product)
9468611000001105,Methotrexate 20mg/0.8ml solution for injection pre-filled syringes (product)
9468711000001101,Methotrexate 22.5mg/0.9ml solution for injection pre-filled syringes (product)
9468811000001109,Methotrexate 25mg/1ml solution for injection pre-filled syringes (product)
9468911000001104,Methotrexate 27.5mg/1.1ml solution for injection pre-filled syringes (product)
9469011000001108,Methotrexate 30mg/1.2ml solution for injection pre-filled syringes (product)
9469111000001109,Methotrexate 32.5mg/1.3ml solution for injection pre-filled syringes (product)
9469211000001103,Methotrexate 35mg/1.4ml solution for injection pre-filled syringes (product)
9469311000001106,Methotrexate 50mg/2ml solution for injection pre-filled syringes (product)
9469411000001104,Methotrexate 5mg/0.2ml solution for injection pre-filled syringes (product)
9469511000001100,Methotrexate 7.5mg/0.3ml solution for injection pre-filled syringes (product)
9509411000001105,Vinorelbine 10mg/1ml solution for injection vials (Mayne Pharma Plc) (product)
9510011000001107,Vinorelbine 50mg/5ml solution for injection vials (Mayne Pharma Plc) (product)
9522211000001109,Myocet 50mg powder and solvent for suspension for injection vials (Zeneus Pharma) (product)
9522511000001107,Navelbine 20mg capsules (Pierre Fabre Ltd) (product)
9522811000001105,Navelbine 30mg capsules (Pierre Fabre Ltd) (product)
9526811000001106,Doxorubicin (liposomal) 50mg powder and solvent for suspension for injection vials (product)
9526911000001101,Vinorelbine 20mg capsules (product)
9527011000001102,Vinorelbine 30mg capsules (product)
9561911000001100,Methotrexate 1g/10ml solution for injection vials (Wockhardt UK Ltd) (product)
9562111000001108,Methotrexate 5g/50ml solution for injection vials (Wockhardt UK Ltd) (product)
9562411000001103,Mitoxantrone 10mg/5ml solution for injection vials (Wockhardt UK Ltd) (product)
9562611000001100,Mitoxantrone 20mg/10ml solution for injection vials (Wockhardt UK Ltd) (product)
9564211000001106,Mitoxantrone 10mg/5ml solution for injection vials (product)
9564711000001104,Tarceva 100mg tablets (Roche Products Ltd) (product)
9565011000001102,Tarceva 150mg tablets (Roche Products Ltd) (product)
98511000001108,Distamine 125mg tablets (Alliance Pharmaceuticals Ltd) (product)"""


c16_df = pd.read_csv(io.StringIO(c16), header=0,delimiter=',').astype(str)
spark.createDataFrame(c16_df).createOrReplaceGlobalTempView("ccu002_06_d17_immrx_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_immrx_primis WHERE code='37919311000001103'

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_immrx_primis

# COMMAND ----------

# MAGIC %md ## spln_primis

# COMMAND ----------

c17 = """code,term
10759351000119103,Sickle cell anemia in mother complicating childbirth
111572002,"beta^0^ Thalassemia, nondeletion type"
123617004,Fleckmilz
1239371000000103,Haemoglobin E beta zero thalassaemia
1239381000000101,Haemoglobin E beta plus thalassaemia
127040003,Sickle cell-hemoglobin SS disease
127041004,Sickle cell-beta-thalassemia
127042006,Sickle cell beta plus thalassemia
127043001,Sickle cell-beta^0^-thalassemia
127044007,Sickle cell-delta beta^0^-thalassemia
127045008,Sickle cell anemia with coexistent alpha-thalassemia
127047000,Sickle cell-hemoglobin Lepore disease
127048005,Sickle cell-Hemoglobin O Arab disease
161626009,History of splenectomy
1671000,Sago spleen
174776001,Total splenectomy
174778000,Total splenectomy and reimplantation of fragments
174789007,Embolization of spleen
17604001,Bilateral right-sidedness sequence
195340002,Embolism and thrombosis of the splenic artery
197478000,Congenital celiac disease
197479008,Acquired celiac disease
205735005,Hypoplasia of spleen
210193004,Spleen massive parenchymal disruption with open wound into cavity
22996003,Splenic infarction
23269001,Double heterozygous sickling disorder
234319005,Splenectomy
234391009,Sickle cell anemia with high hemoglobin F
234392002,Hemoglobin E/beta thalassemia disease
234510005,Amyloidosis of spleen
236854007,Septic splenitis
23761004,Hyposplenism
25472008,Sickle cell-hemoglobin D disease
262821002,Avulsion of spleen
26682008,Homozygous beta thalassemia
27080008,"beta^0^ Thalassemia, deletion type"
275403002,Villous atrophy
275404008,Celiac rickets
275405009,Partial villous atrophy
300564004,Spleen absent
302961007,Hereditary splenic hypoplasia
314118002,Laparoscopic total splenectomy
33479006,Distal subtotal pancreatectomy with splenectomy and pancreaticojejunostomy
35434009,Sickle cell-hemoglobin C disease
36472007,Sickle cell-thalassemia disease
38096003,Functional asplenia
38970002,Doan-Wright syndrome
396330006,Celiac crisis
396331005,Celiac disease
416180004,Hemoglobin SS disease without crisis
416214006,Sickle cell-hemoglobin D disease without crisis
416290001,Hemoglobin S sickling disorder without crisis
416484003,Sickle cell-hemoglobin E disease with crisis
416638004,Sickle cell-hemoglobin E disease without crisis
416826005,Sickle cell-thalassemia disease with crisis
417048006,Sickle cell-thalassemia disease without crisis
417279003,Hemoglobin S sickling disorder with crisis
417357006,Sickling disorder due to hemoglobin S
417425009,Hemoglobin SS disease with crisis
417517009,Sickle cell-hemoglobin C disease with crisis
417683006,Sickle cell-hemoglobin C disease without crisis
417748003,Sickle cell-hemoglobin D disease with crisis
440206000,Hemoglobin SS disease with vasoocclusive crisis
444108000,Acute sickle cell splenic sequestration crisis
45259000,Celiac infantilism
47024008,Sickle cell-hemoglobin E disease
54006005,Hereditary persistence of fetal hemoglobin delta beta plus thalassemia
56338005,Splenic fibrosis
58381000,Hypersplenism
60194009,Distal subtotal pancreatectomy with splenectomy
61535006,Transplantation of spleen
61715008,Celiac disease with diffuse intestinal ulceration
700050004,Overwhelming infection in asplenic patient
700051000,Sepsis in asplenic subject
700052007,Post-splenectomy sepsis
702624008,Aplasia of spleen
707147002,Asplenia
711407000,"Thrombocytopathy, asplenia and miosis"
717156002,Biliary atresia with splenic malformation syndrome
722386009,Celiac disease with epilepsy and cerebral calcification syndrome
724639003,Asplenia following surgical procedure
726708009,Familial isolated congenital asplenia
73190000,epsilon gamma delta beta^0^ Thalassemia
75451007,Thalassemia major
76336008,Delta beta zero thalassemia
770593004,Refractory celiac disease
783254003,Hereditary persistence of fetal hemoglobin with sickle cell disease syndrome
82893001,Splenic atrophy
861371000000102,Acquired absence of spleen
86715000,Beta zero thalassemia
89810003,^A^gamma delta beta^0^ thalassemia
91867008,Adult form of celiac disease
93030006,Congenital absence of spleen
93292008,Congenital hypoplasia of spleen
95846001,Red blood cell sequestration in spleen"""


c17_df = pd.read_csv(io.StringIO(c17), header=0,delimiter=',').astype(str)
spark.createDataFrame(c17_df).createOrReplaceGlobalTempView("ccu002_06_d17_spln_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_spln_primis

# COMMAND ----------

# MAGIC %md ## learndis_primis

# COMMAND ----------

c18 = """code,term
10007009,Coffin-Siris syndrome
1089701000000105,Profound intellectual development disorder without impairment of behaviour
1089711000000107,Profound intellectual development disorder with significant impairment of behaviour
1089721000000101,Profound intellectual development disorder with minimal impairment of behaviour
1089731000000104,Profound intellectual development disorder with impairment of behaviour
1089741000000108,Severe intellectual development disorder without significant impairment of behaviour
1089751000000106,Severe intellectual development disorder with significant impairment of behaviour
1089761000000109,Severe intellectual development disorder with minimal impairment of behaviour
1089771000000102,Severe intellectual development disorder with impairment of behaviour
1089781000000100,Moderate intellectual development disorder without significant impairment of behaviour
1089791000000103,Moderate intellectual development disorder with significant impairment of behaviour
1089811000000102,Moderate intellectual development disorder with minimal impairment of behaviour
1089821000000108,Moderate intellectual development disorder with impairment of behaviour
1089831000000105,Mild intellectual development disorder without significant impairment of behaviour
1089841000000101,Mild intellectual development disorder with significant impairment of behaviour
1089851000000103,Mild intellectual development disorder with minimal impairment of behaviour
1093991000000101,Mild intellectual development disorder with impairment of behaviour
1094001000000106,Intellectual development disorder without significant impairment of behaviour
1094011000000108,Intellectual development disorder with significant impairment of behaviour
1094021000000102,Intellectual development disorder with minimal impairment of behaviour
1094031000000100,Intellectual development disorder with impairment of behaviour
109478007,Kohlschutter's syndrome
110359009,Intellectual disability
1239331000000100,Significant intellectual disability
17827007,Cross syndrome
205615000,Trisomy 21- meiotic nondisjunction
205619006,"Trisomy 13, meiotic nondisjunction"
205620000,Trisomy 13 - mitotic nondisjunction mosaicism
205623003,Trisomy 18 - meiotic nondisjunction
205624009,Trisomy 18 - mitotic nondisjunction mosaicism
21111006,Complete trisomy 13 syndrome
21634003,Borjeson-Forssman-Lehmann syndrome
232059000,Laurence-Moon syndrome
234146006,Hennekam lymphangiectasia-lymphedema syndrome
236529001,"Prune belly syndrome with pulmonic stenosis, mental retardation and deafness"
253176002,Gillespie syndrome
254264002,Partial trisomy 21 in Down's syndrome
254266000,Partial trisomy 18 in Edward's syndrome
254268004,Partial trisomy 13 in Patau's syndrome
31216003,Profound intellectual disability
33982008,Hyperphosphatasemia with intellectual disability
40700009,Severe intellectual disability
41040004,Complete trisomy 21 syndrome
412787009,"Intellectual disability, congenital heart disease, blepharophimosis, blepharoptosis and hypoplastic teeth"
416075005,On learning disability register
422437002,X-linked intellectual disability with marfanoid habitus
432091002,Savant syndrome
508171000000105,Severe learning disability
51500006,Complete trisomy 18 syndrome
5619004,Bardet-Biedl syndrome
57917004,Seckel syndrome
59252009,Cutis laxa-corneal clouding-oligophrenia syndrome
61152003,Moderate intellectual disability
613003,Fragile X syndrome
68618008,Rett's disorder
699297004,Blepharophimosis-intellectual disability syndrome Maat-Kievit-Brunner type
699298009,"Blepharophimosis-mental retardation syndrome, Say-Barber-Biesecker-Young-Simpson type"
699316006,Myhre syndrome
699669001,Renpenning syndrome
702344008,Pitt-Hopkins syndrome
702356009,X-linked intellectual disability-psychosis-macroorchidism syndrome
702412005,X-linked intellectual deficit-dystonia-dysarthria syndrome
702416008,X-linked intellectual disability Snyder type
702441001,Fatal X-linked ataxia with deafness and loss of vision
702816000,Methyl-cytosine phosphate guanine binding protein-2 duplication syndrome
703389002,Calcium/calmodulin-dependent serine protein kinase related intellectual disability
703526007,Progressive epilepsy-intellectual disability syndrome Finnish type
703535000,Mowat-Wilson syndrome
709469005,Periodontitis co-occurrent with Down syndrome
715409005,Trigonocephaly C syndrome
715428003,Skeletal dysplasia with epilepsy and short stature syndrome
715441004,McDonough syndrome
715628009,"Intellectual disability, truncal obesity, retinal dystrophy and micropenis syndrome"
715989002,Congenital cataract with intellectual disability and anal atresia and urinary defect syndrome
716024001,Goniodysgenesis with intellectual disability and short stature syndrome
716089008,Craniofacial digital and genital anomalies syndrome
716096005,Hypospadias and intellectual disability syndrome Goldblatt type
716107009,Early onset parkinsonism and intellectual disability syndrome
716112005,Microcephaly with deafness and intellectual disability syndrome
716191002,Alopecia and intellectual disability syndrome
716334004,Intellectual disability and short stature with hand contracture and genital anomaly syndrome
716706009,Female restricted epilepsy with intellectual disability syndrome
716709002,FRAXE intellectual disability syndrome
716996008,Hypoplasia of corpus callosum and mental retardation with adducted thumbs and spasticity and hydrocephalus syndrome
717157006,Trisomy 10p
717222003,Microphthalmia with ankyloblepharon and intellectual disability syndrome
717223008,X-linked epilepsy with learning disability and behavior disorder syndrome
717763008,Chudley Lowry Hoar syndrome
717822006,Goldberg Shprintzen megacolon syndrome
717887003,Biemond syndrome type 2
717913006,Blepharonasofacial malformation syndrome
717945001,"Brain anomaly, severe mental retardation, ectodermal dysplasia, skeletal deformity, ear anomaly, kidney dysplasia syndrome"
718226002,Wolf Hirschhorn syndrome
718573009,Achalasia microcephaly syndrome
718577005,X-linked intellectual disability Atkin type
718680001,Oro-facial digital syndrome type 9
718681002,Oro-facial digital syndrome type 11
718766002,"Spondyloepiphyseal dysplasia, craniosynostosis, cleft palate, cataract and intellectual disability syndrome"
718845002,X-linked intellectual disability with ataxia and apraxia syndrome
718848000,Fried syndrome
718896000,X-linked recessive intellectual disability and macrocephaly with ciliary dysfunction syndrome
718897009,X-linked intellectual disability Seemanova type
718900002,Syndromic X-linked intellectual disability type 11
718905007,X-linked intellectual disability Shrimpton type
718908009,X-linked intellectual disability Siderius type
718909001,X-linked intellectual disability Stevenson type
718910006,X-linked intellectual disability Stocco Dos Santos type
718911005,X-linked intellectual disability Stoll type
718912003,X-linked intellectual disability Turner type
718914002,X-linked intellectual disability Van Esch type
719009006,X-linked intellectual disability Wilson type
719010001,X-linked intellectual disability Schimke type
719011002,X-linked intellectual disability Pai type
719012009,X-linked intellectual disability Miles Carpenter type
719013004,X-linked intellectual disability Cilliers type
719016007,X-linked intellectual disability Cantagrel type
719017003,X-linked intellectual disability Armfield type
719018008,X-linked intellectual disability Abidi type
719020006,Pallister W syndrome
719042007,Uveal coloboma with cleft lip and palate and intellectual disability syndrome
719046005,12q14 microdeletion syndrome
719069008,Shprintzen Goldberg craniosynostosis syndrome
719097002,Branchioskeletogenital syndrome
719101006,Carpenter Waziri syndrome
719102004,Congenital cataract with ataxia and deafness syndrome
719136005,X-linked intellectual disability with cerebellar hypoplasia syndrome
719138006,X-linked intellectual disability with cubitus valgus and dysmorphism syndrome
719139003,"X-linked Dandy-Walker malformation with intellectual disability, basal ganglia disease and seizure syndrome"
719140001,X-linked intellectual disability with dysmorphism and cerebral atrophy syndrome
719155005,X-linked intellectual disability and epilepsy with progressive joint contracture and facial dysmorphism syndrome
719156006,X-linked intellectual disability with hypogammaglobulinemia and progressive neurological deterioration syndrome
719157002,X-linked intellectual disability and hypotonia with facial dysmorphism and aggressive behavior syndrome
719160009,Syndromic X-linked intellectual disability type 7
719161008,Syndromic X-linked intellectual disability due to jumonji at-rich interactive domain 1c mutation
719162001,Radioulnar synostosis with microcephaly and scoliosis syndrome
719202006,Spondyloepiphyseal dysplasia tarda Kohn type
719212004,Smith Fineman Myers syndrome
719378009,Microcephalus with brachydactyly and kyphoscoliosis syndrome
719380003,Microcephalus cardiomyopathy syndrome
719450007,Disorder of sex development with intellectual disability syndrome
719466009,Cleft palate with short stature and vertebral anomaly syndrome
719583002,17q11.2 microduplication syndrome
719599008,19q13.11 microdeletion syndrome
719600006,1p21.3 microdeletion syndrome
719800009,"Deafness, onychodystrophy, osteodystrophy, intellectual disability syndrome"
719808002,Chromosome Xp11.3 microdeletion syndrome
719810000,X-linked intellectual disability with seizure and psoriasis syndrome
719811001,X-linked intellectual disability Cabezas type
719812008,X-linked intellectual disability with plagiocephaly syndrome
719825000,"X-linked intellectual disability, macrocephaly, macroorchidism syndrome"
719826004,X-linked intellectual disability with acromegaly and hyperactivity syndrome
719834005,Wilson Turner syndrome
719842006,Congenital hypoplasia of ulna and intellectual disability syndrome
719909009,Chromosome Xq28 trisomy syndrome
719947004,Craniofacial dysmorphism with coloboma of eye and corpus callosum agenesis syndrome
720401009,Cystic fibrosis with gastritis and megaloblastic anemia syndrome
720468000,Aniridia and intellectual disability syndrome
720501007,Arachnodactyly with abnormal ossification and intellectual disability syndrome
720502000,Arachnodactyly and intellectual disability with facial dysmorphism syndrome
720517001,Ataxia with deafness and intellectual disability syndrome
720573009,Brachymorphism with onychodysplasia and dysphalangism syndrome
720635002,Cerebro-facio-thoracic dysplasia
720639008,"Coloboma, congenital heart disease, ichthyosiform dermatosis, intellectual disability ear anomaly syndrome"
720746006,Contracture with ectodermal dysplasia and orofacial cleft syndrome
720748007,Aural atresia with multiple congenital anomalies and intellectual disability syndrome
720825005,Cystic leukoencephalopathy without megalencephaly
720855003,Cerebrooculonasal syndrome
720954000,Filippi syndrome
720955004,Fine Lubinsky syndrome
720957007,Deafness with skeletal dysplasia and lip granuloma syndrome
720979002,"Alopecia, contracture, dwarfism, intellectual disability syndrome"
720981000,Alopecia and intellectual disability with hypergonadotropic hypogonadism syndrome
720982007,"Alport syndrome, intellectual disability, midface hypoplasia, elliptocytosis syndrome"
721007005,Hair defect with photosensitivity and intellectual disability syndrome
721008000,Hall Riggs syndrome
721017000,Postaxial polydactyly and intellectual disability syndrome
721073008,Short stature with webbed neck and congenital heart disease syndrome
721086004,"Deafness, genital anomaly, metacarpal and metatarsal synostosis syndrome"
721087008,Deafness and intellectual disability Martin Probst type syndrome
721089006,"Dentinogenesis imperfecta, short stature, hearing loss, intellectual disability syndrome"
721146009,"Intellectual disability, epilepsy, bulbous nose syndrome"
721207002,"Seizure, sensorineural deafness, ataxia, intellectual disability, electrolyte imbalance syndrome"
721208007,Ectodermal dysplasia with blindness syndrome
721224008,Holmes Gang syndrome
721841001,Hypogonadism with mitral valve prolapse and intellectual disability syndrome
721843003,"Growth retardation, alopecia, pseudoanodontia, optic atrophy syndrome"
721875000,Juberg Marsidi syndrome
721883006,Radioulnar synostosis with developmental delay and hypotonia syndrome
721973006,"Lipodystrophy, intellectual disability, deafness syndrome"
721974000,Lowry MacLean syndrome
722002002,"Intellectual disability, balding, patella luxation, acromicria syndrome"
722003007,Intellectual disability with cataract and kyphosis syndrome
722031003,Kapur Toriello syndrome
722033000,"Macrocephaly, short stature, paraplegia syndrome"
722035007,"Intellectual disability, enteropathy, deafness, peripheral neuropathy, ichthyosis, keratoderma syndrome"
722037004,"Intellectual disability, epileptic seizures, hypogonadism and hypogenitalism, microcephaly, obesity syndrome"
722055008,Oculopalatocerebral syndrome
722056009,Oculocerebrofacial syndrome Kaufman type
722065002,Okamoto syndrome
722075004,Oro-facial digital syndrome type 10
722105002,Oro-facial digital syndrome type 5
722106001,Oro-facial digital syndrome type 8
722107005,Ossification anomaly with psychomotor developmental delay syndrome
722110003,"Osteogenesis imperfecta, retinopathy, seizures, intellectual disability syndrome"
722111004,"Osteopenia, myopia, hearing loss, intellectual disability, facial dysmorphism syndrome"
722209002,"Spastic paraplegia, intellectual disability, palmoplantar hyperkeratosis syndrome"
722213009,Severe X-linked intellectual disability Gustavson type
722281001,"Agammaglobulinemia, microcephaly, craniosynostosis, severe dermatitis syndrome"
722282008,"Agenesis of corpus callosum, intellectual disability, coloboma, micrognathia syndrome"
722378009,Congenital cataract with deafness and hypogonadism syndrome
722379001,Congenital cataract with hypertrichosis and intellectual disability syndrome
722380003,Congenital cataract with intellectual disability and hypogonadotropic hypogonadism syndrome
722454003,"Intellectual disability, craniofacial dysmorphism, hypogonadism, diabetes mellitus syndrome"
722455002,"Intellectual disability, hypoplastic corpus callosum, preauricular tag syndrome"
722456001,"Intellectual disability, developmental delay, contracture syndrome"
722459008,"Male hypergonadotropic hypogonadism, intellectual disability, skeletal anomaly syndrome"
722477003,Toriello Carey syndrome
722478008,Skeletal dysplasia with intellectual disability syndrome
723304001,"Microcephaly, seizure, intellectual disability, heart disease syndrome"
723332005,Isodicentric chromosome 15 syndrome
723333000,Faciocardiorenal syndrome
723336008,Fallot complex with intellectual disability and growth delay syndrome
723365002,Hypotrichosis and intellectual disability syndrome Lopes type
723403008,"Microbrachycephaly, ptosis, cleft lip syndrome"
723441001,Non-progressive cerebellar ataxia with intellectual disability
723454008,Phosphoribosylpyrophosphate synthetase superactivity
723501008,Renier Gabreels Jasper syndrome
723504000,Ramos Arroyo syndrome
723621000,"Spastic tetraplegia, retinitis pigmentosa, intellectual disability syndrome"
723676007,"Severe intellectual disability, epilepsy, anal anomaly, distal phalangeal hypoplasia syndrome"
723994004,Seizures and intellectual disability due to hydroxylysinuria syndrome
724001005,"Retinitis pigmentosa, intellectual disability, deafness, hypogenitalism syndrome"
724039002,Psychomotor retardation due to S-adenosylhomocysteine hydrolase deficiency
724137002,"Macrocephaly, obesity, mental disability, ocular abnormality syndrome"
724178000,Laryngeal abductor paralysis with intellectual disability syndrome
724207001,Kleefstra syndrome
724228005,Infantile choroidocerebral calcification syndrome
724643004,Transient abnormal myelopoiesis co-occurrent with Down syndrome
724644005,Myeloid leukemia co-occurrent with Down syndrome
725140007,Temple Baraitser syndrome
725163002,"X-linked spasticity, intellectual disability, epilepsy syndrome"
725289009,5-amino-4-imidazole carboxamide ribosiduria
725589005,Bullous dystrophy macular type
725906006,Intellectual disability Buenos Aires type
725908007,Neurofaciodigitorenal syndrome
725912001,X-linked intellectual disability Brooks type
726031001,"Cerebellar ataxia, intellectual disability, optic atrophy, skin abnormalities syndrome"
726621009,Caudal appendage deafness syndrome
726669007,"Central nervous system calcification, deafness, tubular acidosis, anemia syndrome"
726670008,Weaver Williams syndrome
726672000,"Short stature, unique facies, enamel hypoplasia, progressive joint stiffness, high-pitched voice syndrome"
726709001,"Intellectual disability, cataract, calcified pinna, myopathy syndrome"
726727003,X-linked intellectual disability Hedera type
726732002,X-linked intellectual disability Nascimento type
732246009,"X-linked intellectual disability, limb spasticity, retinal dystrophy, diabetes insipidus syndrome"
732251003,"Cortical blindness, intellectual disability, polydactyly syndrome"
732954002,"Osteopenia, intellectual disability, sparse hair syndrome"
732957009,Brachydactyly and preaxial hallux varus syndrome
732958004,Spastic paraplegia with precocious puberty syndrome
732961003,"Branchial dysplasia, intellectual disability, inguinal hernia syndrome"
733031004,"Epilepsy, microcephaly, skeletal dysplasia syndrome"
733032006,Epilepsy telangiectasia syndrome
733049004,"Encephalopathy, intracerebral calcification, retinal degeneration syndrome"
733050004,"Dysmorphism, short stature, deafness, disorder of sex development syndrome"
733062000,Marfanoid habitus with autosomal recessive intellectual disability syndrome
733072002,"Alaninuria, microcephaly, dwarfism, enamel hypoplasia, diabetes mellitus syndrome"
733086003,Pseudoprogeria syndrome
733088002,"Preaxial polydactyly, colobomata, intellectual disability syndrome"
733097003,"Ichthyosis, intellectual disability, dwarfism, renal impairment syndrome"
733110004,Van den Bosch syndrome
733116005,"Aniridia, renal agenesis, psychomotor retardation syndrome"
733117001,"Thumb stiffness, brachydactyly, intellectual disability syndrome"
733194007,Dementia co-occurrent and due to Down syndrome
733417008,"Facial dysmorphism, macrocephaly, myopia, Dandy-Walker malformation syndrome"
733419006,"Metaphyseal dysostosis, intellectual disability, conductive deafness syndrome"
733455003,"Spastic paraplegia, glaucoma, intellectual disability syndrome"
733472005,"Microcephalus, glomerulonephritis, marfanoid habitus syndrome"
733522005,Megalocornea with intellectual disability syndrome
734017008,"Ectodermal dysplasia, intellectual disability, central nervous system malformation syndrome"
734173003,"Skeletal abnormality, cutis laxa, craniostenosis, ambiguous genitalia, retardation, facial abnormality syndrome"
734349003,Alpha-thalassemia intellectual disability syndrome linked to chromosome 16
763136000,"Charcot-Marie-Tooth disease, deafness, intellectual disability syndrome"
763186006,"Grubben, De Cock, Borghgraef syndrome"
763278004,"Facial dysmorphism, cleft palate, loose skin syndrome"
763320005,Craniofaciofrontodigital syndrome
763344007,"Cerebellar ataxia, intellectual disability, oculomotor apraxia, cerebellar cysts syndrome"
763350002,"Intellectual disability, obesity, brain malformation, facial dysmorphism syndrome"
763353000,Cerebrofacioarticular syndrome
763404001,"Ichthyosis, alopecia, eclabion, ectropion, intellectual disability syndrome"
763615003,"Aortic arch anomaly, facial dysmorphism, intellectual disability syndrome"
763618001,Wiedemann Steiner syndrome
763626009,Intellectual disability due to nutritional deficiency
763665007,Craniodigital syndrome and intellectual disability syndrome
763722004,"Hypotonia, speech impairment, severe cognitive delay syndrome"
763741001,"Intellectual disability, alacrima, achalasia syndrome"
763742008,"Intellectual disability, polydactyly, uncombable hair syndrome"
763743003,"Intellectual disability, spasticity, ectrodactyly syndrome"
763744009,"Intellectual disability, brachydactyly, Pierre Robin syndrome"
763745005,Intellectual disability Wolff type
763773007,Macrocephaly and developmental delay syndrome
763795006,Malan overgrowth syndrome
763797003,Agenesis of corpus callosum and abnormal genitalia syndrome
763837007,Oro-facial digital syndrome type 14
763861000,"Pachygyria, intellectual disability, epilepsy syndrome"
764455002,"Cognitive impairment, coarse facies, heart defects, obesity, pulmonary involvement, short stature, skeletal dysplasia syndrome"
764732004,"Microcephalus, cerebellar hypoplasia, cardiac conduction defect syndrome"
764861005,Intellectual disability Birk-Barel type
764950001,"Cryptorchidism, arachnodactyly, intellectual disability syndrome"
764959000,"Intellectual disability, myopathy, short stature, endocrine defect syndrome"
765089003,"Focal epilepsy, intellectual disability, cerebro-cerebellar malformation syndrome"
765170001,Sodium voltage-gated channel alpha subunit 8-related epilepsy with encephalopathy
765434008,Human immunodeficiency virus type I enhancer binding protein 2 related intellectual disability
765471005,"X-linked intellectual disability, hypogonadism, ichthyosis, obesity, short stature syndrome"
765758008,Microcephalic primordial dwarfism Montreal type
765761009,"Brachydactyly, mesomelia, intellectual disability, heart defect syndrome"
766753005,Nijmegen breakage syndrome-like disorder
766824003,"Activity dependent neuroprotector homeobox related multiple congenital anomalies, intellectual disability, autism spectrum disorder"
766870005,"Epiphyseal dysplasia, hearing loss, dysmorphism syndrome"
766871009,Diencephalic mesencephalic junction dysplasia
768473009,Purine rich element binding protein A syndrome
768677000,Protein phosphatase 2 regulatory subunit b (b56) delta-related intellectual disability
76880004,Angelman syndrome
768843007,"Tall stature, intellectual disability, facial dysmorphism syndrome"
770404004,Autosomal recessive chorioretinopathy and microcephaly syndrome
770431001,"Early-onset epileptic encephalopathy and intellectual disability due to glutamate receptor, ionotropic, N-methyl-D-aspartate, subunit 2A mutation"
770564004,Microcephalic primordial dwarfism Alazami type
770565003,Microcephalic primordial dwarfism Dauber type
770604006,"X-linked cerebral, cerebellar, coloboma syndrome"
770679002,"Polyneuropathy, intellectual disability, acromicria, premature menopause syndrome"
770719004,3q27.3 microdeletion syndrome
770721009,"Microcephaly, thin corpus callosum, intellectual disability syndrome"
770723007,"Optic atrophy, intellectual disability syndrome"
770725000,Infantile cerebral and cerebellar atrophy with postnatal progressive microcephaly
770750002,"Intellectual disability, seizures, macrocephaly, obesity syndrome"
770751003,"Severe motor and intellectual disabilities, sensorineural deafness, dystonia syndrome"
770755007,"Intellectual disability, seizures, hypotonia, ophthalmologic, skeletal anomalies syndrome"
770756008,2p13.2 microdeletion syndrome
770790004,Developmental delay with autism spectrum disorder and gait instability
770793002,5p13 microduplication syndrome
770794008,11p15.4 microduplication syndrome
770898002,"Autosomal recessive cerebellar ataxia, epilepsy, intellectual disability syndrome due to WW domain containing oxidoreductase deficiency"
770901001,"Autosomal recessive intellectual disability, motor dysfunction, multiple joint contracture syndrome"
770907002,Kagami Ogata syndrome
770941005,"Alopecia, progressive neurological defect, endocrinopathy syndrome"
771074000,"Microcephaly, short stature, intellectual disability, facial dysmorphism syndrome"
771077007,"Intellectual disability, short stature, hypertelorism syndrome"
771148008,"X-linked colobomatous microphthalmia, microcephaly, intellectual disability, short stature syndrome"
771149000,"Hepatic fibrosis, renal cyst, intellectual disability syndrome"
771179007,"Extrasystoles, short stature, hyperpigmentation, microcephaly syndrome"
771262009,Pseudoleprechaunism syndrome Patterson type
771336003,Polymicrogyria with optic nerve hypoplasia
771448004,Autism epilepsy syndrome due to branched chain ketoacid dehydrogenase kinase deficiency
771470001,Jawad syndrome
771472009,Developmental and speech delay due to SRY-box 5 deficiency
771476007,"Autosomal recessive leukoencephalopathy, ischemic stroke, retinitis pigmentosa syndrome"
771477003,15q overgrowth syndrome
771512003,Autism spectrum disorder due to AUTS2 activator of transcription and developmental regulator deficiency
772127009,White Sutton syndrome
772224009,Warburg micro syndrome
772225005,"RAB18, member RAS oncogene family deficiency"
77287004,Borderline intellectual disability
773230003,Cyclin-dependent kinase-like 5 deficiency
773274001,"X-linked intellectual disability, craniofacioskeletal syndrome"
773303005,Spondyloepimetaphyseal dysplasia Genevieve type
773307006,Zechi Ceide syndrome
773329005,CK syndrome
773400009,"Severe feeding difficulties, failure to thrive, microcephaly due to ASXL transcriptional regulator 3 deficiency syndrome"
773404000,Roifman syndrome
773405004,Intellectual disability with strabismus syndrome
773416006,"Intellectual disability, facial dysmorphism, hand anomalies syndrome"
773418007,Xylosyltransferase 1 congenital disorder of glycosylation
773419004,"Severe intellectual disability, short stature, behavioral abnormalities, facial dysmorphism syndrome"
773493002,9q31.1q31.3 microdeletion syndrome
773494008,14q24.1q24.3 microdeletion syndrome
773498006,"Autosomal recessive cerebellar ataxia, epilepsy, intellectual disability syndrome due to TUD deficiency"
773547003,13q12.3 microdeletion syndrome
773548008,"Early-onset epileptic encephalopathy, cortical blindness, intellectual disability, facial dysmorphism syndrome"
773551001,"Severe intellectual disability, poor language, strabismus, grimacing face, long fingers syndrome"
773552008,"Intellectual disability, feeding difficulties, developmental delay, microcephaly syndrome"
773553003,"Hypohidrosis, enamel hypoplasia, palmoplantar keratoderma, intellectual disability syndrome"
773554009,"THO complex 6-related developmental delay, microcephaly, facial dysmorphism syndrome"
773556006,"Short ulna, dysmorphism, hypotonia, intellectual disability syndrome"
773578004,"Spondylocostal dysostosis, hypospadias, intellectual disability syndrome"
773581009,"Intellectual disability, craniofacial dysmorphism, cryptorchidism syndrome"
773583007,"Aphonia, deafness, retinal dystrophy, bifid halluces, intellectual disability syndrome"
773587008,"X-linked intellectual disability, cardiomegaly, congestive heart failure syndrome"
773621003,"Intellectual disability, hypotonia, brachycephaly, pyloric stenosis, cryptorchidism syndrome"
773670004,Distal Xq28 microduplication syndrome
773692000,"Late-onset localized junctional epidermolysis bullosa, intellectual disability syndrome"
773699009,Pitt Hopkins-like syndrome
773735007,Deafness with onychodystrophy syndrome
773769008,"Ataxia, photosensitivity, short stature syndrome"
773772001,Rare non-syndromic intellectual disability
773984007,Piebald trait with neurologic defects syndrome
774068004,"AT-hook DNA binding motif containing 1-related intellectual disability, obstructive sleep apnea, mild dysmorphism syndrome"
774070008,"Fibulin 1-related developmental delay, central nervous system anomaly, syndactyly syndrome"
774102003,"Intellectual disability, obesity, prognathism, eye and skin anomalies syndrome"
774149004,"Severe intellectual disability, progressive postnatal microcephaly, midline stereotypic hand movements syndrome"
774203000,"Intellectual disability, severe speech delay, mild dysmorphism syndrome"
776204008,"Colobomatous microphthalmia, obesity, hypogenitalism, intellectual disability syndrome"
777998000,Temtamy preaxial brachydactyly syndrome
778009001,"Blepharophimosis, intellectual disability syndrome, Verloes type"
778011005,Severe intellectual disability and progressive spastic paraplegia
778025006,Atypical hypotonia cystinuria syndrome
780827006,Synaptic Ras GTPase activating protein 1- related intellectual disability
782676009,Distal trisomy 18q
782723007,"Severe intellectual disability, progressive spastic diplegia syndrome"
782736007,"Intellectual disability, facial dysmorphism syndrome due to SET domain containing 5 haploinsufficiency"
782753000,"Intellectual disability, coarse face, macrocephaly, cerebellar hypotrophy syndrome"
782755007,"Primary microcephaly, mild intellectual disability, young-onset diabetes syndrome"
782757004,"Congenital microcephaly, severe encephalopathy, progressive cerebral atrophy syndrome"
782772000,Congenital muscular dystrophy with intellectual disability and severe epilepsy
782886007,"Infantile spasms, psychomotor retardation, progressive brain atrophy, basal ganglia disease syndrome"
782911008,Hereditary cryohydrocytosis with reduced stomatin
782941005,Richieri Costa-da Silva syndrome
782945001,"Ophthalmoplegia, intellectual disability, lingua scrotalis syndrome"
783005002,"Severe microbrachycephaly, intellectual disability, athetoid cerebral palsy syndrome"
783061008,"Facial dysmorphism, developmental delay, behavioral abnormalities syndrome due to 10p11.21p12.31 microdeletion"
783089006,"Macrocephaly, intellectual disability, autism syndrome"
783174004,Congenital muscular dystrophy with intellectual disability
783619003,Dual specificity tyrosine phosphorylation regulated kinase 1A-related intellectual disability syndrome due to 21q22.13q22.2 microdeletion
783702009,X-linked intellectual disability due to glutamate ionotropic receptor AMPA type subunit 3 mutations
783703004,"White matter hypoplasia, corpus callosum agenesis, intellectual disability syndrome"
785298001,Muscle eye brain disease with bilateral multicystic leukodystrophy
785726009,Hyperekplexia epilepsy syndrome
787093004,"Developmental delay, facial dysmorphism syndrome due to mediator complex subunit 13 like deficiency"
787171006,21q22.11q22.12 microdeletion syndrome
787174003,"Intellectual disability, hyperkinetic movement, truncal ataxia syndrome"
787175002,"Ankyrin 3 related intellectual disability, sleep disturbance syndrome"
788417006,"Alopecia, epilepsy, intellectual disability syndrome Moynahan type"
788584007,Blepharophimosis and mental retardation syndrome
79385002,Lowe syndrome
816067005,"Diabetes, hypogonadism, deafness, intellectual disability syndrome"
838441009,"Mental retardation, adducted thumbs, shuffling gait, aphasia syndrome"
840505007,Down syndrome co-occurrent with leukemoid reaction associated transient neonatal pustulosis
86765009,Mild intellectual disability
889211000000104,Specific learning disability
931001000000105,Significant learning disability
984661000000105,Mild learning disability
984671000000103,Moderate learning disability
984681000000101,Profound learning disability"""


c18_df = pd.read_csv(io.StringIO(c18), header=0,delimiter=',').astype(str)
spark.createDataFrame(c18_df).createOrReplaceGlobalTempView("ccu002_06_d17_learndis_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_learndis_primis

# COMMAND ----------

# MAGIC %md ## bmi_stage_primis

# COMMAND ----------

c19 = """code,term
162863004,Body mass index 25-29 - overweight
162864005,Body mass index 30+ - obesity
310252000,Body mass index less than 20
35425004,Normal body mass index
408512008,Body mass index 40+ - severely obese
412768003,Body mass index 20-24 - normal
427090001,Body mass index less than 16.5
443371000124107,Obese class I
443381000124105,Obese class II
6497000,Decreased body mass index
722595002,Overweight in adulthood with body mass index of 25 or more but less than 30
819948005,Obese class III
914721000000105,Obese class I (body mass index 30.0 - 34.9)
914731000000107,Obese class II (body mass index 35.0 - 39.9)
914741000000103,Obese class III (body mass index equal to or greater than 40.0)"""


c19_df = pd.read_csv(io.StringIO(c19), header=0,delimiter=',').astype(str)
spark.createDataFrame(c19_df).createOrReplaceGlobalTempView("ccu002_06_d17_bmi_stage_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_bmi_stage_primis

# COMMAND ----------

# MAGIC %md ## sev_obesity_primis

# COMMAND ----------

c20 = """code,term
408512008,Body mass index 40+ - severely obese
819948005,Obese class III
914741000000103,Obese class III (body mass index equal to or greater than 40.0)"""


c20_df = pd.read_csv(io.StringIO(c20), header=0,delimiter=',').astype(str)
spark.createDataFrame(c20_df).createOrReplaceGlobalTempView("ccu002_06_d17_sev_obesity_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_sev_obesity_primis

# COMMAND ----------

# MAGIC %md ## bmi_primis

# COMMAND ----------

c21 = """code,term
60621009,Body mass index
846931000000101,Baseline body mass index"""


c21_df = pd.read_csv(io.StringIO(c21), header=0,delimiter=',').astype(str)
spark.createDataFrame(c21_df).createOrReplaceGlobalTempView("ccu002_06_d17_bmi_primis")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM global_temp.ccu002_06_d17_bmi_primis

# COMMAND ----------

# MAGIC %md ## Save codelists 

# COMMAND ----------

drop_table("ccu002_06_d17_astadm_primis")
drop_table("ccu002_06_d17_ast_primis")
drop_table("ccu002_06_d17_astrx_primis")
drop_table("ccu002_06_d17_resp_primis")
drop_table("ccu002_06_d17_cns_primis")
drop_table("ccu002_06_d17_diab_primis")
drop_table("ccu002_06_d17_dmres_primis")
drop_table("ccu002_06_d17_sev_mental_primis")
drop_table("ccu002_06_d17_smhres_primis")
drop_table("ccu002_06_d17_chd_primis")
drop_table("ccu002_06_d17_ckd15_primis")
drop_table("ccu002_06_d17_ckd35_primis")
drop_table("ccu002_06_d17_ckd_primis")
drop_table("ccu002_06_d17_cld_primis")
drop_table("ccu002_06_d17_immdx_primis")
drop_table("ccu002_06_d17_immrx_primis")
drop_table("ccu002_06_d17_spln_primis")
drop_table("ccu002_06_d17_learndis_primis")
drop_table("ccu002_06_d17_bmi_stage_primis")
drop_table("ccu002_06_d17_sev_obesity_primis")
drop_table("ccu002_06_d17_bmi_primis")

# COMMAND ----------

create_table("ccu002_06_d17_astadm_primis")
create_table("ccu002_06_d17_ast_primis")
create_table("ccu002_06_d17_astrx_primis")
create_table("ccu002_06_d17_resp_primis")
create_table("ccu002_06_d17_cns_primis")
create_table("ccu002_06_d17_diab_primis")
create_table("ccu002_06_d17_dmres_primis")
create_table("ccu002_06_d17_sev_mental_primis")
create_table("ccu002_06_d17_smhres_primis")
create_table("ccu002_06_d17_chd_primis")
create_table("ccu002_06_d17_ckd15_primis")
create_table("ccu002_06_d17_ckd35_primis")
create_table("ccu002_06_d17_ckd_primis")
create_table("ccu002_06_d17_cld_primis")
create_table("ccu002_06_d17_immdx_primis")
create_table("ccu002_06_d17_immrx_primis")
create_table("ccu002_06_d17_spln_primis")
create_table("ccu002_06_d17_learndis_primis")
create_table("ccu002_06_d17_bmi_stage_primis")
create_table("ccu002_06_d17_sev_obesity_primis")
create_table("ccu002_06_d17_bmi_primis")
