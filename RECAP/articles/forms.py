from django import forms
# models.py의 구조와 비슷함

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=50)
    content = forms.CharField(widget=forms.Textarea)

# 사용자는 무엇을 할지 모르므로 Validation이 필수이다.