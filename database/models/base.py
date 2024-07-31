from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    registry,
)  # required: there would be messages saying there are already models instances in metadata

Base = declarative_base()
