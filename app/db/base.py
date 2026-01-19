


"""
Import all SQLAlchemy models here.
This ensures they are registered with Base.metadata
before running migrations.
"""

from app.db.database import Base

from app.models.school import School
from app.models.user import User 

# We'll import models here as we create them
# from app.models.user import User
# from app.models.student import Student
# etc.
