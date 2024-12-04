drop database if exists cbtrade;
create database cbtrade;


SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

drop user cbtrade@localhost;
CREATE USER cbtrade@localhost IDENTIFIED BY 'cbtrade';
GRANT ALL PRIVILEGES ON cbtrade.* TO 'cbtrade'@'localhost';

use cbtrade;
drop schema if exists cbtrade;
create schema cbtrade default character set utf8mb4;


use cbtrade;
drop table if exists currs;
create table currs(
	curr_id                                       int(11) primary key AUTO_INCREMENT comment 'pk for currs table'
	, symb                                        varchar(64)
	, name                                        varchar(64)
	, curr_uuid                                   varchar(64)
	, prc_usd                                     decimal(36,12) default 0

	, create_dttm                                 timestamp
	, update_dttm                                 timestamp
	, delete_dttm                                 timestamp

	, ignore_tf                                   tinyint default 0
	, note1                                       varchar(1024)
	, note2                                       varchar(1024)
	, note3                                       varchar(1024)
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
	, unique(curr_uuid)
	);


use cbtrade;
drop table if exists bals;
create table bals(
	  bal_id                                      int(11) primary key AUTO_INCREMENT comment 'pk for bals table'

	, curr_uuid                                   varchar(64)
	, symb                                        varchar(64)
	, name                                        varchar(64)

	, bal_avail                                   decimal(36,12) default 0
	, bal_hold                                    decimal(36,12) default 0
	, bal_tot                                     decimal(36,12) default 0

	, rp_id                                       varchar(64)
	, default_tf                                  tinyint default 0
	, active_tf                                   tinyint default 0
	, ready_tf                                    tinyint default 0

	, create_dttm                                 timestamp
	, update_dttm                                 timestamp
	, delete_dttm                                 timestamp

	, curr_prc_usd                                decimal(36,12) default 0
	, curr_val_usd                                decimal(36,12) default 0

	, ignore_tf                                   tinyint default 0
	, note1                                       varchar(1024)
	, note2                                       varchar(1024)
	, note3                                       varchar(1024)
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, del_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
	, unique(curr_uuid)
	);


use cbtrade;
drop table if exists ohlcv_prod_id_freqs;
create table if not exists ohlcv_prod_id_freqs(
    prod_id           varchar(64) 
  , freq              varchar(64) 
  , last_upd_dttm     timestamp default current_timestamp 
  , dlm               timestamp default current_timestamp on update current_timestamp 
  );


use cbtrade;
drop table if exists buy_ords;
create table buy_ords(
	bo_id                                         int(11) primary key AUTO_INCREMENT
	, test_tf                                     tinyint        default 0
	, test_txn_yn                                 char(1)        default 'N'

	, prod_id                                     varchar(64)
	, mkt_name                                    varchar(64)
	, mkt_venue                                   varchar(64)

	, buy_order_uuid                              varchar(64)
	, buy_client_order_id                         varchar(64)

	, pos_type                                    varchar(64)
	, ord_stat                                    varchar(64)

	, buy_strat_type                              varchar(64)
	, buy_strat_name                              varchar(64)
	, buy_strat_freq                              varchar(64)
	, buy_asset_type                              varchar(64)

	, buy_begin_dttm                              timestamp default current_timestamp
	, buy_end_dttm                                timestamp

	, buy_curr_symb                               varchar(64)
	, spend_curr_symb                             varchar(64)
	, fees_curr_symb                              varchar(64)
	, buy_cnt_est                                 decimal(36,12) default 0
	, buy_cnt_act                                 decimal(36,12) default 0
	, fees_cnt_act                                decimal(36,12) default 0
	, tot_out_cnt                                 decimal(36,12) default 0

	, prc_buy_est                                 decimal(36,12) default 0
	, prc_buy_act                                 decimal(36,12) default 0
	, tot_prc_buy                                 decimal(36,12) default 0
	, prc_buy_slip_pct                            decimal(36,12) default 0

	, ignore_tf                                   tinyint default 0
	, reason                                      varchar(1024)
	, note1                                       varchar(1024)
	, note2                                       varchar(1024)
	, note3                                       varchar(1024)
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
	, unique(buy_order_uuid, buy_client_order_id, prod_id)
	);


/*

alter table cbtrade.buy_ords add column test_txn_yn char(1) default 'N' after test_tf;
update cbtrade.buy_ords set test_txn_yn = 'Y' where test_tf = 1;
update cbtrade.buy_ords set test_txn_yn = 'N' where test_tf = 0;


alter table cbtrade.buy_ords modify column reason varchar(1024);
alter table cbtrade.buy_ords add column reason varchar(64) after ignore_tf;
alter table cbtrade.buy_ords add column symb varchar(64) after test_tf;
update cbtrade.buy_ords set symb = 'USDC';
ALTER TABLE cbtrade.buy_ords ADD CONSTRAINT unique_buy_order UNIQUE (buy_order_uuid, buy_client_order_id, prod_id);
ALTER TABLE cbtrade.buy_ords drop index buy_order_uuid;
*/



