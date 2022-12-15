-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- Tokenomics single measures
with base_table as (
    select 
        round(sum(balance)/1000000.0, 2) as balance,
        count(*) as cnt,
        account_type,
        wallet_type
    from accountbalance
    group by
        account_type,
        wallet_type
)
, base_table2 as (
    select
        row_number() over (order by balance desc) as ranknr,
        address,
        round(balance/1000000.0, 2) as balance
    from accountbalance
    where account_type <> 'community'
    order by balance desc
    limit 100
)
, totals as (
    select sum(balance) as total_balance,
    sum(cnt) as total_addr_cnt
    from base_table
)
, tops as (
    select 
        round(top10_balance) as top10_balance,
        round(top100_balance) as top100_balance,
        round(top10_balance_nv) as top10_balance_nv,
        round(sum_bal_ex_com) as sum_bal_ex_com,
        round(sum_bal_ex_com_val) as sum_bal_ex_com_val,
        round(top10_balance / sum_bal_ex_com * 100, 2) as top10_perc,
        round(top10_balance_nv / sum_bal_ex_com_val * 100, 2) as top10_nv_perc,
        round(top100_balance / sum_bal_ex_com * 100, 2) as top100_perc

    from (
        select sum(balance) as top10_balance
        from base_table2
        where ranknr <= 10
    ) a cross join (
        select sum(balance) as top100_balance
        from base_table2
    ) b cross join (
        select sum(balance) as sum_bal_ex_com
        from base_table
        where account_type <> 'community'
    ) c cross join (
        select sum(balance) as top10_balance_nv
        from (
            select round(balance/1000000.0, 2) balance
            from accountbalance
            where account_type not in ('validator', 'community')
            order by 1 desc
            limit 10
        ) i
    ) d cross join (
        select sum(balance) as sum_bal_ex_com_val
        from base_table
        where account_type not in ('community', 'validator')
    ) e
)
, addr_cnt_bal_gt1 as (
    select count(*) as addr_cnt_bal_gt1
    from accountbalance
    where balance > 1
)
, liquidity as (
    select
        sum(case 
                when wallet_type = 'C' then balance
                else NULL
            end) as bal_community,
        sum(case 
                when wallet_type = 'S' then balance
                else NULL
            end) as bal_slow,
        sum(case 
                when wallet_type = 'N' then balance
                else NULL
            end) as bal_liquid,
        sum(case 
                when wallet_type = 'C' then cnt
                else NULL
            end) as cnt_community,
        sum(case 
                when wallet_type = 'S' then cnt
                else NULL
            end) as cnt_slow,
        sum(case 
                when wallet_type = 'N' then cnt
                else NULL
            end) as cnt_liquid
    from base_table
)
, validator_set as (
    select active_set_cnt, validator_cnt
    from (
        select count(*) as validator_cnt
        from accountbalance
        where account_type = 'validator'
    ) a cross join (
        select count(*) as active_set_cnt
        from validatorset
        where is_active = true
    ) b
)
select 
    round(total_balance) as total_balance, 
    total_addr_cnt,
    top10_balance,
    top100_balance,
    top10_balance_nv,
    top10_perc,
    top100_perc,
    top10_nv_perc,
    round(sum_bal_ex_com) as sum_bal_ex_com,
    round(sum_bal_ex_com_val) as sum_bal_ex_com_val,
    addr_cnt_bal_gt1.addr_cnt_bal_gt1,
    round(bal_community) as bal_community,
    round(bal_slow) as bal_slow,
    round(bal_liquid) as bal_liquid,
    round(cnt_community) as cnt_community,
    round(cnt_slow) as cnt_slow,
    round(cnt_liquid) as cnt_liquid,
    active_set_cnt, 
    validator_cnt
from totals tot
    cross join tops
    cross join addr_cnt_bal_gt1
    cross join liquidity
    cross join validator_set;


-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- slide 3 - Tokens by account_type
-->> ORM

-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- slide 4, 5 
-->> Don't make much sense to me anymore...

