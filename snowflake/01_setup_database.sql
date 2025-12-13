-- Use default role
USE ROLE ACCOUNTADMIN;

-- Create warehouse (compute)
CREATE WAREHOUSE IF NOT EXISTS DEV_WH 
  WITH 
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Development warehouse for IPL Analytics';

-- Create database
CREATE DATABASE IF NOT EXISTS IPL_ANALYTICS
  COMMENT = 'IPL Cricket Analytics Database';

-- Create schemas
CREATE SCHEMA IF NOT EXISTS IPL_ANALYTICS.RAW
  COMMENT = 'Raw data layer - direct from source files';

CREATE SCHEMA IF NOT EXISTS IPL_ANALYTICS.STAGING
  COMMENT = 'Staging layer - cleaned and validated data';

CREATE SCHEMA IF NOT EXISTS IPL_ANALYTICS.ANALYTICS
  COMMENT = 'Analytics layer - business logic and aggregations';

-- Set context
USE WAREHOUSE DEV_WH;
USE DATABASE IPL_ANALYTICS;
USE SCHEMA RAW;

-- Verify setup
SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE();