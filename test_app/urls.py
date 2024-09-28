from django.urls import path
from .views import (
    home,
    add_word,
    run_test,
    run_test_all,
    run_test_by_category,
    no_words,
    word_list,
    delete_word,
    edit_word,
    )

urlpatterns = [
    path('', home, name='home'),
    path('add_word/', add_word, name='add_word'),
    path('run_test/', run_test, name='run_test'),
    path('run_test_all/', run_test_all, name='run_test_all'),
    path('run_test_by_category/', run_test_by_category, name='run_test_by_category'),
    path('no_words/', no_words, name='no_words'),
    path('word_list/', word_list, name='word_list'),
    path('delete_word/<int:pk>/', delete_word, name='delete_word'),
    path('edit_word/<int:pk>/', edit_word, name='edit_word'),
]