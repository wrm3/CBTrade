


delete from cbtrade.buy_ords where bo_id in (select bo_id from cbtrade.poss p where pos_id in (2568,4461) ) ;
delete from cbtrade.sell_ords where pos_id in (2568,4461) ;
delete from cbtrade.poss where pos_id in (2568,4461) ;

select * from cbtrade.sell_ords where so_id = 25092;
select * from cbtrade.poss where pos_id = 26294

select * from cbtrade.poss where pos_stat = 'OPEN' and test_txn_yn = 'Y' and gain_loss_pct_est > 0;
update cbtrade.poss set force_sell_tf = 1 where pos_stat = 'OPEN' and test_txn_yn = 'Y' and gain_loss_pct_est > 1;


use ohlcv;
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'ohlcv' 
  AND table_name LIKE 'ohlcv_%';
  