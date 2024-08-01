from django import forms
class TodoForm(forms.Form):
	text = forms.CharField(max_length=40,
		widget=forms.TextInput(
			attrs={'class' : 'form-control',  'placeholder' : 'Enter todo e.g. Delete junk Files', 'aria-lable' : 'Todo', 'aria-describedly' : 'add-btn'}))
class TaskSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
          	label='Search tasks',
        		widget=forms.TextInput(attrs={
            		'class': 'form-control',
            			'placeholder': 'Enter search term...'
        })
		)