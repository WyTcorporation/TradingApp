from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from database import metadata

operation = Table(
    'operation',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('quantity', String),
    Column('figi', String),
    Column('instrument_type', String(length=1024), nullable=True),
    Column('date', TIMESTAMP),
    Column('type', String),
)