use cbtrade;
drop table if exists buy_signals;
create table buy_signals(
	sid                                           int(11) primary key AUTO_INCREMENT
	, test_tf                                     tinyint default 0
	, test_txn_yn                                 char(1)        default 'N'
	, prod_id                                     varchar(64)
	, buy_strat_type                              varchar(64)
	, buy_strat_name                              varchar(64)
	, buy_strat_freq                              varchar(64)
	, buy_yn                                      char(1)
	, buy_deny_yn                                 char(1)
	, wait_yn                                     char(1)
	, actv_dttm                                   timestamp default current_timestamp
	, note1                                       varchar(1024)
	, note2                                       varchar(1024)
	, note3                                       varchar(1024)
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
	);



alter table cbtrade.buy_signals add column test_txn_yn char(1) default 'N' after test_tf;
update cbtrade.buy_signals set test_txn_yn = 'Y' where test_tf = 1;
update cbtrade.buy_signals set test_txn_yn = 'N' where test_tf = 0;


use cbtrade;
drop table if exists buy_signs;
create table buy_signs(
	bs_id                                         int(11) primary key AUTO_INCREMENT
	, test_tf                                     tinyint        default 0
	, test_txn_yn                                 char(1)        default 'N'
	, prod_id                                     varchar(64)
	, buy_strat_type                              varchar(64)
	, buy_strat_name                              varchar(64)
	, buy_strat_freq                              varchar(64)
	, buy_yn                                      char(1)
	, wait_yn                                     char(1)
	, bs_dttm                                     timestamp default current_timestamp
	, buy_curr_symb                               varchar(64)
	, spend_curr_symb                             varchar(64)
	, fees_curr_symb                              varchar(64)
	, buy_cnt_est                                 decimal(36,12) default 0
	, buy_prc_est                                 decimal(36,12) default 0
	, buy_sub_tot_est                             decimal(36,12) default 0
	, buy_fees_est                                decimal(36,12) default 0
	, buy_tot_est                                 decimal(36,12) default 0
	, all_passes                                  varchar(2048)
	, all_fails                                   varchar(2048)
	, ignore_tf                                   tinyint default 0
	, note1                                       varchar(1024)
	, note2                                       varchar(1024)
	, note3                                       varchar(1024)
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
--	, prod_id                                     varchar(64)
--	, mkt_name                                    varchar(64)
--	, mkt_venue                                   varchar(64)
--	, buy_order_uuid                              varchar(64)
--	, buy_client_order_id                         varchar(64)
--	, pos_type                                    varchar(64)
--	, ord_stat                                    varchar(64)
--	, buy_strat_type                              varchar(64)
--	, buy_strat_name                              varchar(64)
--	, buy_strat_freq                              varchar(64)
--	, buy_asset_type                              varchar(64)
--	, buy_begin_dttm                              timestamp default current_timestamp
--	, buy_end_dttm                                timestamp
--	, buy_cnt_act                                 decimal(36,12) default 0
--	, fees_cnt_act                                decimal(36,12) default 0
--	, tot_out_cnt                                 decimal(36,12) default 0
--	, prc_buy_act                                 decimal(36,12) default 0
--	, prc_buy_slip_pct                            decimal(36,12) default 0
	, unique(prod_id, buy_strat_type, buy_strat_name, buy_strat_freq, bs_dttm)
	);


alter table cbtrade.buy_signs add column test_txn_yn char(1) default 'N' after test_tf;
update cbtrade.buy_signs set test_txn_yn = 'Y' where test_tf = 1;
update cbtrade.buy_signs set test_txn_yn = 'N' where test_tf = 0;



use cbtrade;
drop table if exists buy_strats;
create table buy_strats(
	bs_id                                         int(11) primary key AUTO_INCREMENT comment 'pk for buy_strats table'
	, buy_strat_type                              varchar(64)
	, buy_strat_name                              varchar(64)
	, buy_strat_desc                              varchar(64)
	, ignore_tf                                   tinyint default 0
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
	);
insert into cbtrade.buy_strats (buy_strat_type, buy_strat_name, buy_strat_desc, ignore_tf) values ('up', 'sha', 'double smoothed heikin ashi', 0);
insert into cbtrade.buy_strats (buy_strat_type, buy_strat_name, buy_strat_desc, ignore_tf) values ('up', 'imp_macd', 'impulse macd', 0);
insert into cbtrade.buy_strats (buy_strat_type, buy_strat_name, buy_strat_desc, ignore_tf) values ('up', 'bb_bo', 'bollinger band breakout', 0);
-- insert into cbtrade.buy_strats (buy_strat_type, buy_strat_name, buy_strat_desc, ignore_tf) values ('up', 'emax', 'triple ema crossover', 0);
insert into cbtrade.buy_strats (buy_strat_type, buy_strat_name, buy_strat_desc, ignore_tf) values ('dn', 'bb', 'bollinger band', 0);
insert into cbtrade.buy_strats (buy_strat_type, buy_strat_name, buy_strat_desc, ignore_tf) values ('dn', 'drop', 'buy the dip', 0);

