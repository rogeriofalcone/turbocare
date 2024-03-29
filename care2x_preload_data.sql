# The preloaded data follows ################################################

#
# Dumping data for table care_category_diagnosis
#

INSERT INTO care_category_diagnosis VALUES ('1', 'most_responsible', 'Most responsible', 'LDMostResponsible', 'M', 'LDMostResp_s', 'Most responsible diagnosis, must be only one per admission or visit', '0', '', '', '', 20030525120956, '', 00000000000000);
INSERT INTO care_category_diagnosis VALUES ('2', 'associated', 'Associated', 'LDAssociated', 'A', 'LDAssociated_s', 'Associated diagnosis, can be several per  admission or visit', '0', '', '', '', 20030525121005, '', 00000000000000);
INSERT INTO care_category_diagnosis VALUES ('3', 'nosocomial', 'Hospital acquired', 'LDNosocomial', 'N', 'LDNosocomial_s', 'Hospital acquired problem, can be several per admission or visit', '0', '', '', '', 20030525121015, '', 00000000000000);
INSERT INTO care_category_diagnosis VALUES ('4', 'iatrogenic', 'Iatrogenic', 'LDIatrogenic', 'I', 'LDIatrogenic_s', 'Problem resulting from a procedural/surgical complication or medication mistake', '0', '', '', '', 20030525121025, '', 00000000000000);
INSERT INTO care_category_diagnosis VALUES ('5', 'other', 'Other', 'LDOther', 'O', 'LDOther_s', 'Other  diagnosis', '0', '', '', '', 20030525121033, '', 00000000000000);

#
# Dumping data for table care_category_disease
#

