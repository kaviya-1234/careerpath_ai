import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings


from .models import (
    StudentProfile, RIASECResult, BigFiveResult,
    AptitudeResult, AcademicResult, AIRecommendation
)


# ── INDEX PAGE ──────────────────────────────────────────────
def index_view(request):
    return render(request, 'index.html')


# ── ASSESSMENT PAGE ──────────────────────────────────────────
def assessment_view(request):
    return render(request, 'assessment.html')


# ── ADMIN PANEL PAGE ─────────────────────────────────────────
def admin_panel_view(request):
    return render(request, 'admin.html')


# ── STUDENT DASHBOARD PAGE ───────────────────────────────────
def dashboard_view(request):
    return render(request, 'dashboard.html')


# ── SIGNUP ───────────────────────────────────────────────────
@csrf_exempt
@require_POST
def signup_view(request):
    try:
        data = json.loads(request.body)

        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return JsonResponse({'success': False, 'error': 'Username and password required'})

        if len(username) < 3:
            return JsonResponse({'success': False, 'error': 'Username must be at least 3 characters'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        StudentProfile.objects.create(user=user)

        login(request, user)

        return JsonResponse({'success': True, 'username': user.username})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ── LOGIN ────────────────────────────────────────────────────
@csrf_exempt
@require_POST
def login_view(request):
    try:
        data = json.loads(request.body)

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            profile = StudentProfile.objects.filter(user=user).first()
            return JsonResponse({
                'success': True,
                'username': user.username,
                'student_class': profile.student_class if profile else '',
            })
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ── LOGOUT ───────────────────────────────────────────────────
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True})


# ── AUTH STATUS ──────────────────────────────────────────────
def auth_status_view(request):
    if request.user.is_authenticated:
        profile = StudentProfile.objects.filter(user=request.user).first()
        return JsonResponse({
            'logged_in': True,
            'username': request.user.username,
            'student_class': profile.student_class if profile else '',
        })
    return JsonResponse({'logged_in': False})


# ── SAVE RIASEC RESULT ───────────────────────────────────────
@csrf_exempt
@require_POST
def save_riasec(request):

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Login required'})

    try:
        data   = json.loads(request.body)
        scores = data.get('scores', {})

        # update_or_create — overwrite if retaken
        RIASECResult.objects.update_or_create(
            user=request.user,
            defaults=dict(
                realistic      = scores.get('Realistic', 0),
                investigative  = scores.get('Investigative', 0),
                artistic       = scores.get('Artistic', 0),
                social         = scores.get('Social', 0),
                enterprising   = scores.get('Enterprising', 0),
                conventional   = scores.get('Conventional', 0),
                top_trait      = data.get('topTrait', ''),
            )
        )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ── SAVE BIG FIVE RESULT ─────────────────────────────────────
@csrf_exempt
@require_POST
def save_bigfive(request):

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Login required'})

    try:
        data   = json.loads(request.body)
        scores = data.get('scores', {})

        BigFiveResult.objects.update_or_create(
            user=request.user,
            defaults=dict(
                openness          = scores.get('Openness', 0),
                conscientiousness = scores.get('Conscientiousness', 0),
                extraversion      = scores.get('Extraversion', 0),
                agreeableness     = scores.get('Agreeableness', 0),
                neuroticism       = scores.get('Neuroticism', 0),
                top_trait         = data.get('topTrait', ''),
            )
        )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ── SAVE APTITUDE RESULT ─────────────────────────────────────
@csrf_exempt
@require_POST
def save_aptitude(request):

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Login required'})

    try:
        data   = json.loads(request.body)
        scores = data.get('scores', {})

        AptitudeResult.objects.update_or_create(
            user=request.user,
            defaults=dict(
                logical    = scores.get('Logical', 0),
                verbal     = scores.get('Verbal', 0),
                numerical  = scores.get('Numerical', 0),
                spatial    = scores.get('Spatial', 0),
                mechanical = scores.get('Mechanical', 0),
                top_trait  = data.get('topTrait', ''),
            )
        )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ── SAVE ACADEMIC RESULT ─────────────────────────────────────