-- insert into cbtrade.buy_strats (buy_strat_type, buy_strat_name, buy_strat_desc, ignore_tf) values ('up', 'nwe', 'Nadaraya Watson Estimator', 0);
insert into cbtrade.buy_strats (buy_strat_type, buy_strat_name, buy_strat_desc, ignore_tf) values ('up', 'nwe_3row', 'nwe 3 in a row', 0);
insert into cbtrade.buy_strats (buy_strat_type, buy_strat_name, buy_strat_desc, ignore_tf) values ('dn', 'nwe_env', 'nwe envelope', 0);
insert into cbtrade.buy_strats (buy_strat_type, buy_strat_name, buy_strat_desc, ignore_tf) values ('dn', 'nwe_rev', 'nwe reversal', 0);

/*
delete from cbtrade.buy_strats where buy_strat_name not in ('nwe_3row','nwe_env','nwe_rev')
*/


use cbtrade;
drop table if exists force_buy;
create table force_buy(
	fb_id                                         int(11) primary key AUTO_INCREMENT comment 'pk for currs table'
	, prod_id                                     varchar(64)
	, base_symb                                   varchar(64)
	, quote_symb                                  varchar(64)
	, buy_amt                                     decimal(36,12) default 0
	, spend_amt                                   decimal(36,12) default 0
	, done_tf                                     tinyint default 0
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
	);


use cbtrade;
drop table if exists freqs;
create table freqs(
	f_id                                          int(11) primary key AUTO_INCREMENT comment 'pk for freq table'
	, freq                                        varchar(64)
	, freq_desc                                   varchar(64)
	, minutes                                     int(11)
	, ignore_tf                                   tinyint default 0
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
	);
insert into freqs (freq, freq_desc, minutes) values ('1min', '1 minute', 1);
insert into freqs (freq, freq_desc, minutes) values ('3min', '3 minute', 3);
insert into freqs (freq, freq_desc, minutes) values ('5min', '5 minute', 5);
insert into freqs (freq, freq_desc, minutes) values ('15min', '15 minute', 15);
insert into freqs (freq, freq_desc, minutes) values ('30min', '30 minute', 30);
insert into freqs (freq, freq_desc, minutes) values ('1h', '1 hour', 60);
insert into freqs (freq, freq_desc, minutes) values ('4h', '4 hour', 240);
insert into freqs (freq, freq_desc, minutes) values ('1d', '1 day', 1440);


insert into freqs (freq, freq_desc, minutes, ignore_tf) values ('8min', '8 minute', 8, 1);
insert into freqs (freq, freq_desc, minutes, ignore_tf) values ('13min', '13 minute', 13, 1);
insert into freqs (freq, freq_desc, minutes, ignore_tf) values ('21min', '21 minute', 21, 1);
insert into freqs (freq, freq_desc, minutes, ignore_tf) values ('34min', '34 minute', 34, 1);
insert into freqs (freq, freq_desc, minutes, ignore_tf) values ('55min', '55 minute', 55, 1);
insert into freqs (freq, freq_desc, minutes, ignore_tf) values ('89min', '89 minute', 89, 1);
insert into freqs (freq, freq_desc, minutes, ignore_tf) values ('144min', '144 minute', 144, 1);
insert into freqs (freq, freq_desc, minutes, ignore_tf) values ('233min', '233 minute', 233, 1);
insert into freqs (freq, freq_desc, minutes, ignore_tf) values ('377min', '377 minute', 377, 1);
insert into freqs (freq, freq_desc, minutes, ignore_tf) values ('610min', '610 minute', 610, 1);
insert into freqs (freq, freq_desc, minutes, ignore_tf) values ('987min', '987 minute', 987, 1);
insert into freqs (freq, freq_desc, minutes, ignore_tf) values ('1597min', '1597 minute', 1597, 1);

/*
144
233
377
610
987
1597
2584
4181
6765
10946
17711
28657
46368
75025
121393
196418
317811
514229
832040
1346269
2178309
3524578
5702887
9227465
14930352
24157817
39088169
*/


use cbtrade;
drop table if exists mkt_checks;
create table mkt_checks(
	prod_id                                       varchar(64)
	, buy_check_dttm                              timestamp default current_timestamp
	, buy_check_guid                              varchar(64)
	, sell_check_dttm                             timestamp default current_timestamp
	, sell_check_guid                             varchar(64)
	, refresh_check_dttm                          timestamp default current_timestamp
	, refresh_check_guid                          varchar(64)
	, dlm                                         timestamp default current_timestamp on update current_timestamp
	, unique(prod_id)
	);

/*
alter table cbtrade.mkt_checks add column buy_check_guid varchar(64) after buy_check_dttm;
alter table cbtrade.mkt_checks add column sell_check_guid varchar(64) after sell_check_dttm;
alter table cbtrade.mkt_checks add column refresh_check_guid varchar(64) after refresh_check_dttm;
*/


