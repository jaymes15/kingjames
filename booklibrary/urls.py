from django.contrib import admin
from .views import BookDetail,BookList,BookListdemo,Usersview,Friendview
from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns




app_name='booklibrary'
urlpatterns = [
    path('post/byuser/<int:user_id>', views.postbyuser, name='postbyuser'),
    path('book/<int:pk>', BookDetail.as_view(), name='book_paste_detail'),
    path('uploadbook/', views.add_post, name='create'),
    path('register/', views.signup_view,name='register'),
    path('login/', views.login_view,name='login'),
    path('logout/', views.logout_view,name='logout'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$',views.change_friends,name='change_friends'),
    # url(r'^(?P<slug>[-\w]+)/comment/$',Comment.as_view(),name='bookcomment'),
   #path('addcomment/<int:id>', Comment.as_view(), name='addcomment'),
    path('comment/<int:post_id>', views.display_comment, name='bookcomment'),
    path('addcomment/<int:id>', views.add_comment, name='addcomment'),
    #path('addcomment/<int:post_id>',views.add_comment,name='add_comment'),
    path('category/<int:category_id>', views.display_category, name='displaycategory'),

    path('profile/', views.profile,name='userprofile'),
    url(r'^profile(?P<pk>\d+)/$',views.otherprofile,name='otherusersprofile'),
    
    path('editprofile/', views.edit_profile,name='edituserprofile'),
    #path('userupdateform/', views.userupdateform,name='userupdateform'),
    path('', BookList.as_view(), name='book_paste_list'),
    path('books/show', BookListdemo.as_view(), name='book_paste_listdemo'),
   # path('createinfouser/', createinfouser.as_view(), name='createinfouser'),
    path('otherusers/', Usersview.as_view(), name='otherusers'),
    path('friendview/', Friendview.as_view(), name='friendview'),
    path('like/',views.like_post,name='like_post'),
    path('favourites/<int:id>', views.favourite_book,name='favourite_book'),
    path('favouritebooks/', views.userfavourite_book,name='userfavourite_book'),


   
    #path('book/delete/<int:pk>', BookDelete.as_view(), name='book_paste_delete'),
   # path('userprofileupdate/<int:pk>',  userprofileUpdate.as_view(), name=' userprofileupdate'),
    
   
    #path('books/category/(?P<pk>[\d]+)/$', Bookcategory.as_view(), name='post_by_category' )
    #url(r'^category/(?P<category_slug>[-\w]+)/$',views.list_of_post_by_category,name='post_by_category')




]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)