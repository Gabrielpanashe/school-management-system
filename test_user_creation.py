from app.db.database import get_db
from app.models.user import User
from app.utils.security import get_password_hash

# Get database session
db = next(get_db())

try:
    # Try to create a test user directly
    test_user = User(
        email="test@example.com",
        password_hash=get_password_hash("TestPassword123"),
        first_name="Test",
        last_name="User",
        role="super_admin",
        school_id=None
    )
    
    db.add(test_user)
    db.commit()
    
    print("✅ User created successfully!")
    print(f"User ID: {test_user.id}")
    print(f"Email: {test_user.email}")
    
    # Try to find the user
    found_user = db.query(User).filter(User.email == "test@example.com").first()
    
    if found_user:
        print("✅ User found in database!")
    else:
        print("❌ User not found!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    
finally:
    db.close()