use cbtrade;
drop table if exists mkts;
create table mkts(
	mkt_id                                        int(11) primary key AUTO_INCREMENT comment 'pk for mkts table'
	, mkt_name                                    varchar(64)
	, prod_id                                     varchar(64)
	, mkt_venue                                   varchar(64)
	, base_curr_symb                              varchar(64)
	, base_curr_name                              varchar(64)
	, base_size_incr                              decimal(36,12)
	, base_size_min                               decimal(36,12)
	, base_size_max                               decimal(36,12)
	, quote_curr_symb                             varchar(64)
	, quote_curr_name                             varchar(64)
	, quote_size_incr                             decimal(36,12)
	, quote_size_min                              decimal(36,12)
	, quote_size_max                              decimal(36,12)
	, mkt_status_tf                               varchar(64)
	, mkt_view_only_tf                            tinyint default 0
	, mkt_watched_tf                              tinyint default 0
	, mkt_is_disabled_tf                          tinyint default 0
	, mkt_new_tf                                  tinyint default 0
	, mkt_cancel_only_tf                          tinyint default 0
	, mkt_limit_only_tf                           tinyint default 0
	, mkt_post_only_tf                            tinyint default 0
	, mkt_trading_disabled_tf                     tinyint default 0
	, mkt_auction_mode_tf                         tinyint default 0
	, prc                                         decimal(36,12)
	, prc_ask                                     decimal(36,12)
	, prc_buy                                     decimal(36,12)
	, prc_bid                                     decimal(36,12)
	, prc_sell                                    decimal(36,12)
	, prc_mid_mkt                                 decimal(36,12)
	, prc_pct_chg_24h                             decimal(36,12)
	, vol_24h                                     decimal(36,12)
	, vol_base_24h                                decimal(36,12)
	, vol_quote_24h                               decimal(36,12)
	, vol_pct_chg_24h                             decimal(36,12)
	, ignore_tf                                   tinyint default 0
	, note1                                       varchar(1024)
	, note2                                       varchar(1024)
	, note3                                       varchar(1024)
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
	, unique(prod_id)
	);

/*
alter table mkts change ask_prc prc_ask decimal(36,12);
alter table mkts change buy_prc prc_buy decimal(36,12);
alter table mkts change bid_prc prc_bid decimal(36,12);
alter table mkts change sell_prc prc_sell decimal(36,12);
*/



use cbtrade;
drop table if exists ords;
create table ords(
	ord_id                                      int(11) primary key AUTO_INCREMENT
	, ord_uuid                                    varchar(256)

	, mkt_id                                    int(11)
	, pos_id                                    int(11)
	, buy_order_id                              int(11)
	, sell_order_id                             int(11)

	, prod_id                                     varchar(64)
	, ord_bs                                      varchar(64)
	, ord_cfg                                     varchar(1024)
	, ord_base_size                               decimal(36,12) default 0
	, ord_end_time                                timestamp
	, ord_limit_prc                               decimal(36,12) default 0
	, ord_post_only                               tinyint default 0
	, ord_quote_size                              decimal(36,12) default 0
	, ord_stop_dir                                varchar(64)
	, ord_stop_prc                                decimal(36,12) default 0
	, ord_stop_trigger_prc                        decimal(36,12) default 0
	, ord_type                                    varchar(64)
	, order_id                                    varchar(64)             
	, ord_product_id                              varchar(64)             
	, ord_user_id                                 varchar(64)             
	, ord_order_configuration                     varchar(1024)           
	, ord_side                                    varchar(64)             
	, ord_client_order_id                         varchar(64)             
	, ord_status                                  varchar(64)             
	, ord_time_in_force                           varchar(64)             
	, ord_created_time                            timestamp               
	, ord_completion_percentage                   decimal(36,12) default 0  
	, ord_filled_size                             decimal(36,12) default 0  
	, ord_average_filled_price                    decimal(36,12) default 0  
	, ord_fee                                     decimal(36,12) default 0  
	, ord_number_of_fills                         int(11)                   
	, ord_filled_value                            decimal(36,12) default 0  
	, ord_pending_cancel                          tinyint default 0         
	, ord_size_in_quote                           tinyint default 0         
	, ord_total_fees                              decimal(36,12) default 0  
	, ord_size_inclusive_of_fees                  tinyint default 0         
	, ord_total_value_after_fees                  decimal(36,12) default 0  
	, ord_trigger_status                          varchar(64)               
	, ord_order_type                              varchar(64)               
	, ord_reject_reason                           varchar(64)               
	, ord_settled                                 tinyint default 0         
	, ord_product_type                            varchar(64)               
	, ord_reject_message                          varchar(1024)             
	, ord_cancel_message                          varchar(1024)             
	, ord_order_placement_source                  varchar(64)               
	, ord_outstanding_hold_amount                 decimal(36,12) default 0  
	, ord_is_liquidation                          tinyint default 0         
	, ord_last_fill_time                          timestamp                 
	, ord_edit_history                            varchar(1024)             
	, ord_leverage                                decimal(36,12) default 0  
	, ord_margin_type                             varchar(64)               
	, ord_retail_portfolio_id                     varchar(64)               

	, ignore_tf                                   tinyint default 0
	, note1                                       varchar(1024)
	, note2                                       varchar(1024)
	, note3                                       varchar(1024)
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
	, unique(ord_uuid)
	);


