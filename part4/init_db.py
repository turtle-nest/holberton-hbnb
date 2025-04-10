#!/usr/bin/env python3
from app import create_app
from app.extensions import db, bcrypt
from app.models import User, Place, Review, Amenity

app = create_app()

with app.app_context():
    print("✅ App context OK")
    try:
        db.drop_all()
        db.create_all()
        print("✅ Tables reset and created")
    except Exception as e:
        print("❌ Erreur de création des tables :", e)

    # --- Users ---
    password1 = bcrypt.generate_password_hash("password123").decode("utf-8")
    user1 = User(first_name="Alice", last_name="Doe", email="alice@example.com", password=password1)
    
    password2 = bcrypt.generate_password_hash("password456").decode("utf-8")
    user2 = User(first_name="Bob", last_name="Smith", email="bob@example.com", password=password2)
    
    db.session.add_all([user1, user2])
    db.session.commit()
    print("👤 Users created")

    # --- Amenities ---
    wifi = Amenity(name="Wi-Fi")
    parking = Amenity(name="Free Parking")
    pool = Amenity(name="Swimming Pool")
    kitchen = Amenity(name="Kitchen")

    db.session.add_all([wifi, parking, pool, kitchen])
    db.session.commit()
    print("🏷️ Amenities created")

    # --- Places ---
    places = [
        Place(
            title="Sunny Beach House",
            description="Beautiful beach house with ocean view and modern amenities.",
            price=120.0,
            latitude=43.61092,
            longitude=3.87772,
            user_id=user1.id,
            image_url="/static/images/places/beach.jpg"
        ),
        Place(
            title="Cozy Mountain Cabin",
            description="A peaceful retreat in the mountains, perfect for a winter getaway.",
            price=90.0,
            latitude=45.9248,
            longitude=6.8694,
            user_id=user2.id,
            image_url="/static/images/places/cabin.jpg"
        ),
        Place(
            title="Urban Loft",
            description="Modern loft located downtown, walking distance from major attractions.",
            price=150.0,
            latitude=48.8566,
            longitude=2.3522,
            user_id=user1.id,
            image_url="/static/images/places/loft.jpg"
        )
    ]

    db.session.add_all(places)
    db.session.commit()
    print("🏡 Places added")

    # --- Link amenities to places ---
    places[0].amenities.extend([wifi, pool])
    places[1].amenities.extend([parking, kitchen])
    places[2].amenities.extend([wifi, kitchen, parking])
    db.session.commit()
    print("🔗 Amenities linked to places")

    # --- Reviews ---
    reviews = [
        Review(text="Amazing view and great location!", rating=5, place_id=places[0].id, user_id=user2.id),
        Review(text="Very cozy, we loved the fireplace.", rating=4, place_id=places[1].id, user_id=user1.id),
        Review(text="Perfect spot for a city break.", rating=5, place_id=places[2].id, user_id=user2.id)
    ]

    db.session.add_all(reviews)
    db.session.commit()
    print("📝 Reviews added")

    print("🎉 Database initialization complete with 3 places, 2 users, amenities and reviews.")
