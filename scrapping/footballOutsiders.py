import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tabulate import tabulate

import sys
sys.path.insert(0,'..')

from DOConn import connection
from DOsshTunnel import DOConnect





stat_dicts = []



## team offense

stat_dicts.append({'table_name' : 'fo_team_offense',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'rank', 'data_type' : 'integer'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'off_dvoa', 'data_type' : 'float'},
                       {'column_name' : 'last_year_rank', 'data_type' : 'integer'},
                       {'column_name' : 'wei_off', 'data_type' : 'float'},
                       {'column_name' : 'wei_rank', 'data_type' : 'integer'},
                       {'column_name' : 'pass_off', 'data_type' : 'float'},
                       {'column_name' : 'pass_rank', 'data_type' : 'integer'},
                       {'column_name' : 'rush_off', 'data_type' : 'float'},
                       {'column_name' : 'rush_rank', 'data_type' : 'integer'},
                       {'column_name' : 'nadj_total', 'data_type' : 'float'},
                       {'column_name' : 'nadj_pass', 'data_type' : 'float'},
                       {'column_name' : 'nadj_rush', 'data_type' : 'float'},
                       {'column_name' : 'var', 'data_type' : 'float'},
                       {'column_name' : 'var_rank', 'data_type' : 'integer'},
                       {'column_name' : 'sched', 'data_type' : 'float'},
                       {'column_name' : 'sched_rank', 'data_type' : 'integer'}
                       ],
                   'address' : 'teamoff', 'table_index' : 0,
                    'create_table' : True, 'drop_table' : True
                   })

## team defense
stat_dicts.append({'table_name' : 'fo_team_defense',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'rank', 'data_type' : 'integer'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'def_dvoa', 'data_type' : 'float'},
                       {'column_name' : 'last_year_rank', 'data_type' : 'integer'},
                       {'column_name' : 'wei_def', 'data_type' : 'float'},
                       {'column_name' : 'wei_rank', 'data_type' : 'integer'},
                       {'column_name' : 'pass_def', 'data_type' : 'float'},
                       {'column_name' : 'pass_rank', 'data_type' : 'integer'},
                       {'column_name' : 'rush_def', 'data_type' : 'float'},
                       {'column_name' : 'rush_rank', 'data_type' : 'integer'},
                       {'column_name' : 'nadj_total', 'data_type' : 'float'},
                       {'column_name' : 'nadj_pass', 'data_type' : 'float'},
                       {'column_name' : 'nadj_rush', 'data_type' : 'float'},
                       {'column_name' : 'var', 'data_type' : 'float'},
                       {'column_name' : 'var_rank', 'data_type' : 'integer'},
                       {'column_name' : 'sched', 'data_type' : 'float'},
                       {'column_name' : 'sched_rank', 'data_type' : 'integer'}
                       ],
                   'address' : 'teamdef', 'table_index' : 0,
                    'create_table' : True, 'drop_table' : True
                   })


## team defense wr type
stat_dicts.append({'table_name' : 'fo_team_defense_wrtype',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'rank', 'data_type' : 'integer'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'def_dvoa_wr1', 'data_type' : 'float'},
                       {'column_name' : 'rank_wr1', 'data_type' : 'integer'},
                       {'column_name' : 'pa_g_wr1', 'data_type' : 'float'},
                       {'column_name' : 'yd_g_wr1', 'data_type' : 'float'},
                       {'column_name' : 'def_dvoa_wr2', 'data_type' : 'float'},
                       {'column_name' : 'rank_wr2', 'data_type' : 'integer'},
                       {'column_name' : 'pa_g_wr2', 'data_type' : 'float'},
                       {'column_name' : 'yd_g_wr2', 'data_type' : 'float'},
                       {'column_name' : 'def_dvoa_wro', 'data_type' : 'float'},
                       {'column_name' : 'rank_wro', 'data_type' : 'integer'},
                       {'column_name' : 'pa_g_wro', 'data_type' : 'float'},
                       {'column_name' : 'yd_g_wro', 'data_type' : 'float'},
                       {'column_name' : 'def_dvoa_te', 'data_type' : 'float'},
                       {'column_name' : 'rank_te', 'data_type' : 'integer'},
                       {'column_name' : 'pa_g_te', 'data_type' : 'float'},
                       {'column_name' : 'yd_g_te', 'data_type' : 'float'},
                       {'column_name' : 'def_dvoa_rb', 'data_type' : 'float'},
                       {'column_name' : 'rank_rb', 'data_type' : 'integer'},
                       {'column_name' : 'pa_g_rb', 'data_type' : 'float'},
                       {'column_name' : 'yd_g_rb', 'data_type' : 'float'}
                       ],
                   'address' : 'teamdef', 'table_index' : 1,
                    'create_table' : True, 'drop_table' : True
                   })