use cbtrade;
drop table if exists poss;
create table poss(
	pos_id                                        int(11) primary key AUTO_INCREMENT
	, prod_id                                     varchar(64)
	, pos_stat                                    varchar(64)
	, pos_begin_dttm                              timestamp
	, pos_end_dttm                                timestamp
	, age_mins                                    int(11) default 0
	, tot_out_cnt                                 decimal(36,12) default 0
	, tot_in_cnt                                  decimal(36,12) default 0
	, buy_fees_cnt                                decimal(36,12) default 0
	, sell_fees_cnt_tot                           decimal(36,12) default 0
	, fees_cnt_tot                                decimal(36,12) default 0
	, buy_cnt                                     decimal(36,12) default 0
	, sell_cnt_tot                                decimal(36,12) default 0
	, hold_cnt                                    decimal(36,12) default 0
	, pocket_cnt                                  decimal(36,12) default 0
	, clip_cnt                                    decimal(36,12) default 0
	, pocket_pct                                  decimal(36,12) default 0
	, clip_pct                                    decimal(36,12) default 0
	, sell_order_cnt                              int(11)        default 0
	, sell_order_attempt_cnt                      int(11)        default 0
	, prc_buy                                     decimal(36,12) default 0 
	, prc_curr                                    decimal(36,12) default 0
	, prc_high                                    decimal(36,12) default 0 
	, prc_low                                     decimal(36,12) default 0 
	, prc_chg_pct                                 decimal(36,12) default 0
	, prc_chg_pct_high                            decimal(36,12) default 0
	, prc_chg_pct_low                             decimal(36,12) default 0
	, prc_chg_pct_drop                            decimal(36,12) default 0 
	, prc_sell_avg                                decimal(36,12) default 0 
	, val_curr                                    decimal(36,12) default 0
	, val_tot                                     decimal(36,12) default 0
	, gain_loss_amt_est                           decimal(36,12) default 0
	, gain_loss_amt_est_high                      decimal(36,12) default 0
	, gain_loss_amt_est_low                       decimal(36,12) default 0
	, gain_loss_amt                               decimal(36,12) default 0
	, gain_loss_amt_net                           decimal(36,12) default 0
	, gain_loss_pct_est                           decimal(36,12) default 0
	, gain_loss_pct_est_high                      decimal(36,12) default 0
	, gain_loss_pct_est_low                       decimal(36,12) default 0
	, gain_loss_pct                               decimal(36,12) default 0
	, buy_strat_type                              varchar(64)
	, buy_strat_name                              varchar(64)
	, buy_strat_freq                              varchar(64)
	, sell_strat_type                             varchar(64)
	, sell_strat_name                             varchar(64)
	, sell_strat_freq                             varchar(64)
	, bo_id                                       int(11)
	, bo_uuid                                     varchar(64)
	, buy_curr_symb                               varchar(64)
	, spend_curr_symb                             varchar(64)
	, sell_curr_symb                              varchar(64)
	, recv_curr_symb                              varchar(64)
	, fees_curr_symb                              varchar(64)
	, base_curr_symb                              varchar(64)
	, base_size_incr                              decimal(36,12)
	, base_size_min                               decimal(36,12)
	, base_size_max                               decimal(36,12)
	, quote_curr_symb                             varchar(64)
	, quote_size_incr                             decimal(36,12)
	, quote_size_min                              decimal(36,12)
	, quote_size_max                              decimal(36,12)
	, sell_yn                                     char(1) 
	, hodl_yn                                     char(1) 
	, sell_block_yn                               char(1) default 'N'
	, sell_force_yn                               char(1) default 'N'
	, test_tf                                     tinyint default 0
	, test_txn_yn                                 char(1)        default 'N'
	, force_sell_tf                               tinyint default 0
	, ignore_tf                                   tinyint default 0
	, error_tf                                    tinyint default 0
	, reason                                      varchar(1024)
	, note1                                       varchar(1024)
	, note2                                       varchar(1024)
	, note3                                       varchar(1024)
	, mkt_name                                    varchar(64)
	, mkt_venue                                   varchar(64)
	, pos_type                                    varchar(64)
	, buy_asset_type                              varchar(64)
	, check_mkt_dttm                              timestamp default current_timestamp
	, check_last_dttm                             timestamp default current_timestamp
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, del_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
	, unique(bo_uuid)
	);
alter table cbtrade.poss add index idx_prod_id_quote_curr_symb (prod_id, quote_curr_symb);
alter table cbtrade.poss add index idx_prod_id (prod_id);
alter table cbtrade.poss add index idx_prod_id_stat (prod_id, pos_stat);
alter table cbtrade.poss add index idx_buy_strat_name_freq (buy_strat_name, buy_strat_freq);



