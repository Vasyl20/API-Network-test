from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
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