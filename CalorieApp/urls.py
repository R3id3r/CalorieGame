from django.urls import path

from . import views

app_name = "CalorieApp"

urlpatterns = [
    path("", views.index, name="index"),
    # path("buy_item/<int:item_id>/", views.buy_item, name="buy_item"),
    # path("process_purchase/<int:item_id>/", views.process_purchase, name="process_purchase"),
    path("sign-up/", views.sign_up, name="sign-up"),
    path("sign-in/", views.sign_in, name="sign-in"),
    path("sign-out/", views.sign_out, name="sign-out"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("markets/", views.markets, name="markets"),
    path("fields/", views.fields, name="fields"),
    path("items/", views.items, name="items"),
    path("countdown/", views.countdown, name="countdown"),
    path("avatar/", views.avatar, name="avatar"),
]