/*
alter table cbtrade.poss add index prod_id_quote_curr_symb (prod_id, quote_curr_symb);
  , ;
alter table cbtrade.poss add column test_txn_yn char(1) default 'N' after test_tf;
update cbtrade.poss set test_txn_yn = 'Y' where test_tf = 1;
update cbtrade.poss set test_txn_yn = 'N' where test_tf = 0;
*/

-- alter table cbtrade.poss add column symb varchar(64) after pos_id;
-- update cbtrade.poss set symb = 'USDC';


-- alter table cbtrade.poss add column error_tf tinyint default 0 after ignore_tf;
-- alter table cbtrade.poss add column sell_yn char(1) after quote_size_max;
-- alter table cbtrade.poss add column sell_block_yn char(1) after sell_yn;
-- alter table cbtrade.poss add column hodl_yn char(1) after sell_block_yn;
-- alter table cbtrade.poss add column sell_force_yn char(1) default 'N' after sell_block_yn;
-- alter table cbtrade.poss modify column sell_block_yn char(1) default 'N';
-- alter table cbtrade.poss modify column hodl_yn char(1) after sell_yn;




use cbtrade;
drop table if exists sell_ords;
create table sell_ords(
	so_id                                         int(11) primary key AUTO_INCREMENT
	, test_tf                                     tinyint        default 0
	, test_txn_yn                                 char(1)        default 'N'
	, symb                                        varchar(64)
	, prod_id                                     varchar(64)
	, mkt_name                                    varchar(64)
	, mkt_venue                                   varchar(64)

	, pos_id                                      int(11)
	, sell_seq_nbr                                int(11)

	, sell_order_uuid                             varchar(64)
	, sell_client_order_id                        varchar(64)

	, pos_type                                    varchar(64)
	, ord_stat                                    varchar(64)

	, sell_strat_type                             varchar(64)
	, sell_strat_name                             varchar(64)
	, sell_strat_freq                             varchar(64)
	, sell_asset_type                             varchar(64)

	, sell_begin_dttm                             timestamp default current_timestamp
	, sell_end_dttm                               timestamp

	, sell_curr_symb                              varchar(64)
	, recv_curr_symb                              varchar(64)
	, fees_curr_symb                              varchar(64)
	, sell_cnt_est                                decimal(36,12) default 0
	, sell_cnt_act                                decimal(36,12) default 0
	, fees_cnt_act                                decimal(36,12) default 0
	, tot_in_cnt                                  decimal(36,12) default 0

	, prc_sell_est                                decimal(36,12) default 0
	, prc_sell_act                                decimal(36,12) default 0
	, prc_sell_tot                                 decimal(36,12) default 0
	, prc_sell_slip_pct                           decimal(36,12) default 0

	, ignore_tf                                   tinyint default 0
	, reason                                      varchar(1024)
	, note1                                       varchar(1024)
	, note2                                       varchar(1024)
	, note3                                       varchar(1024)
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
	, unique(sell_order_uuid, sell_client_order_id, pos_id)
	);

/*

alter table cbtrade.sell_ords add column test_txn_yn char(1) default 'N' after test_tf;
update cbtrade.sell_ords set test_txn_yn = 'Y' where test_tf = 1;
update cbtrade.sell_ords set test_txn_yn = 'N' where test_tf = 0;


alter table cbtrade.sell_ords add column reason varchar(1024) after ignore_tf;

alter table cbtrade.sell_ords rename column tot_prc_buy to prc_sell_tot;

alter table cbtrade.sell_ords add column symb varchar(64) after test_tf;
update cbtrade.sell_ords set symb = 'USDC';
ALTER TABLE cbtrade.sell_ords ADD CONSTRAINT unique_sell_order UNIQUE (sell_order_uuid, sell_client_order_id, pos_id);
ALTER TABLE cbtrade.sell_ords drop index sell_order_uuid;
sell_ords
*/



use cbtrade;
drop table if exists sell_signals;
create table sell_signals(
	sid                                           int(11) primary key AUTO_INCREMENT
	, test_tf                                     tinyint default 0
	, test_txn_yn                                 char(1)        default 'N'
	, prod_id                                     varchar(64)
	, pos_id                                      int(11)
	, buy_strat_type                              varchar(64)
	, buy_strat_name                              varchar(64)
	, buy_strat_freq                              varchar(64)
	, sell_strat_type                             varchar(64)
	, sell_strat_name                             varchar(64)
	, sell_strat_freq                             varchar(64)
	, sell_yn                                     char(1)
	, sell_block_yn                               char(1)
	, hodl_yn                                     char(1)
	, actv_dttm                                   timestamp default current_timestamp
	, note1                                       varchar(1024)
	, note2                                       varchar(1024)
	, note3                                       varchar(1024)
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
	);

alter table cbtrade.sell_signals add column test_txn_yn char(1) default 'N' after test_txn_yn;
update cbtrade.sell_signals set test_txn_yn = 'Y' where test_txn_yn = 1;
update cbtrade.sell_signals set test_txn_yn = 'N' where test_txn_yn = 0;