@csrf_exempt
@require_POST
def save_academic(request):

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Login required'})

    try:
        data = json.loads(request.body)

        AcademicResult.objects.update_or_create(
            user=request.user,
            defaults=dict(
                student_class  = data.get('studentClass', ''),
                stream         = data.get('stream', ''),
                subjects_json  = json.dumps(data.get('subjects', [])),
                average_score  = data.get('avg', 0),
                top_subject    = data.get('topSubject', ''),
            )
        )

        # keep StudentProfile.student_class in sync
        StudentProfile.objects.filter(user=request.user).update(
            student_class=data.get('studentClass', '')
        )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ── AI RECOMMENDATION GENERATE ───────────────────────────────
@require_GET
def ai_recommend(request):

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Login required'})

    try:
        riasec   = RIASECResult.objects.filter(user=request.user).first()
        aptitude = AptitudeResult.objects.filter(user=request.user).first()

        if not riasec or not aptitude:
            return JsonResponse({'success': False, 'error': 'Complete assessments first'})

        # simple rule-based recommendation
        if aptitude.logical > aptitude.verbal:
            career = "Software Engineer"
        else:
            career = "Business Analyst"

        recommendation = f"Recommended Career: {career}"

        return JsonResponse({
            'success': True,
            'recommendation': recommendation
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ── SAVE AI RECOMMENDATION ───────────────────────────────────
@csrf_exempt
@require_POST
def save_ai_recommendation(request):

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Login required'})

    try:
        data = json.loads(request.body)

        AIRecommendation.objects.update_or_create(
            user=request.user,
            defaults=dict(
                recommendation_text=data.get('recommendation', '')
            )
        )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ── GET RESULTS ──────────────────────────────────────────────
def get_results(request):

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Login required'})

    user = request.user

    riasec   = RIASECResult.objects.filter(user=user).first()
    bigfive  = BigFiveResult.objects.filter(user=user).first()
    aptitude = AptitudeResult.objects.filter(user=user).first()
    academic = AcademicResult.objects.filter(user=user).first()
    ai_rec   = AIRecommendation.objects.filter(user=user).first()

    return JsonResponse({
        'success':         True,
        'riasec':          riasec.top_trait if riasec else None,
        'bigfive':         bigfive.top_trait if bigfive else None,
        'aptitude':        aptitude.top_trait if aptitude else None,
        'academic':        academic.top_subject if academic else None,
        'ai_recommendation': ai_rec.recommendation_text if ai_rec else None,
    })


# ════════════════════════════════════════════════════════════
#  DASHBOARD API  (used by dashboard.html)
# ════════════════════════════════════════════════════════════

def dashboard_api(request):
    """
    GET /api/dashboard/
    Returns full dashboard payload for the logged-in student:
      username, class, all scores, academic marks, AI result, computed stats.
    Called once on page load from dashboard.html via fetch().
    """
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Login required'}, status=401)

    user     = request.user
    profile  = StudentProfile.objects.filter(user=user).first()
    riasec   = RIASECResult.objects.filter(user=user).first()
    bigfive  = BigFiveResult.objects.filter(user=user).first()
    aptitude = AptitudeResult.objects.filter(user=user).first()
    academic = AcademicResult.objects.filter(user=user).first()
    ai_rec   = AIRecommendation.objects.filter(user=user).first()

    # ── helpers ──────────────────────────────────────────────
    def _normalise(raw_scores):
        """Convert raw integer scores → percentage dict."""
        total = sum(raw_scores.values()) or 1
        return {k: round(v / total * 100) for k, v in raw_scores.items()}

    def _riasec_payload(r):
        if not r:
            return None
        raw = {
            'Realistic': r.realistic, 'Investigative': r.investigative,
            'Artistic': r.artistic,   'Social': r.social,
            'Enterprising': r.enterprising, 'Conventional': r.conventional,
        }
        return {'topTrait': r.top_trait, 'normalised': _normalise(raw)}

    def _bigfive_payload(b):
        if not b:
            return None
        raw = {
            'Openness': b.openness, 'Conscientiousness': b.conscientiousness,
            'Extraversion': b.extraversion, 'Agreeableness': b.agreeableness,
            'Neuroticism': b.neuroticism,
        }
        return {'topTrait': b.top_trait, 'normalised': _normalise(raw)}

    def _aptitude_payload(a):
        if not a:
            return None
        raw = {
            'Logical': a.logical, 'Verbal': a.verbal,
            'Numerical': a.numerical, 'Spatial': a.spatial,
        }
        return {'topTrait': a.top_trait, 'normalised': _normalise(raw)}

    def _academic_payload(ac):
        if not ac:
            return None
        try:
            subjects = json.loads(ac.subjects_json)
        except Exception:
            subjects = []
        return {
            'classLabel':  ac.student_class,
            'stream':      ac.stream,
            'avg':         ac.average_score,
            'topSubject':  ac.top_subject,
            'subjects':    subjects,
        }

    # ── stats ─────────────────────────────────────────────────
    tests_done = sum([
        riasec   is not None,
        bigfive  is not None,
        aptitude is not None,
        academic is not None,
    ])

    # average score across all completed tests (mean of normalised top-trait %)
    score_vals = []
    for payload_fn, obj in [(_riasec_payload, riasec), (_bigfive_payload, bigfive), (_aptitude_payload, aptitude)]:
        p = payload_fn(obj)
        if p and p['normalised']:
            score_vals.append(max(p['normalised'].values()))
    avg_score = round(sum(score_vals) / len(score_vals)) if score_vals else None

    stats = {
        'tests_done':  tests_done,
        'tests_total': 6,
        'tests_pending': 6 - tests_done,
        'avg_score':   avg_score,
        'top_career':  riasec.top_trait if riasec else None,
    }

    return JsonResponse({
        'success':       True,
        'username':      user.username,
        'student_class': profile.student_class if profile else '',
        'riasec':        _riasec_payload(riasec),
        'bigfive':       _bigfive_payload(bigfive),
        'aptitude':      _aptitude_payload(aptitude),
        'academic':      _academic_payload(academic),
        'ai_result':     ai_rec.recommendation_text if ai_rec else None,
        'stats':         stats,
    })


# ════════════════════════════════════════════════════════════
#  ADMIN PANEL VIEWS
# ════════════════════════════════════════════════════════════

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin@123'


def _is_admin(request):
    return request.session.get('is_admin') is True


# ── ADMIN LOGIN ──────────────────────────────────────────────
@csrf_exempt
@require_POST
def admin_login_view(request):
    try:
        data     = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            request.session['is_admin'] = True
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid admin credentials'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ── ADMIN LOGOUT ─────────────────────────────────────────────
def admin_logout_view(request):
    request.session.pop('is_admin', None)
    return JsonResponse({'success': True})


# ── LIST ALL STUDENTS ────────────────────────────────────────
def admin_students_list(request):
    if not _is_admin(request):
        return JsonResponse({'success': False, 'error': 'Admin login required'}, status=403)

    students = User.objects.filter(is_staff=False, is_superuser=False).order_by('username')
    data = []
    for u in students:
        profile  = StudentProfile.objects.filter(user=u).first()
        riasec   = RIASECResult.objects.filter(user=u).exists()
        bigfive  = BigFiveResult.objects.filter(user=u).exists()
        aptitude = AptitudeResult.objects.filter(user=u).exists()
        academic = AcademicResult.objects.filter(user=u).exists()
        done     = sum([riasec, bigfive, aptitude, academic])
        data.append({
            'username':      u.username,
            'student_class': profile.student_class if profile else '',
            'tests_done':    done,
            'joined':        u.date_joined.strftime('%d %b %Y'),
        })

    return JsonResponse({'success': True, 'students': data, 'total': len(data)})


# ── ADD STUDENT ──────────────────────────────────────────────
@csrf_exempt
@require_POST
def admin_add_student(request):
    if not _is_admin(request):
        return JsonResponse({'success': False, 'error': 'Admin login required'}, status=403)

    try:
        data     = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return JsonResponse({'success': False, 'error': 'Fill both fields'})
        if len(username) < 3:
            return JsonResponse({'success': False, 'error': 'Username needs 3+ characters'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        StudentProfile.objects.create(user=user)

        return JsonResponse({'success': True, 'username': username})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ── REMOVE STUDENT ───────────────────────────────────────────
@csrf_exempt
@require_POST
def admin_remove_student(request):
    if not _is_admin(request):
        return JsonResponse({'success': False, 'error': 'Admin login required'}, status=403)

    try:
        data     = json.loads(request.body)
        username = data.get('username', '').strip()
        user     = User.objects.get(username=username)
        user.delete()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ── SET CLASS (10th / 12th) ──────────────────────────────────
@csrf_exempt
@require_POST
def admin_set_class(request):
    if not _is_admin(request):
        return JsonResponse({'success': False, 'error': 'Admin login required'}, status=403)

    try:
        data     = json.loads(request.body)
        username = data.get('username', '').strip()
        cls      = data.get('student_class', '').strip()   # '10' or '12'

        user    = User.objects.get(username=username)
        profile = StudentProfile.objects.get(user=user)
        profile.student_class = cls
        profile.save()

        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ── SEARCH STUDENT ───────────────────────────────────────────
def admin_search_student(request):
    if not _is_admin(request):
        return JsonResponse({'success': False, 'error': 'Admin login required'}, status=403)

    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse({'success': False, 'error': 'Query required'})

    users = User.objects.filter(
        username__icontains=q,
        is_staff=False,
        is_superuser=False
    ).order_by('username')

    data = []
    for u in users:
        profile = StudentProfile.objects.filter(user=u).first()
        data.append({
            'username':      u.username,
            'student_class': profile.student_class if profile else '',
        })

    return JsonResponse({'success': True, 'students': data, 'count': len(data)})


# ── GET STUDENT RESULTS (for admin View modal) ───────────────
def admin_student_results(request):
    if not _is_admin(request):
        return JsonResponse({'success': False, 'error': 'Admin login required'}, status=403)

    username = request.GET.get('username', '').strip()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'})

    riasec   = RIASECResult.objects.filter(user=user).first()
    bigfive  = BigFiveResult.objects.filter(user=user).first()
    aptitude = AptitudeResult.objects.filter(user=user).first()
    academic = AcademicResult.objects.filter(user=user).first()

    def riasec_data(r):
        if not r: return None
        scores = {
            'Realistic': r.realistic, 'Investigative': r.investigative,
            'Artistic': r.artistic,   'Social': r.social,
            'Enterprising': r.enterprising, 'Conventional': r.conventional,
        }
        total = sum(scores.values()) or 1
        return {
            'topTrait':   r.top_trait,
            'normalised': {k: round(v / total * 100) for k, v in scores.items()},
        }

    def bigfive_data(b):
        if not b: return None
        scores = {
            'Openness': b.openness, 'Conscientiousness': b.conscientiousness,
            'Extraversion': b.extraversion, 'Agreeableness': b.agreeableness,
            'Neuroticism': b.neuroticism,
        }
        total = sum(scores.values()) or 1
        return {
            'topTrait':   b.top_trait,
            'normalised': {k: round(v / total * 100) for k, v in scores.items()},
        }

    def aptitude_data(a):
        if not a: return None
        scores = {
            'Logical': a.logical, 'Verbal': a.verbal,
            'Numerical': a.numerical, 'Spatial': a.spatial,
        }
        total = sum(scores.values()) or 1
        return {
            'topTrait':   a.top_trait,
            'normalised': {k: round(v / total * 100) for k, v in scores.items()},
        }

    def academic_data(ac):
        if not ac: return None
        try:
            subjects = json.loads(ac.subjects_json)
        except Exception:
            subjects = []
        return {
            'avg':        ac.average_score,
            'topSubject': ac.top_subject,
            'subjects':   subjects,
            'stream':     ac.stream,
        }

    return JsonResponse({
        'success':  True,
        'username': username,
        'riasec':   riasec_data(riasec),
        'bigfive':  bigfive_data(bigfive),
        'aptitude': aptitude_data(aptitude),
        'academic': academic_data(academic),
    })

# assessment/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import StudentProfile
import json

@csrf_exempt
def save_student(request):
    if request.method == "POST":
        data = json.loads(request.body)
        student_class = data.get("student_class")

        # save record (avoid duplicates)
        StudentProfile.objects.get_or_create(
            student_class=student_class,
            defaults={"user_id": 1}  # demo user
        )

        return JsonResponse({"message": "Saved successfully"})