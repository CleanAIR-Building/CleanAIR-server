import datetime
from django.shortcuts import render
from django.utils import timezone

from plotly.offline import plot
import plotly.graph_objs as graphs

from .models import CarbonDioxideData, Limit, PhotoElectricData, WindowStateData

def homepage(request):
    now = timezone.now()
    time_filter = now - datetime.timedelta(minutes=20)

    # retrieve the latest entry to the window state data
    window_state_data = WindowStateData.objects.all().order_by("-id")[0]

    # retrieve the latest entry to the photoelectric data
    visitor_data = PhotoElectricData.objects.all().order_by("-id")[0]
    green = "green" if visitor_data.state == "NOT_FULL" else ""
    red = "red" if visitor_data.state == "FULL" else ""
    entry = "OPEN" if visitor_data.state == "NOT_FULL" else "CLOSED"

    context = {
        'visitors': visitor_data.count,
        'window': window_state_data.state,
        'entry': entry,
        'green': green,
        'red': red,
        'window_open_plot': __create_window_open_plot(time_filter),
        'airquality_plot': __create_airquality_plot(time_filter),
        'visitors_plot': __create_visitors_plot(time_filter),
        'now': now
    }

    return render(request, 'index.html', context)

def __create_window_open_plot(time_filter):

    window_state_data = WindowStateData.objects.filter(time__gte=time_filter)

    if len(window_state_data) > 0:
        figure = graphs.Figure()
        window_time=[]
        window_open=[]

        for data in window_state_data:
            window_time.append(__convert_timezone_for_plotly(data.time))
            window_open.append(data.state)

        # Append another value for the current time with the current state for a more beautiful chart
        window_time.append(__convert_timezone_for_plotly(timezone.now()))
        last_value = window_open[(len(window_open)-1)]
        window_open.append(last_value)

        scatter_plot = graphs.Scatter(x=window_time, y=window_open, mode='lines', line={"shape": "hv"}, name='window_open')
        figure.add_trace(scatter_plot)
        figure.update_layout(title='Opening and Closing of the Window', xaxis_title='time', yaxis_title='window state')

        return plot(figure, output_type='div')
    else:
        return '<p><i>The window state has not changed in the last hour.</i></p>'


def __create_airquality_plot(time_filter):

    airquality_data = CarbonDioxideData.objects.filter(time__gte=time_filter)

    if len(airquality_data) > 0:
        figure = graphs.Figure()
        time=[]
        eCO2=[]

        for data in airquality_data:
            time.append(__convert_timezone_for_plotly(data.time))
            eCO2.append(data.co2)

        scatter_plot = graphs.Scatter(x=time, y=eCO2, mode='lines', name='airquality')
        figure.add_trace(scatter_plot)

        limit = Limit.objects.filter(name="co2_limit")[0]
        figure.add_hline(y=limit.limit, line_dash="dot", annotation_text="Critical air quality threshold", annotation_position="top left")
        
        figure.update_layout(
            title='Airquality in the Building', 
            xaxis_title='time', 
            yaxis_title='eCO2 in ppm')

        return plot(figure, output_type='div')
    else:
        return '<p><i>The airquality was not measured in the last hour.</i></p>'



def __create_visitors_plot(time_filter):

    data = PhotoElectricData.objects.filter(time__gte=time_filter)

    if len(data) > 0:

        figure = graphs.Figure()
        time=[]
        current_visitors=[]

        for data in data:
            time.append(__convert_timezone_for_plotly(data.time))
            current_visitors.append(data.count)

        # Append another value for the current time with the current state for a more beautiful chart
        time.append(__convert_timezone_for_plotly(timezone.now()))
        last_value = current_visitors[(len(current_visitors)-1)]
        current_visitors.append(last_value)

        scatter_plot = graphs.Scatter(x=time, y=current_visitors, mode='lines', line={"shape": "hv"}, name='window_open')
        figure.add_trace(scatter_plot)

        limit = Limit.objects.filter(name="occupation_limit")[0]
        figure.add_hline(y=limit.limit, line_dash="dot", annotation_text="Limit of visitors", annotation_position="top left")

        figure.update_layout(
            title='Visitors in the Building', 
            xaxis_title='time', 
            yaxis_title='number of visitors')

        return plot(figure, output_type='div', include_plotlyjs=False)
    else: 
        return '<p><i>No guests entered or left the building in the last hour.</i></p>'


def __convert_timezone_for_plotly(dt: datetime.datetime):
    return dt + datetime.timedelta(hours=2)