use cbtrade;
drop table if exists sell_signs;
create table sell_signs(
	ss_id                                         int(11) primary key AUTO_INCREMENT
	, test_tf                                     tinyint        default 0
	, test_txn_yn                                 char(1)        default 'N'
	, prod_id                                     varchar(64)
	, pos_id                                      int(11)
	, sell_strat_type                             varchar(64)
	, sell_strat_name                             varchar(64)
	, sell_strat_freq                             varchar(64)
	, sell_asset_type                             varchar(64)
	, sell_yn                                     char(1)
	, hodl_yn                                     char(1)
	, ss_dttm                                     timestamp default current_timestamp
	, sell_curr_symb                              varchar(64)
	, recv_curr_symb                              varchar(64)
	, fees_curr_symb                              varchar(64)
	, sell_cnt_est                                decimal(36,12) default 0
	, sell_prc_est                                decimal(36,12) default 0
	, sell_sub_tot_est                            decimal(36,12) default 0
	, sell_fees_est                               decimal(36,12) default 0
	, sell_tot_est                                decimal(36,12) default 0
	, all_sells                                   varchar(2048)
	, all_hodls                                   varchar(2048)
	, ignore_tf                                   tinyint default 0
	, note1                                       varchar(1024)
	, note2                                       varchar(1024)
	, note3                                       varchar(1024)
	, add_dttm                                    timestamp default current_timestamp
	, upd_dttm                                    timestamp default current_timestamp on update current_timestamp
	, dlm                                         timestamp default current_timestamp on update current_timestamp
--	, sell_cnt_est                                decimal(36,12) default 0
--	, sell_cnt_act                                decimal(36,12) default 0
--	, fees_cnt_act                                decimal(36,12) default 0
--	, tot_in_cnt                                  decimal(36,12) default 0
--	, prc_sell_est                                decimal(36,12) default 0
--	, prc_sell_act                                decimal(36,12) default 0
--	, tot_prc_buy                                 decimal(36,12) default 0
--	, prc_sell_slip_pct                           decimal(36,12) default 0
	, unique(prod_id, pos_id, sell_strat_type, sell_strat_name, sell_strat_freq, ss_dttm)
	);
    


alter table cbtrade.sell_signs add column test_txn_yn char(1) default 'N' after test_tf;
update cbtrade.sell_signs set test_txn_yn = 'Y' where test_tf = 1;
update cbtrade.sell_signs set test_txn_yn = 'N' where test_tf = 0;



use cbtrade;
drop view if exists view_bals;
create view view_bals as
select b.symb
  , b.bal_avail as bal_avail_cnt
  , b.bal_hold as bal_hold_cnt
  , b.bal_tot as bal_tot_cnt
  , case when b.symb in ('USD','USDC') then 1 else m.prc end as prc_usd
  , count(p.pos_id) as bot_open_cnt
  , coalesce(sum(p.hold_cnt),0) as bot_bal_cnt
  , b.bal_tot - coalesce(sum(p.hold_cnt),0) as bal_free_cnt
  , round(case when b.symb in ('USD','USDC') then b.bal_tot else b.bal_tot * m.prc end, 8) as bal_val_usd
  , round(case when b.symb in ('USD','USDC') then b.bal_tot else coalesce(sum(p.hold_cnt),0) * m.prc end, 8) as bot_val_usd
  , round(case when b.symb in ('USD','USDC') then b.bal_tot else (b.bal_tot - coalesce(sum(p.hold_cnt),0)) * m.prc end, 8) as free_val_usd
  , b.curr_uuid
  from cbtrade.bals b
  left outer join (select m.base_curr_symb as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC'
					union 
                    select 'ETH2' as symb, m.prc from cbtrade.mkts m where m.quote_curr_symb = 'USDC' and m.base_curr_symb = 'ETH'
					) m on m.symb = b.symb
  left outer join cbtrade.poss p on p.base_curr_symb = b.symb and p.quote_curr_symb = 'USDC' and p.ignore_tf = 0 --  and p.pos_stat in ('OPEN', 'SELL')
  where b.bal_tot > 0
  
  group by b.symb, b.bal_avail, b.bal_hold, b.bal_tot, b.curr_prc_usd, m.prc, b.curr_uuid
  order by b.symb
  ;
  


