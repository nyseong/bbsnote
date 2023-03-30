from django.contrib import admin
from .models import Board

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    search_fields = ['subject', 'content'] # 검색창 만들기: 제목과 내용을 검색 가능

admin.site.register(Board, BoardAdmin)

