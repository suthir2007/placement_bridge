import sys
import os
from app import create_app, db

app = create_app()


def ensure_demo_seed(app_instance=None):
    """Create the schema and seed demo accounts when the database is empty."""
    target_app = app_instance or app
    with target_app.app_context():
        db.create_all()
        from app.models.user import User
        if not User.query.first():
            from seed import seed_db
            seed_db(target_app)


@app.cli.command("seed")
def seed_command():
    """Runs database seed script."""
    from seed import seed_db
    seed_db(app)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'seed':
        from seed import seed_db
        seed_db(app)
    else:
        ensure_demo_seed(app)
        app.run(host='0.0.0.0', port=5000, debug=True)
