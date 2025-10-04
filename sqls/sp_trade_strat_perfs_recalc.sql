-- Example only: CREATE PROCEDURE for single-strategy L/T/A recalc
-- Does INSERT ... ON DUPLICATE KEY UPDATE to trade_strat_perfs, then SELECTs the row back
use cbtrade;

DROP PROCEDURE IF EXISTS sp_trade_strat_perfs_recalc;

DELIMITER $$

CREATE PROCEDURE sp_trade_strat_perfs_recalc (
    IN p_prod_id         VARCHAR(64)   -- NULL => all prod_ids
  , IN p_buy_strat_type  VARCHAR(64)   -- NULL => all types
  , IN p_buy_strat_name  VARCHAR(64)   -- NULL => all names
  , IN p_buy_strat_freq  VARCHAR(64)   -- NULL => all freqs
  , IN p_lta             CHAR(1)        -- 'L','T','A'; NULL => all three
)
BEGIN
    /* Multi-target upsert with GROUP BY over parameter wildcards */
    INSERT INTO trade_strat_perfs (
        base_symb
      , quote_symb
      , prod_id
      , lta
      , buy_strat_type
      , buy_strat_name
      , buy_strat_freq
      , last_upd_dttm
      , last_upd_unix

      , tot_cnt
      , tot_open_cnt
      , tot_close_cnt
      , win_cnt
      , win_open_cnt
      , win_close_cnt
      , lose_cnt
      , lose_open_cnt
      , lose_close_cnt

      , win_pct
      , win_open_pct
      , win_close_pct
      , lose_pct
      , lose_open_pct
      , lose_close_pct

      , age_mins
      , age_hours

      , tot_out_cnt
      , tot_out_open_cnt
      , tot_out_close_cnt
      , tot_in_cnt
      , tot_in_open_cnt
      , tot_in_close_cnt

      , buy_fees_cnt
      , buy_fees_open_cnt
      , buy_fees_close_cnt
      , sell_fees_cnt_tot
      , sell_fees_open_cnt_tot
      , sell_fees_close_cnt_tot
      , fees_cnt_tot
      , fees_open_cnt_tot
      , fees_close_cnt_tot

      , buy_cnt
      , buy_open_cnt
      , buy_close_cnt
      , sell_cnt_tot
      , sell_open_cnt_tot
      , sell_close_cnt_tot
      , hold_cnt
      , hold_open_cnt
      , hold_close_cnt
      , pocket_cnt
      , pocket_open_cnt
      , pocket_close_cnt
      , clip_cnt
      , clip_open_cnt
      , clip_close_cnt
      , sell_order_cnt
      , sell_order_open_cnt
      , sell_order_close_cnt
      , sell_order_attempt_cnt
      , sell_order_attempt_open_cnt
      , sell_order_attempt_close_cnt

      , val_curr
      , val_open_curr
      , val_close_curr
      , val_tot
      , val_open_tot
      , val_close_tot

      , win_amt
      , win_open_amt
      , win_close_amt
      , lose_amt
      , lose_open_amt
      , lose_close_amt

      , gain_loss_amt
      , gain_loss_open_amt
      , gain_loss_close_amt
      , gain_loss_amt_net
      , gain_loss_open_amt_net
      , gain_loss_close_amt_net

      , gain_loss_pct
      , gain_loss_open_pct
      , gain_loss_close_pct
      , gain_loss_pct_hr
      , gain_loss_open_pct_hr
      , gain_loss_close_pct_hr
      , gain_loss_pct_day
      , gain_loss_open_pct_day
      , gain_loss_close_pct_day

      , last_buy_strat_bo_dttm
      , last_buy_strat_bo_unix
      , last_buy_strat_pos_dttm
      , last_buy_strat_pos_unix
      , last_buy_strat_dttm
      , last_buy_strat_unix
      , needs_recalc_yn
    )
    SELECT
          SUBSTRING_INDEX(pl.prod_id, '-', 1) AS base_symb
        , SUBSTRING_INDEX(pl.prod_id, '-', -1) AS quote_symb
        , pl.prod_id AS prod_id
        , lt.lta AS lta
        , pl.buy_strat_type AS buy_strat_type
        , pl.buy_strat_name AS buy_strat_name
        , pl.buy_strat_freq AS buy_strat_freq
        , NOW() AS last_upd_dttm
        , UNIX_TIMESTAMP() AS last_upd_unix
        , COUNT(p.pos_id) AS tot_cnt
        , COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN 1 ELSE 0 END),0) AS tot_open_cnt
        , COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END),0) AS tot_close_cnt
        , COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot > p.tot_out_cnt THEN 1 ELSE 0 END),0) AS win_cnt
        , COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot > p.tot_out_cnt AND p.pos_stat IN ('OPEN','SELL') THEN 1 ELSE 0 END),0) AS win_open_cnt
        , COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot > p.tot_out_cnt AND p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END),0) AS win_close_cnt
        , COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot < p.tot_out_cnt THEN 1 ELSE 0 END),0) AS lose_cnt
        , COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot < p.tot_out_cnt AND p.pos_stat IN ('OPEN','SELL') THEN 1 ELSE 0 END),0) AS lose_open_cnt
        , COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot < p.tot_out_cnt AND p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END),0) AS lose_close_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot > p.tot_out_cnt THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(p.pos_id),0), 0), 2) AS win_pct
        , ROUND(COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot > p.tot_out_cnt AND p.pos_stat IN ('OPEN','SELL') THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN 1 ELSE 0 END),0), 0), 2) AS win_open_pct
        , ROUND(COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot > p.tot_out_cnt AND p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END),0), 0), 2) AS win_close_pct
        , ROUND(COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot < p.tot_out_cnt THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(p.pos_id),0), 0), 2) AS lose_pct
        , ROUND(COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot < p.tot_out_cnt AND p.pos_stat IN ('OPEN','SELL') THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN 1 ELSE 0 END),0), 0), 2) AS lose_open_pct
        , ROUND(COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot < p.tot_out_cnt AND p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END),0), 0), 2) AS lose_close_pct
        , COALESCE(SUM(p.age_mins), 0) AS age_mins
        , ROUND(COALESCE(SUM(p.age_mins) / 60.0, 0), 2) AS age_hours
        , ROUND(COALESCE(SUM(p.tot_out_cnt), 0), 16) AS tot_out_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.tot_out_cnt ELSE 0 END), 0), 16) AS tot_out_open_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.tot_out_cnt ELSE 0 END), 0), 16) AS tot_out_close_cnt
        , ROUND(COALESCE(SUM(p.tot_in_cnt), 0), 16) AS tot_in_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.tot_in_cnt ELSE 0 END), 0), 16) AS tot_in_open_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.tot_in_cnt ELSE 0 END), 0), 16) AS tot_in_close_cnt
        , ROUND(COALESCE(SUM(p.buy_fees_cnt), 0), 16) AS buy_fees_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.buy_fees_cnt ELSE 0 END), 0), 16) AS buy_fees_open_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.buy_fees_cnt ELSE 0 END), 0), 16) AS buy_fees_close_cnt
        , ROUND(COALESCE(SUM(p.sell_fees_cnt_tot), 0), 16) AS sell_fees_cnt_tot
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.sell_fees_cnt_tot ELSE 0 END), 0), 16) AS sell_fees_open_cnt_tot
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.sell_fees_cnt_tot ELSE 0 END), 0), 16) AS sell_fees_close_cnt_tot
        , ROUND(COALESCE(SUM(p.fees_cnt_tot), 0), 16) AS fees_cnt_tot
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.fees_cnt_tot ELSE 0 END), 0), 16) AS fees_open_cnt_tot
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.fees_cnt_tot ELSE 0 END), 0), 16) AS fees_close_cnt_tot
        , ROUND(COALESCE(SUM(p.buy_cnt), 0), 16) AS buy_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.buy_cnt ELSE 0 END), 0), 16) AS buy_open_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.buy_cnt ELSE 0 END), 0), 16) AS buy_close_cnt
        , ROUND(COALESCE(SUM(p.sell_cnt_tot), 0), 16) AS sell_cnt_tot
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.sell_cnt_tot ELSE 0 END), 0), 16) AS sell_open_cnt_tot
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.sell_cnt_tot ELSE 0 END), 0), 16) AS sell_close_cnt_tot
        , ROUND(COALESCE(SUM(p.hold_cnt), 0), 16) AS hold_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.hold_cnt ELSE 0 END), 0), 16) AS hold_open_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.hold_cnt ELSE 0 END), 0), 16) AS hold_close_cnt
        , ROUND(COALESCE(SUM(p.pocket_cnt), 0), 16) AS pocket_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.pocket_cnt ELSE 0 END), 0), 16) AS pocket_open_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.pocket_cnt ELSE 0 END), 0), 16) AS pocket_close_cnt
        , ROUND(COALESCE(SUM(p.clip_cnt), 0), 16) AS clip_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.clip_cnt ELSE 0 END), 0), 16) AS clip_open_cnt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.clip_cnt ELSE 0 END), 0), 16) AS clip_close_cnt
        , COALESCE(SUM(p.sell_order_cnt), 0) AS sell_order_cnt
        , COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.sell_order_cnt ELSE 0 END), 0) AS sell_order_open_cnt
        , COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.sell_order_cnt ELSE 0 END), 0) AS sell_order_close_cnt
        , COALESCE(SUM(p.sell_order_attempt_cnt), 0) AS sell_order_attempt_cnt
        , COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.sell_order_attempt_cnt ELSE 0 END), 0) AS sell_order_attempt_open_cnt
        , COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.sell_order_attempt_cnt ELSE 0 END), 0) AS sell_order_attempt_close_cnt
        , ROUND(COALESCE(SUM(p.val_curr), 0), 16) AS val_curr
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.val_curr ELSE 0 END), 0), 16) AS val_open_curr
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.val_curr ELSE 0 END), 0), 16) AS val_close_curr
        , ROUND(COALESCE(SUM(p.val_tot), 0), 16) AS val_tot
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.val_tot ELSE 0 END), 0), 16) AS val_open_tot
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.val_tot ELSE 0 END), 0), 16) AS val_close_tot
        , COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot > p.tot_out_cnt THEN p.val_tot ELSE 0 END), 0) AS win_amt
        , COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot > p.tot_out_cnt AND p.pos_stat IN ('OPEN','SELL') THEN p.val_tot ELSE 0 END), 0) AS win_open_amt
        , COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot > p.tot_out_cnt AND p.pos_stat = 'CLOSE' THEN p.val_tot ELSE 0 END), 0) AS win_close_amt
        , COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot < p.tot_out_cnt THEN p.val_tot ELSE 0 END), 0) AS lose_amt
        , COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot < p.tot_out_cnt AND p.pos_stat IN ('OPEN','SELL') THEN p.val_tot ELSE 0 END), 0) AS lose_open_amt
        , COALESCE(SUM(CASE WHEN p.tot_in_cnt + p.val_tot < p.tot_out_cnt AND p.pos_stat = 'CLOSE' THEN p.val_tot ELSE 0 END), 0) AS lose_close_amt
        , ROUND(COALESCE(SUM(p.gain_loss_amt), 0), 16) AS gain_loss_amt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.gain_loss_amt ELSE 0 END), 0), 16) AS gain_loss_open_amt
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.gain_loss_amt ELSE 0 END), 0), 16) AS gain_loss_close_amt
        , ROUND(COALESCE(SUM(p.gain_loss_amt_net), 0), 16) AS gain_loss_amt_net
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.gain_loss_amt_net ELSE 0 END), 0), 16) AS gain_loss_open_amt_net
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.gain_loss_amt_net ELSE 0 END), 0), 16) AS gain_loss_close_amt_net
        , ROUND(COALESCE(SUM(p.gain_loss_amt) * 100.0 / NULLIF(SUM(p.tot_out_cnt), 0), 0), 2) AS gain_loss_pct
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.gain_loss_amt ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.tot_out_cnt ELSE 0 END), 0), 0), 2) AS gain_loss_open_pct
        , ROUND(COALESCE(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.gain_loss_amt ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.tot_out_cnt ELSE 0 END), 0), 0), 2) AS gain_loss_close_pct
        , ROUND(COALESCE( (SUM(p.gain_loss_amt) * 100.0 / NULLIF(SUM(p.tot_out_cnt),0)) / NULLIF(SUM(p.age_mins)/60.0, 0), 0), 16) AS gain_loss_pct_hr
        , ROUND(COALESCE( (SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.gain_loss_amt ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.tot_out_cnt ELSE 0 END),0)) / NULLIF(SUM(p.age_mins)/60.0, 0), 0), 16) AS gain_loss_open_pct_hr
        , ROUND(COALESCE( (SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.gain_loss_amt ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.tot_out_cnt ELSE 0 END),0)) / NULLIF(SUM(p.age_mins)/60.0, 0), 0), 16) AS gain_loss_close_pct_hr
        , ROUND(COALESCE( (SUM(p.gain_loss_amt) * 100.0 / NULLIF(SUM(p.tot_out_cnt),0)) / NULLIF(SUM(p.age_mins)/60.0, 0) * 24, 0), 16) AS gain_loss_pct_day
        , ROUND(COALESCE( (SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.gain_loss_amt ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.tot_out_cnt ELSE 0 END),0)) / NULLIF(SUM(p.age_mins)/60.0, 0) * 24, 0), 16) AS gain_loss_open_pct_day
        , ROUND(COALESCE( (SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.gain_loss_amt ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.tot_out_cnt ELSE 0 END),0)) / NULLIF(SUM(p.age_mins)/60.0, 0) * 24, 0), 16) AS gain_loss_close_pct_day
        /* Elapsed metrics from buy_ords & poss using lt.lta and pl.* keys */
        , CASE WHEN (SELECT MAX(b.buy_begin_unix)
                     FROM buy_ords b
                     WHERE b.prod_id = pl.prod_id
                       AND b.buy_strat_type = pl.buy_strat_type
                       AND b.buy_strat_name = pl.buy_strat_name
                       AND b.buy_strat_freq = pl.buy_strat_freq
                       AND (CASE WHEN lt.lta='L' THEN b.test_txn_yn='N'
                                 WHEN lt.lta='T' THEN b.test_txn_yn='Y'
                                 ELSE 1=1 END)) > 0
               THEN FROM_UNIXTIME((SELECT MAX(b.buy_begin_unix)
                                  FROM buy_ords b
                                  WHERE b.prod_id = pl.prod_id
                                    AND b.buy_strat_type = pl.buy_strat_type
                                    AND b.buy_strat_name = pl.buy_strat_name
                                    AND b.buy_strat_freq = pl.buy_strat_freq
                                    AND (CASE WHEN lt.lta='L' THEN b.test_txn_yn='N'
                                              WHEN lt.lta='T' THEN b.test_txn_yn='Y'
                                              ELSE 1=1 END)))
               ELSE NULL END AS last_buy_strat_bo_dttm
        , COALESCE( (SELECT MAX(b.buy_begin_unix)
                   FROM buy_ords b
                   WHERE b.prod_id = pl.prod_id
                     AND b.buy_strat_type = pl.buy_strat_type
                     AND b.buy_strat_name = pl.buy_strat_name
                     AND b.buy_strat_freq = pl.buy_strat_freq
                     AND (CASE WHEN lt.lta='L' THEN b.test_txn_yn='N'
                               WHEN lt.lta='T' THEN b.test_txn_yn='Y'
                               ELSE 1=1 END)
                 ), 0) AS last_buy_strat_bo_unix

        , CASE WHEN (SELECT MAX(p2.pos_begin_unix)
                     FROM poss p2
                     WHERE p2.prod_id = pl.prod_id
                       AND p2.buy_strat_type = pl.buy_strat_type
                       AND p2.buy_strat_name = pl.buy_strat_name
                       AND p2.buy_strat_freq = pl.buy_strat_freq
                       AND (CASE WHEN lt.lta='L' THEN p2.test_txn_yn='N'
                                 WHEN lt.lta='T' THEN p2.test_txn_yn='Y'
                                 ELSE 1=1 END)) > 0
               THEN FROM_UNIXTIME((SELECT MAX(p2.pos_begin_unix)
                                  FROM poss p2
                                  WHERE p2.prod_id = pl.prod_id
                                    AND p2.buy_strat_type = pl.buy_strat_type
                                    AND p2.buy_strat_name = pl.buy_strat_name
                                    AND p2.buy_strat_freq = pl.buy_strat_freq
                                    AND (CASE WHEN lt.lta='L' THEN p2.test_txn_yn='N'
                                              WHEN lt.lta='T' THEN p2.test_txn_yn='Y'
                                              ELSE 1=1 END)))
               ELSE NULL END AS last_buy_strat_pos_dttm
        , COALESCE( (SELECT MAX(p2.pos_begin_unix)
                   FROM poss p2
                   WHERE p2.prod_id = pl.prod_id
                     AND p2.buy_strat_type = pl.buy_strat_type
                     AND p2.buy_strat_name = pl.buy_strat_name
                     AND p2.buy_strat_freq = pl.buy_strat_freq
                     AND (CASE WHEN lt.lta='L' THEN p2.test_txn_yn='N'
                               WHEN lt.lta='T' THEN p2.test_txn_yn='Y'
                               ELSE 1=1 END)
                 ), 0) AS last_buy_strat_pos_unix

        , CASE WHEN GREATEST(
            COALESCE( (SELECT MAX(p3.pos_begin_unix)
                       FROM poss p3
                       WHERE p3.prod_id = pl.prod_id
                         AND p3.buy_strat_type = pl.buy_strat_type
                         AND p3.buy_strat_name = pl.buy_strat_name
                         AND p3.buy_strat_freq = pl.buy_strat_freq
                         AND (CASE WHEN lt.lta='L' THEN p3.test_txn_yn='N'
                                   WHEN lt.lta='T' THEN p3.test_txn_yn='Y'
                                   ELSE 1=1 END)
                     ), 0),
            COALESCE( (SELECT MAX(b2.buy_begin_unix)
                       FROM buy_ords b2
                       WHERE b2.prod_id = pl.prod_id
                         AND b2.buy_strat_type = pl.buy_strat_type
                         AND b2.buy_strat_name = pl.buy_strat_name
                         AND b2.buy_strat_freq = pl.buy_strat_freq
                         AND (CASE WHEN lt.lta='L' THEN b2.test_txn_yn='N'
                                   WHEN lt.lta='T' THEN b2.test_txn_yn='Y'
                                   ELSE 1=1 END)
                     ), 0)
        ) > 0
               THEN FROM_UNIXTIME(GREATEST(
            COALESCE( (SELECT MAX(p3.pos_begin_unix)
                       FROM poss p3
                       WHERE p3.prod_id = pl.prod_id
                         AND p3.buy_strat_type = pl.buy_strat_type
                         AND p3.buy_strat_name = pl.buy_strat_name
                         AND p3.buy_strat_freq = pl.buy_strat_freq
                         AND (CASE WHEN lt.lta='L' THEN p3.test_txn_yn='N'
                                   WHEN lt.lta='T' THEN p3.test_txn_yn='Y'
                                   ELSE 1=1 END)
                     ), 0),
            COALESCE( (SELECT MAX(b2.buy_begin_unix)
                       FROM buy_ords b2
                       WHERE b2.prod_id = pl.prod_id
                         AND b2.buy_strat_type = pl.buy_strat_type
                         AND b2.buy_strat_name = pl.buy_strat_name
                         AND b2.buy_strat_freq = pl.buy_strat_freq
                         AND (CASE WHEN lt.lta='L' THEN b2.test_txn_yn='N'
                                   WHEN lt.lta='T' THEN b2.test_txn_yn='Y'
                                   ELSE 1=1 END)
                     ), 0)
        ))
               ELSE NULL END AS last_buy_strat_dttm
        , GREATEST(
            COALESCE( (SELECT MAX(p3.pos_begin_unix)
                       FROM poss p3
                       WHERE p3.prod_id = pl.prod_id
                         AND p3.buy_strat_type = pl.buy_strat_type
                         AND p3.buy_strat_name = pl.buy_strat_name
                         AND p3.buy_strat_freq = pl.buy_strat_freq
                         AND (CASE WHEN lt.lta='L' THEN p3.test_txn_yn='N'
                                   WHEN lt.lta='T' THEN p3.test_txn_yn='Y'
                                   ELSE 1=1 END)
                     ), 0),
            COALESCE( (SELECT MAX(b2.buy_begin_unix)
                       FROM buy_ords b2
                       WHERE b2.prod_id = pl.prod_id
                         AND b2.buy_strat_type = pl.buy_strat_type
                         AND b2.buy_strat_name = pl.buy_strat_name
                         AND b2.buy_strat_freq = pl.buy_strat_freq
                         AND (CASE WHEN lt.lta='L' THEN b2.test_txn_yn='N'
                                   WHEN lt.lta='T' THEN b2.test_txn_yn='Y'
                                   ELSE 1=1 END)
                     ), 0)
        ) AS last_buy_strat_unix

        , 'N' AS needs_recalc_yn

    FROM 
      /* Use input params directly to guarantee row creation */
      (SELECT p_prod_id AS prod_id, p_buy_strat_type AS buy_strat_type, p_buy_strat_name AS buy_strat_name, p_buy_strat_freq AS buy_strat_freq
       WHERE p_prod_id IS NOT NULL AND p_buy_strat_type IS NOT NULL AND p_buy_strat_name IS NOT NULL AND p_buy_strat_freq IS NOT NULL
       UNION
       SELECT DISTINCT p.prod_id, p.buy_strat_type, p.buy_strat_name, p.buy_strat_freq
         FROM poss p
        WHERE p.ignore_tf = 0
          AND (p_prod_id IS NULL OR p.prod_id = p_prod_id)
          AND (p_buy_strat_type IS NULL OR p.buy_strat_type = p_buy_strat_type)
          AND (p_buy_strat_name IS NULL OR p.buy_strat_name = p_buy_strat_name)
          AND (p_buy_strat_freq IS NULL OR p.buy_strat_freq = p_buy_strat_freq)
      ) pl
      JOIN (
        SELECT p_lta AS lta WHERE p_lta IS NOT NULL
        UNION ALL
        SELECT 'L' AS lta WHERE p_lta IS NULL
        UNION ALL SELECT 'T' WHERE p_lta IS NULL
        UNION ALL SELECT 'A' WHERE p_lta IS NULL
      ) lt
      LEFT JOIN poss p
        ON p.prod_id = pl.prod_id
       AND p.buy_strat_type = pl.buy_strat_type
       AND p.buy_strat_name = pl.buy_strat_name
        AND p.buy_strat_freq = pl.buy_strat_freq
       AND p.ignore_tf = 0
       AND (CASE WHEN lt.lta='L' THEN p.test_txn_yn='N'
                 WHEN lt.lta='T' THEN p.test_txn_yn='Y'
                 ELSE 1=1 END)

    GROUP BY pl.prod_id, pl.buy_strat_type, pl.buy_strat_name, pl.buy_strat_freq, lt.lta

    ON DUPLICATE KEY UPDATE
        last_upd_dttm = VALUES(last_upd_dttm),
        last_upd_unix = VALUES(last_upd_unix),
        tot_cnt = VALUES(tot_cnt),
        tot_open_cnt = VALUES(tot_open_cnt),
        tot_close_cnt = VALUES(tot_close_cnt),
        win_cnt = VALUES(win_cnt),
        win_open_cnt = VALUES(win_open_cnt),
        win_close_cnt = VALUES(win_close_cnt),
        lose_cnt = VALUES(lose_cnt),
        lose_open_cnt = VALUES(lose_open_cnt),
        lose_close_cnt = VALUES(lose_close_cnt),
        win_pct = VALUES(win_pct),
        win_open_pct = VALUES(win_open_pct),
        win_close_pct = VALUES(win_close_pct),
        lose_pct = VALUES(lose_pct),
        lose_open_pct = VALUES(lose_open_pct),
        lose_close_pct = VALUES(lose_close_pct),
        age_mins = VALUES(age_mins),
        age_hours = VALUES(age_hours),
        tot_out_cnt = VALUES(tot_out_cnt),
        tot_out_open_cnt = VALUES(tot_out_open_cnt),
        tot_out_close_cnt = VALUES(tot_out_close_cnt),
        tot_in_cnt = VALUES(tot_in_cnt),
        tot_in_open_cnt = VALUES(tot_in_open_cnt),
        tot_in_close_cnt = VALUES(tot_in_close_cnt),
        buy_fees_cnt = VALUES(buy_fees_cnt),
        buy_fees_open_cnt = VALUES(buy_fees_open_cnt),
        buy_fees_close_cnt = VALUES(buy_fees_close_cnt),
        sell_fees_cnt_tot = VALUES(sell_fees_cnt_tot),
        sell_fees_open_cnt_tot = VALUES(sell_fees_open_cnt_tot),
        sell_fees_close_cnt_tot = VALUES(sell_fees_close_cnt_tot),
        fees_cnt_tot = VALUES(fees_cnt_tot),
        fees_open_cnt_tot = VALUES(fees_open_cnt_tot),
        fees_close_cnt_tot = VALUES(fees_close_cnt_tot),
        buy_cnt = VALUES(buy_cnt),
        buy_open_cnt = VALUES(buy_open_cnt),
        buy_close_cnt = VALUES(buy_close_cnt),
        sell_cnt_tot = VALUES(sell_cnt_tot),
        sell_open_cnt_tot = VALUES(sell_open_cnt_tot),
        sell_close_cnt_tot = VALUES(sell_close_cnt_tot),
        hold_cnt = VALUES(hold_cnt),
        hold_open_cnt = VALUES(hold_open_cnt),
        hold_close_cnt = VALUES(hold_close_cnt),
        pocket_cnt = VALUES(pocket_cnt),
        pocket_open_cnt = VALUES(pocket_open_cnt),
        pocket_close_cnt = VALUES(pocket_close_cnt),
        clip_cnt = VALUES(clip_cnt),
        clip_open_cnt = VALUES(clip_open_cnt),
        clip_close_cnt = VALUES(clip_close_cnt),
        sell_order_cnt = VALUES(sell_order_cnt),
        sell_order_open_cnt = VALUES(sell_order_open_cnt),
        sell_order_close_cnt = VALUES(sell_order_close_cnt),
        sell_order_attempt_cnt = VALUES(sell_order_attempt_cnt),
        sell_order_attempt_open_cnt = VALUES(sell_order_attempt_open_cnt),
        sell_order_attempt_close_cnt = VALUES(sell_order_attempt_close_cnt),
        val_curr = VALUES(val_curr),
        val_open_curr = VALUES(val_open_curr),
        val_close_curr = VALUES(val_close_curr),
        val_tot = VALUES(val_tot),
        val_open_tot = VALUES(val_open_tot),
        val_close_tot = VALUES(val_close_tot),
        win_amt = VALUES(win_amt),
        win_open_amt = VALUES(win_open_amt),
        win_close_amt = VALUES(win_close_amt),
        lose_amt = VALUES(lose_amt),
        lose_open_amt = VALUES(lose_open_amt),
        lose_close_amt = VALUES(lose_close_amt),
        gain_loss_amt = VALUES(gain_loss_amt),
        gain_loss_open_amt = VALUES(gain_loss_open_amt),
        gain_loss_close_amt = VALUES(gain_loss_close_amt),
        gain_loss_amt_net = VALUES(gain_loss_amt_net),
        gain_loss_open_amt_net = VALUES(gain_loss_open_amt_net),
        gain_loss_close_amt_net = VALUES(gain_loss_close_amt_net),
        gain_loss_pct = VALUES(gain_loss_pct),
        gain_loss_open_pct = VALUES(gain_loss_open_pct),
        gain_loss_close_pct = VALUES(gain_loss_close_pct),
        gain_loss_pct_hr = VALUES(gain_loss_pct_hr),
        gain_loss_open_pct_hr = VALUES(gain_loss_open_pct_hr),
        gain_loss_close_pct_hr = VALUES(gain_loss_close_pct_hr),
        gain_loss_pct_day = VALUES(gain_loss_pct_day),
        gain_loss_open_pct_day = VALUES(gain_loss_open_pct_day),
        gain_loss_close_pct_day = VALUES(gain_loss_close_pct_day),
        last_buy_strat_bo_dttm = VALUES(last_buy_strat_bo_dttm),
        last_buy_strat_bo_unix = VALUES(last_buy_strat_bo_unix),
        last_buy_strat_pos_dttm = VALUES(last_buy_strat_pos_dttm),
        last_buy_strat_pos_unix = VALUES(last_buy_strat_pos_unix),
        last_buy_strat_dttm = VALUES(last_buy_strat_dttm),
        last_buy_strat_unix = VALUES(last_buy_strat_unix),
        needs_recalc_yn = VALUES(needs_recalc_yn);

END$$

DELIMITER ;