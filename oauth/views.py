import logging
import requests
import urllib.parse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from pprint import pformat

logger = logging.getLogger('app')
config = settings.CONFIG


def do_oauth(request):
    """
    # View  /oauth/
    """
    params = {
        'client_id': settings.TWITCH_CLIENT_ID,
        'redirect_uri': settings.TWITCH_REDIRECT_URI,
        'response_type': settings.TWITCH_RESPONSE_TYPE,
    }
    url_params = urllib.parse.urlencode(params)
    url = 'https://id.twitch.tv/oauth2/authorize?{}&scope={}'.format(url_params, settings.TWITCH_SCOPE)
    return HttpResponseRedirect(url)


def callback(request):
    """
    # View  /oauth/callback/
    """
    try:
        oauth_code = request.GET['code']
        logger.info('oauth_code: {}'.format(oauth_code))
        twitch_auth = twitch_token(oauth_code)
        logger.info(pformat(twitch_auth))
        access_token = twitch_auth['access_token']
        logger.info('access_token: {}'.format(access_token))
        twitch_profile = get_twitch(access_token)

        msg = format_msg(twitch_auth, twitch_profile)
        # send_discord(settings.DISCORD_HOOK, msg)

        auth = login_user(request, twitch_profile)
        if not auth:
            message(request, 'danger', 'Unable to complete login process. Report as a Bug.')
            return redirect('home:error')
        message(request, 'success', 'Operation Successful!')
        return redirect('home:success')

    except Exception as error:
        logger.exception(error)
        message(request, 'danger', 'Fatal Login Error. Report as Bug.')
        return redirect('home:error')


@require_http_methods(['POST'])
def log_out(request):
    """
    View  /oauth/logout/
    """
    logout(request)
    return redirect('home:index')


def login_user(request, data):
    """
    Login or Create New User
    """
    try:
        user = User.objects.filter(username=data['username']).get()
        user = update_profile(user, data)
        user.save()
        login(request, user)
        return True
    except ObjectDoesNotExist:
        user = User.objects.create_user(data['username'])
        user = update_profile(user, data)
        user.save()
        login(request, user)
        return True
    except Exception as error:
        logger.exception(error)
        return False


def twitch_token(code):
    """
    Post OAuth code to Twitch and Return access_token
    """
    url = 'https://id.twitch.tv/oauth2/token'
    data = {
        'client_id': settings.TWITCH_CLIENT_ID,
        'client_secret': settings.TWITCH_CLIENT_SECRET,
        'grant_type': settings.TWITCH_GRANT_TYPE,
        'redirect_uri': settings.TWITCH_REDIRECT_URI,
        'code': code,
    }
    headers = {'Accept': 'application/json'}
    r = requests.post(url, data=data, headers=headers, timeout=10)
    logger.debug('status_code: {}'.format(r.status_code))
    logger.debug('content: {}'.format(r.content))
    return r.json()


def get_twitch(access_token):
    """
    Get Twitch Profile for Authenticated User
    """
    url = 'https://api.twitch.tv/helix/users'
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
    }
    r = requests.get(url, headers=headers, timeout=10)
    logger.debug('status_code: {}'.format(r.status_code))
    logger.debug('content: {}'.format(r.content))
    twitch_profile = r.json()
    logger.info(pformat(twitch_profile))
    return {
        'username': twitch_profile['data'][0]['login'],
        'first_name': twitch_profile['data'][0]['display_name'],
        'user_id': twitch_profile['data'][0]['id'],
        'logo_url': twitch_profile['data'][0]['profile_image_url'],
    }


def update_profile(user, data):
    """
    Update user_profile from GitHub data
    """
    user.first_name = data['first_name']
    # user.email = data['email']
    # user.profile.email_verified = data['email_verified']
    # user.profile.twitch_id = data['user_id']
    # user.profile.logo_url = data['logo_url']
    return user


def message(request, level, message):
    """
    Easily add a success or error message
    """
    if level == 'success':
        messages.add_message(request, messages.SUCCESS, message, extra_tags='success')
    else:
        messages.add_message(request, messages.WARNING, message, extra_tags=level)


def format_msg(twitch_auth, twitch_profile):
    logger.info('----------------------------------------')
    logger.info(pformat(twitch_auth))
    logger.info('----------------------------------------')
    logger.info(pformat(twitch_profile))
    logger.info('----------------------------------------')
    return None


def send_discord(url, message):
    try:
        body = {'content': message}
        return requests.post(url, json=body, timeout=10)
    except Exception as error:
        logger.exception(error)
        return False
