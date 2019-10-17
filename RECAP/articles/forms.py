from django import forms
from .models import Article, Comment
# models.py의 구조와 비슷함

# class ArticleForm(forms.Form):
#     title = forms.CharField(
#         max_length=20,
#         label='제목',
#         help_text='제목은 20자 이내로 입력해주세요.',
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control my-title',
#                 'placeholder': '제목을 입력해주세요.',
#             }
#         ),


#         )
#     content = forms.CharField(
#         label='내용',
#         widget=forms.Textarea(
#             attrs={
#                 'class': 'form-control my-content',
#                 'placeholder': '내용을 입력해주세요',
#                 'rows': 5,
#             }

#         )
#     )
# 사용자는 무엇을 할지 모르므로 Validation이 필수이다.

# modelForm ->앞으로는 이것만 사용
class ArticleForm(forms.ModelForm):
    class Meta:
        # 어떤 정보를 가지고 있을지에 대한 정보를 제공함
        model = Article
        fields = ('title', 'content',)
        # exclude 라는 것을 사용하면 form을 생략한다
        #################### 권고되지 않는 스타일 
        # widget을 제외한 어트리뷰트들을 사용하기는 어려울 수 있음
        # widgets = {
        #     #'title': forms.Textarea
        #     'title' : forms.TextInput(attrs={
        #         'placeholder': '제목을 입력해주세요.',
        #         'class': 'form-control title-class',
        #         'id': 'title',
        #     })
        # }

        # label = {
        #     'title':~
        # }
        ##########################################
    ########## 추천버전
    title = forms.CharField(
        max_length=20,
        label='제목',
        help_text='제목은 20자 이내로 입력해주세요.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control my-title',
                'placeholder': '제목을 입력해주세요.',
            }
        ),
    )
    ##########################
        #fields = '__all__' #model의 모든 필드를 가지고 옴
        # widgets = {
        #     '필드(칼럼)': Form 속성
        # }
    # 만들어주는 폼 스타일의 양식은 기본적으로 model의 field name에 해당됨
    ################

class CommentForm(forms.ModelForm):
    #models.py에서 연동한 article 클래스는 자동으로 찾아준다.
    class Meta:
        model = Comment
        fields = ('content',)