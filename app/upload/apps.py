# Import Django's form library
from django import forms

# Define a form for creating a new todo item
class TodoForm(forms.Form):
    # Define a single text field for the todo item's text
    text = forms.CharField(
        # Set the maximum length of the text field to 40 characters
        max_length=40,
        # Define the HTML widget to render the text field
        widget=forms.TextInput(
            # Add HTML attributes to the widget
            attrs={
                # Set the CSS class to 'form-control' for Bootstrap styling
                'class': 'form-control',
                # Set the placeholder text to guide the user
                'placeholder': 'Enter todo e.g. Delete junk Files',
                # Set the aria-label attribute for accessibility
                'aria-label': 'Todo',
                # Set the aria-describedby attribute for accessibility
                'aria-describedby': 'add-btn'
            }
        )
    )

# Define a form for searching tasks
class TaskSearchForm(forms.Form):
    # Define a single text field for the search query
    query = forms.CharField(
        # Make the field optional 
        required=False,
        # Set the label text for the field
        label='Search tasks',
        # Define the HTML widget to render the text field
        widget=forms.TextInput(
            # Add HTML attributes to the widget
            attrs={
                # Set the CSS class to 'form-control' for Bootstrap styling
                'class': 'form-control',
                # Set the placeholder text to guide the user
                'placeholder': 'Enter search term...'
            }
        )
    )