## team st
stat_dicts.append({'table_name' : 'fo_team_st',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'rank', 'data_type' : 'integer'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'st_dvoa', 'data_type' : 'float'},
                       {'column_name' : 'last_year_rank', 'data_type' : 'integer'},
                       {'column_name' : 'weight_dvoa', 'data_type' : 'float'},
                       {'column_name' : 'weight_rank', 'data_type' : 'integer'},
                       {'column_name' : 'fg_xp', 'data_type' : 'float'},
                       {'column_name' : 'kick', 'data_type' : 'float'},
                       {'column_name' : 'kick_ret', 'data_type' : 'float'},
                       {'column_name' : 'punt', 'data_type' : 'float'},
                       {'column_name' : 'punt_ret', 'data_type' : 'float'},
                       {'column_name' : 'hidden_pts', 'data_type' : 'float'},
                       {'column_name' : 'hidden_rank', 'data_type' : 'integer'},
                       {'column_name' : 'weather_pts', 'data_type' : 'float'},
                       {'column_name' : 'weather_rank', 'data_type' : 'integer'},
                       {'column_name' : 'nadj_voa', 'data_type' : 'float'}
                       ],
                   'address' : 'teamst', 'table_index' : 0,
                    'create_table' : True, 'drop_table' : True
                   })


## quarter backs
stat_dicts.append({'table_name' : 'fo_qb',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'player', 'data_type' : 'text'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'dyar', 'data_type' : 'float'},
                       {'column_name' : 'dyar_rk', 'data_type' : 'integer'},
                       {'column_name' : 'yar', 'data_type' : 'float'},
                       {'column_name' : 'yar_rk', 'data_type' : 'integer'},
                       {'column_name' : 'dvoa', 'data_type' : 'float'},
                       {'column_name' : 'dvoa_rk', 'data_type' : 'integer'},
                       {'column_name' : 'voa', 'data_type' : 'float'},
                       {'column_name' : 'qbr', 'data_type' : 'float'},
                       {'column_name' : 'qbr_rk', 'data_type' : 'integer'},
                       {'column_name' : 'pass', 'data_type' : 'integer'},
                       {'column_name' : 'yards', 'data_type' : 'integer'},
                       {'column_name' : 'eyds', 'data_type' : 'integer'},
                       {'column_name' : 'td', 'data_type' : 'integer'},
                       {'column_name' : 'fk', 'data_type' : 'integer'},
                       {'column_name' : 'fl', 'data_type' : 'integer'},
                       {'column_name' : 'intThrown', 'data_type' : 'integer'},
                       {'column_name' : 'c_perct', 'data_type' : 'float'},
                       {'column_name' : 'dpi', 'data_type' : 'text'},
                       {'column_name' : 'alex', 'data_type' : 'float'}
                       ],
                   'address' : 'qb', 'table_index' : 0,
                    'create_table' : True, 'drop_table' : True
                   })


