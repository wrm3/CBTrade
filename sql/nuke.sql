


delete from cbtrade.buy_ords where bo_id in (select bo_id from cbtrade.poss p where pos_id in (2568,4461) ) ;
delete from cbtrade.sell_ords where pos_id in (2568,4461) ;
delete from cbtrade.poss where pos_id in (2568,4461) ;
