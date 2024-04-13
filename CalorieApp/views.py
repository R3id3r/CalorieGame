from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm, AuthenticateUserForm

#from .models import Item, Transaction
from .models import Player, FarmingSkill, PlayerSkill, Field, Planting, Seed

from .tasks import add

def index(request):
    # print("running task")
    # print(add.delay(1,2))
    # print(type(add.delay(1,2)))
    # print("task complete")
    return render(request, 'CalorieApp/index.html')

# def buy_item(request, item_id):
#     context = {
#     "item" : Item.objects.get(pk=item_id)
#     }
#     return render(request, "CalorieApp/buy_item.html", context)

# @login_required
# @require_POST
# def process_purchase(request, item_id):
#     item = get_object_or_404(Item, id=item_id)

#     # Check if the item is already sold
#     if item.is_sold:
#         messages.error(request, "This item has already been sold.")
#         return redirect('CalorieApp:index')

#     # Update the item to mark it as sold
#     item.is_sold = True
#     item.save()

#     # Create a transaction record
#     Transaction.objects.create(
#         item=item,
#         buyer=request.user,
#         date=timezone.now()
#     )

#     messages.success(request, "Purchase successful! You have bought the item.")
#     return redirect('CalorieApp:index')  # Redirect to a suitable page, such as the marketplace home page


def sign_up(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('CalorieApp:sign-in')

    context = {
        'form' : form,
    }
    
    return render(request, 'CalorieApp/sign_up.html', context)

def sign_in(request):
    form = AuthenticateUserForm()

    if request.method == 'POST':
        form = AuthenticateUserForm(request, data=request.POST)
        print(form.errors)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('CalorieApp:dashboard')

    context = {
        'form': form
    }
    return render(request, 'CalorieApp/sign_in.html', context)

def sign_out(request):
    print(request)
    auth.logout(request)
    return redirect('CalorieApp:index')

#@login_required
def dashboard(request):
    player = Player.objects.get(username=request.user) # request.user  # Or use request.user to get the logged-in user
    player_skills = PlayerSkill.objects.filter(player=player).select_related('skill')
    plantings = Planting.objects.filter(player=player)

    context = {
        'player': player,
        'player_skills': player_skills,
        'plantings': plantings
        }
    return render(request, 'CalorieApp/dashboard.html', context)

#@login_required
def markets(request):
    player = Player.objects.get(username=request.user) # request.user  # Or use request.user to get the logged-in user
    player_skills = PlayerSkill.objects.filter(player=player).select_related('skill')
    context = {
        'player': player,
        'player_skills': player_skills,
        }
    return render(request, 'CalorieApp/markets.html', context)

@login_required
def fields(request):
    player = Player.objects.get(username=request.user)
    player_skills = PlayerSkill.objects.filter(player=player).select_related('skill')
    fields = Field.objects.filter(owner=player)
    plantings = Planting.objects.filter(player=player)

    context = {
        'player': player,
        'player_skills': player_skills,
        'fields': fields,
        'plantings': plantings
    }
    print(plantings)
    return render(request, 'CalorieApp/fields.html', context)

def countdown(request):
    return render(request, 'CalorieApp/countdown_timer.html')

def avatar(request):
    return render(request, 'CalorieApp/avatar.html')

def items(request):
    player = Player.objects.get(username=request.user) # request.user  # Or use request.user to get the logged-in user
    player_skills = PlayerSkill.objects.filter(player=player).select_related('skill')
    context = {
        'player': player,
        'player_skills': player_skills,
        }
    return render(request, 'CalorieApp/items.html', context)