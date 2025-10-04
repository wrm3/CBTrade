SELECT b.symb
  , b.bal_tot
  , case when b.symb = 'USDC' then 1 else b.curr_prc_usd end as curr_prc_usd
  , COALESCE(s.open_pos_cnt, 0) AS open_pos
  , COALESCE(s.closed_pos_cnt, 0) AS closed_pos
  , COALESCE(s.open_buy_cnt, 0) AS open_buy_cnt
  , COALESCE(s.open_hold_cnt, 0) AS open_hold_cnt
  , (b.bal_tot - COALESCE(s.open_hold_cnt, 0) - COALESCE(s.closed_hold_cnt, 0)) AS over_under_cnt
  , b.curr_val_usd
  , round(COALESCE(s.open_hold_cnt, 0) * case when b.symb = 'USDC' then 1 else b.curr_prc_usd end, 2) AS open_hold_val_usdc
  , round(COALESCE(s.closed_hold_cnt, 0) * case when b.symb = 'USDC' then 1 else b.curr_prc_usd end, 2) AS closed_hold_val_usdc
  , round((b.bal_tot - COALESCE(s.open_hold_cnt, 0) - COALESCE(s.closed_hold_cnt, 0)) * case when b.symb = 'USDC' then 1 else b.curr_prc_usd end, 2) AS over_under_val_usdc
FROM cbtrade.bals b
LEFT JOIN (SELECT p.base_curr_symb AS symb
    , SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN 1 ELSE 0 END) AS open_pos_cnt
    , SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.buy_cnt ELSE 0 END) AS open_buy_cnt
    , SUM(CASE WHEN p.pos_stat IN ('OPEN','SELL') THEN p.hold_cnt ELSE 0 END) AS open_hold_cnt
    , SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN 1 ELSE 0 END) AS closed_pos_cnt
    , SUM(CASE WHEN p.pos_stat = 'CLOSE' THEN p.hold_cnt ELSE 0 END) AS closed_hold_cnt
  FROM cbtrade.poss p
  WHERE p.ignore_tf = 0 AND p.test_txn_yn = 'N' AND p.quote_curr_symb = 'USDC'
  GROUP BY p.base_curr_symb
) s ON s.symb = b.symb
WHERE b.bal_tot > 0
ORDER BY 12 desc;

select * from cbtrade.poss p where hold_cnt < 0;
delete from cbtrade.poss p where pos_id = 1039918;
delete from cbtrade.poss p where pos_id = 1040474;
delete from cbtrade.poss p where pos_id = 1040812;

select * 
from cbtrade.poss p 
where p.pos_stat = 'CLOSE'
and p.prod_id = 'SOL-USDC'
and p.test_txn_yn = 'N'
order by p.pos_end_dttm desc
