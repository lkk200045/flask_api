-- system_params_confi
-- storage_type
INSERT INTO `system_params_config`(
`config_id`,`config_parent_code`,`group_code`,`config_code`,`config_name`,`is_disabled`,`config_description`,`crt_user_id`, `crt_user_name`, `crt_date`, `mdy_user_id`, `mdy_user_name`, `mdy_date`
) VALUES (
uuid(),null,'storage_type','MySQL','MySQL',0,null, 'SYSTEM', 'SYSTEM', now(), 'SYSTEM', 'SYSTEM', now()
);
INSERT INTO `system_params_config`(
`config_id`,`config_parent_code`,`group_code`,`config_code`,`config_name`,`is_disabled`,`config_description`,`crt_user_id`, `crt_user_name`, `crt_date`, `mdy_user_id`, `mdy_user_name`, `mdy_date`
) VALUES (
uuid(),null,'storage_type','MongoDB','MongoDB',0,null, 'SYSTEM', 'SYSTEM', now(), 'SYSTEM', 'SYSTEM', now()
);

-- table_type
INSERT INTO `system_params_config`(
`config_id`,`config_parent_code`,`group_code`,`config_code`,`config_name`,`is_disabled`,`config_description`,`crt_user_id`, `crt_user_name`, `crt_date`, `mdy_user_id`, `mdy_user_name`, `mdy_date`
)
SELECT
uuid(),
MD5(CONCAT(group_code , config_code)),
'table_type','Table','MySQL資料表',0,null, 'SYSTEM', 'SYSTEM', now(), 'SYSTEM', 'SYSTEM', now()
FROM system_params_config where group_code='storage_type' and config_code='MySQL'
;
INSERT INTO `system_params_config`(
`config_id`,`config_parent_code`,`group_code`,`config_code`,`config_name`,`is_disabled`,`config_description`,`crt_user_id`, `crt_user_name`, `crt_date`, `mdy_user_id`, `mdy_user_name`, `mdy_date`
)
SELECT
uuid(),
MD5(CONCAT(group_code , config_code)),
'table_type','Collection','MongoDB資料表',0,null, 'SYSTEM', 'SYSTEM', now(), 'SYSTEM', 'SYSTEM', now()
FROM system_params_config where group_code='storage_type' and config_code='MongoDB'
;

-- table_format
INSERT INTO `system_params_config`(
`config_id`,`config_parent_code`,`group_code`,`config_code`,`config_name`,`is_disabled`,`config_description`,`crt_user_id`, `crt_user_name`, `crt_date`, `mdy_user_id`, `mdy_user_name`, `mdy_date`
)
SELECT
uuid(),
MD5(CONCAT(group_code , config_code)),
'table_format','Table','資料表格式',0,null, 'SYSTEM', 'SYSTEM', now(), 'SYSTEM', 'SYSTEM', now()
FROM system_params_config where group_code='storage_type' and config_code='MySQL'
;
INSERT INTO `system_params_config`(
`config_id`,`config_parent_code`,`group_code`,`config_code`,`config_name`,`is_disabled`,`config_description`,`crt_user_id`, `crt_user_name`, `crt_date`, `mdy_user_id`, `mdy_user_name`, `mdy_date`
)
SELECT
uuid(),
MD5(CONCAT(group_code , config_code)),
'table_format','JSON','JSON',0,null, 'SYSTEM', 'SYSTEM', now(), 'SYSTEM', 'SYSTEM', now()
FROM system_params_config where group_code='storage_type' and config_code='MongoDB'
;

-- field_type
INSERT INTO `system_params_config`(
`config_id`,`group_code`,`config_code`,`config_name`,`is_disabled`,`config_description`,`crt_user_id`, `crt_user_name`, `crt_date`, `mdy_user_id`, `mdy_user_name`, `mdy_date`
) VALUES (
uuid(),'field_type','String','字串',0,null, 'SYSTEM', 'SYSTEM', now(), 'SYSTEM', 'SYSTEM', now()
);
INSERT INTO `system_params_config`(
`config_id`,`group_code`,`config_code`,`config_name`,`is_disabled`,`config_description`,`crt_user_id`, `crt_user_name`, `crt_date`, `mdy_user_id`, `mdy_user_name`, `mdy_date`
) VALUES (
uuid(),'field_type','DateTime','日期',0,null, 'SYSTEM', 'SYSTEM', now(), 'SYSTEM', 'SYSTEM', now()
);
INSERT INTO `system_params_config`(
`config_id`,`group_code`,`config_code`,`config_name`,`is_disabled`,`config_description`,`crt_user_id`, `crt_user_name`, `crt_date`, `mdy_user_id`, `mdy_user_name`, `mdy_date`
) VALUES (
uuid(),'field_type','Integer','整數',0,null, 'SYSTEM', 'SYSTEM', now(), 'SYSTEM', 'SYSTEM', now()
);
INSERT INTO `system_params_config`(
`config_id`,`group_code`,`config_code`,`config_name`,`is_disabled`,`config_description`,`crt_user_id`, `crt_user_name`, `crt_date`, `mdy_user_id`, `mdy_user_name`, `mdy_date`
) VALUES (
uuid(),'field_type','Float','浮點數(Float)',0,null, 'SYSTEM', 'SYSTEM', now(), 'SYSTEM', 'SYSTEM', now()
);
INSERT INTO `system_params_config`(
`config_id`,`group_code`,`config_code`,`config_name`,`is_disabled`,`config_description`,`crt_user_id`, `crt_user_name`, `crt_date`, `mdy_user_id`, `mdy_user_name`, `mdy_date`
) VALUES (
uuid(),'field_type','Long','長整數',0,null, 'SYSTEM', 'SYSTEM', now(), 'SYSTEM', 'SYSTEM', now()
);
INSERT INTO `system_params_config`(
`config_id`,`group_code`,`config_code`,`config_name`,`is_disabled`,`config_description`,`crt_user_id`, `crt_user_name`, `crt_date`, `mdy_user_id`, `mdy_user_name`, `mdy_date`
) VALUES (
uuid(),'field_type','BigDecimal','浮點數(BigDecimal)',0,null, 'SYSTEM', 'SYSTEM', now(), 'SYSTEM', 'SYSTEM', now()
);
INSERT INTO `system_params_config`(
`config_id`,`group_code`,`config_code`,`config_name`,`is_disabled`,`config_description`,`crt_user_id`, `crt_user_name`, `crt_date`, `mdy_user_id`, `mdy_user_name`, `mdy_date`
) VALUES (
uuid(),'field_type','Boolean','布林(Boolean)',0,null, 'SYSTEM', 'SYSTEM', now(), 'SYSTEM', 'SYSTEM', now()
);