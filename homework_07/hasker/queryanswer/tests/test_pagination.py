from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse

from queryanswer.models import Question
from queryanswer.views import QuestionsListView
from user.models import User

class QuestionListPaginationTest(TestCase):
    """test pagination on main page"""

    ACTIVE_PAGINATION_HTML = """
    <li class="active">
        <a href="{}?page={}" class="page-active">{}</a>}
    </li>
    """

    def setUp(self):
        for q in range(40):
            Question.objects.create(
                slug='slug-1{}'.format(q),
                title='Title {}'.format(q),
                user=User.objects.all()[1],
            )

    def testFirstPage(self):
        # resolve the name into a path
        question_list_path = reverse('index')
        # factory for creating fake HTTP request
        request = RequestFactory().get(path=question_list_path)
        response = QuestionsListView.as_view()(request)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context_data['is_paginated'])
        self.assertInHTML(
            self.ACTIVE_PAGINATION_HTML.format(question_list_path, 1, 1),
            response.rendered_content
        )