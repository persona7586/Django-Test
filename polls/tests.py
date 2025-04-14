import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse # view test) url을 하드코딩 하지 않도록 reverse를 import

from .models import Question

# Create your tests here.

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)


# date는 각 question 함수마다 재설정 되므로 필요할 때마다 그때그때 함수를 호출해서 만들어야 함
# test를 위해서 함수를 여러개 작성했는데 상황만 다르고 패턴은 같게 만듬
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
# test date를 만들기 위해 함수를 만듬 함수를 호출하게 되면 date하나가 만들어짐

class QuestionIndexViewTests(TestCase):
    # 상황을 만들어서 quest client가 요청을 하고, response를 받아서 원하는 값이 나오는지에 대해서 확인을 하는 것
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        # 첫번째 test case는 date가 없는 경우를 호출하여 상태코드 응답에 포함되어 있는 내용, context가 비어있는 것을 확인하는 코드. 같은 값인지 비교하는 경우에는 Equal을 쓰고, 포함되어 있는지는 Contains, Queryset인 경우에는 QuerysetEqual 이러한 test mathod를 사용해서 test진행. 이러한 패턴들을 익혀가면 좋음.

    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
        # 과거 date를 하나 만들고 호출한 다음에 date가 나오는지 확인 date가 나오지 않으면 문제가 있는 것

    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        # 미래 date를 만들고 date가 안나오는 경우를 확인 이 경우는 date가 나오면 문제가 있음

    def test_future_question_and_past_question(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
        # 미래 date, 과거 date 각각 한개씩 입력한 다음에 호출을 하면 과거 date만 나오는 모습을 확인

    def test_tow_past_question(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
        # 과거 date 2개를 입력했을 때는 date 2개가 나오는 모습 확인

        