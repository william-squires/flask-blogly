from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
# An alternative if you don't want to drop
# and recreate your tables:
# User.query.delete()

#Add users

bob = User(first_name='Bob', last_name='Ross', 
            image_url="https://www.bobross.com/content/bob_ross_img.png")
rick = User(first_name="Rick", last_name="Astley", 
    image_url="https://www.nme.com/wp-content/uploads/2021/07/RickAstley2021-1392x884.jpg")
samira = User(first_name='Samira', last_name='Brandt',
     image_url="")
peggy = User(first_name='Peggy', last_name='Sanchez',
     image_url="")
tahlia = User(first_name='Tahlia', last_name='Tyler',
     image_url="")
susie = User(first_name='Susie', last_name='Espinoza', 
    image_url="")
gracie = User(first_name='Gracie', last_name='Wood', 
    image_url="")
roosevelt = User(first_name='Roosevelt', last_name='Eaton', 
    image_url="")
millie = User(first_name='Millie', last_name='Norris', 
    image_url="")
maximus = User(first_name='Maximus', last_name='Davila', 
    image_url="")
krish = User(first_name='Krish', last_name='Rivera', 
    image_url="")
alex = User(first_name='Alex', last_name='Mathews', 
    image_url="")

# Add new objects to session, so they'll persist
db.session.add(bob)
db.session.add(rick)
db.session.add(samira)
db.session.add(peggy)
db.session.add(tahlia)
db.session.add(susie)
db.session.add(gracie)
db.session.add(roosevelt)
db.session.add(millie)
db.session.add(maximus)
db.session.add(krish)
db.session.add(alex)

#commit
db.session.commit()