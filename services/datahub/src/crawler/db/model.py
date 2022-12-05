from sqlalchemy import Column, DateTime, Integer, String, func, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

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
    address = Column(String(100), nullable=False)
    account_type = Column(String(100), nullable=False)
    balance = Column(BigInteger, nullable=False)
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

if engine:
    Base.metadata.create_all(engine)
