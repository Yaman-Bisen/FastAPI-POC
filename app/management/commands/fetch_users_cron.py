from typing import Optional
from sqlalchemy.orm import Session
# from config.Database.database import SessionLocal, engine
# from app.models import Users
from app.management.setup_commands import Command, register_command


@register_command
class ListUsersCommand(Command):
    name = "list_users"
    help = "List users from the database with optional filtering"
    
    def handle(self, limit: Optional[int] = 10, email_filter: Optional[str] = None):
        print(f"Fetching users (limit: {limit}, filter: {email_filter})")
        
        # # Create database session
        # db = SessionLocal()
        # try:
        #     # Build query
        #     query = db.query(User)
            
        #     # Apply filters
        #     if email_filter:
        #         query = query.filter(User.email.contains(email_filter))
            
        #     # Apply limit
        #     query = query.limit(limit)
            
        #     # Execute query
        #     users = query.all()
            
        #     # Print results
        #     if not users:
        #         logger.info("No users found")
        #         return
            
        #     logger.info(f"Found {len(users)} users:")
        #     for user in users:
        #         logger.info(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
            
        #     # Print summary
        #     total_users = db.query(User).count()
        #     logger.info(f"Displayed {len(users)} of {total_users} total users")
            
        # except Exception as e:
        #     logger.error(f"Error fetching users: {e}")
        # finally:
        #     db.close()