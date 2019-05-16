from django.conf.urls import url
from BoulderBlueServerWebApp.blue_views import views

urlpatterns = [
    url(r'mouse_viewer[/]?$', views.index, name='mouse_viewer'),
    url(r'home[/]?$', views.home, name='home'),
    url(r'mouse_viewer/(?P<mac>[^\/]+)/register[/]?$', views.register, name='mouse_viewer_register'),
    url(r'mouse_viewer/(?P<mac>[^\/]+)/unregister[/]?$', views.unregister, name='mouse_viewer_unregister'),
    url(r'mouse_viewer/mouse_viewer_select_commands[/]?$', views.select_commands, name='mouse_viewer_select_commands'),
    url(r'mouse_viewer/mouse_viewer_send_selected_commands/(?P<chip_commands>[^\/]+)', views.send_selected_commands,
        name='mouse_viewer_send_selected_commands'),
    url(r'mouse_viewer/command_create[/]?$', views.command_create, name='command_create'),
    url(r'mouse_viewer/scheduled_commands[/]?$', views.scheduled_commands, name='scheduled_commands'),
    url(r'mouse_viewer_log[/]?$', views.log, name='mouse_viewer_log'),
    # url(r'mouse_chart[/]?$', views.demo_linechart, name='mouse_chart'),
    url(r'mouse_viewer_csv[/]?$', views.csv_out, name='mouse_viewer_csv'),
    url(r'mouse_receive_data_log[/]?$', views.received_data_log, name='mouse_receive_data_log'),
    url(r'mouse_receive_data_csv[/]?$', views.received_data_csv_out, name='mouse_receive_data_csv'),
    url(r'mouse_viewer_save_text[/]?$', views.save_text, name='mouse_viewer_save_text'),
    url(r'run_test[/]?$', views.run_test, name='run_test'),
]