## quarter backs other
stat_dicts.append({'table_name' : 'fo_qb_other',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'player', 'data_type' : 'text'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'dyar', 'data_type' : 'float'},
                       {'column_name' : 'yar', 'data_type' : 'float'},
                       {'column_name' : 'dvoa', 'data_type' : 'float'},
                       {'column_name' : 'voa', 'data_type' : 'float'},
                       {'column_name' : 'qbr', 'data_type' : 'float'},
                       {'column_name' : 'pass', 'data_type' : 'integer'},
                       {'column_name' : 'yards', 'data_type' : 'integer'},
                       {'column_name' : 'eyds', 'data_type' : 'integer'},
                       {'column_name' : 'td', 'data_type' : 'integer'},
                       {'column_name' : 'fk', 'data_type' : 'integer'},
                       {'column_name' : 'fl', 'data_type' : 'integer'},
                       {'column_name' : 'intThrown', 'data_type' : 'integer'},
                       {'column_name' : 'c_perct', 'data_type' : 'float'},
                       {'column_name' : 'dpi', 'data_type' : 'text'},
                       {'column_name' : 'alex', 'data_type' : 'float'}
                       ],
                   'address' : 'qb', 'table_index' : 1,
                    'create_table' : True, 'drop_table' : True
                   })

## quarter backs rush
stat_dicts.append({'table_name' : 'fo_qb_rush',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'player', 'data_type' : 'text'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'dyar', 'data_type' : 'float'},
                       {'column_name' : 'dyar_rk', 'data_type' : 'integer'},
                       {'column_name' : 'yar', 'data_type' : 'float'},
                       {'column_name' : 'yar_rk', 'data_type' : 'integer'},
                       {'column_name' : 'dvoa', 'data_type' : 'float'},
                       {'column_name' : 'dvoa_rk', 'data_type' : 'integer'},
                       {'column_name' : 'voa', 'data_type' : 'float'},
                       {'column_name' : 'runs', 'data_type' : 'integer'},
                       {'column_name' : 'yards', 'data_type' : 'integer'},
                       {'column_name' : 'eyds', 'data_type' : 'integer'},
                       {'column_name' : 'td', 'data_type' : 'integer'},
                       {'column_name' : 'fum', 'data_type' : 'integer'}
                       ],
                   'address' : 'qb', 'table_index' : 2,
                    'create_table' : True, 'drop_table' : True
                   })

## running backs rush
stat_dicts.append({'table_name' : 'fo_rb_rush',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'player', 'data_type' : 'text'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'dyar', 'data_type' : 'float'},
                       {'column_name' : 'dyar_rk', 'data_type' : 'integer'},
                       {'column_name' : 'yar', 'data_type' : 'float'},
                       {'column_name' : 'yar_rk', 'data_type' : 'integer'},
                       {'column_name' : 'dvoa', 'data_type' : 'float'},
                       {'column_name' : 'dvoa_rk', 'data_type' : 'integer'},
                       {'column_name' : 'voa', 'data_type' : 'float'},
                       {'column_name' : 'runs', 'data_type' : 'integer'},
                       {'column_name' : 'yards', 'data_type' : 'integer'},
                       {'column_name' : 'eyds', 'data_type' : 'integer'},
                       {'column_name' : 'td', 'data_type' : 'integer'},
                       {'column_name' : 'fum', 'data_type' : 'integer'},
                       {'column_name' : 'suc_rate', 'data_type' : 'float'},
                       {'column_name' : 'rk', 'data_type' : 'integer'}
                       ],
                   'address' : 'rb', 'table_index' : 0,
                    'create_table' : True, 'drop_table' : True
                   })

## running backs receiv
stat_dicts.append({'table_name' : 'fo_rb_receiv',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'player', 'data_type' : 'text'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'dyar', 'data_type' : 'float'},
                       {'column_name' : 'dyar_rk', 'data_type' : 'integer'},
                       {'column_name' : 'yar', 'data_type' : 'float'},
                       {'column_name' : 'yar_rk', 'data_type' : 'integer'},
                       {'column_name' : 'dvoa', 'data_type' : 'float'},
                       {'column_name' : 'dvoa_rk', 'data_type' : 'integer'},
                       {'column_name' : 'voa', 'data_type' : 'float'},
                       {'column_name' : 'passes', 'data_type' : 'integer'},
                       {'column_name' : 'yards', 'data_type' : 'integer'},
                       {'column_name' : 'eyds', 'data_type' : 'integer'},
                       {'column_name' : 'td', 'data_type' : 'integer'},
                       {'column_name' : 'catch_rt', 'data_type' : 'float'},
                       {'column_name' : 'fum', 'data_type' : 'integer'}
                       ],
                   'address' : 'rb', 'table_index' : 2,
                    'create_table' : True, 'drop_table' : True
                   })


