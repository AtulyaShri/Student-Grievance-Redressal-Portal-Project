from sqlalchemy.orm import declarative_base


Base = declarative_base()

# Optional: expose metadata for Alembic/autogenerate
metadata = Base.metadata
