from google.colab import drive
import json
import ipywidgets as widgets
from IPython.display import display
from IPython.html.widgets import interactive

drive.mount('/content/drive')
file_path = '/content/drive/My Drive/students.json' # file path in drive

def update_students_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def read_students_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_student_form(students_data):
    students_names = [f"{student['First Name']} {student['Last Name']}" for student in students_data]
    student_dropdown = widgets.Dropdown(
        options=students_names,
        description='Select Student:',
        style={'description_width': 'initial', 'color': 'blue'}
    )

    # Simple UI to display each student details
    first_name = widgets.Text(description='First Name:', style={'description_width': 'initial', 'color': 'green'})
    last_name = widgets.Text(description='Last Name:', style={'description_width': 'initial', 'color': 'green'})
    email = widgets.Text(description='Email:', style={'description_width': 'initial', 'color': 'green'})
    courses_text = widgets.Textarea(description='Courses:', style={'description_width': 'initial', 'color': 'green'}, layout=widgets.Layout(width='auto', height='100px'))
    link = widgets.Text(description='Link:', style={'description_width': 'initial', 'color': 'green'})
    favorite_program = widgets.Text(description='Favorite Program:', style={'description_width': 'initial', 'color': 'green'})

    # Label widget to display update message
    update_label = widgets.Label(value='', style={'color': 'blue'})

    def update_form(student_name):
        selected_student_index = students_names.index(student_name)
        selected_student = students_data[selected_student_index]
        first_name.value = selected_student['First Name']
        last_name.value = selected_student['Last Name']
        email.value = selected_student['Email']
        courses_text.value = ', '.join(selected_student['Courses'])
        link.value = selected_student['Interesting Link']
        favorite_program.value = selected_student['Favorite Program']
        update_label.value = ''  # Reset update message

    interactive(update_form, student_name=student_dropdown)

    def update_favorite_program(change):
        selected_student_index = students_names.index(student_dropdown.value)
        students_data[selected_student_index]['Favorite Program'] = favorite_program.value

    def update_button_clicked(button):
        update_students_data(file_path, students_data)
        update_label.value = 'Favorite Program Updated!'  # Set update message

    favorite_program.observe(update_favorite_program, names='value')

    update_button = widgets.Button(description='Update', style={'button_color': 'lightblue'})
    update_button.on_click(update_button_clicked)

    form_widgets = [student_dropdown, first_name, last_name, email, courses_text, link, favorite_program, update_button, update_label]

    form_layout = widgets.Layout(display='flex', flex_flow='column', align_items='stretch')
    form_container = widgets.VBox(form_widgets, layout=form_layout)

    display(form_container)

students_data = read_students_data(file_path)  # Read data from file

create_student_form(students_data)  # Display student form
