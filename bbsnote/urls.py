from django.urls import path
from . import views # .: 현재 디렉토리

# bbsnote앱이 관ㄹ리하는 독립된 이름 공간 정의
app_name = "bbsnote"

urlpatterns = [
    path("", views.index, name="index"),
    #board_id는 숫자 값으로 넘김 / view.detail을 연결/ 별칭 detail
    path("<int:board_id>/", views.detail, name="detail"), # 상세페이지 기능 구현하기
    path("comment/create/<int:board_id>/", views.comment_create, name='comment_create'),
    path("board/create/", views.board_create, name='board_create'),
    path("board/modify/<int:board_id>/", views.board_modify, name='board_modify'),
    path("board/delete/<int:board_id>/", views.board_delete, name='board_delete'),
    path("comment/modify/<int:comment_id>/", views.comment_modify, name='comment_modify'),
    path("comment/delete/<int:comment_id>/", views.comment_delete, name='comment_delete'),
    ]