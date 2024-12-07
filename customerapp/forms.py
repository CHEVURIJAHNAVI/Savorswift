# forms.py
from django import forms

class OrderItemForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
    address = forms.CharField(widget=forms.Textarea)
    action = forms.ChoiceField(
        choices=[('wishlist', 'Add to Wishlist'), ('buy', 'Buy Now')],
        widget=forms.RadioSelect
    )

from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']  # Fields to be shown in the feedback form
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your feedback here...'}),}
