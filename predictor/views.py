from django.shortcuts import render
import json

# Create your views here.
# predictor/views.py

from django.shortcuts import render
from .forms import RunInputForm
from .models import RunningData
from .predictor import predict_run, estimate_marathon_time, estimate_half_marathon_time

def predict_view(request):
    if request.method == 'POST':
        form = RunInputForm(request.POST)
        if form.is_valid():
            distance = form.cleaned_data['distance']
            minutes = form.cleaned_data['minutes']
            seconds = form.cleaned_data['seconds']
            
            # Perform prediction
            predicted = predict_run(distance, minutes, seconds)
            print("Predicted values:", predicted)  # Debug
            pace, avg_bpm, stride, cadence = predicted[0]

            # Estimate the marathon and half marathon times based on predicted pace
            marathon_time = estimate_marathon_time(pace)
            half_marathon_time = estimate_half_marathon_time(pace)

            # Save data to the database
            RunningData.objects.create(
                distance=distance,
                minutes=minutes,
                seconds=seconds,
                pace=pace,
                avg_bpm=avg_bpm,
                stride=stride,
                cadence=cadence
            )

            # Get data for the chart
            recent_data = RunningData.objects.order_by('-date')[:4]
            distances = [data.distance for data in recent_data]
            paces = [data.pace for data in recent_data]

            # Prepare data for the chart
            chart_data = {
                'distances': distances,
                'paces': paces,
            }

            context = {
                'form': form,
                'predicted_pace': pace,
                'predicted_avg_bpm': avg_bpm,
                'predicted_stride': stride,
                'predicted_cadence': cadence,
                'marathon_time': marathon_time,
                'half_marathon_time': half_marathon_time,
                'chart_data': json.dumps(chart_data),
            }

            return render(request, 'result.html', context)
        
    else:
        form = RunInputForm()

    return render(request, 'predict.html', {'form': form})
