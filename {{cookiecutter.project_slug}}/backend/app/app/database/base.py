# Import all the models, so that Base has them before being
# imported by Alembic
from app.database.base_class import Base  # noqa
from app.database.models.item import Item  # noqa
from app.database.models.user import User  # noqa
