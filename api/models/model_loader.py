from . import (
    users,
    categories,
    menu_items,
    orders,
    order_items,
    payments,
    reviews,
    resources,
    promotions
)

from ..dependencies.database import engine


def index():
    users.Base.metadata.create_all(engine)
    categories.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    orders.Base.metadata.create_all(engine)
    order_items.Base.metadata.create_all(engine)
    payments.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
