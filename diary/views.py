from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import TripForm
from .models import Trip, Photo

class TripListView(ListView):
    template_name = 'diary/trip_list.html'
    context_object_name = 'trips'
    paginate_by = 10

    def get_queryset(self):
        qs = Trip.objects.filter(visibility=Trip.Visibility.PUBLIC).select_related('user')
        user_id = self.request.GET.get('user')
        city = self.request.GET.get('city')
        country = self.request.GET.get('country')
        if user_id:
            qs = qs.filter(user_id=user_id)
        if city:
            qs = qs.filter(city__iexact=city)
        if country:
            qs = qs.filter(country__iexact=country)
        return qs

def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if trip.visibility == Trip.Visibility.PRIVATE and trip.user != request.user:
        messages.error(request, 'Этот дневник закрыт автором.')
        return redirect('trip_list')
    return render(request, 'diary/trip_detail.html', {'trip': trip})

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'diary/trip_form.html'

    def form_valid(self, form):
        trip = form.save(user=self.request.user)
        # загрузка фото
        for f in self.request.FILES.getlist('photos'):
            Photo.objects.create(trip=trip, image=f)
        messages.success(self.request, 'Путешествие добавлено.')
        return redirect(trip.get_absolute_url())

class TripUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Trip
    form_class = TripForm
    template_name = 'diary/trip_form.html'

    def form_valid(self, form):
        trip = form.save(user=self.request.user)
        for f in self.request.FILES.getlist('photos'):
            Photo.objects.create(trip=trip, image=f)
        messages.success(self.request, 'Дневник обновлён.')
        return redirect(trip.get_absolute_url())

class TripDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Trip
    success_url = reverse_lazy('trip_list')
    template_name = 'diary/trip_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Дневник удалён.')
        return super().delete(request, *args, **kwargs)

class UserListView(ListView):
    model = User
    template_name = 'diary/user_list.html'
    context_object_name = 'users'
    paginate_by = 30

    def get_queryset(self):
        return User.objects.all()

def user_detail(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    trips = profile_user.trips.all()
    visible = [t for t in trips if (t.visibility == Trip.Visibility.PUBLIC or request.user == profile_user)]
    return render(request, 'diary/user_detail.html', {'profile_user': profile_user, 'trips': visible})
