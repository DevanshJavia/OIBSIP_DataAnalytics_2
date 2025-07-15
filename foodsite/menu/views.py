import os
import pandas as pd
import numpy as np
import plotly.express as px
from django.shortcuts import render, redirect
from sklearn.linear_model import LinearRegression
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

# Base directory for loading CSV
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, 'static/data/menu.csv'))
df.columns = df.columns.str.strip()

# 🏠 Home Page
def home(request):
    return render(request, 'menu/home.html')

# 📊 Dashboard
@login_required(login_url='login')
def dashboard(request):
    categories = df['Category'].unique()
    selected_categories = request.GET.getlist("category")
    if not selected_categories:
        selected_categories = list(categories)

    cal_min = int(request.GET.get("cal_min", df['Calories'].min()))
    cal_max = int(request.GET.get("cal_max", df['Calories'].max()))

    filtered_df = df[
        (df['Category'].isin(selected_categories)) &
        (df['Calories'] >= cal_min) &
        (df['Calories'] <= cal_max)
    ]

    total = len(filtered_df)
    avg_cal = filtered_df['Calories'].mean()
    avg_fat = filtered_df['Total Fat'].mean()
    avg_protein = filtered_df['Protein'].mean()

    count = min(20, total)
    top_items = filtered_df.sort_values(by='Calories', ascending=False).head(count)

    fig1 = px.bar(top_items, x='Item', y='Calories', color='Category', text='Calories', title="Top High-Calorie Items", template="plotly_white")
    fig2 = px.pie(filtered_df, names='Category', hole=0.4, title="Category Distribution", template="plotly_white")
    fig3 = px.scatter(filtered_df, x='Total Fat', y='Calories', size='Protein', color='Category', hover_data=['Item'], title="Calories vs Fat (Protein Size)", template="plotly_white")

    charts = {
        'bar': fig1.to_html(full_html=False),
        'pie': fig2.to_html(full_html=False),
        'scatter': fig3.to_html(full_html=False),
    }

    return render(request, 'menu/dashboard.html', {
        'categories': categories,
        'selected_categories': selected_categories,
        'cal_min': cal_min,
        'cal_max': cal_max,
        'filtered_df': filtered_df,
        'total': total,
        'avg_cal': round(avg_cal, 1) if total else 0,
        'avg_fat': round(avg_fat, 1) if total else 0,
        'avg_protein': round(avg_protein, 1) if total else 0,
        'charts': charts,
    })

# 🔮 Predictor Page
@login_required(login_url='login')
def predict(request):
    prediction = None
    if request.method == 'POST':
        fat = int(request.POST.get("fat"))
        sodium = int(request.POST.get("sodium"))
        carbs = int(request.POST.get("carbs"))
        protein = int(request.POST.get("protein"))
        X = df[['Total Fat', 'Sodium', 'Carbohydrates', 'Protein']]
        y = df['Calories']
        model = LinearRegression()
        model.fit(X, y)
        prediction = model.predict(np.array([[fat, sodium, carbs, protein]]))[0]
    return render(request, 'menu/predict.html', {'prediction': round(prediction, 2) if prediction else None})

@login_required(login_url='login')
def menu_data(request):
    categories = df['Category'].unique()
    selected_categories = request.GET.getlist("category")

    if not selected_categories:
        selected_categories = list(categories)

    filtered_df = df[df['Category'].isin(selected_categories)]
    table_html = filtered_df.to_html(classes='table-auto border', index=False)

    return render(request, 'menu/menu_data.html', {
        'table': table_html,
        'categories': categories,
        'selected_categories': selected_categories,
    })

# 👤 Signup Page
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'menu/signup.html', {'form': form})

# 🔐 Login Page
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'menu/login.html', {'error': 'Invalid credentials'})
    return render(request, 'menu/login.html')

# 🔓 Logout View
def logout_view(request):
    logout(request)
    return redirect('login')