-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- slide 6 - Whales
with totals as (
    select sum(balance)/1000000 as total
    from accountbalance
    where account_type <> 'community'
)
select 
    address,
    balance/1000000 as balance,
    round(((balance/1000000.0)/total)*100, 2) as percentage
from accountbalance ab
    cross join totals t
where account_type <> 'community'
order by balance desc
LIMIT 10;


-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- slide 7 - Non validator whales
with totals as (
    select sum(balance)/1000000 as total
    from accountbalance
    where account_type not in ('community')
)
select 
    address,
    balance/1000000 as balance,
    round(((balance/1000000.0)/total)*100, 2) as percentage
from accountbalance ab
    cross join totals t
where account_type not in ('community', 'validator')
order by balance desc
LIMIT 10;


-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- slide 9 & 10 - Community wallets - internal vs external
-- with base_table as (
--     select 
--         ab.address, 
--         wd.focus, 
--         ab.balance/1000000.0, 
--         wd.program_name
--     from accountbalance ab 
--         inner join walletdescription wd on 
--             lower(ab.address) = lower(wd.address)
--     where ab.account_type = 'community'
--     and lower(wd.description) not like '%test%'
-- )
-- , sumzz as (
--     select sum(balance) as total
--     from base_table
-- )
-- select bt.*, round(bt.balance/sz.total, 2) as percentage 
-- from base_table bt
--     cross join sumzz sz


-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- slide 11 - Address holders by account_type
-->> ORM

-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- slide 12 - Address holders
-->> Doesn't make much sense to me

-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- slide 13 - Coin distribution by top addresses
with addr_bal_base as (
    select address, 
        round(balance/1000000.0, 2) as balance, 
        row_number() over (order by balance desc) as nr
    from accountbalance
    where account_type <> 'community'
    order by 2 desc
)
, addr_bal_buckets as (
    select 
        round(sum(balance)) as bucket_balance,
        case 
            when nr between 1 and 10 then 'Top 10' 
            when nr between 10 and 20 then 'Top 20'
            when nr between 20 and 50 then 'Top 50'
            when nr between 50 and 100 then 'Top 100'
            when nr between 100 and 500 then 'Top 500'
            when nr <= 1000 then 'Top 1000'
            else 'All'
        end as bucket_name,
        case 
            when nr between 1 and 10 then 1
            when nr between 10 and 20 then 2
            when nr between 20 and 50 then 3
            when nr between 50 and 100 then 4
            when nr between 100 and 500 then 5
            when nr <= 1000 then 6
            else 7
        end as bucket_order
    from addr_bal_base
    group by 
        case 
            when nr between 1 and 10 then 'Top 10' 
            when nr between 10 and 20 then 'Top 20'
            when nr between 20 and 50 then 'Top 50'
            when nr between 50 and 100 then 'Top 100'
            when nr between 100 and 500 then 'Top 500'
            when nr <= 1000 then 'Top 1000'
            else 'All'
        end,
        case 
            when nr between 1 and 10 then 1
            when nr between 10 and 20 then 2
            when nr between 20 and 50 then 3
            when nr between 50 and 100 then 4
            when nr between 100 and 500 then 5
            when nr <= 1000 then 6
            else 7
        end
    order by 3
)
select 
    bucket_balance,
    bucket_name,
    sum(bucket_balance) over (order by bucket_order) as bucket_running_sum,
    bucket_order
from addr_bal_buckets
order by bucket_order;


-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- slide 14 - Adress balance distribution
with addr_bal_base as (
    select address, 
        round(balance/1000000.0, 2) as balance, 
        row_number() over (order by balance desc) as nr
    from accountbalance
    where account_type <> 'community'
    order by 2 desc
)
, addr_bal_counts as (
    select count(*) addr_cnt, 
        sum(balance) as total_balance,
        trunc(count(*) / 200) as bucket_size
    from addr_bal_base
)
select trunc(nr / bucket_size) + 1 as bucket_nr,
    round(sum(balance)) as balance,
    -- count(*) as cnt,
    min(nr) || '-' || max(nr) bucket_name
from addr_bal_base a 
    cross join addr_bal_counts b
group by trunc(nr / bucket_size) + 1
order by 1;
