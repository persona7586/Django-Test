from django.contrib import admin

from .models import Question, Choice
# Register your models here.

# question admin 위치에서 Choice 관리할 수 있게 설정
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3 # 3개의 데이터 입력란이 생김

class QuestionAdmin(admin.ModelAdmin):
    # 개별 필드를 표시 list_display admin 옵션 사용
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline] # question admin 위치에서 Choice 관리할 수 있게 설정

    list_filter = ['pub_date']
    search_fields = ['question_text']

# admin.site.register(Question)
admin.site.register(Question, QuestionAdmin) # 관리자 폼 커스터마이징
# admin.site.register(Choice)

