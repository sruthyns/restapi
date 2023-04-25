from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import View
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

class GoogleCalendarInitView(View):
    def get(self, request):
        
        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRETS_FILE,
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri=request.build_absolute_uri('http://127.0.0.1:8080/rest/v1/calendar/redirect')
        )

        
        auth_url, _ = flow.authorization_url(prompt='consent')
        return redirect(auth_url)

class GoogleCalendarRedirectView(View):
    def get(self, request):
        
        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRETS_FILE,
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri=request.build_absolute_uri('http://127.0.0.1:8080/rest/v1/calendar/redirect')
        )

        try:
            flow.fetch_token(authorization_response=request.build_absolute_uri())
        except HttpError:
            return HttpResponseBadRequest('Failed to fetch token')

        credentials = flow.credentials

       
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

       
