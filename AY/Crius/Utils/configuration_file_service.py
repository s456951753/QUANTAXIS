from configparser import ConfigParser

TOKEN_SECTION_NAME = "TOKENS"
TS_TOKEN_NAME = "ts_token"

GMAIL_SECTION_NAME = "GMAIL"
GM_ACCOUNT_NAME = "gmail_acct"
GM_PASSWORD_NAME = "gmail_password"
GM_SERVER_DNS_NAME = "gmail_server"
GM_SERVER_SSL_SMTP_PORT_NAME = "gmail_port"

DEFAULT_DATABASE_SECTION_NAME = "DEFAULT_DATABASE"
DATABASE_HOST_NAME = "db_host"
DATABASE_PORT = "db_port"
DATABASE_DB_NAME = "db_name"
DATABASE_USER_NAME = "db_user"
DATABASE_PASSWORD = "db_pw"

DATA_CONFIG_SECTION_NAME = "DATA_CONFIG"
DATA_CONFIG_YEAR_GRANULARITY_NAME = "year"

QUANTAXIS_RUNTIME_CONFIG_SECTION_NAME = "QUANTAXIS_RUNTIME_CONFIG"
HIGHROA_LOWPE_LIST_SIZE_NAME = "year"
TEXT_PART_OF_EMAIL = "Crius Data Analysis Report"

config = ConfigParser()
config.read("../crius.properties")


def getProperty(section_name, property_name):
    if (config.has_option(section_name, property_name)):
        return config[section_name][property_name]
    else:
        return None


def getDefaultDB():
    db_name = getProperty(DEFAULT_DATABASE_SECTION_NAME, DATABASE_DB_NAME)
    db_host = getProperty(DEFAULT_DATABASE_SECTION_NAME, DATABASE_HOST_NAME)
    db_user = getProperty(DEFAULT_DATABASE_SECTION_NAME, DATABASE_USER_NAME)
    db_pw = getProperty(DEFAULT_DATABASE_SECTION_NAME, DATABASE_PASSWORD)
    return 'mysql:/' + '/' + db_user + ':' + db_pw + '@' + db_host + '/' + db_name + '?' + 'charset=utf8mb4'

def getDefaultDB_cursor_host():
    db_host = getProperty(DEFAULT_DATABASE_SECTION_NAME, DATABASE_HOST_NAME)
    return db_host

def getDefaultDB_cursor_user():
    db_user = getProperty(DEFAULT_DATABASE_SECTION_NAME, DATABASE_USER_NAME)
    return db_user

def getDefaultDB_cursor_passwd():
    db_pw = getProperty(DEFAULT_DATABASE_SECTION_NAME, DATABASE_PASSWORD)
    return db_pw

def getDefaultDB_cursor_database():
    db_name = getProperty(DEFAULT_DATABASE_SECTION_NAME, DATABASE_DB_NAME)
    return db_name
