from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item

engine = create_engine('sqlite:///item_catalog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create Category
Basketball = Category(name="Basketball")
session.add(Basketball)
session.commit()

# Item for Basketball
sneakers = Item(name="Sneakers", description="Nike Air Force Ones - Pure White", cat_id=1)

session.add(sneakers)
session.commit()

basketball = Item(name="Basketball", description="Spaldin Professional leather basketball", cat_id=1)

session.add(basketball)
session.commit()

court = Item(name="Basketball court", description="Adjustable sand filled basketball rim up to 10 feet", cat_id=1)

session.add(court)
session.commit()

# Create Category
Football = Category(name="Football")
session.add(Football)
session.commit()

# Item for Football
cleats = Item(name="Cleats", description="Nike custom design cleats - size 13", cat_id=2)

session.add(cleats)
session.commit()

football = Item(name="Football", description="Spaldin Professional leather football", cat_id=2)

session.add(football)
session.commit()

pads = Item(name="Shoulder Pads", description="Shoulder pads for ages 15 and below", cat_id=2)

session.add(pads)
session.commit()

# Create Category
Baseball = Category(name="Baseball")
session.add(Basketball)
session.commit()

# Item for Baseball
cleats = Item(name=" Baseball Cleats", description="Addidas custom design cleats - size 13", cat_id=3)

session.add(cleats)
session.commit()

bat = Item(name=" Baseball bat", description="Hybrid baseball bat. Wooden bat with a metal core", cat_id=3)

session.add(bat)
session.commit()

gloves = Item(name="Catcher's Glove", description="Premium Leather catchers glove...Size XL", cat_id=3)

session.add(court)
session.commit()

# Create Category
Voleyball = Category(name="Voleyball")
session.add(Voleyball)
session.commit()

# Item for Voleyball
ball = Item(name="Voleyball", description="Premium Leather VoleyballL", cat_id=4)

session.add(ball)
session.commit()

net = Item(name="Voleyball", description="Full Size Voleyball net. Everything included to play immediately. Ball puchased Seperately", cat_id=4)

session.add(net)
session.commit()

jersey = Item(name="Volleyball Jerseys", description="Fully Customizable jersey from color to size to font, but it will cost you", cat_id=4)

session.add(jersey)
session.commit()

print "added Category and items"
