from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 게시판 기능 구현
class Board(models.Model): # models의 Model로부터 상속받겠다.
    subject = models.CharField(max_length=200) # subject(class속성(변수)):타이틀, 문자열로 담겠다.
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자 정보
    #like = models.IntegerField(blank=True, default=0) # 좋아요
    create_date = models.DateTimeField(auto_now_add=True) # 작성일(최초 등록)
    update_date = models.DateTimeField(auto_now=True) # 글이 등록될 때 자동으로 시간이 등록되도록 설정

    def __str__(self):
        # f: 형식을 만들겠다.
        # Board를 불러올 때, 제목을 [id][제목(subject)]로 출력
        return f'[{self.id}] {self.subject}' 

# 댓글 기능 구현
class Comment(models.Model): # models의 Model로부터 상속받겠다.
    board = models.ForeignKey(Board, on_delete=models.CASCADE) # 외래키 설정(종속관계 설정), 마음대로 삭제 안되게 설정
    content = models.TextField()    
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자 정보
    #like = models.IntegerField(blank=True, default=0) # 좋아요
    create_date = models.DateTimeField(auto_now_add=True) # 작성일(최초 등록)
    update_date = models.DateTimeField(auto_now=True) # 글이 등록될 때 자동으로 시간이 등록되도록 설정

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        # f: 형식을 만들겠다.
        # Board를 불러올 때, 제목을 [id][몇번:제목(댓글)]로 출력
        return f'[{self.board.id}:{self.board.subject}] {self.content}' 
