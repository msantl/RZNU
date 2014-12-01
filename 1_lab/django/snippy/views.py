import base64
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from snippy.models import Snippet

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.

def log_request(request):
    with open("django.log", "a") as log:
        log.write(request.path + " " + request.META['HTTP_USER_AGENT'] + "\n")
    return

def basic_auth(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        uname, passwd = base64.b64decode(auth[1]).split(':')
        user = authenticate(username=uname, password=passwd)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.user = user
    return request

def index(request):
    log_request(request)
    context = { 'user' : request.user }
    return render(request, 'index.html', context)

def error(request, *args, **kwargs):
    log_request(request)
    return render(request, 'snippy/error.html')

def new_user(request):
    log_request(request)
    if request.user.is_superuser:
        return render(request, 'snippy/post_user_detail.html')
    else:
        return redirect('/error/')

@login_required
def new_snippet(request):
    log_request(request)
    context = { 'user' : request.user }
    return render(request, 'snippy/post_snippet_detail.html', context)

def users(request):
    def get(request):
        users = User.objects.all()
        context = { 'user_list' : users }
        return render(request, 'snippy/users.html', context)
    def post(request):
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.create_user(username, '', password)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
        except:
            return redirect('/error/')

        return redirect('/users/%d/' % user.id)
    def put(request):
        pass
    def delete(request):
        pass

    log_request(request)
    if request.method == 'POST':
        return post(request)
    elif request.method == 'PUT':
        return put(request)
    elif request.method == 'DELETE':
        return delete(request)
    else:
        return get(request)

def snippets(request):
    def get(request):
        snippets = Snippet.objects.all()
        context = { 'snippet_list' : snippets }
        return render(request, 'snippy/snippets.html', context)
    def post(request):
        user_id = request.POST['user']
        title = request.POST['title']
        language = request.POST['language']
        source = request.POST['source']

        try:
            user = User.objects.get(pk=user_id)
            snippet = Snippet.objects.create_snippet(user, title, language, source)
            snippet.save()
        except:
            return redirect('/error/')

        return redirect('/snippets/%d/' % snippet.id)
    def put(request):
        pass
    def delete(request):
        pass

    log_request(request)
    if request.method == 'POST':
        return post(request)
    elif request.method == 'PUT':
        return put(request)
    elif request.method == 'DELETE':
        return delete(request)
    else:
        return get(request)

@login_required
def user_detail(request, user_id):
    def get(request, user_id):
        context = {}
        username = None
        snippets = None
        try:
            username = User.objects.get(pk=user_id).username
            snippets = Snippet.objects.filter(user=user_id)
        except User.DoesNotExist:
            raise Http404
        except Snippet.DoesNotExist:
            pass

        context = { 'snippets' : snippets, 'username' : username}
        return render(request, 'snippy/get_user_detail.html', context)

    def post(request, user_id):
        pass
    def put(request, user_id):
        pass
    def delete(request, user_id):
        pass

    log_request(request)
    if request.method == 'POST':
        return post(request, user_id)
    elif request.method == 'PUT':
        return put(request, user_id)
    elif request.method == 'DELETE':
        return delete(request, user_id)
    else:
        return get(request, user_id)

@login_required
def snippet_detail(request, snippet_id):
    def get(request, snippet_id):
        context = {}
        username = None
        snippet = None
        try:
            snippet = Snippet.objects.get(pk=snippet_id)
        except User.DoesNotExist:
            pass
        except Snippet.DoesNotExist:
            raise Http404

        context = { 'snippet' : snippet }
        return render(request, 'snippy/get_snippet_detail.html', context)

    def post(request, snippet_id):
        pass
    def put(request, snippet_id):
        pass
    def delete(request, snippet_id):
        pass

    log_request(request)
    if request.method == 'POST':
        return post(request, snippet_id)
    elif request.method == 'PUT':
        return put(request, snippet_id)
    elif request.method == 'DELETE':
        return delete(request, snippet_id)
    else:
        return get(request, snippet_id)


def api_detail(request):
    log_request(request)
    return render(request, 'snippy/get_api_detail.html')

@csrf_exempt
def api_users(request):
    def get(request):
        users = User.objects.all()

        data = []
        for user in users:
            data.append({'user_id' : user.id,
                         'username' : user.username})

        return HttpResponse(json.dumps({'users' : data}), content_type="application/json")

    def post(request):
        res = HttpResponse()

        if request.user and request.user.is_superuser:
            try:
                username = request.POST['username']
                password = request.POST['password']
                user = User.objects.create_user(username, '', password)
                user.save()
                res.status_code = 201
                res['Location'] = "/users/%d/" % user.id
            except:
                res.status_code = 400
        else:
            res.status_code = 401

        return res

    def put(request):
        res = HttpResponse()

        if request.user and request.user.is_superuser:
            try:
                user_id = None
                username = None
                password = None
                body = request.body.split('&')
                for part in body:
                    if part.split('=')[0] == 'username':
                        username = part.split('=')[1]
                    if part.split('=')[0] == 'password':
                        password = part.split('=')[1]
                    if part.split('=')[0] == 'id':
                        user_id = part.split('=')[1]

                if user_id:
                    user = User.objects.get(pk=user_id)
                    if username: user.username = username
                    if password: user.set_password(password)
                    user.save()
                    res.status_code = 200
                else:
                    res.status_code = 400
            except:
                res.status_code = 400
        else:
            res.status_code = 401

        return res

    def delete(request):
        res = HttpResponse()
        res.status_code = 200
        users = User.objects.all()
        snippets = Snippet.objects.all()

        if request.user and request.user.is_superuser:
            for snippet in snippets:
                if snippet.user.id != request.user.id:
                    try:
                        snippet.delete()
                    except:
                        res.status_code = 400

            for user in users:
                if user.id != request.user.id:
                    try:
                        user.delete()
                    except:
                        res.status_code = 400
        else:
            res.status_code = 401

        return res

    request = basic_auth(request)
    log_request(request)
    if request.method == 'POST':
        return post(request)
    elif request.method == 'PUT':
        return put(request)
    elif request.method == 'DELETE':
        return delete(request)
    else:
        return get(request)

@csrf_exempt
def api_snippets(request):
    def get(request):
        snippets = Snippet.objects.all()

        data = []
        for snippet in snippets:
            data.append({'user_id' : snippet.user.id,
                         'title' : snippet.title,
                         'language' : snippet.language,
                         'date' : str(snippet.date)})

        return HttpResponse(json.dumps({'snippets' : data}), content_type="application/json")
    def post(request):
        res = HttpResponse()

        if request.user.is_authenticated():
            try:
                title = request.POST['title']
                language = request.POST['language']
                source = request.POST['source']
                user = request.user

                snippet = Snippet.objects.create_snippet(user, title, language, source)
                snippet.save()
                res.status_code = 201
                res['Location'] = "/snippets/%d/" % snippet.id
            except:
                res.status_code = 400
        else:
            res.status_code = 401

        return res

    def put(request):
        res = HttpResponse()

        if request.user.is_authenticated():
            try:
                body = request.body.split('&')
                snippet_id = None
                title = None
                language = None
                source = None
                for part in body:
                    if part.split('=')[0] == 'snippet_id':
                        snippet_id = part.split('=')[1]
                    if part.split('=')[0] == 'title':
                        title = part.split('=')[1]
                    if part.split('=')[0] == 'language':
                        language = part.split('=')[1]
                    if part.split('=')[0] == 'source':
                        source = part.split('=')[1]

                if snippet_id:
                    snippet = Snippet.objects.get(pk=snippet_id)
                    if snippet.user.id == request.user.id:
                        if title: snippet.title = title
                        if language: snippet.language = language
                        if source: snippet.source = source
                        snippet.save()
                        res.status_code = 200
                    else:
                        res.status_code = 400
                else:
                    res.status_code = 400
            except:
                res.status_code = 400
        else:
            res.status_code = 401

        return res

    def delete(request):
        res = HttpResponse()
        res.status_code = 200
        snippets = Snippet.objects.all()

        if request.user and request.user.is_superuser:
            for snippet in snippets:
                try:
                    snippet.delete()
                except:
                    res.status_code = 400
        else:
            res.status_code = 401

        return res

    request = basic_auth(request)
    log_request(request)
    if request.method == 'POST':
        return post(request)
    elif request.method == 'PUT':
        return put(request)
    elif request.method == 'DELETE':
        return delete(request)
    else:
        return get(request)

@csrf_exempt
def api_user_detail(request, user_id):
    def get(request, user_id):
        if not request.user.is_authenticated():
            return HttpResponse(status=401)

        try:
            snippets = Snippet.objects.filter(user=user_id)
        except:
            return HttpResponse(status=400)

        data = []
        for snippet in snippets:
            data.append({'user_id' : snippet.user.id,
                         'title' : snippet.title,
                         'language' : snippet.language,
                         'date' : str(snippet.date),
                         'source' : snippet.source})

        return HttpResponse(json.dumps({'snippets' : data}), content_type="application/json")

    def post(request, user_id):
        return HttpResponse(status=405)

    def put(request, user_id):
        res = HttpResponse()

        if request.user and str(request.user.id) == user_id:
            try:
                username = None
                password = None
                body = request.body.split('&')
                for part in body:
                    if part.split('=')[0] == 'username':
                        username = part.split('=')[1]
                    if part.split('=')[0] == 'password':
                        password = part.split('=')[1]

                user = User.objects.get(pk=user_id)
                if username: user.username = username
                if password: user.set_password(password)
                user.save()
                res.status_code = 200
            except:
                res.status_code = 400
        else:
            res.status_code = 401

        return res

    def delete(request, user_id):
        res = HttpResponse()
        res.status_code = 200
        try:
            user = User.objects.get(pk=user_id)
            snippets = Snippet.objects.filter(user=user_id)
        except:
            return HttpResponse(status=400)

        if str(request.user.id) == user_id:
            for snippet in snippets:
                snippet.delete()

            user.delete()
        else:
            res.status_code = 401

        return res

    request = basic_auth(request)
    log_request(request)
    if request.method == 'POST':
        return post(request, user_id)
    elif request.method == 'PUT':
        return put(request, user_id)
    elif request.method == 'DELETE':
        return delete(request, user_id)
    else:
        return get(request, user_id)

@csrf_exempt
def api_snippet_detail(request, snippet_id):
    def get(request, snippet_id):
        if not request.user.is_authenticated():
            return HttpResponse(status=401)

        try:
            snippet = Snippet.objects.get(pk=snippet_id)
        except:
            return HttpResponse(status=400)

        data = {'user_id' : snippet.user.id,
                'title' : snippet.title,
                'language' : snippet.language,
                'date' : str(snippet.date),
                'source' : snippet.source}

        return HttpResponse(json.dumps(data), content_type="application/json")

    def post(request, snippet_id):
        return HttpResponse(status=405)

    def put(request, snippet_id):
        res = HttpResponse()

        if request.user.is_authenticated():
            try:
                body = request.body.split('&')
                title = None
                language = None
                source = None
                for part in body:
                    if part.split('=')[0] == 'title':
                        title = part.split('=')[1]
                    if part.split('=')[0] == 'language':
                        language = part.split('=')[1]
                    if part.split('=')[0] == 'source':
                        source = part.split('=')[1]

                snippet = Snippet.objects.get(pk=snippet_id)
                if snippet.user.id == request.user.id:
                    if title: snippet.title = title
                    if language: snippet.language = language
                    if source: snippet.source = source
                    snippet.save()
                    res.status_code = 200
                else:
                    res.status_code = 400
            except:
                res.status_code = 400
        else:
            res.status_code = 401

        return res

    def delete(request, snippet_id):
        res = HttpResponse()
        res.status_code = 200
        snippet = Snippet.objects.get(pk=snippet_id)

        if request.user and request.user.id == snippet.user.id:
            try:
                snippet.delete()
            except:
                res.status_code = 400
        else:
            res.status_code = 401

        return res

    request = basic_auth(request)
    log_request(request)
    if request.method == 'POST':
        return post(request, snippet_id)
    elif request.method == 'PUT':
        return put(request, snippet_id)
    elif request.method == 'DELETE':
        return delete(request, snippet_id)
    else:
        return get(request, snippet_id)

