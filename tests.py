from models import User, db
from app import app
from unittest import TestCase
import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_add_user(self):
        """Tests adding a user to database"""

        with self.client as c:
            response = c.post("/users/new",
                              data={"first_name": "Bob",
                                    "last_name": "Smith",
                                    "img_url": ""})

            user = User().query.filter(
                User.first_name == "Bob",
                User.last_name == "Smith").one()

            # Make sure user in database
            self.assertEqual(user.first_name, "Bob")
            self.assertEqual(user.last_name, "Smith")
            # Make sure we redirect
            self.assertAlmostEqual(response.status_code, 302)

    def test_show_new_user_form(self):
        """Tests showing new user form"""

        with self.client as c:
            response = c.get('/users/new')            
            html = response.get_data(as_text=True)

            self.assertIn("Add New User",html)
            self.assertEqual(response.status_code, 200)

    def test_show_user_info(self):
        """Tests showing user info"""

        with self.client as c:
            response = c.get(f"/users/{self.user_id}")
            html = response.get_data(as_text=True)
            # breakpoint()
            self.assertIn("<h1>test1_first test1_last </h1>", html)
            self.assertEqual(response.status_code, 200)   

    def test_show_edit_user(self):
        """Tests showing edit user form"""

        with self.client as c:
            response = c.get(f"/users/{self.user_id}/edit")         
            html = response.get_data(as_text=True)
          
            self.assertIn("<h1>Edit user information</h1>", html)
            self.assertEqual(response.status_code, 200)   