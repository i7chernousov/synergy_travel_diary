from django import forms
from .models import Trip, Photo, Place

class TripForm(forms.ModelForm):
    photos = forms.FileField(label='Фотографии', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    places_csv = forms.CharField(label='Места для посещения (через запятую)', required=False,
                                 help_text='Пример: Старый город, Набережная, Центральный парк')
    heritage_csv = forms.CharField(label='Объекты культурного наследия (через запятую)', required=False,
                                   help_text='Пример: Собор Св. Иакова, Крепость, Ратуша')

    class Meta:
        model = Trip
        fields = [
            'title', 'description',
            'country', 'city', 'address', 'latitude', 'longitude',
            'start_date', 'end_date', 'total_cost',
            'rating_convenience', 'rating_safety', 'rating_crowd', 'rating_greenery',
            'visibility',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows':5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['places_csv'].initial = ", ".join(p.name for p in self.instance.places_to_visit.all())
            self.fields['heritage_csv'].initial = ", ".join(p.name for p in self.instance.heritage_sites.all())

    def save(self, user=None, commit=True):
        trip = super().save(commit=False)
        if user is not None:
            trip.user = user
        if commit:
            trip.save()
            self._save_places(trip)
        return trip

    def _save_places(self, trip):
        def parse(csv_text):
            return [n.strip() for n in (csv_text or "").split(",") if n.strip()]
        visit_names = parse(self.cleaned_data.get('places_csv'))
        heritage_names = parse(self.cleaned_data.get('heritage_csv'))
        visit_objs = []
        for name in dict.fromkeys(visit_names):
            obj, _ = Place.objects.get_or_create(name=name, kind=Place.Kind.VISIT)
            visit_objs.append(obj)
        heritage_objs = []
        for name in dict.fromkeys(heritage_names):
            obj, _ = Place.objects.get_or_create(name=name, kind=Place.Kind.HERITAGE)
            heritage_objs.append(obj)
        trip.places_to_visit.set(visit_objs)
        trip.heritage_sites.set(heritage_objs)
