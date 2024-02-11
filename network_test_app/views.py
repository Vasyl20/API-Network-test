from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .models import NetworkTestResult
from .serializers import NetworkTestResultSerializer
import speedtest

class NetworkTestView(APIView):
    def get(self, request):
        try:
            st = speedtest.Speedtest()

            # Тестування швидкості інтернет-з'єднання
            download_speeds = [st.download() for _ in range(3)]
            upload_speeds = [st.upload() for _ in range(3)]

            # Отримання мінімальної, максимальної та середньої швидкостей
            min_download_speed = min(download_speeds) / 1_000_000
            max_download_speed = max(download_speeds) / 1_000_000
            avg_download_speed = sum(download_speeds) / len(download_speeds) / 1_000_000

            min_upload_speed = min(upload_speeds) / 1_000_000
            max_upload_speed = max(upload_speeds) / 1_000_000
            avg_upload_speed = sum(upload_speeds) / len(upload_speeds) / 1_000_000

            # Тестування пінгу
            ping = st.results.ping

            # Збереження результатів тестування в базі даних
            self.save_test_results(min_download_speed, max_download_speed, avg_download_speed,
                                   min_upload_speed, max_upload_speed, avg_upload_speed, ping)

            response_data = {
                'min_download_speed': min_download_speed,
                'max_download_speed': max_download_speed,
                'avg_download_speed': avg_download_speed,
                'min_upload_speed': min_upload_speed,
                'max_upload_speed': max_upload_speed,
                'avg_upload_speed': avg_upload_speed,
                'ping': ping
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_test_results(self, min_download, max_download, avg_download,
                          min_upload, max_upload, avg_upload, ping):
        # Збереження результатів тестування в базі даних
        test_results = NetworkTestResult.objects.all().order_by('-created_at')[:5]

        # Видалення першого результату, якщо їх більше 5
        if len(test_results) >= 5:
            test_results[0].delete()

        # Посування інших результатів
        for i in range(len(test_results) - 1, 0, -1):
            test_results[i].created_at = test_results[i - 1].created_at
            test_results[i].min_download_speed = test_results[i - 1].min_download_speed
            test_results[i].max_download_speed = test_results[i - 1].max_download_speed
            test_results[i].avg_download_speed = test_results[i - 1].avg_download_speed
            test_results[i].min_upload_speed = test_results[i - 1].min_upload_speed
            test_results[i].max_upload_speed = test_results[i - 1].max_upload_speed
            test_results[i].avg_upload_speed = test_results[i - 1].avg_upload_speed
            test_results[i].ping = test_results[i - 1].ping
            test_results[i].save()

        # Збереження нового результату на місце 5
        new_result = NetworkTestResult.objects.create(
            min_download_speed=min_download,
            max_download_speed=max_download,
            avg_download_speed=avg_download,
            min_upload_speed=min_upload,
            max_upload_speed=max_upload,
            avg_upload_speed=avg_upload,
            ping=ping
        )