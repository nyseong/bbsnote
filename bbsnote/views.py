from django.shortcuts import render, redirect, get_object_or_404
#from django.http import HttpResponse
from .models import Board, Comment
from django.utils import timezone
from .forms import BoardForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def index(request): # request: HttpResponse의 요처을 실행하겠다
    #return HttpResponse("bbsnote에 오신 것을 환영합니다!")
    # 입력인자
    page = request.GET.get('page', 1) # 페이지가 있으면 그 값을 가져오고, 없으면 1로 가져오겠다.
    # 조회
    board_list = Board.objects.order_by('-create_date') # Board의 object(객체)를 역순(-)정렬해서 가져오겠다.
    # 페이징 처리
    paginator = Paginator(board_list, 5) # 5개씩 쪼개서 페이지를 구성하겠다.
    page_obj = paginator.get_page(page) # 입력인자의 page를 넘겨준후 page_obj에 담는다.
    context = {'board_list': page_obj} # 딕셔너리 타입
    return render(request, 'bbsnote/board_list.html', context) #bbsnote/board_list.html의 context를 찾아서 요청하겠다.(출력)
    #return render(request, 'bbsnote/board_list.html', {'board_list': board_list})

def detail(request, board_id):
    # Board.objects.get: SELECT * FROM bbsnote_Board
    # (id=board_id): WHERE id = board_id
    board = Board.objects.get(id=board_id) # get()함수는 가져오는 역할
    context = {"board" : board}
    return render(request, 'bbsnote/board_detail.html', context) # 이제 board_detail.html 만들어야함

# 댓글 기능 함수 만들기
@login_required(login_url='common:login') # 애너테이션 적용, 로그인이 되었는지 우선 검사하여 오류 방지
def comment_create(request, board_id): # board_id를 요청
    if request.method == 'POST':
        board = Board.objects.get(id=board_id) # board정보를 가져오기
        comment = Comment(board=board, content=request.POST.get("content"), create_date=timezone.now(), author=request.user)
        comment.save() # INSERT문을 실행
        return redirect("bbsnote:detail", board_id=board.id) # redirect()는 넘겨주는 함수
    return redirect("bbsnote:detail", board_id=board_id)

@login_required(login_url='common:login') # 애너테이션 적용, 로그인이 되었는지 우선 검사하여 오류 방지
def board_create(request):
    # 요청이 'POST' 형태로 되면,(submit을 눌렀으면)
    if request.method == 'POST':
        form = BoardForm(request.POST)
        # form에 값이 있다면,
        if form.is_valid(): # is_valid()는 값이 있는지 확인하는 함수
            board = form.save(commit=False) # 저장할건데, 아직 commit은 하지않은 상태
            #board.create_date = timezone.now() # 현재 시간 할당(model.py에 auto_now_add설정해서 없어도 됨)
            board.author = request.user
            board.save() # commit
            return redirect("bbsnote:index") # '저장'을 누르면 목차를 출력
    else:
        form = BoardForm()
    return render(request, "bbsnote/board_form.html", {'form':form}) # board_form.html 만들어야함

@login_required(login_url='common:login')
def board_modify(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages.error(request, "수정 권한이 없습니다!")
        return redirect("bbsnote:detail", board_id=board.id)
    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.author = request.user
            board.update_date = timezone.now()
            board.save()
            return redirect("bbsnote:detail", board_id=board.id)
    else: # get방식으로 넘어올 때
        form = BoardForm(instance=board)
    context = {'form':form}
    return render(request, 'bbsnote/board_form.html', context)

@login_required(login_url='common:login')
def board_delete(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages.error(request, '삭제 권한이 없습니다!')
        return redirect("bbsnote:detail", board_id=board.id)
    board.delete()
    return redirect("bbsnote:index")

@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정 권한이 없습니다!')
        return redirect("bbsnote:detail", board_id=comment.board.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect("bbsnote:detail", board_id=comment.board.id)
    else:
        form = CommentForm(instance=comment)
    context = {'comment':comment, 'form':form}
    return render(request, "bbsnote/comment_form.html", context)

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "삭제 권한이 없습니다!")
        return redirect("bbsnote:detail", board_id=comment.board.id)    
    comment.delete()
    return redirect("bbsnote:detail", board_id=comment.board.id)