## running backs rush other
stat_dicts.append({'table_name' : 'fo_rb_rush_other',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'player', 'data_type' : 'text'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'dyar', 'data_type' : 'float'},
                       {'column_name' : 'yar', 'data_type' : 'float'},
                       {'column_name' : 'dvoa', 'data_type' : 'float'},
                       {'column_name' : 'voa', 'data_type' : 'float'},
                       {'column_name' : 'runs', 'data_type' : 'integer'},
                       {'column_name' : 'yards', 'data_type' : 'integer'},
                       {'column_name' : 'eyds', 'data_type' : 'integer'},
                       {'column_name' : 'td', 'data_type' : 'integer'},
                       {'column_name' : 'fum', 'data_type' : 'integer'}
                       ],
                   'address' : 'rb', 'table_index' : 1,
                    'create_table' : True, 'drop_table' : True
                   })

## running backs receiv other
stat_dicts.append({'table_name' : 'fo_rb_receiv_other',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'player', 'data_type' : 'text'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'dyar', 'data_type' : 'float'},
                       {'column_name' : 'yar', 'data_type' : 'float'},
                       {'column_name' : 'dvoa', 'data_type' : 'float'},
                       {'column_name' : 'voa', 'data_type' : 'float'},
                       {'column_name' : 'passes', 'data_type' : 'integer'},
                       {'column_name' : 'yards', 'data_type' : 'integer'},
                       {'column_name' : 'eyds', 'data_type' : 'integer'},
                       {'column_name' : 'td', 'data_type' : 'integer'},
                       {'column_name' : 'catch_rt', 'data_type' : 'float'},
                       {'column_name' : 'fum', 'data_type' : 'integer'}
                       ],
                   'address' : 'rb', 'table_index' : 3,
                    'create_table' : True, 'drop_table' : True
                   })

## te
stat_dicts.append({'table_name' : 'fo_te',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'player', 'data_type' : 'text'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'dyar', 'data_type' : 'float'},
                       {'column_name' : 'dyar_rk', 'data_type' : 'integer'},
                       {'column_name' : 'yar', 'data_type' : 'float'},
                       {'column_name' : 'yar_rk', 'data_type' : 'integer'},
                       {'column_name' : 'dvoa', 'data_type' : 'float'},
                       {'column_name' : 'dvoa_rk', 'data_type' : 'integer'},
                       {'column_name' : 'voa', 'data_type' : 'float'},
                       {'column_name' : 'passes', 'data_type' : 'integer'},
                       {'column_name' : 'yards', 'data_type' : 'integer'},
                       {'column_name' : 'eyds', 'data_type' : 'integer'},
                       {'column_name' : 'td', 'data_type' : 'integer'},
                       {'column_name' : 'catch_rt', 'data_type' : 'float'},
                       {'column_name' : 'fum', 'data_type' : 'integer'},
                       {'column_name' : 'dpi', 'data_type' : 'text'}
                       ],
                   'address' : 'te', 'table_index' : 0,
                    'create_table' : True, 'drop_table' : True
                   })

## wide receivers
stat_dicts.append({'table_name' : 'fo_wr',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'player', 'data_type' : 'text'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'dyar', 'data_type' : 'float'},
                       {'column_name' : 'dyar_rk', 'data_type' : 'integer'},
                       {'column_name' : 'yar', 'data_type' : 'float'},
                       {'column_name' : 'yar_rk', 'data_type' : 'integer'},
                       {'column_name' : 'dvoa', 'data_type' : 'float'},
                       {'column_name' : 'dvoa_rk', 'data_type' : 'integer'},
                       {'column_name' : 'voa', 'data_type' : 'float'},
                       {'column_name' : 'passes', 'data_type' : 'integer'},
                       {'column_name' : 'yards', 'data_type' : 'integer'},
                       {'column_name' : 'eyds', 'data_type' : 'integer'},
                       {'column_name' : 'td', 'data_type' : 'integer'},
                       {'column_name' : 'catch_rt', 'data_type' : 'float'},
                       {'column_name' : 'fum', 'data_type' : 'integer'},
                       {'column_name' : 'dpi', 'data_type' : 'text'}
                       ],
                   'address' : 'wr', 'table_index' : 0,
                    'create_table' : True, 'drop_table' : True
                   })