INSERT INTO care_category_disease VALUES ('1', '2', 'asphyxia', 'Asphyxia', 'LDAsphyxia', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_category_disease VALUES ('2', '2', 'infection', 'Infection', 'LDInfection', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_category_disease VALUES ('3', '2', 'congenital_abnomality', 'Congenital abnormality', 'LDCongenitalAbnormality', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_category_disease VALUES ('4', '2', 'trauma', 'Trauma', 'LDTrauma', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_category_procedure
#

INSERT INTO care_category_procedure VALUES ('1', 'main', 'Main', 'LDMain', 'M', 'LDMain_s', 'Main procedure, must be only one per op or intervention visit', '0', '', '', '', 20030614013508, '', 00000000000000);
INSERT INTO care_category_procedure VALUES ('2', 'supplemental', 'Supplemental', 'LDSupplemental', 'S', 'LDSupp_s', 'Supplemental procedure, can be several per  encounter op or intervention or visit', '0', '', '', '', 20030614015324, '', 00000000000000);

#
# Dumping data for table care_class_encounter
#

INSERT INTO care_class_encounter VALUES (1, 'inpatient', 'Inpatient', 'LDStationary', 'Inpatient admission - stays at least in a ward and assigned a bed', '0', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_encounter VALUES (2, 'outpatient', 'Outpatient', 'LDAmbulant', 'Outpatient visit - does not stay in a ward nor assigned a bed', '0', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_class_ethnic_orig
#

INSERT INTO care_class_ethnic_orig VALUES (1, 'race', 'LDRace', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_ethnic_orig VALUES (2, 'country', 'LDCountry', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_class_financial
#

INSERT INTO care_class_financial VALUES (1, 'care_c', 'care', 'c', 'common', 'LDcommon', 'Common nursing care services. (Non-private)', 'Patient with common health fund insurance policy.', '', '', '', 20021229134050, '', 00000000000000);
INSERT INTO care_class_financial VALUES (2, 'care_pc', 'care', 'p/c', 'private + common', 'LDprivatecommon', 'Private services added to common services', 'Patient with common health fund insurance\r\npolicy with additional private insurance policy\r\nOR self paying components.', '', '', '', 20021229134451, '', 20021229134451);
INSERT INTO care_class_financial VALUES (3, 'care_p', 'care', 'p', 'private', 'LDprivate', 'Private nursing care services', 'Patient with private insurance policy\r\nOR self paying.', 'LDprivate', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_financial VALUES (4, 'care_pp', 'care', 'pp', 'private plus', 'LDprivateplus', '"Very private" nursing care services', 'Patient with private health insurance policy\r\nAND self paying components.', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_financial VALUES (5, 'room_c', 'room', 'c', 'common', 'LDcommon', 'Common room services (non-private)', 'Patient with common health fund insurance policy. ', 'LDcommon', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_financial VALUES (6, 'room_pc', 'room', 'p/c', 'private + common', '', 'Private services added to common services', 'Patient with common health fund insurance policy with additional private insurance policy OR self paying components.', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_financial VALUES (7, 'room_p', 'room', 'p', 'private', '', 'Private room services', 'Patient with private insurance policy OR self paying. ', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_financial VALUES (8, 'room_pp', 'room', 'pp', 'private plus', '', '"Very private" room services', 'Patient with private health insurance policy AND self paying components.', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_financial VALUES (9, 'att_dr_c', 'att_dr', 'c', 'common', '', 'Common clinician services', 'Patient with common health fund insurance policy. ', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_financial VALUES (10, 'att_dr_pc', 'att_dr', 'p/c', 'private + common', '', 'Private services added to common clinician services', 'Patient with common health fund insurance policy with additional private insurance policy OR self paying components.', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_financial VALUES (11, 'att_dr_p', 'att_dr', 'p', 'private', '', 'Private clinician services', 'Patient with private insurance policy OR self paying.', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_financial VALUES (12, 'att_dr_pp', 'att_dr', 'pp', 'private plus', '', '"Very private" clinician services', 'Patient with private health insurance policy AND self paying components.', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_class_insurance
#

INSERT INTO care_class_insurance VALUES (1, 'private', 'Private', 'LDPrivate', 'Private insurance plan (paid by insured alone)', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_insurance VALUES (2, 'common', 'Health Fund', 'LDInsurance', 'Public (common) health fund - usually paid both by the insured and his employer, eventually paid by the state', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_insurance VALUES (3, 'self_pay', 'Self pay', 'LDSelfPay', '', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_class_therapy
#

INSERT INTO care_class_therapy VALUES (1, '2', 'photo', 'Phototherapy', 'LDPhototherapy', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_therapy VALUES (2, '2', 'iv', 'IV Fluids', 'LDIVFluids', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_therapy VALUES (3, '2', 'oxygen', 'Oxygen therapy', 'LDOxygenTherapy', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_therapy VALUES (4, '2', 'cpap', 'CPAP', 'LDCPAP', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_therapy VALUES (5, '2', 'ippv', 'IPPV', 'LDIPPV', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_therapy VALUES (6, '2', 'nec', 'NEC', 'LDNEC', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_therapy VALUES (7, '2', 'tpn', 'TPN', 'LDTPN', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_class_therapy VALUES (8, '2', 'hie', 'HIE', 'LDHIE', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_classif_neonatal
#

INSERT INTO care_classif_neonatal VALUES (1, 'jaundice', 'Neonatal jaundice', 'LDNeonatalJaundice',  NULL, '', '', 20030807125731, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (2, 'x_transfusion', 'Exchange transfusion', 'LDExchangeTransfusion',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (3, 'photo_therapy', 'Photo therapy', 'LDPhotoTherapy',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (4, 'h_i_encep', 'Hypoxic ischaemic encephalopathy', 'LDH_I_Encephalopathy',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (5, 'parenteral', 'Parenteral nutrition', 'LDParenteralNutrition',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (6, 'vent_support', 'Ventilatory support', 'LDVentilatorySupport',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (7, 'oxygen_therapy', 'Oxygen therapy', 'LDOxygenTherapy',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (8, 'cpap', 'CPAP', 'LDCPAP', 'Continuous positive airway pressure', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (9, 'congenital_abnormality', 'Congenital abnormality', 'LDCongenitalAbnormality',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (10, 'congenital_infection', 'Congenital infection', 'LDCongenitalInfection',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (11, 'acquired_infection', 'Acquired infection', 'LDAcquiredInfection',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (12, 'gbs_infection', 'GBS infection', 'LDGBSInfection', 'Group B Strep Infection', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (13, 'rds', 'Resp Distress Syndrome', 'LDRespDistressSyndrome',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (14, 'blood_transfusion', 'Blood transfusion', 'LDBloodTransfusion',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (15, 'antibiotic_therapy', 'Antibiotic therapy', 'LDAntibioticTherapy',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_classif_neonatal VALUES (16, 'necrotising_enterocolitis', 'Necrotising enterocolitis', 'LDNecrotisingEnterocolitis',  NULL, '', '', 20030807191727, '', 00000000000000);

#
# Dumping data for table care_complication
#

INSERT INTO care_complication VALUES (1, 1, 'Previous C/S', 'LDPreviousCS', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (2, 1, 'Pre-eclampsia', 'LDPreEclampsia', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (3, 1, 'Eclampsia', 'LDEclampsia', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (4, 1, 'Other hypertension', 'LDOtherHypertension', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (5, 1, 'Other proteinuria', 'LDProteinuria', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (6, 1, 'Cardiac', 'LDCardiac', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (7, 1, 'Anaemia < 8.5g', 'LDAnaemia', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (8, 1, 'Asthma', 'LDAsthma', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (9, 1, 'Epilepsy', 'LDEpilepsy', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (10, 1, 'Placenta praevia', 'LDPlacentaPraevia', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (11, 1, 'Abruptio placentae', 'LDAbruptioPlacentae', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (12, 1, 'Other APH', 'LDOtherAPH', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (13, 1, 'Diabetes', 'LDDiabetes', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (14, 1, 'Cord prolapse', 'LDCordProlapse', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (15, 1, 'Ruptured uterus', 'LDRupturedUterus', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_complication VALUES (16, 1, 'Extrauterine pregnancy', 'LDExtraUterinePregnancy', '', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_config_global
#


INSERT INTO care_config_global VALUES ('date_format', 'dd/MM/yyyy', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('time_format', 'HH.MM', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('patient_reg_nr_adder', '10000000','', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('main_info_police_nr', '11?', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('main_info_fire_dept_nr', '12?', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('main_info_emgcy_nr', '13?', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('main_info_phone', '1234567', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('main_info_fax', '567890','', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('main_info_address', 'Virtualstr. 89AA\r\nCyberia 89300\r\nLas Vegas County', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('main_info_email', 'contact@care2x.com', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_id_nr_adder', '10000000', '', '', '', '', 00000000000000, '', 000000000000000);
INSERT INTO care_config_global VALUES ('patient_outpatient_nr_adder', '500000','', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('patient_inpatient_nr_adder', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_name_2_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_name_3_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_name_middle_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_name_maiden_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_ethnic_orig_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_name_others_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_nat_id_nr_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_religion_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_cellphone_2_nr_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_phone_2_nr_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_citizenship_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_sss_nr_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('language_default', 'en', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('language_single', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('mascot_hide', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('mascot_style', 'default', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('gui_frame_left_nav_width', '150', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('gui_frame_left_nav_border', '1', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_fotos_path', 'fotos/news/', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_headline_title_font_size', '5', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_headline_title_font_face', 'arial,verdana,helvetica,sans serif', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_headline_title_font_color', '#CC3333', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_headline_preface_font_size', '2', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_headline_preface_font_face', 'arial,verdana,helvetica,sans serif','', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_headline_preface_font_color', '#336666', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_headline_body_font_size', '2', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_headline_body_font_face', 'arial,verdana,helvetica,sans serif', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_headline_body_font_color', '#000033', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_normal_preview_maxlen', '600', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_headline_title_font_bold', '1', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_headline_preface_font_bold', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('news_normal_display_width', '100%', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_fax_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_email_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_phone_1_nr_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_cellphone_1_nr_hide', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_foto_path', 'fotos/registration/', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('patient_service_care_hide', '1', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('patient_service_room_hide', '1', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('patient_service_att_dr_hide', '1', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('patient_financial_class_single_result', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('patient_name_2_show', '1', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('patient_name_3_show', '1', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('patient_name_middle_show', '1', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('theme_control_buttons', 'default', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('gui_frame_left_nav_bdcolor', '#990000', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('theme_control_theme_list', 'default,blue_aqua', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('medocs_text_preview_maxlen', '100', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('personell_nr_adder', '100000', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('notes_preview_maxlen', '120', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_id_nr_init', '10000000', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('personell_nr_init', '100000', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('encounter_nr_init', '000000', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('encounter_nr_fullyear_prepend', '1', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('theme_mascot', 'default', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('pagin_address_list_max_block_rows', '20', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('pagin_address_search_max_block_rows', '25', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('pagin_insurance_list_max_block_rows', '30', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('pagin_insurance_search_max_block_rows', '25', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('pagin_personell_search_max_block_rows', '20', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('pagin_person_search_max_block_rows', '20', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('pagin_personell_list_max_block_rows', '20', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('pagin_patient_search_max_block_rows', '20', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('pagin_or_patient_search_max_block_rows', '5', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('timeout_inactive', '0', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('timeout_time', '001500', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_title_hide', '0', NULL, 'normal', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_bloodgroup_hide', '0', NULL, 'normal', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_civilstatus_hide', '0', NULL, 'normal', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_insurance_hide', '0', NULL, 'normal', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_config_global VALUES ('person_other_his_nr_hide', '0', NULL, 'normal', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_config_user
#
 
INSERT INTO care_config_user VALUES ('default', 'a:19:{s:4:"mask";s:1:"1";s:11:"idx_bgcolor";s:7:"#99ccff";s:12:"idx_txtcolor";s:7:"#000066";s:9:"idx_hover";s:7:"#ffffcc";s:9:"idx_alink";s:7:"#ffffff";s:11:"top_bgcolor";s:7:"#99ccff";s:12:"top_txtcolor";s:7:"#330066";s:12:"body_bgcolor";s:7:"#ffffff";s:13:"body_txtcolor";s:7:"#000066";s:10:"body_hover";s:7:"#cc0033";s:10:"body_alink";s:7:"#cc0000";s:11:"bot_bgcolor";s:7:"#cccccc";s:12:"bot_txtcolor";s:4:"gray";s:5:"bname";s:0:"";s:8:"bversion";s:0:"";s:2:"ip";s:0:"";s:3:"cid";s:0:"";s:5:"dhtml";s:1:"1";s:4:"lang";s:0:"";}',  '',  '',  '', '', 20030210161831, '', 00000000000000);

#
# Dumping data for table care_currency
#

INSERT INTO care_currency VALUES (13, '', 'Euro', 'European currency', 'main', 'Elpidio Latorilla', 20030802190637, '', 20021126200534);
INSERT INTO care_currency VALUES (3, 'L', 'Pound', 'GB British Pound (ISO = GBP)', '', '', 20030213173107, '', 20020816230349);
INSERT INTO care_currency VALUES (10, 'R', 'Rand', 'South African Rand (ISO = ZAR)', '', '', 20030802190637, 'Elpidio Latorilla', 20020817171805);
INSERT INTO care_currency VALUES (8, 'R', 'Rupees', 'Indian Rupees (ISO = INR)', '', '', 20030213173059, 'Elpidio Latorilla', 20020920234306);

#
# Dumping data for table care_department
#

INSERT INTO care_department VALUES (1, 'pr', '2', 'Public Relations', 'PR', 'Press Relations', 'LDPressRelations', '', '0', '0', '1', '1', '0', '1', '0', '0', '', '', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (2, 'cafe', '2', 'Cafeteria', 'Cafe', 'Canteen', 'LDCafeteria', '', '0', '0', '1', '1', '0', '1', '0', '0', '', '', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (3, 'general_surgery', '1', 'General Surgery', 'General', 'General', 'LDGeneralSurgery', '', '1', '1', '1', '1', '1', '1', '0', '0', '8.30 - 21.00', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 20030828114327, '', 00000000000000);
INSERT INTO care_department VALUES (4, 'emergency_surgery', '1', 'Emergency Surgery', 'Emergency', '', 'LDEmergencySurgery', '', '1', '1', '1', '1', '1', '1', '0', '0', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (5, 'plastic_surgery', '1', 'Plastic Surgery', 'Plastic', 'Aesthetic Surgery', 'LDPlasticSurgery', '', '1', '1', '1', '1', '1', '1', '0', '0', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (6, 'ent', '1', 'Ear-Nose-Throath', 'ENT', 'HNO', 'LDEarNoseThroath', 'Ear-Nose-Throath, in german Hals-Nasen-Ohren. The department with  very old traditions that date back to the early beginnings of premodern medicine.', '1', '1', '1', '1', '1', '1', '0', '0', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0',  NULL, '', 'kope akjdielj asdlkasdf', '', '', 'Update: 2003-08-13 23:24:16 Elpidio Latorilla\r\nUpdate: 2003-08-13 23:25:27 Elpidio Latorilla\r\nUpdate: 2003-08-13 23:29:05 Elpidio Latorilla\r\nUpdate: 2003-08-13 23:30:21 Elpidio Latorilla\r\nUpdate: 2003-08-13 23:31:52 Elpidio Latorilla\r\nUpdate: 2003-08-13 23:34:08 Elpidio Latorilla\r\n', 'Elpidio Latorilla', 20031019155346, '', 00000000000000);
INSERT INTO care_department VALUES (7, 'opthalmology', '1', 'Opthalmology', 'Opthalmology', 'Eye Department', 'LDOpthalmology', '', '1', '1', '1', '1', '1', '1', '0', '0', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (8, 'pathology', '1', 'Pathology', 'Pathology', 'Patho', 'LDPathology', '', '0', '0', '1', '1', '0', '1', '0', '0', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (9, 'ob_gyn', '1', 'Ob-Gynecology', 'Ob-Gyne', 'Gyn', 'LDObGynecology', '', '1', '1', '1', '1', '1', '1', '0', '0', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (10, 'physical_therapy', '1', 'Physical Therapy', 'Physical', 'PT', 'LDPhysicalTherapy', 'Physical therapy department with on-call therapists. Day care clinics, training, rehab.', '1', '0', '1', '1', '0', '1', '1', '16', '8:00 - 15:00', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 20030828114351, '', 00000000000000);
INSERT INTO care_department VALUES (11, 'internal_med', '1', 'Internal Medicine', 'Internal Med', 'InMed', 'LDInternalMedicine', '', '1', '1', '1', '1', '0', '1', '0', '0', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (12, 'imc', '1', 'Intermediate Care Unit', 'IMC', 'Intermediate', 'LDIntermediateCareUnit', '', '1', '1', '1', '1', '0', '1', '0', '0', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (13, 'icu', '1', 'Intensive Care Unit', 'ICU', 'Intensive', 'LDIntensiveCareUnit', '', '1', '1', '1', '1', '0', '1', '0', '0', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (14, 'emergency_ambulatory', '1', 'Emergency Ambulatory', 'Emergency', 'Emergency Amb', 'LDEmergencyAmbulatory', '', '0', '1', '1', '1', '0', '1', '1', '4', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', 'Update: 2003-09-23 00:06:27 Elpidio Latorilla\n', 'Elpidio Latorilla', 20030923000627, '', 00000000000000);
INSERT INTO care_department VALUES (15, 'general_ambulatory', '1', 'General Ambulatory', 'Ambulatory', 'General Amb', 'LDGeneralAmbulatory', '', '0', '1', '1', '1', '0', '1', '1', '3', 'round the clock', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 20030828114254, '', 00000000000000);
INSERT INTO care_department VALUES (16, 'inmed_ambulatory', '1', 'Internal Medicine Ambulatory', 'InMed Ambulatory', 'InMed Amb', 'LDInternalMedicineAmbulatory', '', '0', '1', '1', '1', '0', '1', '1', '11', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (17, 'sonography', '1', 'Sonography', 'Sono', 'Ultrasound diagnostics', 'LDSonography', '', '0', '1', '1', '1', '0', '1', '1', '11', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (18, 'nuclear_diagnostics', '1', 'Nuclear Diagnostics', 'Nuclear', 'Nuclear Testing', 'LDNuclearDiagnostics', '', '0', '1', '1', '1', '0', '1', '1', '19', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (19, 'radiology', '1', 'Radiology', 'Radiology', 'Xray', 'LDRadiology', '', '0', '1', '1', '1', '0', '1', '0', '0', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (20, 'oncology', '1', 'Oncology', 'Oncology', 'Cancer Department', 'LDOncology', '', '1', '1', '1', '1', '1', '1', '0', '11', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (21, 'neonatal', '1', 'Neonatal', 'Neonatal', 'Newborn Department', 'LDNeonatal', '', '1', '1', '1', '1', '1', '1', '1', '9', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0',  NULL, '343', '', '', '', 'Update: 2003-08-13 22:32:07 Elpidio Latorilla\nUpdate: 2003-08-13 22:33:10 Elpidio Latorilla\nUpdate: 2003-08-13 22:43:39 Elpidio Latorilla\nUpdate: 2003-08-13 22:43:59 Elpidio Latorilla\nUpdate: 2003-08-13 22:44:19 Elpidio Latorilla\n', 'Elpidio Latorilla', 20030813224419, '', 00000000000000);
INSERT INTO care_department VALUES (22, 'central_lab', '1', 'Central Laboratory', 'Central Lab', 'General Lab', 'LDCentralLaboratory', '', '0', '0', '1', '1', '0', '1', '0', '0', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', 'kdkdododospdfjdasljfda\r\nasdflasdjf\r\nasdfklasdjflasdjf', '', '', 'Update: 2003-08-13 23:12:30 Elpidio Latorilla\r\nUpdate: 2003-08-13 23:14:59 Elpidio Latorilla\r\nUpdate: 2003-08-13 23:15:28 Elpidio Latorilla\r\n', 'Elpidio Latorilla', 20030828114243, '', 00000000000000);
INSERT INTO care_department VALUES (23, 'serological_lab', '1', 'Serological Laboratory', 'Serological Lab', 'Serum Lab', 'LDSerologicalLaboratory', '', '0', '1', '1', '1', '0', '1', '1', '22', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (24, 'chemical_lab', '1', 'Chemical Laboratory', 'Chemical Lab', 'Chem Lab', 'LDChemicalLaboratory', '', '0', '1', '1', '1', '0', '1', '1', '22', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (25, 'bacteriological_lab', '1', 'Bacteriological Laboratory', 'Bacteriological Lab', 'Bacteria Lab', 'LDBacteriologicalLaboratory', '', '0', '1', '1', '1', '0', '1', '1', '22', '', '12.30 - 15.00 , 19.00 - 21.00', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (26, 'tech', '2', 'Technical Maintenance', 'Tech', 'Technical Support', 'LDTechnicalMaintenance', '', '0', '0', '1', '1', '0', '1', '0', '0', '', '', '0', '0', '', '', '', 'jpg', '', 'Update: 2003-08-10 23:42:30 Elpidio Latorilla\n', 'Elpidio Latorilla', 20030810234230, '', 00000000000000);
INSERT INTO care_department VALUES (27, 'it', '2', 'IT Department', 'IT', 'EDP', 'LDITDepartment', '', '0', '0', '1', '1', '0', '1', '0', '0', '', '', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (28, 'management', '2', 'Management', 'Management', 'Busines Administration', 'LDManagement', '', '0', '0', '1', '1', '0', '1', '0', '0', '', '', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (29, 'exhibition', '3', 'Exhibitions', 'Exhibit', 'Showcases', 'LDExhibitions', '', '0', '0', '1', '1', '1', '1', '0', '0', '', '', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (30, 'edu', '3', 'Education', 'Edu', 'Training', 'LDEducation', 'Education news bulletin of the hospital.', '0', '0', '1', '1', '0', '1', '0', '0', '', '', '0', '0', '', '', '', '', '', 'Update: 2003-08-13 22:44:45 Elpidio Latorilla\nUpdate: 2003-08-13 23:00:37 Elpidio Latorilla\n', 'Elpidio Latorilla', 20030813230037, '', 00000000000000);
INSERT INTO care_department VALUES (31, 'study', '3', 'Studies', 'Studies', 'Advance studies or on-the-job training', 'LDStudies', '', '0', '0', '1', '1', '1', '1', '0', '0', '', '', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (32, 'health_tip', '3', 'Health Tips', 'Tips', 'Health Information', 'LDHealthTips', '', '0', '0', '1', '1', '1', '1', '0', '0', '', '', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (33, 'admission', '2', 'Admission', 'Admit', 'Admission information', 'LDAdmission', '', '0', '0', '1', '1', '1', '0', '1', '0', '', '', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (34, 'news_headline', '3', 'Headline', 'News head', 'Major news', 'LDHeadline', '', '0', '0', '1', '1', '1', '1', '0', '0', '', '', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (35, 'cafenews', '3', 'Cafe News', 'Cafe news', 'Cafeteria news', 'LDCafeNews', '', '0', '0', '1', '1', '1', '0', '0', '0', '', '', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (36, 'nursing', '3', 'Nursing', 'Nursing', 'Nursing care', 'LDNursing', '', '1', '1', '1', '1', '1', '1', '1', '0', '', '', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (37, 'doctors', '3', 'Doctors', 'Doctors', 'Medical personell', 'LDDoctors', '', '0', '0', '1', '1', '1', '1', '0', '0', '', '', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (38, 'pharmacy', '2', 'Pharmacy', 'Pharma', 'Drugstore', 'LDPharmacy', '', '0', '0', '1', '1', '1', '1', '0', '0', '', '', '0', '0',  NULL, '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (39, 'anaesthesiology', '1', 'Anesthesiology', 'ana', 'Anesthesia Department', 'LDAnesthesiology', 'Anesthesiology', '0', '0', '1', '1', '1', '1', '0', '0', '', '', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (40, 'general_ambulant', '1', 'General Outpatient Clinic', 'General Clinic', 'General Ambulatory Clinic', 'LDGeneralOutpatientClinic', 'Outpatient/Ambulant Clinic for general/internal medicine', '0', '1', '1', '1', '0', '0', '1', '16', 'round the clock', '8:30 AM - 11:30 AM , 2:00 PM - 5:30 PM', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_department VALUES (41, 'blood_bank', '1', 'Blood Bank', 'Blood Blank', 'Blood Lab', 'LDBloodBank', '', '0', '0', '1', '1', '0', '1', '0', '0', '', '', '0', '0', '', '', '', '', '', '', '', 00000000000000, '', 00000000000000);


#
# Dumping data for table care_effective_day
#

INSERT INTO care_effective_day VALUES ('1', 'entire stay', 'effective starting from admission date & ending on discharge date', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_effective_day VALUES ('2', 'admission day', 'Effective only on admission day', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_effective_day VALUES ('3', 'discharge day', 'Effective only on discharge day', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_effective_day VALUES ('4', 'op day', 'Effective only on operation day', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_effective_day VALUES ('5', 'transfer day', 'Effective only on transfer day', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_effective_day VALUES ('6', 'period', 'defined start and end dates', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_group
#

INSERT INTO care_group VALUES (1, 'pregnancy', 'Pregnancy', 'LDPregnancy', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_group VALUES (2, 'neonatal', 'Neonatal', 'LDNeonatal', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_group VALUES (3, 'encounter', 'Encounter', 'LDEncounter', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_group VALUES (4, 'op', 'OP', 'LDOP', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_group VALUES (5, 'anesthesia', 'Anesthesia', 'LDAnesthesia', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_group VALUES (6, 'prescription', 'Prescription', 'LDPrescription', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_menu_main
#

INSERT INTO care_menu_main VALUES ('1', '1', 'Home', 'LDHome', 'main/startframe.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('2', '5', 'Patient', 'LDPatient', 'modules/registration_admission/patient_register_pass.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('3', '10', 'Admission', 'LDAdmission', 'modules/registration_admission/aufnahme_pass.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('4', '15', 'Ambulatory', 'LDAmbulatory', 'modules/ambulatory/ambulatory.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('5', '20', 'Medocs', 'LDMedocs', 'modules/medocs/medocs_pass.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('6', '25', 'Doctors', 'LDDoctors', 'modules/doctors/doctors.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('7', '35', 'Nursing', 'LDNursing', 'modules/nursing/nursing.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('8', '40', 'OR', 'LDOR', 'main/op-doku.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('9', '45', 'Laboratories', 'LDLabs', 'modules/laboratory/labor.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('10', '50', 'Radiology', 'LDRadiology', 'modules/radiology/radiolog.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('11', '55', 'Pharmacy', 'LDPharmacy', 'modules/pharmacy/apotheke.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('12', '60', 'Medical Depot', 'LDMedDepot', 'modules/med_depot/medlager.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('13', '65', 'Directory', 'LDDirectory', 'modules/phone_directory/phone.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('14', '70', 'Tech Support', 'LDTechSupport', 'modules/tech/technik.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('15', '72', 'System Admin', 'LDEDP', 'modules/system_admin/edv.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('16', '75', 'Intranet Email', 'LDIntraEmail', 'modules/intranet_email/intra-email-pass.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('17', '80', 'Internet Email', 'LDInterEmail', 'modules/nocc/index.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('18', '85', 'Special Tools', 'LDSpecials', 'main/spediens.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('19', '90', 'Login', 'LDLogin', 'main/login.php', '1', '', '', 20030922232015, 00000000000000);
INSERT INTO care_menu_main VALUES ('20', '7', 'Appointments', 'LDAppointments', 'modules/appointment_scheduler/appt_main_pass.php', '1', '',  '', 20030922232015, 20030405000145);

#
# Dumping data for table `care_menu_sub`
#

INSERT INTO care_menu_sub  VALUES ('3', '0', '2', '0', '', '', '', '', '../gui/img/common/default/new_group.gif', '../gui/img/common/default/new_group.gif', '1', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('70', '0', '7', '0', '', '', '', '', '../gui/img/common/default/nurse.gif', '../gui/img/common/default/nurse.gif', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('20', '0', '1', '0', '', '', '', '', '../gui/img/common/default/articles.gif', '../gui/img/common/default/home.gif', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('30', '0', '20', '0', '', '', '', '', '../gui/img/common/default/calendar.gif', '', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('5', '2', '2', '1', 'Admission', 'LDAdmission', '../modules/registration_admission/aufnahme_pass.php', '', '../gui/img/common/default/bn.gif', '../gui/img/common/default/bn.gif', '1', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('1', '1', '2', '1', 'Registration', '', '../modules/registration_admission/patient_register_pass.php', '&target=entry', '../gui/img/common/default/post_discussion.gif', '', '1', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('130', '1', '2', '1', 'Search', 'LDSearch', '../modules/registration_admission/patient_register_pass.php', '&target=search', '../gui/img/common/default/findnew.gif', '../gui/img/common/default/findnew.gif', '1', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('135', '1', '2', '1', 'Archive', 'LDArchive', '../modules/registration_admission/patient_register_pass.php', '&target=archiv', '', '', '1', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('140', '5', '2', '2', 'Search', 'LDSearch', '../modules/registration_admission/aufnahme_pass.php', '&target=search', '../gui/img/common/default/findnew.gif', '../gui/img/common/default/findnew.gif', '1', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('145', '6', '2', '2', 'Archive', 'LDArchive', '../modules/registration_admission/aufnahme_pass.php', '&target=archiv', '', '', '1', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('71', '1', '7', '1', 'Wards', '', '../modules/nursing/nursing.php', '', '../gui/img/common/default/bul_arrowgrnsm.gif', '../gui/img/common/default/bul_arrowgrnsm.gif', '', '', '[station]', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('155', '1', '3', '1', 'Archive', 'LDArchive', '../modules/registration_admission/aufnahme_pass.php', '&target=archiv', '', '', '1', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('40', '0', '3', '0', '', '', '', '', '../gui/img/common/default/bn.gif', '../gui/img/common/default/bn.gif', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('165', '0', '13', '0', '', '', '', '', '../gui/img/common/default/violet_phone.gif', '../gui/img/common/default/violet_phone.gif', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('7', '3', '7', '1', 'Search', '', '../modules/nursing/nursing-patient-such-start.php', '', '../gui/img/common/default/findnew.gif', '', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('72', '2', '7', '1', 'Quick view', '', '../modules/nursing/nursing-schnellsicht.php', '', '../gui/img/common/default/eye_s.gif', '', '1', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('50', '0', '4', '0', '', '', '', '', '../gui/img/common/default/disc_unrd.gif', '', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('120', '0', '6', '0', '', '', '', '', '../gui/img/common/default/forums.gif', '', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('160', '0', '17', '0', '', '', '', '', '../gui/img/common/default/c-mail.gif', '', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('190', '0', '16', '0', '', '', '', '', '../gui/img/common/default/bubble2.gif', '', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('195', '0', '10', '0', '', '', '', '', '../gui/img/common/default/torso.gif', '', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('200', '0', '18', '0', '', '', '', '', '../gui/img/common/default/settings_tree.gif', '', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('205', '0', '11', '0', '', '', '', '', '../gui/img/common/default/add.gif', '', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('160', '0', '19', '0', '', '', '', '', '../gui/img/common/default/padlock.gif', '../gui/img/common/default/bul_arrowgrnsm.gif', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('215', '0', '15', '0', '', '', '', '', '../gui/img/common/default/sections.gif', '', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('220', '0', '12', '0', '', '', '', '', '../gui/img/common/default/storage.gif', '', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('225', '0', '8', '0', '', '', '', '', '../gui/img/common/default/people_search_online.gif', '', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('230', '0', '9', '0', '', '', '', '', '../gui/img/common/default/chart.gif', '', '', '', '', '', '0001-01-01 00:00:00');
INSERT INTO care_menu_sub  VALUES ('235', '0', '14', '0', '', '', '', '', '../gui/img/common/default/settings_tree.gif', '', '', '', '', '', '0001-01-01 00:00:00');


#
# Dumping data for table care_method_induction
#

INSERT INTO care_method_induction VALUES (3, '1', 'prostaglandin', 'Prostaglandin', 'LDProstaglandin', '', '', '', 20030805191247, '', 00000000000000);
INSERT INTO care_method_induction VALUES (4, '1', 'oxytocin', 'Oxytocin', 'LDOxytocin', '', '', '', 20030805191254, '', 00000000000000);
INSERT INTO care_method_induction VALUES (5, '1', 'arom', 'AROM', 'LDAROM', '', '', '', 20030805191302, '', 00000000000000);
INSERT INTO care_method_induction VALUES (2, '1', 'unknown', 'Unknown', 'LDUnknown', '', '', '', 20030805191240, '', 00000000000000);
INSERT INTO care_method_induction VALUES (1, '1', 'not_induced', 'Not induced', 'LDNotInduced', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_mode_delivery
#

INSERT INTO care_mode_delivery VALUES (1, '2', 'normal', 'Normal', 'LDNormal', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_mode_delivery VALUES (2, '2', 'breech', 'Breech', 'LDBreech', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_mode_delivery VALUES (3, '2', 'caesarian', 'Caesarian', 'LDCaesarian', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_mode_delivery VALUES (4, '2', 'forceps', 'Forceps', 'LDForceps', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_mode_delivery VALUES (5, '2', 'vacuum', 'Vacuum', 'LDVacuum', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_registry
#

INSERT INTO care_registry VALUES ('amb', 'modules/ambulatory/ambulatory.php', 'modules/news/newscolumns.php', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_registry VALUES ('dept', 'modules/news/departments.php', 'modules/news/newscolumns.php', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_registry VALUES ('radiology', 'modules/radiology/radiolog.php', 'modules/news/newscolumns.php', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_registry VALUES ('doctors', 'modules/doctors/doctors.php', 'modules/news/newscolumns.php', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_registry VALUES ('nursing', 'modules/nursing/pflege.php', 'modules/news/newscolumns.php', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_registry VALUES ('edp', 'modules/admin/edv.php', 'modules/news/newscolumns.php', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_registry VALUES ('pharmacy', 'modules/pharmacy/apotheke.php', 'modules/news/newscolumns.php', '', '', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_registry VALUES ('pr', 'modules/news/start_page.php', 'modules/news/start_page.php', 'modules/news/headline-edit.php', 'modules/news/headline-read.php', 'modules/news/editor-pass.php', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_registry VALUES ('cafe', 'modules/cafeteria/cafenews.php', 'modules/cafeteria/cafenews.php', 'modules/cafenews/cafenews-edit.php', 'modules/cafenews/cafenews-read.php', 'modules/cafenews/cafenews-edit-pass.php', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_registry VALUES ('main_start', 'modules/news/start_page.php', 'modules/news/start_page.php', 'modules/news/headline-edit-select-art.php', 'modules/news/headline-read.php', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_registry VALUES ('it', 'modules/system_admin/edv.php', 'modules/news/newscolumns.php', 'modules/news/editor-4plus1-select-art.php', 'modules/news/editor-4plus1-read.php', '', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_registry VALUES ('admission_module', 'modules/admission/aufnahme_start.php', '', '', '', 'modules/admission/aufnahme_pass.php', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_role_person
#

INSERT INTO care_role_person VALUES (1, '3', 'contact', 'Contact person', 'LDContactPerson', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (2, '3', 'guarantor', 'Guarantor', 'LDGuarantor', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (3, '3', 'doctor_att', 'Attending doctor', 'LDAttDoctor', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (4, '3', 'supervisor', 'Supervisor', 'LDSupervisor', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (5, '3', 'doctor_admit', 'Admitting doctor', 'LDAdmittingDoctor', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (6, '3', 'doctor_consult', 'Consulting doctor', 'LDConsultingDoctor', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (7, '4', 'surgeon', 'Surgeon', 'LDSurgeon', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (8, '4', 'surgeon_asst', 'Assisting surgeon', 'LDAssistingSurgeon', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (9, '4', 'nurse_scrub', 'Scrub nurse', 'LDScrubNurse', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (10, '4', 'nurse_rotating', 'Rotating nurse', 'LDRotatingNurse', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (11, '4', 'nurse_anesthesia', 'Anesthesia nurse', 'LDAnesthesiaNurse', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (12, '4', 'anesthesiologist', 'Anesthesiologist', 'LDAnesthesiologist', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (13, '4', 'anesthesiologist_asst', 'Assisting anesthesiologist', 'LDAssistingAnesthesiologist', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (14, '0', 'nurse_on_call', 'Nurse On Call', 'LDNurseOnCall', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (15, '0', 'doctor_on_call', 'Doctor On Call', 'LDDoctorOnCall', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (16, '0', 'nurse', 'Nurse', 'LDNurse', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_role_person VALUES (17, '0', 'doctor', 'Doctor', 'LDDoctor', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_room
#

INSERT INTO care_room VALUES ('1', '2', '2003-04-27', '0000-00-00', '0', 1, 0, 0, '1', '',  NULL, '', '', '', 20030427175459, '', 20030427175459);
INSERT INTO care_room VALUES ('2', '2', '2003-04-27', '0000-00-00', '0', 2, 0, 0, '1', '',  NULL, '', '', '', 20030427175704, '', 20030427175631);
INSERT INTO care_room VALUES ('3', '2', '2003-04-27', '0000-00-00', '0', 3, 0, 0, '1', '',  NULL, '', '', '', 20030427175813, '', 20030427175727);
INSERT INTO care_room VALUES ('4', '2', '2003-04-27', '0000-00-00', '0', 4, 0, 0, '1', '',  NULL, '', '', '', 20030427180021, '', 20030427175846);
INSERT INTO care_room VALUES ('5', '2', '2003-04-27', '0000-00-00', '0', 5, 0, 0, '1', '',  NULL, '', '', '', 20030427180132, '', 20030427175927);
INSERT INTO care_room VALUES ('6', '2', '2003-04-27', '0000-00-00', '0', 6, 0, 0, '1', '',  NULL, '', '', '', 20030427180122, '', 20030427180105);
INSERT INTO care_room VALUES ('7', '2', '2003-04-27', '0000-00-00', '0', 7, 0, 0, '1', '',  NULL, '', '', '', 20030427180310, '', 20030427180310);
INSERT INTO care_room VALUES ('8', '2', '2003-04-27', '0000-00-00', '0', 8, 0, 0, '1', '',  NULL, '', '', '', 20030427180350, '', 20030427180350);
INSERT INTO care_room VALUES ('9', '2', '2003-04-27', '0000-00-00', '0', 9, 0, 0, '1', '',  NULL, '', '', '', 20030427180433, '', 20030427180433);
INSERT INTO care_room VALUES ('10', '2', '2003-04-27', '0000-00-00', '0', 10, 0, 0, '1', '',  NULL, '', '', '', 20030427180503, '', 20030427180503);
INSERT INTO care_room VALUES ('11', '2', '2003-04-27', '0000-00-00', '0', 11, 0, 0, '1', '',  NULL, '', '', '', 20030427180636, '', 20030427180636);
INSERT INTO care_room VALUES ('12', '2', '2003-04-27', '0000-00-00', '0', 12, 0, 0, '1', '',  NULL, '', '', '', 20030427180759, '', 20030427180759);
INSERT INTO care_room VALUES ('13', '2', '2003-04-27', '0000-00-00', '0', 13, 0, 0, '1', '',  NULL, '', '', '', 20030427180826, '', 20030427180826);
INSERT INTO care_room VALUES ('14', '2', '2003-04-27', '0000-00-00', '0', 14, 0, 0, '1', '',  NULL, '', '', '', 20030427180852, '', 20030427180852);
INSERT INTO care_room VALUES ('15', '2', '2003-04-27', '0000-00-00', '0', 15, 0, 0, '1', '',  NULL, '', '', '', 20030427180918, '', 20030427180918);

#
# Dumping data for table care_test_group
#

INSERT INTO care_test_group VALUES (1, 'priority', 'Priority', '5', '', '', 20030711164456, '', 20030711164402);
INSERT INTO care_test_group VALUES (2, 'clinical_chem', 'Clinical chemistry', '10', '', '', 20030711164607, '', 20030711164549);
INSERT INTO care_test_group VALUES (3, 'liquor', 'Liquor', '15', '', '', 20030711164647, '', 00000000000000);
INSERT INTO care_test_group VALUES (4, 'coagulation', 'Coagulation', '20', '', '', 20030711164722, '', 00000000000000);
INSERT INTO care_test_group VALUES (5, 'hematology', 'Hematology', '25', '', '', 20030711164751, '', 00000000000000);
INSERT INTO care_test_group VALUES (6, 'blood_sugar', 'Blood sugar', '30', '', '', 20030711164835, '', 00000000000000);
INSERT INTO care_test_group VALUES (7, 'neonate', 'Neonate', '35', '', '', 20030711164928, '', 00000000000000);
INSERT INTO care_test_group VALUES (8, 'proteins', 'Proteins', '40', '', '', 20030711164951, '', 00000000000000);
INSERT INTO care_test_group VALUES (9, 'thyroid', 'Thyroid', '45', '', '', 20030711165013, '', 00000000000000);
INSERT INTO care_test_group VALUES (10, 'hormones', 'Hormones', '50', '', '', 20030711165032, '', 00000000000000);
INSERT INTO care_test_group VALUES (11, 'tumor_marker', 'Tumor marker', '55', '', '', 20030711165052, '', 00000000000000);
INSERT INTO care_test_group VALUES (12, 'tissue_antibody', 'Tissue antibody', '60', '', '', 20030711165200, '', 00000000000000);
INSERT INTO care_test_group VALUES (13, 'rheuma_factor', 'Rheuma factor', '65', '', '', 20030711165220, '', 00000000000000);
INSERT INTO care_test_group VALUES (14, 'hepatitis', 'Hepatitis', '70', '', '', 20030711165259, '', 00000000000000);
INSERT INTO care_test_group VALUES (15, 'biopsy', 'Biopsy', '75', '', '', 20030711165432, '', 00000000000000);
INSERT INTO care_test_group VALUES (16, 'infection_serology', 'Infection serology', '80', '', '', 20030711165513, '', 00000000000000);
INSERT INTO care_test_group VALUES (17, 'medicines', 'Medicines', '85', '', '', 20030711165535, '', 00000000000000);
INSERT INTO care_test_group VALUES (18, 'prenatal', 'Prenatal', '90', '', '', 20030711165554, '', 00000000000000);
INSERT INTO care_test_group VALUES (19, 'stool', 'Stool', '95', '', '', 20030711165646, '', 00000000000000);
INSERT INTO care_test_group VALUES (20, 'rare', 'Rare', '100', '', '', 20030711165758, '', 00000000000000);
INSERT INTO care_test_group VALUES (21, 'urine', 'Urine', '105', '', '', 20030711165817, '', 00000000000000);
INSERT INTO care_test_group VALUES (22, 'total_urine', 'Total urine', '110', '', '', 20030711165848, '', 00000000000000);
INSERT INTO care_test_group VALUES (23, 'special_params', 'Special', '115', '', '', 20030711170005, '', 00000000000000);

#
# Dumping data for table care_test_param
#

INSERT INTO care_test_param VALUES (1, 'priority', 'Quick', '00q', 'mm/s', '', '', '15', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (2, 'priority', 'PTT', '00ptt', 'mm/s', '', '350', '', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (3, 'priority', 'Hb', '00hb', 'g/dl', '', '18', '12', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (4, 'priority', 'Hk', '00hc', '%', '48', '58', '36', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (5, 'priority', 'Platelets', '00pla', 'c/cmm', '', '500000', '200000', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (6, 'priority', 'RBC', '00rbc', 'mil/cmm', '', '5.5', '4.5', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (7, 'priority', 'WBC', '00wbc', 'c/ccm', '', '9000', '5000', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (8, 'priority', 'Calcium', '00ca', 'mEq/ml', '', '', '', '67', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (9, 'priority', 'Sodium', '00na', 'mEq/ml', '', '100', '20', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (10, 'priority', 'Potassium', '00k', 'mEq/ml', '', '100', '10', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (11, 'priority', 'Blood sugar', '00sug', 'mg/dL', '', '140', '', '260', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (12, 'clinical_chem', 'Alk. Ph.', '0aph', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (13, 'clinical_chem', 'Alpha GT', '0agt', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (14, 'clinical_chem', 'Ammonia', '0amm', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (15, 'clinical_chem', 'Amylase', '0amy', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (16, 'clinical_chem', 'Bili total', '0bit', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (17, 'clinical_chem', 'Bili direct', '0bid', '', '56', '', '', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (18, 'clinical_chem', 'Calcium', '0ca', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (19, 'clinical_chem', 'Chloride', '0chl', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (20, 'clinical_chem', 'Chol', '0cho', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (21, 'clinical_chem', 'Cholinesterase', '0chol', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (22, 'clinical_chem', 'CKMB', '0ccmb', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (23, 'clinical_chem', 'CPK', '0cpc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (24, 'clinical_chem', 'CRP', '0crp', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (25, 'clinical_chem', 'Iron', '0fe', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (26, 'clinical_chem', 'RBC', '0rbc', 'c/ccm', '', '', '', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (27, 'clinical_chem', 'free HgB', '0fhb', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (28, 'clinical_chem', 'GLDH', '0gldh', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (29, 'clinical_chem', 'GOT', '0got', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (30, 'clinical_chem', 'GPT', '0gpt', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (31, 'clinical_chem', 'Uric acid', '0ucid', '', '', '', '', '', '', '', '', '', 'Update 2003-09-05 17:34:05 Elpidio Latorilla\n', 'Elpidio Latorilla', 20030905173405, '', 00000000000000);
INSERT INTO care_test_param VALUES (32, 'clinical_chem', 'Urea', '0urea', '', '', '', '', '', '', '', '', '', 'Update 2003-09-05 17:34:33 Elpidio Latorilla\n', 'Elpidio Latorilla', 20030905173433, '', 00000000000000);
INSERT INTO care_test_param VALUES (33, 'clinical_chem', 'HBDH', '0hbdh', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (34, 'clinical_chem', 'HDL Chol', '0hdlc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (35, 'clinical_chem', 'Potassium', '0pot', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (36, 'clinical_chem', 'Creatinine', '0cre', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (37, 'clinical_chem', 'Copper', '0co', '', '', '', '', '', '', '', '', '', 'Update 2003-09-05 17:22:10 Elpidio Latorilla\n', 'Elpidio Latorilla', 20030905172210, '', 00000000000000);
INSERT INTO care_test_param VALUES (38, 'clinical_chem', 'Lactate i.P.', '0lac', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (39, 'clinical_chem', 'LDH', '0ldh', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (40, 'clinical_chem', 'LDL Chol', '0ldlc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (41, 'clinical_chem', 'Lipase', '0lip', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (42, 'clinical_chem', 'Lipid Elpho', '0lpid', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (43, 'clinical_chem', 'Magnesium', '0mg', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (44, 'clinical_chem', 'Myoglobin', '0myo', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (45, 'clinical_chem', 'Sodium', '0na', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (46, 'clinical_chem', 'Osmolal.', '0osm', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (47, 'clinical_chem', 'Phosphor', '0pho', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (48, 'clinical_chem', 'Serum sugar', '0glo', 'mg/dL', '', '140', '', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (49, 'clinical_chem', 'Tri', '0tri', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (50, 'clinical_chem', 'Troponin T', '0tro', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (51, 'liquor', 'Liquor status', '1stat', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (52, 'liquor', 'Liquor elpho', '1elp', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (53, 'liquor', 'Oligoclonales IgG', '1oli', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (54, 'liquor', 'Reiber Scheme', '1sch', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (55, 'liquor', 'A1', '1a1', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (56, 'coagulation', 'Fibrinolysis', '2fiby', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (57, 'coagulation', 'Quick', '2q', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (58, 'coagulation', 'PTT', '2ptt', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (59, 'coagulation', 'PTZ', '2ptz', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (60, 'coagulation', 'Fibrinogen', '2fibg', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (61, 'coagulation', 'Sol.Fibr.mon.', '2fibs', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (62, 'coagulation', 'FSP dimer', '2fsp', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (63, 'coagulation', 'Thr.Coag.', '2coag', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (64, 'coagulation', 'AT III', '2at3', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (65, 'coagulation', 'Faktor VII', '2f8', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172153, '', 00000000000000);
INSERT INTO care_test_param VALUES (66, 'coagulation', 'APC Resistance', '2apc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (67, 'coagulation', 'Protein C', '2prc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (68, 'coagulation', 'Protein S', '2prs', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (69, 'coagulation', 'Bleeding time', '2bt', 'ml/s', '', '', '', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (70, 'hematology', 'Retikulocytes', '3ret', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (71, 'hematology', 'Malaria', '3mal', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (72, 'hematology', 'Hb Elpho', '3hbe', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (73, 'hematology', 'HLA B 27', '3hla', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (74, 'hematology', 'Platelets AB', '3tab', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (75, 'hematology', 'WBC Phosp.', '3wbp', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (76, 'blood_sugar', 'Blood sugar fasting', '4bsf', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (77, 'blood_sugar', 'Blood sugar 9:00', '4bs9', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (78, 'blood_sugar', 'Blood sugar p.prandial', '4bsp', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (79, 'blood_sugar', 'Bl15:00', '4bs15', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (80, 'blood_sugar', 'Blood sugar 1', '4bs1', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (81, 'blood_sugar', 'Blood sugar 2', '4bs2', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (82, 'blood_sugar', 'Glucose stress.', '4glo', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (83, 'blood_sugar', 'Lactose stress', '4lac', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (84, 'blood_sugar', 'HBA 1c', '4hba', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (85, 'blood_sugar', 'Fructosamine', '4fru', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (86, 'neonate', 'Neonate bilirubin', '5bil', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (87, 'neonate', 'Cord bilirubin', '5bilc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (88, 'neonate', 'Bilirubin direct', '5bild', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (89, 'neonate', 'Neonate sugar 1', '5glo1', 'mg/dL', '', '', '', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (90, 'neonate', 'Neonate sugar 2', '5glo2', 'mg/DL', '', '', '30', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (91, 'neonate', 'Reticulocytes', '5ret', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (92, 'neonate', 'B1', '5b1', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (93, 'proteins', 'Total proteins', '6tot', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (94, 'proteins', 'Albumin', '6alb', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (95, 'proteins', 'Elpho', '6elp', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (96, 'proteins', 'Immune fixation', '6imm', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (97, 'proteins', 'Beta2 Microglobulin.i.S', '6b2', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (98, 'proteins', 'Immune globulin quant.', '6img', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (99, 'proteins', 'IgE', '6ige', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (100, 'proteins', 'Haptoglobin', '6hap', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (101, 'proteins', 'Transferrin', '6tra', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (102, 'proteins', 'Ferritin', '6fer', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (103, 'proteins', 'Coeruloplasmin', '6coe', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (104, 'proteins', 'Alpha 1 Antitrypsin', '6alp', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (105, 'proteins', 'AFP Grav.', '6afp', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (106, 'proteins', 'SSW:', '6ssw', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (107, 'proteins', 'Alpha 1 Microglobulin', '6mic', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (108, 'thyroid', 'T3', '7t3', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (109, 'thyroid', 'Thyroxin/T4', '7t4', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (110, 'thyroid', 'TSH basal', '7tshb', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (111, 'thyroid', 'TSH stim.', '7tshs', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (112, 'thyroid', 'TAB', '7tab', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (113, 'thyroid', 'MAB', '7mab', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (114, 'thyroid', 'TRAB', '7trab', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (115, 'thyroid', 'Thyreoglobulin', '7glob', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (116, 'thyroid', 'Thyroxinbind.Glob.', '7thx', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (117, 'thyroid', 'free T3', '7ft3', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (118, 'thyroid', 'free T4', '7ft4', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (119, 'hormones', 'ACTH', '8acth', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (120, 'hormones', 'Aldosteron', '8ald', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (121, 'hormones', 'Calcitonin', '8cal', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (122, 'hormones', 'Cortisol', '8cor', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (123, 'hormones', 'Cortisol day', '8dcor', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (124, 'hormones', 'FSH', '8fsh', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (125, 'hormones', 'Gastrin', '8gas', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (126, 'hormones', 'HCG', '8hcg', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (127, 'hormones', 'Insulin', '8ins', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (128, 'hormones', 'Catecholam.i.P.', '8cat', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (129, 'hormones', 'LH', '8lh', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (130, 'hormones', 'Ostriol', '8osd', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (131, 'hormones', 'SSW:', '8ssw', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172154, '', 00000000000000);
INSERT INTO care_test_param VALUES (132, 'hormones', 'Parat hormone', '8par', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (133, 'hormones', 'Progesteron', '8prg', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (134, 'hormones', 'Prolactin I', '8pr1', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (135, 'hormones', 'Prolactin II', '8pr2', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (136, 'hormones', 'Renin', '8ren', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (137, 'hormones', 'Serotonin', '8ser', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (138, 'hormones', 'Somatomedin C', '8som', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (139, 'hormones', 'Testosteron', '8tes', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (140, 'hormones', 'C1', '8c1', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (141, 'tumor_marker', 'AFP', '9afp', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (142, 'tumor_marker', 'CA. 15 3', '9c153', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (143, 'tumor_marker', 'CA. 19 9', '9c199', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (144, 'tumor_marker', 'CA. 125', '9c125', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (145, 'tumor_marker', 'CEA', '9cea', '', '', '', '', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (146, 'tumor_marker', 'Cyfra. 21 2', '9c212', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (147, 'tumor_marker', 'HCG', '9hcg', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (148, 'tumor_marker', 'NSE', '9nse', 'test', '', '', '', '', '', '', '', '', '', 'Elpidio Latorilla', 20030806033227, '', 00000000000000);
INSERT INTO care_test_param VALUES (149, 'tumor_marker', 'PSA', '9psa', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (150, 'tumor_marker', 'SCC', '9scc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (151, 'tumor_marker', 'TPA', '9tpa', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (152, 'tissue_antibody', 'ANA', '10ana', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (153, 'tissue_antibody', 'AMA', 'ama', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (154, 'tissue_antibody', 'DNS AB', '10dnsab', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (155, 'tissue_antibody', 'ASMA', '10asm', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (156, 'tissue_antibody', 'ENA', '10ena', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (157, 'tissue_antibody', 'ANCA', '10anc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (158, 'rheuma_factor', 'Anti Strepto Titer', '11ast', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (159, 'rheuma_factor', 'Lat. RF', '11lrf', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (160, 'rheuma_factor', 'Streptozym', '11stz', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (161, 'rheuma_factor', 'Waaler Rose', '11waa', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (162, 'hepatitis', 'Anti HAV', '12hav', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (163, 'hepatitis', 'Anti HAV IgM', '12hai', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (164, 'hepatitis', 'Hbs Antigen', '12hba', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (165, 'hepatitis', 'Anti HBs Titer', '12hbt', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (166, 'hepatitis', 'Anti HBe', '12hbe', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (167, 'hepatitis', 'Anti HBc', '12hbc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (168, 'hepatitis', 'Anti HBc.IgM', '12hci', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (169, 'hepatitis', 'Anti HCV', '12hcv', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (170, 'hepatitis', 'Hep.D Delta A.', '12hda', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (171, 'hepatitis', 'Anti HEV', '12hev', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (172, 'biopsy', 'Protein i.biopsy', '13pro', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (173, 'biopsy', 'LDH i.biopsy', '13ldh', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (174, 'biopsy', 'Chol.i.biopsy', '13cho', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (175, 'biopsy', 'CEA i.biopsy', '13cea', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (176, 'biopsy', 'AFP i.biopsy', '13afp', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (177, 'biopsy', 'Uric acid.i.biopsy', '13ure', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (178, 'biopsy', 'Rheuma fact.i.biopsy', '13rhe', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (179, 'biopsy', 'D1', '13d1', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (180, 'biopsy', 'D2', '13d2', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (181, 'infection_serology', 'Antistaph.Titer', '14stap', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (182, 'infection_serology', 'Adenovirus AB', '14ade', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (183, 'infection_serology', 'Borrelia AB', '14bor', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (184, 'infection_serology', 'Borr.Immunoblot', '14bori', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (185, 'infection_serology', 'Brucellia AB', '14bru', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (186, 'infection_serology', 'Campylob. AB', '14cam', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (187, 'infection_serology', 'Candida AB', '14can', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (188, 'infection_serology', 'Cardiotr.Virus', '14car', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (189, 'infection_serology', 'Chlamydia AB', '14chl', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (190, 'infection_serology', 'C.psittaci AB', '14psi', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (191, 'infection_serology', 'Coxsack. AB', '14cox', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (192, 'infection_serology', 'Cox.burn. AB(Q fever)', '14qf', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (193, 'infection_serology', 'Cytomegaly AB', '14cyt', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (194, 'infection_serology', 'EBV AB', '14ebv', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (195, 'infection_serology', 'Echinococcus AB', '14ecc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (196, 'infection_serology', 'Echo Virus AB', '14ecv', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (197, 'infection_serology', 'FSME AB', '14fsme', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172155, '', 00000000000000);
INSERT INTO care_test_param VALUES (198, 'infection_serology', 'Herpes simp. I AB', '14hs1', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (199, 'infection_serology', 'Herpes simp. II AB', '14hs2', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (200, 'infection_serology', 'HIV1/HIV2 AB', '14hiv', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (201, 'infection_serology', 'Influenza A AB', '14ina', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (202, 'infection_serology', 'Influenza B AB', '14inb', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (203, 'infection_serology', 'LCM AB', '14lcm', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (204, 'infection_serology', 'Leg.pneum AB', '14leg', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (205, 'infection_serology', 'Leptospiria AB', '14lep', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (206, 'infection_serology', 'Listeria AB', '14lis', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (207, 'infection_serology', 'Masern AB', '14mas', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (208, 'infection_serology', 'Mononucleose', '14mon', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (209, 'infection_serology', 'Mumps AB', '14mum', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (210, 'infection_serology', 'Mycoplas.pneum AB', '14myc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (211, 'infection_serology', 'Neutrop Virus AB', '14neu', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (212, 'infection_serology', 'Parainfluenza II AB', '14pi2', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (213, 'infection_serology', 'Parainfluenza III AB', '14pi3', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (214, 'infection_serology', 'Picorna Virus AB', '14pic', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (215, 'infection_serology', 'Rickettsia AB', '14vric', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (216, 'infection_serology', 'Röteln AB', '14rot', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (217, 'infection_serology', 'Röteln Immune status', '14roi', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (218, 'infection_serology', 'RS Virus AB', '14rsv', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (219, 'infection_serology', 'Shigella/Salm AB', '14shi', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (220, 'infection_serology', 'Toxoplasma AB', '14tox', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (221, 'infection_serology', 'TPHA', '14tpha', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (222, 'infection_serology', 'Varicella AB', '14vrc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (223, 'infection_serology', 'Yersinia AB', '14yer', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (224, 'infection_serology', 'E1', '14e1', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (225, 'infection_serology', 'E2', '14e2', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (226, 'infection_serology', 'E3', '14e3', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (227, 'infection_serology', 'E4', '14e4', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (228, 'medicines', 'Amiodaron', '15ami', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (229, 'medicines', 'Barbiturate.i.S.', '15bar', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (230, 'medicines', 'Benzodiazep.i.S.', '15ben', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (231, 'medicines', 'Carbamazepin', '15car', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (232, 'medicines', 'Clonazepam', '15clo', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (233, 'medicines', 'Digitoxin', '15dig', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (234, 'medicines', 'Digoxin', '15dgo', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (235, 'medicines', 'Gentamycin', '15gen', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (236, 'medicines', 'Lithium', '15lit', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (237, 'medicines', 'Phenobarbital', '15phe', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (238, 'medicines', 'Phenytoin', '15pny', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (239, 'medicines', 'Primidon', '15pri', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (240, 'medicines', 'Salicylic acid', '15sal', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (241, 'medicines', 'Theophyllin', '15the', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (242, 'medicines', 'Tobramycin', '15tob', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (243, 'medicines', 'Valproin acid', '15val', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (244, 'medicines', 'Vancomycin', '15van', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (245, 'medicines', 'Amphetamine.i.u.', '15amp', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (246, 'medicines', 'Antidepressant.i.u.', '15ant', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (247, 'medicines', 'Barbiturate.i.u.', '15bau', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (248, 'medicines', 'Benzodiazep.i.u.', '15beu', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (249, 'medicines', 'Cannabinol.i.u.', '15can', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (250, 'medicines', 'Cocain.i.u', '15coc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (251, 'medicines', 'Methadon.i.u.', '15met', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (252, 'medicines', 'Opiate.i.u.', '15opi', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (253, 'prenatal', 'Chlamyd.cult./SSW', '16chl', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (254, 'prenatal', 'SSW:', '16ssw', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (255, 'prenatal', 'Down Screening', '16dow', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (256, 'prenatal', 'Strep B quick test', '16stb', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (257, 'prenatal', 'TPHA', '16tpha', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (258, 'prenatal', 'HBs Ag', '16hbs', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (259, 'prenatal', 'HIV1/HIV2 AV', '16hiv', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (260, 'stool', 'Chymotrypsin', '17chy', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (261, 'stool', 'Occult blood 1', '17ob1', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (262, 'stool', 'Occult blood 2', '17ob2', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (263, 'stool', 'Occult blood 3', '17ob3', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (264, 'rare', 'Rare H.', '18rh', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (265, 'rare', 'Rare E.', '18re', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172156, '', 00000000000000);
INSERT INTO care_test_param VALUES (266, 'rare', 'Rare S.', '18rs', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (267, 'rare', 'Urine rare', '18uri', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (268, 'rare', 'F1', '18f1', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (269, 'rare', 'F2', '18f2', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (270, 'rare', 'F3', '18f3', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (271, 'urine', 'Urine amylase', '19amy', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (272, 'urine', 'Urine sugar', '19sug', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (273, 'urine', 'Protein.i.u.', '19pro', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (274, 'urine', 'Albumin.i.u.', '19alb', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (275, 'urine', 'Osmol.i.u.', '19osm', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (276, 'urine', 'Pregnancy test.', '19pre', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (277, 'urine', 'Cytomeg.i.urine', '19cym', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (278, 'urine', 'Urine cytology', '19cyt', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (279, 'urine', 'Bence Jones', '19bj', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (280, 'urine', 'Urine elpho', '19elp', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (281, 'urine', 'Beta2 microglobulin.i.u.', '19bm2', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (282, 'total_urine', 'Addis Count', '20adc', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (283, 'total_urine', 'Sodium i.u.', '20na', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (284, 'total_urine', 'Potass. i.u.', '20k', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (285, 'total_urine', 'Calcium i.u.', '20ca', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (286, 'total_urine', 'Phospor i.u.', '20pho', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (287, 'total_urine', 'Uric acid i.u.', '20ura', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (288, 'total_urine', 'Creatinin i.u.', '20cre', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (289, 'total_urine', 'Porphyrine i.u.', '20por', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (290, 'total_urine', 'Cortisol i.u.', '20cor', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (291, 'total_urine', 'Hydroxyprolin i.u.', '20hyd', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (292, 'total_urine', 'Catecholamins i.u.', '20cat', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (293, 'total_urine', 'Pancreol.', '20pan', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (294, 'total_urine', 'Gamma Aminoläbulinsre.i.u.', '20gam', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (295, 'special_params', 'Blood alcohol', '21bal', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (296, 'special_params', 'CDT', '21cdt', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (297, 'special_params', 'Vitamin B12', '21vb12', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (298, 'special_params', 'Folic acid', '21fol', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (299, 'special_params', 'Insulin AB', '21inab', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (300, 'special_params', 'Intrinsic AB', '21iab', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (301, 'special_params', 'Stone analysis', '21sto', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (302, 'special_params', 'ACE', '21ace', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (303, 'special_params', 'G1', '21g1', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (304, 'special_params', 'G2', '21g2', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (305, 'special_params', 'G3', '21g3', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (306, 'special_params', 'G4', '21g4', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (307, 'special_params', 'G5', '21g5', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (308, 'special_params', 'G6', '21g6', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (309, 'special_params', 'G7', '21g7', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (310, 'special_params', 'G8', '21g8', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (311, 'special_params', 'G9', '21g9', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);
INSERT INTO care_test_param VALUES (312, 'special_params', 'G10', '21g10', '',  NULL,  NULL,  NULL,  NULL,  NULL,  NULL,  NULL, '', '', '', 20030711172157, '', 00000000000000);

#
# Dumping data for table care_type_anaesthesia
#

INSERT INTO care_type_anaesthesia VALUES (1, 'none', 'None', 'LDNone', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_anaesthesia VALUES (2, 'unknown', 'Unknown', 'LDUnknown', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_anaesthesia VALUES (3, 'general', 'General', 'LDGeneral', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_anaesthesia VALUES (4, 'spinal', 'Spinal', 'LDSpinal', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_anaesthesia VALUES (5, 'epidural', 'Epidural', 'LDEpidural', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_anaesthesia VALUES (6, 'pudendal', 'Pudendal', 'LDPudendal', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_application
#

INSERT INTO care_type_application VALUES (1, '5', 'ita', 'ITA', 'LDITA', 'Intratracheal anesthesia', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_application VALUES (2, '5', 'la', 'LA', 'LDLA', 'Locally applied anesthesia', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_application VALUES (3, '5', 'as', 'AS', 'LDAS', 'Analgesic sedation', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_application VALUES (4, '5', 'mask', 'Mask', 'LDMask', 'Gas anesthesia through breathing mask', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_application VALUES (5, '6', 'oral', 'Oral', 'LDOral', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_application VALUES (6, '6', 'iv', 'Intravenous', 'LDIntravenous', '', '', '', 00000000000000, 'preload', 00000000000000);
INSERT INTO care_type_application VALUES (7, '6', 'sc', 'Subcutaneous', 'LDSubcutaneous', '', '', '', 00000000000000, 'preload', 00000000000000);
INSERT INTO care_type_application VALUES (8, '6', 'im', 'Intramuscular', 'LDIntramuscular', '', '', '', 00000000000000, 'preload', 00000000000000);
INSERT INTO care_type_application VALUES (9, '6', 'sublingual', 'Sublingual', 'LDSublingual', 'Applied under the tounge', '', '', 00000000000000, 'preload', 00000000000000);
INSERT INTO care_type_application VALUES (10, '6', 'ia', 'Intraarterial', 'LDIntraArterial', '', '', '', 00000000000000, 'preload', 00000000000000);
INSERT INTO care_type_application VALUES (11, '6', 'pre_admit', 'Pre-admission', 'LDPreAdmission', '', '', '', 00000000000000, 'preload', 00000000000000);

#
# Dumping data for table care_type_assignment
#

INSERT INTO care_type_assignment VALUES (1, 'ward', 'Ward', 'LDWard', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_assignment VALUES (2, 'dept', 'Department', 'LDDepartment', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_assignment VALUES (3, 'firm', 'Firm', 'LDFirm', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_assignment VALUES (4, 'clinic', 'Clinic', 'LDClinic', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_cause_opdelay
#

INSERT INTO care_type_cause_opdelay VALUES (1, 'patient', 'Patient was delayed', 'LDPatientDelayed', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_cause_opdelay VALUES (2, 'nurse', 'Nurses were delayed', 'LDNursesDelayed', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_cause_opdelay VALUES (3, 'surgeon', 'Surgeons were delayed', 'LDSurgeonsDelayed', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_cause_opdelay VALUES (4, 'cleaning', 'Cleaning delayed', 'LDCleaningDelayed', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_cause_opdelay VALUES (5, 'anesthesia', 'Anesthesiologist was delayed', 'LDAnesthesiologistDelayed', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_cause_opdelay VALUES (0, 'other', 'Other causes', 'LDOtherCauses', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_color
#

INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('yellow', 'yellow', 'LDyellow', '', '', 00000000000000);
INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('black', 'black', 'LDblack', '', '', 00000000000000);
INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('blue_pale', 'pale blue', 'LDpaleblue', '', '', 00000000000000);
INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('brown', 'brown', 'LDbrown', '', '', 00000000000000);
INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('pink', 'pink', 'LDpink', '', '', 00000000000000);
INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('yellow_pale', 'pale yellow', 'LDpaleyellow', '', '', 00000000000000);
INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('red', 'red', 'LDred', '', '', 00000000000000);
INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('green_pale', 'pale green', 'LDpalegreen', '', '', 00000000000000);
INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('violet', 'violet', 'LDviolet', '', '', 00000000000000);
INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('blue', 'blue', 'LDblue', '', '', 00000000000000);
INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('biege', 'biege', 'LDbiege', '', '', 00000000000000);
INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('orange', 'orange', 'LDorange', '', '', 00000000000000);
INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('green', 'green', 'LDgreen', '', '', 00000000000000);
INSERT INTO care_type_color (color_id, name, LD_var, status, modify_id, modify_time) VALUES ('rose', 'rose', 'LDrose', '', '', 00000000000000);

#
# Dumping data for table care_type_department
#

INSERT INTO care_type_department VALUES (1, 'medical', 'Medical', 'LDMedical', 'Medical, Nursing, Diagnostics, Labs, OR', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_department VALUES (2, 'support', 'Support (non-medical)', 'LDSupport', 'non-medical departments', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_department VALUES (3, 'news', 'News', 'LDNews', 'News group or category', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_discharge
#

INSERT INTO care_type_discharge VALUES (1, 'regular', 'Regular discharge', 'LDRegularRelease', '', '', 20030415010555, '', 20030413121226);
INSERT INTO care_type_discharge VALUES (2, 'own', 'Patient left hospital on his own will', 'LDSelfRelease', '', '', 20030415010606, '', 20030413121317);
INSERT INTO care_type_discharge VALUES (3, 'emergency', 'Emergency discharge', 'LDEmRelease', '', '', 20030415010617, '', 20030413121452);
INSERT INTO care_type_discharge VALUES (4, 'change_ward', 'Change of ward', 'LDChangeWard', '', '', 00000000000000, '', 20030413121526);
INSERT INTO care_type_discharge VALUES (6, 'change_bed', 'Change of bed', 'LDChangeBed', '', '', 20030415000942, '', 20030413121619);
INSERT INTO care_type_discharge VALUES (7, 'death', 'Death of patient', 'LDPatientDied', '', '', 20030415010642, '', 00000000000000);
INSERT INTO care_type_discharge VALUES (5, 'change_room', 'Change of room', 'LDChangeRoom', '', '', 20030415010659, '', 00000000000000);
INSERT INTO care_type_discharge VALUES (8, 'change_dept', 'Change of department', 'LDChangeDept', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_duty
#

INSERT INTO care_type_duty VALUES (1, 'regular', 'Regular duty', 'LDRegularDuty', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_duty VALUES (2, 'standby', 'Standby duty', 'LDStandbyDuty', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_duty VALUES (3, 'morning', 'Morning duty', 'LDMorningDuty', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_duty VALUES (4, 'afternoon', 'Afternoon duty', 'LDAfternoonDuty', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_duty VALUES (5, 'night', 'Night duty', 'LDNightDuty', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_encounter
#

INSERT INTO care_type_encounter VALUES (1, 'referral', 'Referral', 'LDEncounterReferral', 'Referral admission or visit', '0', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_encounter VALUES (2, 'emergency', 'Emergency', 'LDEmergency', 'Emergency admission or visit', '0', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_encounter VALUES (3, 'birth_delivery', 'Birth delivery', 'LDBirthDelivery', 'Admission or visit for birth delivery', '0', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_encounter VALUES (4, 'walk_in', 'Walk-in', 'LDWalkIn', 'Walk -in admission or visit (non-referred)', '0', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_encounter VALUES (5, 'accident', 'Accident', 'LDAccident', 'Emergency admission due to accident', '0', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_ethnic_orig
#

INSERT INTO care_type_ethnic_orig VALUES (1, '1', 'asian', 'LDAsian', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_ethnic_orig VALUES (2, '1', 'black', 'LDBlack', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_ethnic_orig VALUES (3, '1', 'caucasian', 'LDCaucasian', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_ethnic_orig VALUES (4, '1', 'white', 'LDWhite', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_feeding
#

INSERT INTO care_type_feeding VALUES (1, '2', 'breast', 'Breast', 'LDBreast', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_feeding VALUES (2, '2', 'formula', 'Formula', 'LDFormula', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_feeding VALUES (3, '2', 'both', 'Both', 'LDBoth', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_feeding VALUES (4, '2', 'parenteral', 'Parenteral', 'LDParenteral', '', '', '', 20030727221351, '', 00000000000000);
INSERT INTO care_type_feeding VALUES (5, '2', 'never_fed', 'Never fed', 'LDNeverFed', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_insurance
#

INSERT INTO care_type_insurance VALUES (1, 'medical_main', 'Medical insurance', 'LDMedInsurance', 'Main (default) medical insurance', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_insurance VALUES (2, 'medical_extra', 'Extra medical insurance', 'LDExtraMedInsurance', 'Extra medical insurance (evt. pays extra services)', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_insurance VALUES (3, 'dental', 'Dental insurance', 'LDDentalInsurance', 'Separate dental plan in case not included in medical plan or simply additional private plan', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_insurance VALUES (4, 'disability', 'Disability plan', 'LDDisabilityPlan', 'Disability insurance plan - general , both long term & short term', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_insurance VALUES (5, 'disability_short', 'Disability plan (short term)', 'LDDisabilityPlanShort', 'Short term disability plan', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_insurance VALUES (6, 'disability_long', 'Disability plan (long term)', 'LDDisabilityPlanLong', 'Long term disability plan', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_insurance VALUES (7, 'retirement_income', 'Retirement  income plan (general)', 'LDRetirementIncomePlan', 'Retirement income plan - either private or income/employer supported', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_insurance VALUES (8, 'edu_reimbursement', 'Educational Reimbursement Plan', 'LDEduReimbursementPlan', 'Reimbursement plan for education, either private or employer supported', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_insurance VALUES (9, 'retirement_medical', 'Retirement medical plan', 'LDRetirementMedPlan', 'Medical plan in retirement  - might include other care services', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_insurance VALUES (10, 'liability', 'Liability Insurance Plan', 'LDLiabilityPlan', 'General liability insurance - either private or employer supported', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_insurance VALUES (11, 'malpractice', 'Malpractice Insurance Plan', 'LDMalpracticeInsurancePlan', 'Insurance plan against possible malpractice', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_insurance VALUES (12, 'unemployment', 'Unemployment Insurance Plan', 'LDUnemploymentPlan', 'Unemployment insurance , in case compulsory unemployment funds are guaranteed by the state, this plan is usually privately paid by the insured', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_localization
#

INSERT INTO care_type_localization VALUES ('1', 'left', 'Left', 'LDLeft', 'L', 'LDLeft_s', '', '0', '', '', '', 20030525150414, '', 20030525150414);
INSERT INTO care_type_localization VALUES ('2', 'right', 'Right', 'LDRight', 'R', 'LDRight_s', '', '0', '', '', '', 20030525150522, '', 20030525150500);
INSERT INTO care_type_localization VALUES ('3', 'both_side', 'Both sides', 'LDBothSides', 'B', 'LDBothSides_s', '', '0', '', '', '', 20030525150618, '', 20030525150618);

#
# Dumping data for table care_type_location
#

INSERT INTO care_type_location VALUES (1, 'dept', 'Department', 'LDDepartment', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_location VALUES (2, 'ward', 'Ward', 'LDWard', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_location VALUES (3, 'firm', 'Firm', 'LDFirm', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_location VALUES (4, 'room', 'Room', 'LDRoom', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_location VALUES (5, 'bed', 'Bed', 'LDBed', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_location VALUES (6, 'clinic', 'Clinic', 'LDClinic', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_measurement
#

INSERT INTO care_type_measurement VALUES (1, 'bp_systolic', 'Systolic', 'LDSystolic', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_measurement VALUES (2, 'bp_diastolic', 'Diastolic', 'LDDiastolic', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_measurement VALUES (3, 'temp', 'Temperature', 'LDTemperature', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_measurement VALUES (4, 'fluid_intake', 'Fluid intake', 'LDFluidIntake', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_measurement VALUES (5, 'fluid_output', 'Fluid output', 'LDFluidOutput', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_measurement VALUES (6, 'weight', 'Weight', 'LDWeight', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_measurement VALUES (7, 'height', 'Height', 'LDHeight', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_measurement VALUES (8, 'bp_composite', 'Sys/Dias', 'LDSysDias', '', '', 20030419143920, '', 20030419143920);
INSERT INTO care_type_measurement VALUES (9, 'head_circumference', 'Head circumference', 'LDHeadCircumference', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_notes
#

INSERT INTO care_type_notes VALUES (1, 'histo_physical', 'Admission History and Physical', 'LDAdmitHistoPhysical', 5, '', '', 20030517182939, '', 00000000000000);
INSERT INTO care_type_notes VALUES (2, 'daily_doctor', 'Doctor\'s daily notes', 'LDDoctorDailyNotes', 55, '', '', 20030517183835, '', 00000000000000);
INSERT INTO care_type_notes VALUES (3, 'discharge', 'Discharge summary', 'LDDischargeSummary', 50, '', '', 20030517183707, '', 00000000000000);
INSERT INTO care_type_notes VALUES (4, 'consult', 'Consultation notes', 'LDConsultNotes', 25, '', '', 20030517183151, '', 00000000000000);
INSERT INTO care_type_notes VALUES (5, 'op', 'Operation notes', 'LDOpNotes', 100, '', '', 20030517184314, '', 00000000000000);
INSERT INTO care_type_notes VALUES (6, 'daily_ward', 'Daily ward\'s notes', 'LDDailyNurseNotes', 30, '', '', 20030517183212, '', 00000000000000);
INSERT INTO care_type_notes VALUES (7, 'daily_chart_notes', 'Chart notes', 'LDChartNotes', 20, '', '', 20030517183141, '', 00000000000000);
INSERT INTO care_type_notes VALUES (8, 'chart_notes_etc', 'PT,ATG,etc. daily notes', 'LDPTATGetc', 115, '', '', 20030517184356, '', 00000000000000);
INSERT INTO care_type_notes VALUES (9, 'daily_iv_notes', 'IV daily notes', 'LDIVDailyNotes', 75, '', '', 20030517184024, '', 00000000000000);
INSERT INTO care_type_notes VALUES (10, 'daily_anticoag', 'Anticoagulant daily notes', 'LDAnticoagDailyNotes', 15, '', '', 20030517183117, '', 00000000000000);
INSERT INTO care_type_notes VALUES (11, 'lot_charge_nr', 'Material LOT, Charge Nr.', 'LDMaterialLOTChargeNr', 80, '', '', 20030517184039, '', 00000000000000);
INSERT INTO care_type_notes VALUES (12, 'text_diagnosis', 'Diagnosis text', 'LDDiagnosis', 40, '', '', 20030517183530, '', 00000000000000);
INSERT INTO care_type_notes VALUES (13, 'text_therapy', 'Therapy text', 'LDTherapy', 120, '', '', 20030517184408, '', 00000000000000);
INSERT INTO care_type_notes VALUES (14, 'chart_extra', 'Extra notes on therapy & diagnosis', 'LDExtraNotes', 65, '', '', 20030517183912, '', 00000000000000);
INSERT INTO care_type_notes VALUES (15, 'nursing_report', 'Nursing care report', 'LDNursingReport', 85, '', '', 20030517184141, '', 00000000000000);
INSERT INTO care_type_notes VALUES (16, 'nursing_problem', 'Nursing problem report', 'LDNursingProblemReport', 95, '', '', 20030517184208, '', 00000000000000);
INSERT INTO care_type_notes VALUES (17, 'nursing_effectivity', 'Nursing effectivity report', 'LDNursingEffectivityReport', 90, '', '', 20030517184156, '', 00000000000000);
INSERT INTO care_type_notes VALUES (18, 'nursing_inquiry', 'Inquiry to doctor', 'LDInquiryToDoctor', 70, '', '', 20030517183951, '', 00000000000000);
INSERT INTO care_type_notes VALUES (19, 'doctor_directive', 'Doctor\'s directive', 'LDDoctorDirective', 60, '', '', 20030517183859, '', 00000000000000);
INSERT INTO care_type_notes VALUES (20, 'problem', 'Problem', 'LDProblem', 110, '', '', 20030517184345, '', 00000000000000);
INSERT INTO care_type_notes VALUES (21, 'development', 'Development', 'LDDevelopment', 35, '', '', 20030517183228, '', 00000000000000);
INSERT INTO care_type_notes VALUES (22, 'allergy', 'Allergy', 'LDAllergy', 10, '', '', 20030517184439, '', 00000000000000);
INSERT INTO care_type_notes VALUES (23, 'daily_diet', 'Diet plan', 'LDDietPlan', 45, '', '', 20030517183545, '', 00000000000000);
INSERT INTO care_type_notes VALUES (99, 'other', 'Other', 'LDOther', 105, '', '', 20030517184331, '', 00000000000000);

#
# Dumping data for table care_type_outcome
#

INSERT INTO care_type_outcome VALUES (1, '2', 'alive', 'Alive', 'LDAlive', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_outcome VALUES (2, '2', 'stillborn', 'Stillborn', 'LDStillborn', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_outcome VALUES (3, '2', 'early_neonatal_death', 'Early neonatal death', 'LDEarlyNeonatalDeath', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_outcome VALUES (4, '2', 'late_neonatal_death', 'Late neonatal death', 'LDLateNeonatalDeath', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_outcome VALUES (5, '2', 'death_uncertain_timing', 'Death uncertain timing', 'LDDeathUncertainTiming', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_perineum
#

INSERT INTO care_type_perineum VALUES (1, 'intact', 'Intact', 'LDIntact', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_perineum VALUES (2, '1_degree', '1st degree tear', 'LDFirstDegreeTear', '', '', '', 20030727212219, '', 00000000000000);
INSERT INTO care_type_perineum VALUES (3, '2_degree', '2nd degree tear', 'LDSecondDegreeTear', '', '', '', 20030727212231, '', 00000000000000);
INSERT INTO care_type_perineum VALUES (4, '3_degree', '3rd degree tear', 'LDThirdDegreeTear', '', '', '', 20030727212242, '', 00000000000000);
INSERT INTO care_type_perineum VALUES (5, 'episiotomy', 'Episiotomy', 'LDEpisiotomy', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_prescription
#

INSERT INTO care_type_prescription VALUES (1, 'anticoag', 'Anticoagulant', 'LDAnticoagulant', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_prescription VALUES (2, 'hemolytic', 'Hemolytic', 'LDHemolytic', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_prescription VALUES (3, 'diuretic', 'Diuretic', 'LDDiuretic', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_prescription VALUES (4, 'antibiotic', 'Antibiotic', 'LDAntibiotic', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_room
#

INSERT INTO care_type_room VALUES (1, 'ward', 'Ward room', 'LDWard', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_room VALUES (2, 'op', 'Operating room', 'LDOperatingRoom', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_test
#

INSERT INTO care_type_test VALUES (1, 'chemlabor', 'Chemical-Serology Lab', 'LDChemSerologyLab', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_test VALUES (2, 'patho', 'Pathological Lab', 'LDPathoLab', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_test VALUES (3, 'baclabor', 'Bacteriological Lab', 'LDBacteriologicalLab', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_test VALUES (4, 'radio', 'Radiological Lab', 'LDRadiologicalLab', 'Lab for X-ray, Mammography, Computer Tomography, NMR', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_test VALUES (5, 'blood', 'Blood test & product', 'LDBloodTestProduct', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_test VALUES (6, 'generic', 'Generic test program', 'LDGenericTestProgram', '', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_time
#

INSERT INTO care_type_time VALUES (1, 'patient_entry_exit', 'Patient entry/exit', 'LDPatientEntryExit', 'Times when patient entered and left the op room', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_time VALUES (2, 'op_start_end', 'OP start/end', 'LDOPStartEnd', 'Times when op started (1st incision) and ended (last suture)', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_time VALUES (3, 'delay', 'Delay time', 'LDDelayTime', 'Times when the op was delayed due to any reason', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_time VALUES (4, 'plaster_cast', 'Plaster cast', 'LDPlasterCast', 'Times when the plaster cast was made', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_time VALUES (5, 'reposition', 'Reposition', 'LDReposition', 'Times when a dislocated joint(s) was repositioned (non invasive op)', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_time VALUES (6, 'coro', 'Coronary catheter', 'LDCoronaryCatheter', 'Times when a coronary catherer op was done (minimal invasive op)', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_time VALUES (7, 'bandage', 'Bandage', 'LDBandage', 'Times when the bandage was made', '', '', 00000000000000, '', 00000000000000);

#
# Dumping data for table care_type_unit_measurement
#

INSERT INTO care_type_unit_measurement VALUES (1, 'volume', 'Volume', 'LDVolume', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_unit_measurement VALUES (2, 'weight', 'Weight', 'LDWeight', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_unit_measurement VALUES (3, 'length', 'Length', 'LDLength', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_unit_measurement VALUES (4, 'pressure', 'Pressure', 'LDPressure', '', '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_type_unit_measurement VALUES (5, 'temperature', 'Temperature', 'LDTemperature', '', '', '', 20030419144724, '', 20030419144724);

#
# Dumping data for table care_unit_measurement
#

INSERT INTO care_unit_measurement VALUES (1, 1, 'ml', 'Milliliter', 'LDMilliliter', 'metric',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (2, 2, 'mg', 'Milligram', 'LDMilligram', 'metric',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (3, 3, 'mm', 'Millimeter', 'LDMillimeter', 'metric',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (4, 1, 'ltr', 'liter', 'LDLiter', 'metric',  NULL, '', '', 20030727131658, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (5, 2, 'gm', 'gram', 'LDGram', 'metric',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (6, 2, 'kg', 'kilogram', 'LDKilogram', 'metric',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (7, 3, 'cm', 'centimeter', 'LDCentimeter', 'metric',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (8, 3, 'm', 'meter', 'LDMeter', 'metric',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (9, 3, 'km', 'kilometer', 'LDKilometer', 'metric',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (10, 3, 'in', 'inch', 'LDInch', 'english',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (11, 3, 'ft', 'foot', 'LDFoot', 'english',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (12, 3, 'yd', 'yard', 'LDYard', 'english',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (14, 4, 'mmHg', 'mmHg', 'LDmmHg', 'metric',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (15, 5, 'celsius', 'Celsius', 'LDCelsius', 'metric',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (16, 1, 'dl', 'deciliter', 'LDDeciliter', 'metric',  NULL, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (17, 1, 'cl', 'centiliter', 'LDCentiliter', 'metric', 0, '', '', 00000000000000, '', 00000000000000);
INSERT INTO care_unit_measurement VALUES (18, 1, 'µl', 'microliter', 'LDMicroliter', 'metric', 0, '', '', 00000000000000, '', 00000000000000);


#
# Dumping data for table care_version
#

INSERT INTO care_version VALUES ('CARE2X', 'beta', '2.0.0', '1.0', '2004-05-14', '00:00:00', 'Elpidio Latorilla');
