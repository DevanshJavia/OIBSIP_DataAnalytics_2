from django import forms
import pandas as pd

df = pd.read_csv('static/data/menu.csv')
categories = df['Category'].dropna().unique()

class FilterForm(forms.Form):
    category = forms.MultipleChoiceField(
        choices=[(cat, cat) for cat in categories],
        widget=forms.CheckboxSelectMultiple,
        initial=categories
    )
    cal_min = int(df['Calories'].min())
    cal_max = int(df['Calories'].max())
    calories = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': cal_min, 'max': cal_max, 'step': 10, 'value': cal_max}))