## te other
stat_dicts.append({'table_name' : 'fo_te_other',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'player', 'data_type' : 'text'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'dyar', 'data_type' : 'float'},
                       {'column_name' : 'yar', 'data_type' : 'float'},
                       {'column_name' : 'dvoa', 'data_type' : 'float'},
                       {'column_name' : 'voa', 'data_type' : 'float'},
                       {'column_name' : 'passes', 'data_type' : 'integer'},
                       {'column_name' : 'yards', 'data_type' : 'integer'},
                       {'column_name' : 'eyds', 'data_type' : 'integer'},
                       {'column_name' : 'td', 'data_type' : 'integer'},
                       {'column_name' : 'catch_rt', 'data_type' : 'float'},
                       {'column_name' : 'fum', 'data_type' : 'integer'},
                       {'column_name' : 'dpi', 'data_type' : 'text'}
                       ],
                   'address' : 'te', 'table_index' : 1,
                    'create_table' : True, 'drop_table' : True
                   })

## wide receivers other
stat_dicts.append({'table_name' : 'fo_wr_other',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'player', 'data_type' : 'text'},
                       {'column_name' : 'team', 'data_type' : 'text'},
                       {'column_name' : 'dyar', 'data_type' : 'float'},
                       {'column_name' : 'yar', 'data_type' : 'float'},
                       {'column_name' : 'dvoa', 'data_type' : 'float'},
                       {'column_name' : 'voa', 'data_type' : 'float'},
                       {'column_name' : 'passes', 'data_type' : 'integer'},
                       {'column_name' : 'yards', 'data_type' : 'integer'},
                       {'column_name' : 'eyds', 'data_type' : 'integer'},
                       {'column_name' : 'td', 'data_type' : 'integer'},
                       {'column_name' : 'catch_rt', 'data_type' : 'float'},
                       {'column_name' : 'fum', 'data_type' : 'integer'},
                       {'column_name' : 'dpi', 'data_type' : 'text'}
                       ],
                   'address' : 'wr', 'table_index' : 1,
                    'create_table' : True, 'drop_table' : True
                   })

## offensive line
stat_dicts.append({'table_name' : 'fo_ol',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'rn_rank', 'data_type' : 'integer'},
                       {'column_name' : 'rn_team', 'data_type' : 'text'},
                       {'column_name' : 'adj_line_yards', 'data_type' : 'float'},
                       {'column_name' : 'rb_yards', 'data_type' : 'float'},
                       {'column_name' : 'pow_succ', 'data_type' : 'float'},
                       {'column_name' : 'pow_rk', 'data_type' : 'integer'},
                       {'column_name' : 'stuff', 'data_type' : 'float'},
                       {'column_name' : 'stuff_rk', 'data_type' : 'integer'},
                       {'column_name' : 'sec_lvl_yards', 'data_type' : 'float'},
                       {'column_name' : 'sec_lvl_rk', 'data_type' : 'integer'},
                       {'column_name' : 'open_fld_yards', 'data_type' : 'float'},
                       {'column_name' : 'open_field_rank', 'data_type' : 'integer'},
                       {'column_name' : 'ps_team', 'data_type' : 'text'},
                       {'column_name' : 'ps_rank', 'data_type' : 'integer'},
                       {'column_name' : 'sacks', 'data_type' : 'integer'},
                       {'column_name' : 'adj_sack_rate', 'data_type' : 'float'}
                       ],
                   'address' : 'ol', 'table_index' : 0,
                    'create_table' : True, 'drop_table' : True
                   })

