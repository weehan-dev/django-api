from django import forms
from meeting.models import Team
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "name",
            "avatar",
            "description",
            "member_access",
            "manager_access"
        ]