from django.urls import path
from . import views

urlpatterns = [

    # ── PAGES ────────────────────────────────────────────────
    path('',            views.index_view,       name='index'),
    path('assessment/', views.assessment_view,  name='assessment'),
    path('dashboard/',  views.dashboard_view,   name='dashboard'),   # ← Student Dashboard
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),

    # ── AI RECOMMEND ─────────────────────────────────────────
    path('api/ai-recommend/', views.ai_recommend, name='api_ai_recommend'),

    # ── AUTH API ─────────────────────────────────────────────
    path('api/signup/',      views.signup_view,      name='api_signup'),
    path('api/login/',       views.login_view,       name='api_login'),
    path('api/logout/',      views.logout_view,      name='api_logout'),
    path('api/auth-status/', views.auth_status_view, name='api_auth_status'),

    # ── SAVE RESULTS API ─────────────────────────────────────
    path('api/save/riasec/',           views.save_riasec,           name='api_save_riasec'),
    path('api/save/bigfive/',          views.save_bigfive,          name='api_save_bigfive'),
    path('api/save/aptitude/',         views.save_aptitude,         name='api_save_aptitude'),
    path('api/save/academic/',         views.save_academic,         name='api_save_academic'),
    path('api/save/ai-recommendation/', views.save_ai_recommendation, name='api_save_ai_rec'),

    # ── GET RESULTS API ──────────────────────────────────────
    path('api/results/',   views.get_results,  name='api_get_results'),

    # ── DASHBOARD API ────────────────────────────────────────
    path('api/dashboard/', views.dashboard_api, name='api_dashboard'),  # ← Dashboard data

    # ── ADMIN PANEL API ──────────────────────────────────────
    path('api/admin/login/',           views.admin_login_view,      name='api_admin_login'),
    path('api/admin/logout/',          views.admin_logout_view,     name='api_admin_logout'),
    path('api/admin/students/',        views.admin_students_list,   name='api_admin_students'),
    path('api/admin/students/add/',    views.admin_add_student,     name='api_admin_add_student'),
    path('api/admin/students/remove/', views.admin_remove_student,  name='api_admin_remove_student'),
    path('api/admin/students/set-class/', views.admin_set_class,   name='api_admin_set_class'),
    path('api/admin/students/search/', views.admin_search_student,  name='api_admin_search_student'),
    path('api/admin/students/results/', views.admin_student_results, name='api_admin_student_results'),
    path('save/', views.save_student, name='save_student'),
]
