from django.shortcuts import render, redirect, get_object_or_404
from .forms import WordPairForm
from .models import WordPair, Category
import random

# Create your views here.

def home(request):
    return render(request,'base.html')

def add_word(request):
    if request.method == 'POST':
        form = WordPairForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_word')
    else:
        form = WordPairForm()
    return render(request, 'add_word.html', {'form':form})

def edit_word(request, pk):
    word = get_object_or_404(WordPair, pk=pk)
    if request.method == 'POST':
        form = WordPairForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            return redirect('word_list')
    else:
        form = WordPairForm(instance=word)
    return render(request, 'edit_word.html', {'form':form})

def delete_word(request, pk):
    word = get_object_or_404(WordPair, pk = pk)
    if request.method == 'POST':
        word.delete()
        return redirect('word_list')
    return render(request, 'delete_word.html', {'word':word})

def run_test(request):
    return render(request, 'run_test.html')

def run_test_all(request):
    word_pairs = list(WordPair.objects.all())
    if not word_pairs:
        return render(request, 'no_words.html')
    
    if request.method == 'POST':
        selected_answer = request.POST.get('answer')
        correct_option = request.POST.get('correct_option')
        
        if selected_answer == correct_option:
            return redirect('run_test_all')
    
    random.shuffle(word_pairs)
    selected_pair = random.choice(word_pairs)
    korean_word = selected_pair.word_ko
    correct_option = selected_pair.word_uz
    incorrect_options = [pair.word_uz for pair in WordPair.objects.all() if pair.word_uz != selected_pair.word_uz]
    uzbek_options = [correct_option] + random.sample(incorrect_options, 3)
    random.shuffle(uzbek_options)

    context = {
        'korean_word': korean_word,
        'uzbek_options': uzbek_options,
        'correct_option': correct_option,
    }
    
    return render(request, 'run_test_all.html', context)

def run_test_by_category(request):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=1)
    word_pairs = WordPair.objects.filter(category=category)
    context = {
        'categories':categories,
        'word_pairs':word_pairs,
    }
    return render(request, 'run_test_by_category.html', context)

def no_words(request):
    return  render(request, 'no_words.html')

def word_list(request):
    words =  WordPair.objects.all()
    categories = Category.objects.all()
    if not words:
        return render(request, 'no_words.html')
    
    contex = {
        'words': words,
        'categories': categories,
    }

    return render(request, 'word_list.html', contex)
