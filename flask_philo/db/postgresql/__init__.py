def syncdb():
    """
    Create tables if they don't exist
    """
    from flask_philo.db.postgresql.schema import Base
    from flask_philo.db.postgresql.orm import BaseModel  # noqa
    from flask_philo.db.postgresql.connection import get_pool

    for conn_name, conn in get_pool().connections.items():
        Base.metadata.create_all(conn.engine)
