from django.urls import path
from hs.views.ask import HSAskView
from hs.views.search import HSSearchView
from hs.views.chapter import HSChapterView
from hs.views.predict import HSPredictView
from hs.views.analyze import HSAnalyzeView

urlpatterns = [
    path("predict/", HSPredictView.as_view()),
    path("analyze/", HSAnalyzeView.as_view()),
    path("ask/", HSAskView.as_view()),
    path("search/", HSSearchView.as_view()),
    path("chapter/<int:chapter_num>/", HSChapterView.as_view()),
]
