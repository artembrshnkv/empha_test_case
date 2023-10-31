from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, \
                                 DeleteView, FormView
from django.shortcuts import redirect, reverse
from django.contrib.auth import logout
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Room
from .utils import BaseMixin, BaseListMixin, booked_room_date_is_correct
from .forms import *


class RoomList(BaseListMixin, ListView):
    template_name = 'mainapp/all_products.html'
    queryset = Room.objects.all()
    context_object_name = 'rooms'

    def get_context_data(self, **kwargs):
        super_data = super().get_context_data()
        c_def = self.get_general_data(**kwargs)
        context = dict(list(super_data.items()) + list(c_def.items()))

        return context

    def get_queryset(self, cleaned_data=None):
        all_rooms = Room.objects.all()
        if self.request.GET.get('min_price'):
            queryset = all_rooms.order_by('price')
        elif self.request.GET.get('max_price'):
            queryset = all_rooms.order_by('-price')
        elif self.request.GET.get('min_quantity'):
            queryset = all_rooms.order_by('quantity')
        elif self.request.GET.get('max_quantity'):
            queryset = all_rooms.order_by('-quantity')
        else:
            queryset = all_rooms

        return queryset


class ShowRoom(BaseMixin, DetailView):
    template_name = 'mainapp/show_room.html'
    model = Room
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        super_data = super().get_context_data(**kwargs)
        c_def = self.get_general_data(**kwargs)
        room_number = f'{self.request.path}'.split('/')[-1]
        context = dict(list(super_data.items()) + list(c_def.items()))
        context['room_number'] = room_number

        return context


class BookRoom(BaseMixin, LoginRequiredMixin, FormView):
    template_name = 'mainapp/book_room.html'
    form_class = BookRoomForm

    def get_data(self):
        room_number = f'{self.request.path}'.split('/')[-1]
        user_id = self.request.user.id
        data = {
            'room_number': room_number,
            'user_id': user_id,
        }

        return data

    def form_valid(self, form):
        if booked_room_date_is_correct(form.cleaned_data):
            form.save()
            # ReservedRoom.objects.create(**form.cleaned_data)
            return redirect('main_page')
        else:
            return redirect(self.request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    def get_context_data(self, **kwargs):
        super_data = super().get_context_data(**kwargs)
        c_def = self.get_general_data(**kwargs)
        context = dict(list(super_data.items()) + list(c_def.items()))

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['user'] = self.get_data()['user_id']
        kwargs['initial']['number'] = self.get_data()['room_number']

        return kwargs

    def get_success_url(self):
        return reverse('main_page')


# class SortByAvailableDates(BaseMixin, FormMixin, ListView):
#     template_name = 'mainapp/sort_by_available_dates.html'
#     form_class = SortByDateForm
#     queryset = Room.objects.all()
#
#     # def post(self):
#
#
#     def get_context_data(self, **kwargs):
#         super_data = super().get_context_data(**kwargs)
#         c_def = self.get_general_data(**kwargs)
#         context = dict(list(super_data.items()) + list(c_def.items()))
#
#         return context


class UserRegistration(BaseMixin, CreateView):
    template_name = 'mainapp/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('main_page')

    def get_context_data(self, **kwargs):
        super_data = super().get_context_data(**kwargs)
        c_def = self.get_general_data(**kwargs)
        context = dict(list(super_data.items()) + list(c_def.items()))

        return context


class UserAccount(LoginRequiredMixin, BaseMixin, ListView):
    template_name = 'mainapp/user_account.html'
    context_object_name = 'user_booked_rooms'

    def get_context_data(self, **kwargs):
        super_data = super().get_context_data(**kwargs)
        c_def = self.get_general_data(**kwargs)
        context = dict(list(super_data.items()) + list(c_def.items()))

        return context

    def get_queryset(self):
        return ReservedRoom.objects.filter(user_id=self.request.user.id)


class DeleteBooking(LoginRequiredMixin, BaseMixin, DeleteView):
    template_name = 'mainapp/delete_booking.html'
    model = ReservedRoom
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        super_data = super().get_context_data(**kwargs)
        c_def = self.get_general_data(**kwargs)
        context = dict(list(super_data.items()) + list(c_def.items()))

        return context

    def get_success_url(self):
        return reverse_lazy('account')


class UserLogin(BaseMixin, LoginView):
    template_name = 'mainapp/user_login.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            super_data = super().get_context_data(**kwargs)
            c_def = self.get_general_data(**kwargs)
            context = dict(list(super_data.items()) + list(c_def.items()))

            return context
        else:
            raise http.Http404


def user_logout(request):
    logout(request)
    return redirect('main_page')
