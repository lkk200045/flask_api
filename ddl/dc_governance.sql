DROP TABLE IF EXISTS metric_catalog_provider;
DROP TABLE IF EXISTS metric_catalog_relation;
DROP TABLE IF EXISTS metric_catalog_tag;
DROP TABLE IF EXISTS metric_feature;
DROP TABLE IF EXISTS metric_feature_catalog;
DROP TABLE IF EXISTS metric_feature_relation;
DROP TABLE IF EXISTS metric_field;
DROP TABLE IF EXISTS metric_field_catalog;
DROP TABLE IF EXISTS metric_field_feature;
DROP TABLE IF EXISTS metric_field_relation;
DROP TABLE IF EXISTS metric_table;
DROP TABLE IF EXISTS metric_table_field;
DROP TABLE IF EXISTS metric_table_relation;
DROP TABLE IF EXISTS provider_account;
DROP TABLE IF EXISTS provider_user;
DROP TABLE IF EXISTS storage_info;
DROP TABLE IF EXISTS storage_metric_table;
DROP TABLE IF EXISTS storage_provider;
DROP TABLE IF EXISTS system_params_config;


CREATE TABLE metric_catalog_provider (
    catalog_tag_id VARCHAR(36) NOT NULL,
    account_id VARCHAR(36) NOT NULL,
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (catalog_tag_id , account_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='企業與分類標籤關聯表';

CREATE TABLE metric_catalog_relation (
    source_catalog_tag_id VARCHAR(36) NOT NULL,
    sink_catalog_tag_id VARCHAR(36) NOT NULL,
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間'
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='分類標籤關係表';

CREATE INDEX metric_catalog_relation_idx01 ON metric_catalog_relation(source_catalog_tag_id);
CREATE INDEX metric_catalog_relation_idx02 ON metric_catalog_relation(sink_catalog_tag_id);

CREATE TABLE metric_catalog_tag (
    tag_id VARCHAR(36) NOT NULL COMMENT 'PK',
    tag_parent_id VARCHAR(36),
    tag_code VARCHAR(20) NOT NULL COMMENT '維度主題領域代碼',
    tag_name VARCHAR(20) NOT NULL COMMENT '維度主題領域名稱',
    tag_type VARCHAR(6) NOT NULL COMMENT '分類標籤類型：BASE(基礎) / RULE(規則)',
    tag_description VARCHAR(200) COMMENT '維度主題領域簡述',
    is_disabled INT(1) DEFAULT 0 COMMENT '停用註記：0(不停用)/1(停用)',
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (tag_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='分類標籤主表';

CREATE INDEX metric_catalog_tag_idx01 ON metric_catalog_tag(tag_parent_id);

CREATE TABLE metric_feature (
    feature_id VARCHAR(36) NOT NULL,
    feature_label VARCHAR(255) NOT NULL COMMENT '特徵名稱',
    feature_value VARCHAR(255) NOT NULL COMMENT '特徵數值',
    is_disabled INT(1) DEFAULT 0 COMMENT '停用註記：0(不停用)/1(停用)',
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (feature_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='特徵標籤主表';

CREATE TABLE metric_feature_catalog (
    feature_id VARCHAR(36) NOT NULL,
    catalog_tag_id VARCHAR(36) NOT NULL,
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (feature_id , catalog_tag_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='特徵標籤與分類標籤關聯表';

CREATE TABLE metric_feature_relation (
    source_feature_id VARCHAR(36) NOT NULL,
    sink_feature_id VARCHAR(36) NOT NULL,
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間'
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='特徵標籤關係表';

CREATE INDEX metric_feature_relation_idx01 ON metric_feature_relation(source_feature_id);
CREATE INDEX metric_feature_relation_idx02 ON metric_feature_relation(sink_feature_id);

CREATE TABLE metric_field (
    field_id VARCHAR(36) NOT NULL COMMENT 'PK',
    field_name VARCHAR(120) NOT NULL COMMENT '維度欄位名稱',
    field_alias VARCHAR(50) NOT NULL COMMENT '維度欄位別名',
    field_type VARCHAR(20) NOT NULL COMMENT '維度欄位型態',
    field_length INT(11) COMMENT '維度欄位長度',
    field_default_value VARCHAR(20),
    field_description VARCHAR(200) COMMENT '維度欄位簡述',
    is_required INT(1) NOT NULL COMMENT '維度欄位是否為必要欄位',
    is_disabled INT(1) DEFAULT 0 COMMENT '停用註記：0(不停用)/1(停用)',
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (field_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='維度欄位資訊';

CREATE TABLE metric_field_catalog (
    field_id VARCHAR(36) NOT NULL,
    catalog_tag_id VARCHAR(36) NOT NULL,
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (field_id , catalog_tag_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='維度欄位與分類標籤關聯表';

CREATE TABLE metric_field_feature (
    field_id VARCHAR(36) NOT NULL,
    feature_id VARCHAR(36) NOT NULL,
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (field_id , feature_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='維度欄位與特徵標籤關聯表';

CREATE TABLE metric_field_relation (
    source_storage_id VARCHAR(36) NOT NULL,
    source_table_id VARCHAR(36) NOT NULL,
    source_field_id VARCHAR(36) NOT NULL,
    sink_storage_id VARCHAR(36) NOT NULL,
    sink_table_id VARCHAR(36) NOT NULL,
    sink_field_id VARCHAR(36) NOT NULL,
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間'
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='維度欄位關係表';

CREATE INDEX metric_field_relation_idx01 ON metric_field_relation(source_field_id);
CREATE INDEX metric_field_relation_idx02 ON metric_field_relation(sink_field_id);
CREATE INDEX metric_field_relation_idx03 ON metric_field_relation(source_table_id);
CREATE INDEX metric_field_relation_idx04 ON metric_field_relation(sink_table_id);
CREATE INDEX metric_field_relation_idx05 ON metric_field_relation(source_storage_id);
CREATE INDEX metric_field_relation_idx06 ON metric_field_relation(sink_storage_id);

CREATE TABLE metric_table (
    table_id VARCHAR(36) NOT NULL COMMENT 'PK',
    `table_name` VARCHAR(120) NOT NULL COMMENT '維度表名稱',
    table_alias VARCHAR(50) NOT NULL COMMENT '維度表別名',
    table_type VARCHAR(20) NOT NULL COMMENT '資料類型：TABLE(數據表)/DOC(文件)',
    table_format VARCHAR(20) NOT NULL COMMENT '表格式：TABLE(數據表)/JSON/CSV',
    table_description VARCHAR(200) COMMENT '維度表簡述',
    is_disabled INT(1) DEFAULT 0 COMMENT '停用註記：0(不停用)/1(停用)',
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (table_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='維度表資訊';

CREATE TABLE metric_table_field (
    storage_id VARCHAR(36) NOT NULL,
    table_id VARCHAR(36) NOT NULL,
    field_id VARCHAR(36) NOT NULL,
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (storage_id , table_id , field_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='維度表與維度欄位關聯表';

CREATE TABLE metric_table_relation (
    source_storage_id VARCHAR(36) NOT NULL,
    source_table_id VARCHAR(36) NOT NULL,
    sink_storage_id VARCHAR(36) NOT NULL,
    sink_table_id VARCHAR(36) NOT NULL,
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    crt_user_name VARCHAR(20),
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間'
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='維度表關係表';

CREATE INDEX metric_table_relation_idx01 ON metric_table_relation(source_table_id);
CREATE INDEX metric_table_relation_idx02 ON metric_table_relation(sink_table_id);
CREATE INDEX metric_table_relation_idx03 ON metric_table_relation(source_storage_id);
CREATE INDEX metric_table_relation_idx04 ON metric_table_relation(sink_table_id);

CREATE TABLE provider_account (
    account_id VARCHAR(36) NOT NULL COMMENT '企業帳號ID',
    account_name VARCHAR(255) COMMENT '企業名稱',
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (account_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='企業資料';

CREATE TABLE provider_user (
    provider_id VARCHAR(32) NOT NULL COMMENT 'PK',
    account_id VARCHAR(36) NOT NULL COMMENT '企業帳號ID',
    user_id VARCHAR(36) NOT NULL UNIQUE COMMENT '艾斯用戶唯一識別碼',
    user_name VARCHAR(255) COMMENT '用戶姓名',
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (provider_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='企業用戶主表';

CREATE INDEX provider_user_idx01 ON provider_user(user_id);
CREATE INDEX provider_user_idx02 ON provider_user(account_id);

CREATE TABLE storage_info (
    storage_id VARCHAR(36) NOT NULL COMMENT 'PK',
    storage_type VARCHAR(20) NOT NULL COMMENT '儲存庫類型：MYSQL/MONGO/S3/REDIS',
    storage_name VARCHAR(120) NOT NULL COMMENT '儲存庫名稱',
    storage_alias VARCHAR(50) NOT NULL COMMENT '儲存庫別名',
    storage_account VARCHAR(30) COMMENT '儲存庫登入帳號',
    storage_pwd VARCHAR(20) COMMENT '儲存庫登入密碼',
    storage_host TEXT COMMENT '儲存庫host',
    storage_port INT(11) COMMENT '儲存庫埠號',
    storage_url TEXT COMMENT '儲存庫URL位置',
    storage_description VARCHAR(200) COMMENT '儲存庫簡述',
    is_disabled INT(1) DEFAULT 0 COMMENT '停用註記：0(不停用)/1(停用)',
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (storage_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='數據來源資訊';

CREATE TABLE storage_metric_table (
    storage_id VARCHAR(36) NOT NULL,
    table_id VARCHAR(36) NOT NULL,
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (storage_id , table_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='數據來源與維度表關聯表';

CREATE TABLE storage_provider (
    storage_id VARCHAR(36) NOT NULL,
    account_id VARCHAR(36) NOT NULL COMMENT '企業帳戶PK',
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (storage_id , account_id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='企業與數據來源關聯表';

CREATE TABLE system_params_config (
    config_id VARCHAR(36) NOT NULL,
    config_parent_code varchar(36) comment '所屬上層編號，由 MD5(group_code, config_code) 組成',
    group_code VARCHAR(20) NOT NULL COMMENT '系統常數標籤群組代碼',
    config_code VARCHAR(20) NOT NULL COMMENT '系統常數標籤代碼',
    config_name VARCHAR(20) NOT NULL COMMENT '系統常數標籤名稱',
    is_disabled INT(1) DEFAULT 0 COMMENT '是否停用',
    config_description VARCHAR(100),
    crt_user_id VARCHAR(36) NOT NULL COMMENT '新增人員',
    crt_user_name VARCHAR(20),
    crt_date DATETIME(3) NOT NULL COMMENT '新增時間',
    mdy_user_id VARCHAR(36) NOT NULL COMMENT '異動人員',
    mdy_user_name VARCHAR(20),
    mdy_date DATETIME(3) NOT NULL COMMENT '異動時間',
    PRIMARY KEY (config_id),
    CONSTRAINT unique_code UNIQUE (config_code , group_code)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_UNICODE_520_CI COMMENT='系統常數標籤表';

CREATE INDEX system_params_config_idx01 ON system_params_config(group_code);