## defensive line
stat_dicts.append({'table_name' : 'fo_dl',
                   'columns' : [
                       {'column_name' : 'data_year', 'data_type' : 'integer'},
                       {'column_name' : 'data_week', 'data_type' : 'integer'},
                       {'column_name' : 'rn_rank', 'data_type' : 'integer'},
                       {'column_name' : 'rn_team', 'data_type' : 'text'},
                       {'column_name' : 'adj_line_yards', 'data_type' : 'float'},
                       {'column_name' : 'rb_yards', 'data_type' : 'float'},
                       {'column_name' : 'pow_succ', 'data_type' : 'float'},
                       {'column_name' : 'pow_rk', 'data_type' : 'integer'},
                       {'column_name' : 'stuff', 'data_type' : 'float'},
                       {'column_name' : 'stuff_rk', 'data_type' : 'integer'},
                       {'column_name' : 'sec_lvl_yards', 'data_type' : 'float'},
                       {'column_name' : 'sec_lvl_rk', 'data_type' : 'integer'},
                       {'column_name' : 'open_fld_yards', 'data_type' : 'float'},
                       {'column_name' : 'open_field_rank', 'data_type' : 'integer'},
                       {'column_name' : 'ps_team', 'data_type' : 'text'},
                       {'column_name' : 'ps_rank', 'data_type' : 'integer'},
                       {'column_name' : 'sacks', 'data_type' : 'integer'},
                       {'column_name' : 'adj_sack_rate', 'data_type' : 'float'}
                       ],
                   'address' : 'dl', 'table_index' : 0,
                    'create_table' : True, 'drop_table' : True
                   })


with DOConnect() as tunnel:
    c, conn = connection(tunnel)


    for sql_table in stat_dicts:

        if sql_table['drop_table'] == True:
            c.execute('drop table if exists scrapped_data.%s' % sql_table['table_name'])
            conn.commit()

        if sql_table['create_table'] == True:
            create_statement = "create table scrapped_data.%s (" % sql_table['table_name']
            create_statement += sql_table['columns'][0]['column_name']
            create_statement += ' '
            create_statement += sql_table['columns'][0]['data_type']
            for column in sql_table['columns'][1:]:
                create_statement += ', '
                create_statement += column['column_name']
                create_statement += ' '
                create_statement += column['data_type']
            create_statement += ', dataCreate datetime)'
            c.execute(create_statement)
            conn.commit()

        

        yearRange = range(2010,2018)
        for year in yearRange:
            url = 'http://www.footballoutsiders.com/stats/'

            url2 = url + sql_table['address']
            
            if year != 2017:
                url2 += str(year)

            req = requests.get(url2)

            xml = bs(req.text,'lxml')

            
            table = xml.find_all('table')[sql_table['table_index']]
            sql_statement = "INSERT INTO scrapped_data." + sql_table['table_name'] + " (%s) values "
            for row in table.find_all('tr'):
                if len(row.find_all('td')) > 0:
                    if row.find_all('td')[0].get_text() not in ('','Rk','x','Player','RUN BLOCKING'):
                        row_data = []
                        row_data.append(year)
                        row_data.append(17)
                        for cell in row.find_all('td'):
                            row_data.append(cell.get_text())
                        sql_statement += "("
                        columnStat = ""
                        for i, cell in enumerate(row_data):
                            columnStat += sql_table['columns'][i]['column_name']
                            columnStat += ","
                            if '%' in str(cell):
                                cell = cell.replace("%","")
                                cell = float(cell)/100
                            cell = str(cell).replace(",","").replace("'","_")
                            sql_statement += "'" + str(cell) +  "', "
                        sql_statement += " current_timestamp()),"
            columnStat += "dataCreate"
            sql_statement = sql_statement[:-1]
            sql_statement = sql_statement % columnStat
            try:
                c.execute(sql_statement)
            except Exception as e:
                print(str(e))
                print(sql_statement)
            conn.commit()
            print("year: "+str(year)+" table: "+sql_table['table_name'])

             


            

conn.close()


