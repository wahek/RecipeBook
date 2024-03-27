from django.db.models import QuerySet
from django.test import TestCase
from .models import Recipe, Ingredient, User, RecipeRating


class BaseTestCase(TestCase):
    """
    Base test case with common setup methods.
    """

    @staticmethod
    def create_user(*args: int) -> User | QuerySet[User]:
        """
        Creates a test users. If no arguments are provided, a single user is created.
        """
        try:
            for i in range(*args):
                User.objects.create_user(username=f'testuser{i}', email=f'test@example{i}', password='password',
                                         gender='M')
            return User.objects.all()
        except TypeError:
            return User.objects.create_user(username='testuser', email='test@example.com', password='password',
                                            gender='M')

    def create_recipe(self):
        return Recipe.objects.create(name='Test Recipe', description='Test Description', cooking_time=30,
                                     instructions='Test Instructions', author=self.create_user())


class RecipeModelTest(BaseTestCase):
    """
    Test cases for the Recipe model.

    Methods:
        setUp(self): Initializes necessary objects for testing.
        test_recipe_creation(self): Tests the creation of a Recipe instance.
        test_recipe_str(self): Tests the string representation of a Recipe instance.
    """

    def setUp(self):
        """
        Set up necessary objects for testing.
        This function creates a user and a recipe object for testing purposes.
        """
        self.recipe = self.create_recipe()
        self.user = self.recipe.author

    def test_recipe_creation(self) -> None:
        """
        Test case to verify the creation of a Recipe instance.
        """
        self.assertEqual(self.recipe.name, 'Test Recipe')
        self.assertEqual(self.recipe.description, 'Test Description')
        self.assertEqual(self.recipe.instructions, 'Test Instructions')
        self.assertEqual(self.recipe.cooking_time, 30)
        self.assertEqual(self.recipe.author, self.user)
        self.assertEqual(self.recipe.view, 0)
        self.assertTrue(self.recipe.is_active)

    def test_recipe_str(self) -> None:
        """
        Test case to verify the string representation of a Recipe instance.
        """
        self.assertEqual(str(self.recipe), 'Test Recipe')


class IngredientModelTest(TestCase):
    def setUp(self) -> None:
        self.ingredient = Ingredient.objects.create(name='Test Ingredient')

    def test_ingredient_creation(self) -> None:
        self.assertEqual(self.ingredient.name, 'Test Ingredient')

    def test_ingredient_str(self) -> None:
        self.assertEqual(str(self.ingredient), 'Test Ingredient')


class UserModelTest(BaseTestCase):

    def setUp(self) -> None:
        self.user = self.create_user()

    def test_user_creation(self) -> None:
        """
        Test user creation function to verify the attributes of the newly created user.
        """
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertNotEquals(self.user.password, 'password')
        self.assertEqual(self.user.gender, 'M')
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.is_superuser, False)

    def test_user_str(self) -> None:
        self.assertEqual(str(self.user), 'testuser')


class RecipeRatingModelTest(BaseTestCase):
    def setUp(self) -> None:
        self.recipe = self.create_recipe()
        self.user = self.recipe.author
        self.recipe_rating = RecipeRating.objects.create(user=self.user, recipe=self.recipe, rating=4)

    def test_recipe_rating_creation(self) -> None:
        self.assertEqual(self.recipe_rating.user, self.user)
        self.assertEqual(self.recipe_rating.recipe, self.recipe)
        self.assertEqual(self.recipe_rating.rating, 4)

    def test_recipe_rating_str(self) -> None:
        self.assertEqual(str(self.recipe_rating), f'{self.user.username} ({self.recipe_rating.rating})')
