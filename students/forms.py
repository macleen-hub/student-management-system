from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "registration_number": "REG-001",
            "first_name": "First name",
            "last_name": "Last name",
            "gender": "Gender",
            "email": "student@example.com",
            "phone": "+254 700 000 000",
            "course": "Course name",
            "year": "Year",
        }

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = placeholders.get(field_name, field.label)

        self.fields["year"].widget.attrs["min"] = "1"
