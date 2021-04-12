from django.views import generic 
from django.urls import reverse_lazy
from boto3 import Session
from .models import Meeting, Attendee
import json
from django.contrib.auth.mixins import LoginRequiredMixin

class MeetingListView(generic.ListView):
  model = Meeting
  template_name = 'meeting/list.html'

class MeetingView(LoginRequiredMixin,generic.TemplateView):
  model = Meeting
  template_name = 'meeting/meeting.html'
  context_object_name = 'chime'

  login_url = '/accounts/login/'
  redirect_field_name = 'redirect_to'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    meeting = Meeting.objects.get(pk=self.kwargs['pk'])
    if meeting.response == None:
        meeting.response = use_chime_meeting(meeting.token)
        meeting.save()
        for member in meeting.member.all():
            attendee = Attendee.objects.create(meeting=meeting,user=member)
            attendee.response = use_chime_attendee(meeting.response["Meeting"]["MeetingId"],member.pk)
            attendee.save()

    context['meeting'] = meeting
    try:
        context['attendee'] = Attendee.objects.get(meeting=self.kwargs['pk'],user=self.request.user)
    except:
        context['attendee'] = ""

    return context

class MeetingDetailView(generic.DetailView):
  model = Meeting
  template_name = 'meeting/detail.html'

class MeetingCreateView(generic.CreateView):
  model = Meeting
  template_name = 'meeting/create.html'
  success_url = reverse_lazy('meeting:list')
  fields = ['name','datetime','member']

def use_chime_meeting(token):

    # create session
    session = Session(profile_name="default")
    chime = session.client("chime")

    response = chime.create_meeting(
        ClientRequestToken=str(token),
        MediaRegion='us-east-1'
    )

    return response

def use_chime_attendee(meeting_id,user_id):

    # create session
    session = Session(profile_name="default")
    chime = session.client("chime")

    response = chime.create_attendee(
        MeetingId=str(meeting_id),
        ExternalUserId="user"+str(user_id),
    )

    return response
