from os.path import join
from django import http
from django.views.generic import  ListView, RedirectView, TemplateView

from tool.document import doc_html_text, doc_page
from tool.log import log_page

from .models import Student
from .sensei import list_lessons, schedule, slides_markdown, site_settings


class UncDocViewer(TemplateView):
    template_name = 'unc_doc.html'

    def get_context_data(self, **kwargs):
        title = self.kwargs.get('title')
        if title.split('/')[1:]:
            course = title.split('/')[0]
        else:
            course = 'bacs350'
        log_page(self.request, 'course=%s, title=%s' % (course,title))
        doc = join('unc', title)
        text = doc_html_text(doc, '/static/images/unc/%s' % title)
        return site_settings(title=title, text=text, course=course)

    def get(self, request, *args, **kwargs):
        title = self.kwargs.get('title', 'xxx')
        url = doc_page('unc/' + title)
        if url:
            return http.HttpResponseRedirect('/' + url)
        else:
            return self.render_to_response(self.get_context_data(**kwargs))


class UncDocDisplay(TemplateView):
    template_name = 'unc_doc.html'

    def get_context_data(self, **kwargs):
        title = self.kwargs.get('title', 'Index')
        course = self.kwargs.get('course')
        log_page(self.request, 'course=%s, title=%s' % (course, title))
        if course:
            doc = join('unc', course, title)
            text = doc_html_text(doc, '/static/images/unc/%s' % course)
            return site_settings(title=title, text=text, course=course)
        else:
            doc = join('unc', title)
            text = doc_html_text(doc, '/static/images/unc/%s' % title)
            return site_settings(title=title, text=text, course=None)


class UncLessonList(TemplateView):
    # model = Lesson
    template_name = 'unc_lesson_list.html'

    def get_context_data(self, **kwargs):
        course = self.kwargs.get('course')
        title = 'Lessons for ' + course
        lessons = list_lessons(course)
        # lessons = Lesson.objects.filter(course__name=course).order_by('date')
        return site_settings(title=title, course=course, lessons=lessons)


class UncSchedule(TemplateView):
    template_name = 'unc_schedule.html'

    def get_context_data(self, **kwargs):
        course = self.kwargs.get('course')
        title = 'Schedule for '+course
        return site_settings(title=title, course=course, schedule=schedule(course))


class UncSlidesDisplay(TemplateView):
    template_name = 'unc_slides.html'

    def get_context_data(self, **kwargs):
        title = self.kwargs.get('title')
        course  = self.kwargs.get('course')
        text = slides_markdown(title)
        return site_settings(title=title, course=course, markdown=text)


class UncStudentList(TemplateView):
    template_name = 'unc_dashboard.html'

    def get_context_data(self, **kwargs):
        title = 'Student Dashboards'
        course  = self.kwargs.get('course')
        students = Student.objects.filter(course__name=course)
        return site_settings(title=title, course=course, students=students)


#
# class UncRegister(FormView):
#     class EditDocForm(Form):
#         name = forms.CharField()
#         email = forms.CharField()
#         password = forms.CharField()
#         domain = forms.CharField()
#
#     form_class = EditDocForm
#     template_name = 'unc_register.html'
#     success_url = '/unc/registered'
#
#     def form_valid(self, form):
#         name = form.data.get('name')
#         email = form.data.get('email')
#         password = form.data.get('password')
#         domain = form.data.get('domain')
#         register_user_domain(name, email, password, domain)
#         return super(UncRegister, self).form_valid(form)
