from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from app.forms import StartForm, EndForm, DaysForm
from app.models import AttendanceModels
from django.shortcuts import redirect, render
from django.utils import timezone
from django.urls import reverse
from django import forms
from django.views.generic.edit import FormView
from datetime import timedelta, datetime
from django.contrib.auth import get_user_model




class IndexView(TemplateView):
    template_name = "app/index.html"
    login_url = '/accounts/login/'



class AttendanceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/attendance.html')


class StatusView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_day = AttendanceModels.objects.filter(user=self.request.user)
        current_datetime = timezone.now().date()
        year = current_datetime.year
        month = current_datetime.month
        user = self.request.user
        form = DaysForm()

        total_work_time, work_time_count = self.calculate_total_work_time(user_day, year, month)

        return render(request, 'app/status.html', {
            'form': form,
            'user': user,
            'user_day': user_day,
            'year': year,
            'month': month,
            'total_work_time': total_work_time,
            'work_time_count': work_time_count,
        })

    def calculate_total_work_time(self, attendance_qs, target_year, target_month):
            total_work_time_user = timedelta()
            work_time_count_user = 0

            for attendance in attendance_qs.filter(
                days__year=target_year, days__month=target_month
            ):
                if attendance.start and attendance.end:  # Check for None
                    total_work_time_user += attendance.end - attendance.start
                    work_time_count_user += 1

            return total_work_time_user, work_time_count_user

    def post(self, request, *args, **kwargs):
        user_day = AttendanceModels.objects.filter(user=self.request.user)
        form = DaysForm(request.POST or None)
        user = self.request.user

        if form.is_valid():
            day = form.cleaned_data["days"]
            year = day.year
            month = day.month
            total_work_time, work_time_count = self.calculate_total_work_time(user_day, year, month)

        return render(request, 'app/status.html', {
            'form': form,
            'user': user,
            'user_day': user_day,
            'year': year,
            'month': month,
            'total_work_time': total_work_time,
            'work_time_count': work_time_count,
        })



class AllStatusView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        users = get_user_model().objects.all()

        user_attendance = {}
        total_work_times = {}
        work_time_counts = {}

        current_datetime = timezone.now().date()
        year = current_datetime.year
        month = current_datetime.month
        form = DaysForm()

        for user in users:
            user_attendance[user] = AttendanceModels.objects.filter(user=user)
            total_work_times[user], work_time_counts[user] = self.calculate_total_work_time(user_attendance[user], year, month)

        return render(request, 'app/allstatus.html', {
            'form': form,
            'user_attendance': user_attendance,
            'year': year,
            'month': month,
            'total_work_times': total_work_times,
            'work_time_counts': work_time_counts,
        })

    def calculate_total_work_time(self, attendance_qs, target_year, target_month):
            total_work_time_user = timedelta()
            work_time_count_user = 0

            for attendance in attendance_qs.filter(
                days__year=target_year, days__month=target_month
            ):
                if attendance.start and attendance.end:  # Check for None
                    total_work_time_user += attendance.end - attendance.start
                    work_time_count_user += 1

            return total_work_time_user, work_time_count_user

    def post(self, request, *args, **kwargs):
        users = get_user_model().objects.all()

        user_attendance = {}
        total_work_times = {}
        work_time_counts = {}

        form = DaysForm(request.POST or None)

        if form.is_valid():
            day = form.cleaned_data["days"]
            year = day.year
            month = day.month

            for user in users:
                user_attendance[user] = AttendanceModels.objects.filter(user=user)
                total_work_times[user], work_time_counts[user] = self.calculate_total_work_time(user_attendance[user], year, month)

        return render(request, 'app/allstatus.html', {
            'form': form,
            'user_attendance': user_attendance,
            'year': year,
            'month': month,
            'total_work_times': total_work_times,
            'work_time_counts': work_time_counts,
        })



class CorrectionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        users = get_user_model().objects.all()

        user_attendance = {}
        total_work_times = {}
        work_time_counts = {}

        current_datetime = timezone.now().date()
        year = current_datetime.year
        month = current_datetime.month
        form = DaysForm()
        forms = StartForm()
        forme = EndForm()

        for user in users:
            user_attendance[user] = AttendanceModels.objects.filter(user=user)
            total_work_times[user], work_time_counts[user] = self.calculate_total_work_time(user_attendance[user], year, month)

        return render(request, 'app/correction.html', {
            'form': form,
            'forms': forms,
            'forme': forme,
            'user_attendance': user_attendance,
            'year': year,
            'month': month,
            'total_work_times': total_work_times,
            'work_time_counts': work_time_counts,
        })

    def calculate_total_work_time(self, attendance_qs, target_year, target_month):
            total_work_time_user = timedelta()
            work_time_count_user = 0

            for attendance in attendance_qs.filter(
                days__year=target_year, days__month=target_month
            ):
                if attendance.start and attendance.end:  # Check for None
                    total_work_time_user += attendance.end - attendance.start
                    work_time_count_user += 1

            return total_work_time_user, work_time_count_user


    def post(self, request, *args, **kwargs):
        users = get_user_model().objects.all()

        user_attendance = {}
        total_work_times = {}
        work_time_counts = {}

        form = DaysForm(request.POST or None)
        forms = StartForm(request.POST or None)
        forme = EndForm(request.POST or None)


        if form.is_valid():
            day = form.cleaned_data["days"]
            year = day.year
            month = day.month

            for user in users:
                user_attendance[user] = AttendanceModels.objects.filter(user=user)
                total_work_times[user], work_time_counts[user] = self.calculate_total_work_time(user_attendance[user], year, month)

        return render(request, 'app/correction.html', {
            'form': form,
            'forms': forms,
            'forme': forme,
            'user_attendance': user_attendance,
            'year': year,
            'month': month,
            'total_work_times': total_work_times,
            'work_time_counts': work_time_counts,
        })




class StartView(FormView):
    template_name = 'app/attendance.html'
    form_class = StartForm

    def form_valid(self, form):
        # Check if the user has already submitted attendance for today
        dates = timezone.now().date() + timedelta(hours=9)
        user_records = AttendanceModels.objects.filter(user=self.request.user, days=dates)

        if user_records.exists():
            # User has already submitted attendance for today
            form.add_error(None, 'すでに登録があります。')
            return self.form_invalid(form)
        
        else:
            # Save the new attendance record
            user = form.save(commit=False)
            user.user = self.request.user
            user.days = dates
            user.start = timezone.now()
            user.save()

            return redirect('status')

    def form_invalid(self, form):
        # Return the form with errors
        return self.render_to_response(self.get_context_data(form=form))


class EndView(FormView):
    template_name = 'app/attendance.html'
    form_class = EndForm
    days = timezone.now().date() + timedelta(hours=9)

    def form_valid(self, form):
        try:
            user = AttendanceModels.objects.get(user=self.request.user, days=self.days)

            if user.end is None:
                user.end = timezone.now()
                user.save()
                return redirect('status')
            else:
                raise forms.ValidationError('すでに登録があります。')


        except AttendanceModels.DoesNotExist:
            # The object does not exist, handle accordingly
            form.add_error(None, '業務開始が押されていません。')
            return self.form_invalid(form)

        except forms.ValidationError as e:
            # Add the validation error to the form errors
            form.add_error(None, e)

            # Return the form to display errors
            return self.form_invalid(form)

        return render(self.request, 'app/status.html')  # Assuming you want to render 'status.html' after a successful form submission


def UpdateStart(request, pk, id):
    if request.method == "POST":


        form = StartForm(request.POST)
        date_obj = datetime.strptime(pk, '%Y年%m月%d日%H:%M')
        user = AttendanceModels.objects.get(user=id, days=date_obj)
        
        if form.is_valid():
            starttime = form.cleaned_data['start']
            user.start = timezone.make_aware(datetime.strptime(f'{pk[:-5]}{starttime}', '%Y年%m月%d日%H:%M'))

            user.save()
            return redirect(reverse('correction'))
    return redirect(reverse('correction'))

def UpdateEnd(request, pk, id):
    if request.method == "POST":
        form = EndForm(request.POST)
        user = AttendanceModels.objects.get(user=id, days=pk)
        if form.is_valid():
            user.end = form.cleaned_data['end']
            user.save()
            return redirect(reverse('correction'))
    return redirect(reverse('correction'))