from django.urls import path

from cine import views

urlpatterns = [


    path('index/', views.index, name='index'),

    path('movie/genre', views.movie_genre_filter, name="movie_genre_filter"),

    path('movie-view/<int:id>/view', views.movie_view, name="movie_view"),
    path('movie-detail/<int:id>/edit', views.movie_detail, name="movie_detail"),
    path('movie/new', views.movie_new, name="movie_new"),
    path('movie/save', views.movie_save, name="movie_save"),
    path('movie/<int:id>/load', views.movie_load, name="movie_load"),
    path('movie/<int:pk>/delete', views.movie_delete, name='movie_delete'),
    path('accounts/login/', views.do_login, name="login"),
    path('accounts/logout/', views.do_logout, name="logout"),
    path('accounts/register/', views.do_register, name="register"),
    path('movie/<int:id>/favourite', views.movie_favourite, name='favourite-add'),
    path('movie/<int:id>/favourite-delete', views.favourite_delete, name='favourite-delete'),
    path('favourite/', views.favourite, name='favourite'),
    path('studio-view/<int:id>/view', views.studio_view, name='studio-view'),
    path('studio-detail/<int:id>/edit', views.studio_detail, name='studio-detail'),
    path('studio-list/', views.studio_list, name='studio-list'),
    path('studio-delete/<int:id>/delete', views.studio_delete, name='studio-delete'),
    path('studio-new/', views.studio_new, name='studio-new'),
    path('studio-save/', views.studio_save, name='studio-save'),
    path('country-view/<int:id>/view', views.country_view, name='country-view'),
    path('country-detail/<int:id>/edit', views.country_detail, name='country-detail'),
    path('country-list/', views.country_list, name='country-list'),
    path('country-delete/<int:id>/delete', views.country_delete, name='country-delete'),
    path('country-new/', views.country_new, name='country-new'),
    path('country-save/', views.country_save, name='country-save'),
    path('genre-view/<int:id>/view', views.genre_view, name='genre-view'),
    path('genre-detail/<int:id>/edit', views.genre_detail, name='genre-detail'),
    path('genre-list/', views.genre_list, name='genre-list'),
    path('genre-delete/<int:id>/delete', views.genre_delete, name='genre-delete'),
    path('genre-new/', views.genre_new, name='genre-new'),
    path('genre-save/', views.genre_save, name='genre-save'),
    path('actor/', views.actor, name="actor"),
    path('director/', views.director, name="director"),
    path('filtrar_actor/<clave>/', views.filtro_actor, name="actor-view"),
    path('filtrar_director/<clave>/', views.filtro_director, name="director-view"),
    path('borrar_actor/<clave>/', views.borra_actor, name="actor-delete"),
    path('modificar_actor/<clave>/', views.modifica_actor, name="actor-update"),
    path('guardar_actor/', views.guardar_actor, name="actor-save"),
    path('crear_actor/', views.crear_actor, name="actor-create"),
    path('borrar_director/<clave>/', views.borra_director, name="director-delete"),
    path('modificar_director/<clave>/', views.modifica_director, name="director-update"),
    path('guardar_director/', views.guardar_director, name="director-save"),
    path('crear_director/', views.crear_director, name="director-create"),
    path('site-list/', views.site_list, name='site-list'),
    # path('lugares/', views.lugar, name="lugares"),
    # path('filtrar_lugares/<clave>/', views.filtro, name="site-view"),
    # path('borrar/<clave>/', views.borra, name="site-delete"),
    # path('modificar/<clave>/', views.modifica, name="site-update"),
    # path('guardar_lugares/', views.guardar_lugares, name="site-save"),
    # path('crear_lugares/', views.crear_lugares, name="site-create")
]
