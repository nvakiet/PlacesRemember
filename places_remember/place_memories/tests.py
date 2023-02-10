from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserMemories
from .forms import AddMemoryForm
from .views import UserMemoriesView, AddMemoryView
from django.core.management import call_command

class TestViewUserMemories(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        # Create a user to be used for all tests
        cls.user = (User.objects.create_user('testuser', 'sample_mail@example.com', 'testpassword', id=1))
        # Load data fixtures
        call_command("loaddata", "user_memories.json",app="place_memories", format="json")
        
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.is_logged_in = self.client.login(username='testuser', password='testpassword')
            
    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()
    
    def test_default_queryset(self):
        """Test the default query set fetching options
        """
        # Construct the query request with RequestFactory
        # to bypass middlewares
        url = reverse("place_memories:user_memories")
        request = RequestFactory().get(url)
        request.user = self.user
        # Call the view function directly
        view = UserMemoriesView()
        view.setup(request)
        qs = view.get_queryset()
        # Get the expected result
        excepted_qs = UserMemories.objects.filter(user_id=self.user.id).order_by("placename")
        # The queryset from the view function based on the request should be the same as the based query without request
        self.assertQuerysetEqual(qs, excepted_qs)
    
    def test_view_success(self):
        """Test the user memories when it successfully return the default page (sort by placename ascending).
        """
        # Ensure the client is logged in
        self.assertEqual(self.is_logged_in, True)
        # Fetch rendered template response
        url = reverse("place_memories:user_memories")
        response = self.client.get(url)
        # Assert response codes and correct template used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "place_memories/user_memories.html")
        # Assert important page contexts
        context = response.context
        self.assertIn("user", context)
        self.assertIn("page_obj", context)
        # Assert that the template is rendered with the correct objects
        self.assertContains(response, "Address:", UserMemoriesView.paginate_by)
        excepted_qs = UserMemories.objects.filter(user_id=self.user.id).order_by("placename")[:UserMemoriesView.paginate_by]
        for obj in excepted_qs:
            self.assertContains(response, f"Address: {obj.address}")
            

class TestViewAddMemory(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        # Create a user to be used for all tests
        cls.user = (User.objects.create_user('testuser', 'sample_mail@example.com', 'testpassword', id=1))
        # Load data fixtures
        call_command("loaddata", "user_memories.json",app="place_memories", format="json")
        
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.is_logged_in = self.client.login(username='testuser', password='testpassword')
            
    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()
    
    def test_get_add_memory_view(self):
        """Test the get method of AddMemoryView
        """
        # Ensure the client is logged in
        self.assertEqual(self.is_logged_in, True)
        # Fetch rendered template response
        url = reverse("place_memories:add_memory")
        response = self.client.get(url)
        # Assert response codes and correct template used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "place_memories/add_memory.html")
        # Assert all the required input fields
        fields = AddMemoryForm().fields
        self.assertContains(response, "Address:")
        self.assertContains(response, "id=\"id_address\"")
        self.assertContains(response, "Place name:")
        self.assertContains(response, "id=\"id_placename\"")
        self.assertContains(response, "Comment:")
        self.assertContains(response, "id=\"id_comment\"")
        
    def test_post_empty(self):
        # Ensure the client is logged in
        self.assertEqual(self.is_logged_in, True)
        # Fetch rendered template response
        url = reverse("place_memories:add_memory")
        response = self.client.post(url, {})
        # If the post data is empty, the response should be the same page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "place_memories/add_memory.html")
        
    def test_post_success(self):
        # Ensure the client is logged in
        self.assertEqual(self.is_logged_in, True)
        # # Post and fetch final redirected page
        url = reverse("place_memories:add_memory")
        response = self.client.post(url, {
            "address": "105 Test Street, District 23, Testing City",
            "placename": "Test Building",
            "comment": "This is a test record."
        }, follow=True)
        # If add memory success, we should end up at the user memories page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "place_memories/user_memories.html")
        # There should be a success alert in the redirected page
        self.assertContains(response, "Successfully added new memory!")