drop view if exists cbtrade.view_mkt_perf;
create view cbtrade.view_mkt_perf as 
select p.prod_id
  , p.quote_curr_symb
  , count(p.pos_id) as tot_cnt 
  , sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) as win_cnt 
  , sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) as lose_cnt 
  , coalesce(round(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as win_pct 
  , coalesce(round(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then 1 else 0 end) / count(p.pos_id) * 100, 2),0) as lose_pct 
  , sum(p.age_mins) as age_mins
  , sum(p.age_mins) / 60 as age_hours
  , (select coalesce(TIMESTAMPDIFF(SECOND, max(bo.buy_begin_dttm), NOW())/60, 9999) from cbtrade.buy_ords bo where bo.prod_id = p.prod_id) as bo_elapsed
  , (select coalesce(TIMESTAMPDIFF(SECOND, max(px.pos_begin_dttm), NOW())/60, 9999) from cbtrade.poss px where px.prod_id = p.prod_id and px.pos_stat not in ('TIME') ) as pos_elapsed
  , round(sum(p.tot_out_cnt), 2) as tot_out_cnt
  , round(sum(p.tot_in_cnt), 2) as tot_in_cnt
  , round(sum(p.buy_fees_cnt), 2) as buy_fees_cnt
  , round(sum(p.sell_fees_cnt_tot), 2) as sell_fees_cnt_tot
  , round(sum(p.fees_cnt_tot), 2) as fees_cnt_tot
  , sum(p.buy_cnt) as buy_cnt
  , sum(p.sell_cnt_tot) as sell_cnt_tot
  , sum(p.hold_cnt) as hold_cnt
  , sum(p.pocket_cnt) as pocket_cnt
  , sum(p.clip_cnt) as clip_cnt
  , sum(p.sell_order_cnt) as sell_order_cnt
  , sum(p.sell_order_attempt_cnt) as sell_order_attempt_cnt
  , round(sum(p.val_curr), 2) as val_curr
  , round(sum(p.val_tot), 2) as val_tot
  , round(sum(case when p.tot_in_cnt + p.val_tot > p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as win_amt 
  , round(sum(case when p.tot_in_cnt + p.val_tot < p.tot_out_cnt then p.gain_loss_amt else 0 end), 2) as lose_amt
  , round(sum(p.gain_loss_amt), 2) as gain_loss_amt
  , round(sum(p.gain_loss_amt_net), 2) as gain_loss_amt_net
  , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100,2) as gain_loss_pct
  , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60), 8) as gain_loss_pct_hr
  , round(sum(p.gain_loss_amt) / sum(p.tot_out_cnt) * 100/ (sum(p.age_mins) / 60) * 24, 8) as gain_loss_pct_day
--  , p.test_txn_yn
  from cbtrade.poss p
  where ignore_tf = 0
  group by p.prod_id
  order by gain_loss_pct_day desc
  ;




drop view if exists cbtrade.view_pos;
create view cbtrade.view_pos as 
select p.pos_id
  , p.prod_id
  , p.pos_stat
  , p.pos_begin_dttm
  , p.pos_end_dttm
  , date(p.pos_end_dttm) as dt
  , p.age_mins
  , p.age_mins / 60 as age_hours
  , round(p.tot_out_cnt, 2) as tot_out_cnt
  , round(p.tot_in_cnt, 2) as tot_in_cnt
  , round(p.buy_fees_cnt, 2) as buy_fees_cnt
  , round(p.sell_fees_cnt_tot, 2) as sell_fees_cnt_tot
  , round(p.fees_cnt_tot, 2) as fees_cnt_tot
  , p.buy_cnt
  , p.sell_cnt_tot
  , p.hold_cnt
  , p.pocket_cnt
  , p.clip_cnt
  , p.pocket_pct
  , p.clip_pct
  , p.sell_order_cnt
  , p.sell_order_attempt_cnt
  , p.prc_buy
  , prc_curr
  , p.prc_high
  , p.prc_low
  , p.prc_chg_pct
  , p.prc_chg_pct_high
  , p.prc_chg_pct_low
  , p.prc_chg_pct_drop
  , p.prc_sell_avg
  , round(p.val_curr, 2) as val_curr
  , round(p.val_tot, 2) as val_tot
  , round(p.gain_loss_amt_est, 2) as gain_loss_amt_est
  , round(p.gain_loss_amt_est_high, 2) as gain_loss_amt_est_high
  , round(p.gain_loss_amt_est_low, 2) as gain_loss_amt_est_low
  , round(p.gain_loss_amt, 2) as gain_loss_amt
  , round(p.gain_loss_amt_net, 2) as gain_loss_amt_net
  , round(p.gain_loss_pct_est, 2) as gain_loss_pct_est
  , round(p.gain_loss_pct_est_high, 2) as gain_loss_pct_est_high
  , round(p.gain_loss_pct_est_low, 2) as gain_loss_pct_est_low
  , round(p.gain_loss_pct, 2) as gain_loss_pct
  , p.buy_strat_type
  , p.buy_strat_name
  , p.buy_strat_freq
  , p.sell_strat_type
  , p.sell_strat_name
  , p.sell_strat_freq
  , p.bo_id
  , p.bo_uuid
  , p.buy_curr_symb
  , p.spend_curr_symb
  , p.sell_curr_symb
  , p.recv_curr_symb
  , p.fees_curr_symb
  , p.test_txn_yn
  , round(p.gain_loss_amt / p.tot_out_cnt * 100 / p.age_mins / 60, 8) as gain_loss_pct_hr
  from cbtrade.poss p
  where ignore_tf = 0
  order by p.pos_id desc
  ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;




