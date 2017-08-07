from django import forms
import stats.models


class OfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['one_goal'].queryset = (stats.models.Goal.objects
                                            .filter(offer=self.instance.pk))
