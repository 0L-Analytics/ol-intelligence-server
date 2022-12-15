from src import db
from src.api.oldata.models import (
    AccountBalance, 
    PaymentEvent, 
    AccountTransaction, 
    ValidatorSet
)
from src.api.connect import session, engine
from sqlalchemy.sql.expression import cast, func, label, text
from sqlalchemy import Integer


def get_acc_balances():
    return session.query(
        AccountBalance.id, 
        AccountBalance.address,
        AccountBalance.account_type,
        label("balance", cast(AccountBalance.balance / 1000000, Integer)),
        AccountBalance.updated_at)\
            .filter(AccountBalance.account_type=='community')\
            .all()


def get_acc_balance_by_type():
    out_py = {
        "data": [],
        "sum_balance": 0,
        "sum_count": 0,
    }

    acc_balances = session.query(
        AccountBalance.account_type,
        label("balance", cast(func.sum(AccountBalance.balance) / 1000000, Integer)),
        label("count", func.count(AccountBalance.id), Integer))\
            .group_by(AccountBalance.account_type)\
            .order_by(AccountBalance.account_type)\
            .all()
    
    acc_balance_sums = session.query(
        label("sum_balance", cast(func.sum(AccountBalance.balance) / 1000000, Integer)),
        label("sum_count", func.count(AccountBalance.id), Integer))\
            .first()
    
    out_py["data"] = acc_balances
    out_py["sum_balance"] = 0 if 'sum_balance' not in acc_balance_sums else int(acc_balance_sums['sum_balance'])
    out_py["sum_count"] = 0 if 'sum_count' not in acc_balance_sums else int(acc_balance_sums['sum_count'])
    
    return out_py


def get_payment_events_by_account(addr, seq_start, limit):
    return session.query(
        AccountTransaction.address,
        AccountTransaction.sequence_number,
        AccountTransaction.version,
        AccountTransaction.tx,
        AccountTransaction.hash,
        AccountTransaction.vm_status,
        AccountTransaction.gas_used,
        AccountTransaction.created_at)\
            .filter(
                AccountTransaction.address==addr, 
                AccountTransaction.sequence_number>=seq_start)\
            .order_by(AccountTransaction.sequence_number)\
            .limit(limit)\
            .all()


def get_active_validator_set():
    return session.query(
        ValidatorSet.id,
        ValidatorSet.address,
        ValidatorSet.ip,
        ValidatorSet._json,
        ValidatorSet.tower_epoch,
        ValidatorSet.updated_at)\
            .filter(ValidatorSet.is_active==True)\
            .all()


