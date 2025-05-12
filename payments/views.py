from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.db.models import F, Sum, Q
from payments.forms import PaymentForm, PaymentCatForm,PaymentCreateForm, BankRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import os
from payments.models import PaymentDetail, PaymentChart, PaymentCategory, BankDetail
from students.models import Student
from django.http import HttpResponse
from django.http import FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import(ListView, FormView, CreateView, UpdateView, DeleteView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# For Filter
from .filters import PaymentFilter, MyPaymentFilter, PaymentChartFilter, PaymentReportFilter, PaymentSummaryFilter
from django_filters.views import FilterView
# For panigation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# for csv
import csv
from django.template.loader import get_template
from xhtml2pdf import pisa


# Create your views here.
@login_required
def payment_form(request):
    account_info = BankDetail.objects.all()
    if request.method == 'POST':       
        payment_form = PaymentForm(request.POST)

        if payment_form.is_valid():         
            payment_form.save()
            messages.success(request, f'The Payment has been entered successfully')
            return redirect('payments:payment_form')
    else:
        payment_form = PaymentForm()

    context ={
        'payment_form' : payment_form,
        'account_info' : account_info,
    }
    return render(request, 'payments/make_payment.html', context)

class PaymentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'payment/student_payment_form.html'
    form_class = PaymentCreateForm
    context_object_name = 'payment_create'
    # model = PaymentDetail
    
    success_url = reverse_lazy('payment:my_payments')



    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.student_id = self.request.user
        object.save()
        return super(PaymentCreateView, self).form_valid(form)
    


@login_required
def payment_cat_form(request):
    if request.method == 'POST':
        payment_cat_form = PaymentCatForm(request.POST)
        # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if payment_cat_form.is_valid():
            payment_cat_form.save()

            messages.success(request, f'The Payment Category has been entered successfully')
            return redirect('payment:payment-category')
    else:
        payment_cat_form = PaymentCatForm()

    context ={
        'payment_cat_form' : payment_cat_form
    }
    return render(request, 'payment/payment_cat_form.html', context)


@login_required
def payment_chart_form(request):
    if request.method == 'POST':
        payment_chart_form = PaymentChartForm(request.POST)
        # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if payment_chart_form.is_valid():
            payment_chart_form.save()

            messages.success(request, f'The Payment has been entered successfully')
            return redirect('payment:payment_chart')
    else:
        payment_chart_form = PaymentChartForm()

    context ={
        'payment_chart_form' : payment_chart_form
    }
    return render(request, 'payment/payment_chart_form.html', context)



# Not used anymore on the portal
@login_required
def paymentlist(request):
    paymentlist = PaymentDetail.objects.all()
    paymentlist_filter = PaymentFilter(request.GET, queryset=paymentlist)
    #balance_pay = PaymentDetail.objects.annotate(balance_pay= F('amount_paid') - F('payment_name__amount_due'))
    # balance_pay = PaymentDetail.objects.annotate(balance_pay= F('payment_name__amount_due') - F('amount_paid_a' + 'amount_paid_b' + 'amount_paid_c'))
  

    paymentlist = paymentlist_filter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(paymentlist, 40)
    try:
        paymentlist = paginator.page(page)
    except PageNotAnInteger:
        paymentlist = paginator.page(1)
    except EmptyPage:
        paymentlist = paginator.page(paginator.num_pages)


    context = {
        'paymentlist': PaymentDetail.objects.all(),
        'paymentlist_filter': paymentlist_filter,
        'paymentlist' : paymentlist,
        # 'balance_pay': balance_pay,
        # 'balance_pay' : PaymentDetail.objects.annotate(balance_pay= F('payment_name__amount_due') - F('amount_paid_a' + 'amount_paid_b' + 'amount_paid_c'))
         

    }
    return render (request, 'payment/all_payments.html', context )

    # return render(request, 'payment/schoolly_test_table.html',)


@login_required
def view_self_payments(request):
    # mypayment = PaymentDetail.objects.filter(student_detail=StudentDetail.objects.get(user=request.user))
    mypayment = PaymentDetail.objects.filter(student_id=User.objects.get(username=request.user))
    mypayment_filter = MyPaymentFilter(request.GET, queryset=mypayment)
    mypayment = mypayment_filter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(mypayment, 40)
    try:
        mypayment = paginator.page(page)
    except PageNotAnInteger:
        mypayment = paginator.page(1)
    except EmptyPage:
        mypayment = paginator.page(paginator.num_pages)
    context = {
        # 'mypayment' : PaymentDetail.objects.filter(student=StudentDetail.objects.get(user=request.user)).order_by("-payment_date"),
        'mypayment' : PaymentDetail.objects.filter(student_id=User.objects.get(username=request.user)).order_by("payment_date_a"),
        'mypayment':mypayment,
        'mypayment_filter' : mypayment_filter,
    }

    return render(request, 'payment/view_self_payment.html', context)


    


@login_required
def payment_chart_list(request):
    payment_chart_list = PaymentChart.objects.all()
    payment_chart_filter = PaymentChartFilter(request.GET, queryset=payment_chart_list)
    payment_chart_list = payment_chart_filter.qs
   

    page = request.GET.get('page', 1)
    paginator = Paginator(payment_chart_list, 40)
    try:
        payment_chart_list = paginator.page(page)
    except PageNotAnInteger:
        paymentChart = paginator.page(1)
    except EmptyPage:
        payment_chart_list = paginator.page(paginator.num_pages)


    context = {
        'payment_chart_list': PaymentDetail.objects.all(),
        'payment_chart_filter' : payment_chart_filter,
        'payment_chart_list' : payment_chart_list

    }
    return render (request, 'payment/payment_chart.html', context )



# FUNCTION FOR DOWNLOADING FILE
def download(request,path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path, 'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/file")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response

    raise Http404


#  Function for pdf and csv

# Generate a PDF staff list
def allpayment_pdf(request):
    # create Bytestream buffer
    buf = io.BytesIO()
    #create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 12)
    # Add some lines of text
    # lines = [
    #     "This is line 1",
    #     "This is line 2",
    #     "This is line31",
    #     "This is line 4",
    # ]
    # Designate the model
    payment = PaymentDetail.objects.all()

    # Create a blank list

    lines = [" PAYMENT DETAIL REPORT"]

    for payments in payment:
        lines.append(""),
        lines.append("Username: " + payments.user.username),
        lines.append("Amount: " + str(payments.amount_paid_a)),
        lines.append("Date: " + str(payments.payment_date_a)),
        lines.append("Method:" + payments.other_details_a),

        lines.append("------->----------->----------->"),


    # loop
    for line in lines:
        textob.textLine(line)
    #fininsh up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    # Return something
    return FileResponse(buf, as_attachment=False, filename='payment.pdf')


# Generate a CSV staff list
def allpayment_csv(request):
    response = HttpResponse(content_type ='text/csv')
    response['Content-Disposition'] = 'attachment; filename=payment-detail.csv'

# Create a csv writer
    writer = csv.writer(response)

    payment = PaymentDetail.objects.all()

    # Add column headings to the csv files
    writer.writerow(['STD.ID', 'STUDENT DETAIL ', 'SESSION', 'TERM', 'FEE DUE',  'PURPOSE', 'PAID_1', 'DATE_1', 'METHOD_1', 'CHECKED_1', 'PAID_2', 'DATE_2', 'METHOD_2', 'CHECKED_2', 'PAID_3', 'DATE_3', 'METHOD_3', 'CHECKED_3', 'TOTAL PAID', 'TOTAL DEBT'])


    # Loop thru and output
    for payments in payment:
        
        # writer.writerow([payments.student_detail.user.username, payments.student_detail.last_name, payments.student_detail.first_name, payments.student_detail.current_class, payments.payment_name.session, payments.payment_name.term, payments.payment_name.amount_due, payments.payment_name, payments.amount_paid_a, payments.payment_date_a, payments.bank_name_a, payments.confirmed_a,
        #  payments.amount_paid_b, payments.payment_date_b, payments.bank_name_b, payments.confirmed_b, payments.amount_paid_c, payments.payment_date_c, payments.bank_name_c, payments.confirmed_c, payments.amount_paid_a + payments.amount_paid_b + payments.amount_paid_c, payments.payment_name.amount_due - (payments.amount_paid_a + payments.amount_paid_b + payments.amount_paid_c) ])

        writer.writerow([  payments.student_id, payments.student_detail, payments.payment_name.session, payments.payment_name.term, payments.payment_name.amount_due, payments.payment_name, payments.amount_paid_a, payments.payment_date_a, payments.bank_name_a, payments.confirmed_a,
         payments.amount_paid_b, payments.payment_date_b, payments.bank_name_b, payments.confirmed_b, payments.amount_paid_c, payments.payment_date_c, payments.bank_name_c, payments.confirmed_c, payments.amount_paid_a + payments.amount_paid_b + payments.amount_paid_c, payments.payment_name.amount_due - (payments.amount_paid_a + payments.amount_paid_b + payments.amount_paid_c) ])

    return response

 
def payment_chart_pdf(request):
    # create Bytestream buffer
    buf = io.BytesIO()
    #create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 12)
    # Add some lines of text

    # Designate the model
    payment_chart = PaymentChart.objects.all()

    # Create a blank list

    lines = [" PAYMENT CHART "]

    for payment in payment_chart:
        lines.append(""),
        lines.append("PAYMENT NAME: " + payment.name),
        lines.append("CATEGORY: " + str(payment.payment_cat)),
        lines.append("SESSION: " + str(payment.session)),
        lines.append("TERM:" + payment.term),
        lines.append("AMOUNT:" + payment.amount_due),

        lines.append("------->----------->----------->"),


    # loop
    for line in lines:
        textob.textLine(line)
    #fininsh up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    # Return something
    return FileResponse(buf, as_attachment=False, filename='payment_chart.pdf')


# Generate a CSV staff list
def payment_chart_csv(request):
    response = HttpResponse(content_type ='text/csv')
    response['Content-Disposition'] = 'attachment; filename=payment_chart.csv'

# Create a csv writer
    writer = csv.writer(response)

    payment_chart = PaymentChart.objects.all()

    # Add column headings to the csv files
    writer.writerow(['PAYMENT NAME ', 'CATEGORY', 'SESSION', 'TERM', 'AMOUNT DUE',])


    # Loop thru and output
    for payment in payment_chart:
        writer.writerow([payment.name, payment.payment_cat, payment.session,
        payment.term, payment.amount_due,])

    return response

#This code generates the receipt
class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = PaymentDetail
    context_object_name = 'my_receipt'
    template_name = 'payment/receipt.html'
    

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        new_str = self.kwargs.get('pk') or self.request.GET.get('pk') or None

        queryset = queryset.filter(pk=new_str)
        obj = queryset.get()
        return obj


@login_required
def payment_report(request):
    paymentlist = PaymentDetail.objects.all()
    total_pay = PaymentDetail.objects.values('student_detail__student_username', 'student_detail__first_name', 'payment_name__amount_due', 'payment_name__name').annotate(total_payment=Sum('amount_paid_a')).order_by('student_detail')
    # paymentreport_filter = PaymentReportFilter(request.GET, queryset=paymentlist)
    balance_pay = PaymentDetail.objects.annotate(balance_pay= F('amount_paid_a') + ('amount_paid_b') + ('amount_paid_c')- F('payment_name__amount_due'))

  

    # paymentlist = paymentreport_filter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(paymentlist, 40)
    try:
        paymentlist = paginator.page(page)
    except PageNotAnInteger:
        paymentlist = paginator.page(1)
    except EmptyPage:
        paymentlist = paginator.page(paginator.num_pages)


    context = {
        'paymentlist': PaymentDetail.objects.all(),
        # 'paymentreport_filter': paymentreport_filter,
        'paymentlist' : paymentlist,
        'balance_pay': balance_pay,
        'total_pay': total_pay,
        'balance_pay' : PaymentDetail.objects.annotate(balance_pay= F('amount_paid_a') +('amount_paid_b') + ('amount_paid_c') - F('payment_name__amount_due')),
   
    }
   
    return render(request, 'payment/payment_report_table.html', context )
    



@login_required
def debtor_list(request):
    debtorlist = PaymentDetail.objects.all()
    total_pay = PaymentDetail.objects.values('student_detail__student_username', 'student_detail__first_name', 'payment_name__amount_due', 'payment_name__name').annotate(total_payment=Sum('amount_paid_a')).order_by('student_detail')
    # paymentreport_filter = PaymentReportFilter(request.GET, queryset=debtorlist)
    balance_pay = PaymentDetail.objects.annotate(balance_pay= F('amount_paid_a') + ('amount_paid_b') + ('amount_paid_c')- F('payment_name__amount_due'))

  

    # debtorlist = paymentreport_filter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(debtorlist, 40)
    try:
        debtorlist = paginator.page(page)
    except PageNotAnInteger:
        debtorlist = paginator.page(1)
    except EmptyPage:
        debtorlist = paginator.page(paginator.num_pages)


    context = {
        # 'debtorlist': PaymentDetail.objects.all(),
        # 'paymentreport_filter': paymentreport_filter,
        'debtorlist' : debtorlist,
        'balance_pay': balance_pay,
        'total_pay': total_pay,
        'balance_pay' : PaymentDetail.objects.annotate(balance_pay= F('amount_paid_a') +('amount_paid_b') + ('amount_paid_c') - F('payment_name__amount_due')),
   
    }
   
    return render(request, 'payment/debtor_report.html', context )

def debtor_csv(request):
    response = HttpResponse(content_type ='text/csv')
    response['Content-Disposition'] = 'attachment; filename=debtors_list.csv'

# Create a csv writer
    writer = csv.writer(response)

    payment = PaymentDetail.objects.all()

    # Add column headings to the csv files
    writer.writerow(['STD.ID', 'STUDENT DETAILS ',  'SESSION', 'FEE DUE',  'PURPOSE', 'TOTAL PAID', 'TOTAL DEBT'])


    # Loop thru and output
    for payments in payment:
        
        writer.writerow([ payments.student_id, payments.student_detail, payments.payment_name.session, payments.payment_name.amount_due, payments.payment_name, payments.amount_paid_a + payments.amount_paid_b + payments.amount_paid_c, payments.payment_name.amount_due - (payments.amount_paid_a + payments.amount_paid_b + payments.amount_paid_c)])

    return response



class PaymentCategoryListView(LoginRequiredMixin, ListView):
    context_object_name = 'categorylist'
    model = PaymentCategory
    queryset = PaymentCategory.objects.all()
    template_name = 'payment/payment_cat_list.html'
    paginate_by = 30

class BankListView(LoginRequiredMixin, ListView):
    context_object_name = 'banklist'
    model = BankDetail
    queryset = BankDetail.objects.all()
    template_name = 'payment/bank_list.html'
    paginate_by = 30


class BankCreateView(LoginRequiredMixin, CreateView):
    form_class = BankRegisterForm
    template_name = 'payment/bank_register_form.html'
    success_url = reverse_lazy('payment:bank-list')
    # queryset= StudentDetail.objects.all()

    # success_url = '/'
    def form_valid(self, form):
        return super().form_valid(form)


class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    fields = ('amount_paid_a', 'payment_date_a', 'bank_name_a', 
              'amount_paid_b', 'payment_date_b', 'bank_name_b',
              'amount_paid_c', 'payment_date_c', 'bank_name_c',)
    model = PaymentDetail
    template_name = 'payment/payment_update_form.html'
    # context_object_name = 'payment_update'
    
    
    def form_valid(self, form):
        form.instance.student_id = self.request.user
        return super().form_valid(form)

    def test_func(self):
        paymentdetail = self.get_object()
        if self.request.user == paymentdetail.student_detail:
            return True
        return False
    

# Payment Search Query

def payment_search_list(request):
    payment = PaymentDetail.objects.all()
    
     # PAGINATOR METHOD
    page = request.GET.get('page', 1)
    paginator = Paginator(payment, 30)
    try:
        payment = paginator.page(page)
    except PageNotAnInteger:
        payment = paginator.page(1)
    except EmptyPage:
        payment = paginator.page(paginator.num_pages)

    return render(request, 'payment/payment_search_list.html', {'payment': payment })

# Define function to search student
def search(request):
    results = []

    if request.method == "GET":
        query = request.GET.get('search')

        if query == '':
            query = 'None'
           

        results = PaymentDetail.objects.filter(Q(student_detail__student_username__icontains=query) | Q(student_detail__first_name__icontains=query) | Q(student_detail__current_class__name__icontains=query) )

        
    return render(request, 'payment/payment_search.html', {'query': query, 'results': results})


# RECEIPT PDF FILE

@login_required
def receipt_render_pdf_view(request, *args, **kwargs):    

    pk = kwargs.get('pk')
    
    my_receipt = get_object_or_404(PaymentDetail, pk=pk)
    template_path = 'payment/receipt_pdf.html'
    # template_path = 'results/result_sheet.html'
    context = {'my_receipt': my_receipt}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if you want to download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if you just want to display
    response['Content-Disposition'] = 'filename="receipt.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def payment_instruction(request):
    return render(request, 'payments/payment_instruction.html')