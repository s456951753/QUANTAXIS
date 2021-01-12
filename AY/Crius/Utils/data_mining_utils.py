import AY.Crius.Utils.trading_calendar_utils as calendar_util
import pandas as pd
from QUANTAXIS.QAUtil import DATABASE

CASH_FLOW_TYPE_NAME = 'cash_flow'
BALANCE_SHEET_TYPE_NAME = 'balance_sheet'
FINACIAL_INDICATOR_TYPE_NAME = 'finacial_indicator'


def get_latest_daily_basic_table(mongoDB=DATABASE.daily_basic_tushare):
    trade_date = calendar_util.get_last_x_trading_day_from_mongodb(1)
    cursor = mongoDB.find({'trade_date': str(trade_date)})
    df = pd.DataFrame(list(cursor))

    return df


def get_latest_finacial_indicator_table(mongoDB=DATABASE.finacial_indicator):
    pipeline = [
        {
            '$project': {
                'ts_code': 1,
                'ann_date': 1,
            }
        }, {
            '$group': {
                '_id': '$ts_code',
                'date': {
                    '$max': '$ann_date'
                }
            }
        }
    ]
    df = pd.DataFrame()
    for a in mongoDB.aggregate(pipeline):
        b = mongoDB.find_one({'ts_code': a['_id'], 'ann_date': a['date']})
        df = df.append(b, ignore_index=True)
    return df


def get_latest_balance_sheet_table(mongoDB=DATABASE.balance_sheet):
    pipeline = [
        {
            '$project': {
                'ts_code': 1,
                'f_ann_date': 1,
            }
        }, {
            '$group': {
                '_id': '$ts_code',
                'date': {
                    '$max': '$f_ann_date'
                }
            }
        }
    ]
    df = pd.DataFrame()
    for a in mongoDB.aggregate(pipeline):
        b = mongoDB.find({'ts_code': a['_id'], 'f_ann_date': a['date']})
        for c in b:
            df = df.append(c, ignore_index=True)
    return df


def get_latest_cash_flow_table(mongoDB=DATABASE.cash_flow):
    pipeline = [
        {
            '$project': {
                'ts_code': 1,
                'f_ann_date': 1,
            }
        }, {
            '$group': {
                '_id': '$ts_code',
                'date': {
                    '$max': '$f_ann_date'
                }
            }
        }
    ]
    df = pd.DataFrame()
    for a in mongoDB.aggregate(pipeline):
        b = mongoDB.find({'ts_code': a['_id'], 'f_ann_date': a['date']})
        for c in b:
            df = df.append(c, ignore_index=True)
    return df


def get_stock_list(mongoDB=DATABASE.stock_list, version='crius'):
    df = pd.DataFrame(list(mongoDB.find()))
    if (version == 'crius'):
        return df
    df = df.assign(ts_code=lambda x: x.code + '.' + x.sse)
    df['ts_code'] = df['ts_code'].str.upper()
    return df


def rename_adding_suffix_with_exceptions(df, suffix, exception_column_name):
    return df.rename(columns=lambda x: x + suffix if x != exception_column_name else x)


def add_necessary_data(start_date=None, mongoDB=DATABASE, auto_detect=False):
    import QUANTAXIS.QASU.save_tushare as st

    # drop and rebuild
    __coll_stock_list = mongoDB.stock_list
    __coll_trade_date = mongoDB.trade_date

    # append daily
    __coll_daily_basic = mongoDB.daily_basic

    # report like tables
    __coll_balance_sheet = mongoDB.balance_sheet
    __coll_finance_indicator = mongoDB.finance_inicator
    __coll_cash_flow = mongoDB.cash_flow

    # initially adding all data
    if (start_date is None):
        st.QA_SU_save_trade_date_all()
        st.QA_SU_save_stock_list('tushare')