def get_tokenomics():
    sql = text("with base_table as ("
               "    select" 
               "     round(sum(balance)/1000000.0, 2) as balance,"
               "    count(*) as cnt,"
               "        account_type,"
               "        wallet_type"
               "    from accountbalance"
               "    group by"
               "        account_type,"
               "        wallet_type"
               ")"
               ", base_table2 as ("
               "    select"
               "        row_number() over (order by balance desc) as ranknr,"
               "        address,"
               "        round(balance/1000000.0, 2) as balance"
               "    from accountbalance"
               "    where account_type <> 'community'"
               "    order by balance desc"
               "    limit 100"
               ")"
               ", totals as ("
               "    select sum(balance) as total_balance,"
               "    sum(cnt) as total_addr_cnt"
               "    from base_table"
               ")"
               ", tops as ("
               "    select "
               "        round(top10_balance) as top10_balance,"
               "        round(top100_balance) as top100_balance,"
               "        round(top10_balance_nv) as top10_balance_nv,"
               "        round(sum_bal_ex_com) as sum_bal_ex_com,"
               "        round(sum_bal_ex_com_val) as sum_bal_ex_com_val,"
               "        round(top10_balance / sum_bal_ex_com * 100, 2) as top10_perc,"
               "        round(top10_balance_nv / sum_bal_ex_com_val * 100, 2) as top10_nv_perc,"
               "        round(top100_balance / sum_bal_ex_com * 100, 2) as top100_perc"
               "    from ("
               "        select sum(balance) as top10_balance"
               "        from base_table2"
               "        where ranknr <= 10"
               "    ) a cross join ("
               "        select sum(balance) as top100_balance"
               "        from base_table2"
               "    ) b cross join ("
               "        select sum(balance) as sum_bal_ex_com"
               "        from base_table"
               "        where account_type <> 'community'"
               "    ) c cross join ("
               "        select sum(balance) as top10_balance_nv"
               "        from ("
               "            select round(balance/1000000.0, 2) balance"
               "            from accountbalance"
               "            where account_type not in ('validator', 'community')"
               "            order by 1 desc"
               "            limit 10"
               "        ) i"
               "    ) d cross join ("
               "        select sum(balance) as sum_bal_ex_com_val"
               "        from base_table"
               "        where account_type not in ('community', 'validator')"
               "    ) e"
               ")"
               ", addr_cnt_bal_gt1 as ("
               "    select count(*) as addr_cnt_bal_gt1"
               "    from accountbalance"
               "    where balance > 1"
               ")"
               ", liquidity as ("
               "    select"
               "        sum(case "
               "                when wallet_type = 'C' then balance"
               "                else NULL"
               "            end) as bal_community,"
               "        sum(case "
               "                when wallet_type = 'S' then balance"
               "                else NULL"
               "            end) as bal_slow,"
               "        sum(case "
               "                when wallet_type = 'N' then balance"
               "                else NULL"
               "            end) as bal_liquid,"
               "        sum(case "
               "                when wallet_type = 'C' then cnt"
               "                else NULL"
               "            end) as cnt_community,"
               "        sum(case "
               "                when wallet_type = 'S' then cnt"
               "                else NULL"
               "            end) as cnt_slow,"
               "        sum(case "
               "                when wallet_type = 'N' then cnt"
               "                else NULL"
               "            end) as cnt_liquid"
               "    from base_table"
               ")"
               ", validator_set as ("
               "    select active_set_cnt, validator_cnt"
               "    from ("
               "        select count(*) as validator_cnt"
               "        from accountbalance"
               "        where account_type = 'validator'"
               "    ) a cross join ("
               "        select count(*) as active_set_cnt"
               "        from validatorset"
               "        where is_active = true"
               "    ) b"
               ")"
               "select "
               "    round(total_balance) as total_balance, "
               "    total_addr_cnt,"
               "    top10_balance,"
               "    top100_balance,"
               "    top10_balance_nv,"
               "    top10_perc,"
               "    top100_perc,"
               "    top10_nv_perc,"
               "    round(sum_bal_ex_com) as sum_bal_ex_com,"
               "    round(sum_bal_ex_com_val) as sum_bal_ex_com_val,"
               "    addr_cnt_bal_gt1.addr_cnt_bal_gt1,"
               "    round(bal_community) as bal_community,"
               "    round(bal_slow) as bal_slow,"
               "    round(bal_liquid) as bal_liquid,"
               "    round(cnt_community) as cnt_community,"
               "    round(cnt_slow) as cnt_slow,"
               "    round(cnt_liquid) as cnt_liquid,"
               "    active_set_cnt, "
               "    validator_cnt "
               "from totals tot"
               "    cross join tops"
               "    cross join addr_cnt_bal_gt1"
               "    cross join liquidity"
               "    cross join validator_set")
    with engine.connect() as con:
        res = con.execute(sql)
        out = {}
        for l in res:
            out["total_balance"] = l[0]
            out["total_addr_cnt"] = l[1]
            out["top10_balance"] = l[2]
            out["top100_balance"] = l[3]
            out["top10_balance_nv"] = l[4]
            out["top10_perc"] = l[5]
            out["top100_perc"] = l[6]
            out["top10_nv_perc"] = l[7]
            out["sum_bal_ex_com"] = l[8]
            out["sum_bal_ex_com_val"] = l[9]
            out["addr_cnt_bal_gt1"] = l[10]
            out["bal_community"] = l[11]
            out["bal_slow"] = l[12]
            out["bal_liquid"] = l[13]
            out["cnt_community"] = l[14]
            out["cnt_slow"] = l[15]
            out["cnt_liquid"] = l[16]
            out["active_set_cnt"] = l[17]
            out["validator_cnt"] = l[18]
    return out
