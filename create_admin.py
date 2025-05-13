import os
import sys
from werkzeug.security import generate_password_hash
from app import app, db
from models import Admin

def create_admin_user(username, password, is_super_admin=True):
    """Create an admin user in the database"""
    with app.app_context():
        # Check if admin already exists
        existing_admin = Admin.query.filter_by(username=username).first()
        if existing_admin:
            print(f"Admin user '{username}' already exists.")
            return False
        
        # Create new admin
        password_hash = generate_password_hash(password)
        new_admin = Admin(
            username=username,
            password_hash=password_hash,
            is_super_admin=is_super_admin
        )
        
        db.session.add(new_admin)
        db.session.commit()
        
        print(f"Admin user '{username}' created successfully!")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python create_admin.py <username> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    # Default to super admin
    is_super_admin = True
    
    # Create the admin user
    create_admin_user(username, password, is_super_admin)