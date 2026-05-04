from . import orders, order_items


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_items.router)
