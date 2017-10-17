from django import forms
import stats.models


class OfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        clauses = {
            'offer': self.instance.pk,
            'status': 'active'
        }
        qs = (stats.models.Goal.objects.filter(**clauses))
        self.fields['one_goal'].queryset = qs
