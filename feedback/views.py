import boto3
import json
from aiohttp import ClientError
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .models import Report
from .forms import ReportForm, UploadFileForm


class AboutView(TemplateView):
    template_name = 'feedback/about.html'

class ResourcesView(TemplateView):
    template_name = 'feedback/resources.html'

def home(request):
    if request.session.get('is_admin', False):
        return render(request, 'feedback/home.html')
    return render(request, 'feedback/home.html')


def admin_page(request):
    if request.session.get('is_admin', False):
        return render(request, 'feedback/admin_files.html')
    else:
        return redirect('/')


def report_view(request):
    message = ""

    if request.method == 'POST':
        report_form = ReportForm(request.POST)
        file_form = UploadFileForm(request.POST, request.FILES)
        files_uploaded = bool(request.FILES.getlist('files'))
        print(files_uploaded)
        
        if report_form.is_valid():
            report = report_form.save(commit=False)

            if request.user.is_authenticated:
                report.user = request.user
            else:
                report.user = None

            report.status = "New"

            if files_uploaded and file_form.is_valid():
                files = request.FILES.getlist('files')
                file_names = [file.name for file in files]
                # file = file_form.cleaned_data['file']
                s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
                for file in files:
                    try:
                        s3.upload_fileobj(
                            file,
                            settings.AWS_STORAGE_BUCKET_NAME,
                            file.name
                        )
                        print("uplaoded!")
                    except Exception as e:
                        print(e)
                        return JsonResponse({'status': 'error', 'message': 'Failed to upload file.'})
                report.file_names = json.dumps(file_names)
                report.save()

                return JsonResponse({'status': 'success', 'message': str(report)})
            else:
                # upload_message = "No file attached or file is not valid."
                report.save()
                message = str(report)
        else:
            print(file_form.errors)
            return JsonResponse({'status': 'error', 'message': 'Please correct the errors in the form.'})

    else:
        report_form = ReportForm()
        file_form = UploadFileForm()

    context = {
        'report_form': report_form,
        'file_form': file_form,
        'message': message,
        # 'upload_message': upload_message,
    }

    return render(request, 'feedback/report.html', context)


def report_success_view(request):
    return render(request, 'feedback/report_success.html')


@login_required
def user_submitted_reports(request):
    if request.method == 'POST' and 'report_id' in request.POST:
        try:
            report_id = request.POST['report_id']
            report = Report.objects.get(pk=report_id, user=request.user)
            report.delete()
            return HttpResponseRedirect(request.path_info)  # Refresh the page
        except Report.DoesNotExist:
            return HttpResponse('Report not found', status=404)
    print("Logged-in User:", request.user)
    user_submitted_reports = Report.objects.filter(user=request.user)
    print("User Submitted Reports:", user_submitted_reports)
    return render(request, 'feedback/user_submitted_reports.html', {'user_submitted_reports': user_submitted_reports})


def admin_pending_reports(request):
    new_reports_count = Report.objects.filter(status="New").count()
    in_progress_reports_count = Report.objects.filter(status="In Progress").count()
    resolved_reports_count = Report.objects.filter(status="Resolved").count()
    reports = Report.objects.order_by('-date').all()
    return render(request, 'feedback/admin_pending_reports.html', {
        'new_reports_count': new_reports_count,
        'in_progress_reports_count': in_progress_reports_count,
        'resolved_reports_count': resolved_reports_count,
        'reports': reports,
    })


def report_details(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    print(request.session.get('is_admin', False))
    file_urls = []
    if report.file_names:
        file_names = json.loads(report.file_names)
        for file_name in file_names:
            if not file_name.endswith(".txt"):
                file_urls.append(get_file_url(file_name))

    file_contents = []
    if report.file_names:
        file_names = json.loads(report.file_names)
        for file_name in file_names:
            if file_name.endswith(".txt"):
                content = get_file_content(file_name)
                if content is not None:
                    file_contents.append(content)


    if request.method == 'POST':
        if 'admin_comment' in request.POST and request.session.get('is_admin'):
            admin_comment = request.POST['admin_comment']
            report.admin_comment = admin_comment
            report.status = 'Resolved'  # Update the status
            report.save()
            return redirect('admin_pending_reports')  # Redirect to admin page after saving comments

    elif request.session.get('is_admin', False) and not report.status == 'Resolved':
        report.status = 'In Progress'  # Update the status
        report.save()

    return render(request, 'feedback/report_details.html', {'report': report, 'file_urls': file_urls, 'file_contents': file_contents})


@csrf_exempt
def get_file_url(file_name):
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    try:
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        if file_name.endswith(".pdf"):
            presigned_url = s3.generate_presigned_url('get_object',
                                                      Params={'Bucket': bucket_name, 'Key': file_name,
                                                              'ResponseContentDisposition': 'inline',
                                                              'ResponseContentType': 'application/pdf'},
                                                      ExpiresIn=3600)
        else:
            presigned_url = s3.generate_presigned_url('get_object',
                                                      Params={'Bucket': bucket_name, 'Key': file_name,
                                                              'ResponseContentDisposition': 'inline'},
                                                      ExpiresIn=3600)
        return presigned_url
    except ClientError as e:
        print(f"Error generating presigned URL for object '{file_name}': {e}")
        return

def get_file_content(file_name):
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    try:
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        content = response['Body'].read().decode('utf-8')
        return content
    except Exception as e:
        print(f"Error retrieving content of file '{file_name}': {e}")
        return None

def faq(request):
    return render(request, 'feedback/faq.html')