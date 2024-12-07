# forms.py
from django import forms

class OrderItemForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
    address = forms.CharField(widget=forms.Textarea)
    action = forms.ChoiceField(
        choices=[('wishlist', 'Add to Wishlist'), ('buy', 'Buy Now')],
        widget=forms.RadioSelect
    )
