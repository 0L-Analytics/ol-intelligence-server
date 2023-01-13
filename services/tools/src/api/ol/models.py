from sqlalchemy import Column, DateTime, Integer, String, func, Float, BigInteger, Boolean, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.expression import case
from typing import List
from datetime import datetime

try:
    from crawler.db import engine, session
except ModuleNotFoundError as err:
    engine = None


Base = declarative_base()


class PaymentEvent(Base):
    __tablename__ = "paymentevent"

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False, default=0)
    currency = Column(String(16), nullable=False)
    _metadata = Column(String(100), nullable=False)
    sender = Column(String(100))
    recipient = Column(String(100))
    type = Column(String(100), nullable=False)
    transactionkey = Column(String(100))
    seq = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class AccountTransaction(Base):
    __tablename__ = "accounttransaction"

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False)
    sequence_number = Column(Integer, nullable=False)
    version = Column(Integer, nullable=False)
    tx = Column(JSONB, nullable=False)
    hash = Column(String(64), nullable=False)
    vm_status = Column(JSONB)
    gas_used = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class AccountBalance(Base):
    __tablename__ = "accountbalance"

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False, unique=True)
    account_type = Column(String(100), nullable=False)
    balance = Column(BigInteger, nullable=False)
    wallet_type = Column(String(1), nullable=False, default='X')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    wallet_type_name = case(
        [(wallet_type == 'C', 'Community'),(wallet_type == 'S', 'Slow'),(wallet_type == 'N', 'Normal'),],
        else_ = 'Unknown'
        ).label("full_name")


class ValidatorSet(Base):
    __tablename__ = "validatorset"

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False, unique=True)
    ip = Column(String(15), nullable=False)
    is_active = Column(Boolean, default=False)
    _json = Column(JSONB, nullable=False)
    tower_epoch = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def load_validator_list(validator_list: List) -> None:
        try:
            if len(validator_list) > 0:
                # reset is_active flag
                u = update(ValidatorSet)
                u = u.values({"is_active": False})
                u = u.where(ValidatorSet.is_active == True)
                engine.execute(u)

                for val in validator_list:
                    id = session.query(ValidatorSet.id)\
                        .filter(ValidatorSet.address==val['account_address'])\
                        .first()
                    avs = ValidatorSet(
                        address = val['account_address'],
                        ip = val['validator_ip'],
                        is_active = True,
                        _json = val,
                        tower_epoch = val['tower_epoch']
                    )
                    if id:
                        avs.id = id[0]
                        session.merge(avs)
                    else:
                        session.add(avs)
                    session.commit()
        except Exception as e:
            # TODO add proper logging + throw specific exception to break when called in a loop
            print(f"[{datetime.now()}]:{e}")
        

class WalletDescription(Base):
    __tablename__ = "walletdescription"

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False, unique=True)
    program_name = Column(String(500), nullable=False, default='unknown') 
    description = Column(String(2000), nullable=False, default='unknown')
    focus = Column(String(50), nullable=False, default='unknown')
    manager = Column(String(200), nullable=False, default='unknown')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())



# class ChainEvent(Base):
#     __tablename__ = "chainevent"

#     id = Column(Integer, primary_key=True)
#     address = Column(String(100), nullable=False)
#     height = Column(Integer, nullable=False)
#     timestamp = Column(DateTime, nullable=True)
#     type = Column(String(100), nullable=True)
#     status = Column(String(100), nullable=True)
#     sender = Column(String(100), nullable=True)
#     recipient = Column(String(100), nullable=True)
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# class Epoch(Base):
#     __tablename__ = "epoch"

#     id = Column(Integer, primary_key=True)
#     epoch = Column(Integer, nullable=False, unique=True)
#     timestamp = Column(DateTime, nullable=True)
#     height = Column(Integer, nullable=False)
#     totalsupply = Column(Integer, nullable=True)
#     miners = Column(Integer, nullable=True)
#     proofs = Column(Integer, nullable=True)
#     minerspayable = Column(Integer, nullable=True)
#     minerspayableproofs = Column(Integer, nullable=True)
#     validatorproofs = Column(Integer, nullable=True)
#     minerpaymenttotal = Column(Float, nullable=True)
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# class NetworkStat(Base):
#     __tablename__ = "networkstat"

#     id = Column(Integer, primary_key=True)
#     height = Column(Integer, nullable=False)
#     epoch = Column(Integer, nullable=False)
#     progress = Column(Float, nullable=False)
#     totalsupply = Column(Integer, nullable=False)
#     totaladdresses = Column(Integer, nullable=False)
#     totalminers = Column(Integer, nullable=False)
#     activeminers = Column(Integer, nullable=False)
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# class EventLog(Base):
#     __tablename__ = "eventlog"

#     id = Column(Integer, primary_key=True)
#     event_source = Column(String(500), nullable=True)
#     type = Column(String(100), nullable=True)
#     subject = Column(String(1000), nullable=True)
#     message = Column(String(5000), nullable=True)
#     response = Column(String(5000), nullable=True)
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

# ENABLE IF MODEL NEEDS TO BE DEPLOYED FROM SCRATCH
# if engine:
#     Base.metadata.create_all(engine)
