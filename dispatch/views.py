from django.db.models import Count, Q
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from dispatch.tasks import send_message_async
from dispatch.models import Dispatch, Client, Mailing, Message
from dispatch.serializerss import DispatchSerializer, MailingSerializer, ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def perform_create(self, serializer):
        mailing = serializer.save()
        send_message_async.delay(mailing.client.id, mailing.message_text)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)


class DispatchViewSet(viewsets.ModelViewSet):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer


class MailingStatsView(APIView):
    def get(self, request):
        #Получаем общую статистику по рассылкам
        mailing_stats = Mailing.objects.aggregate(
            total_mailings=Count('id'),
            total_messages=Count('message_text'),
            delivered_messages=Count('messages', filter=Q(messages__status='delivered')),
            failed_messages=Count('messages', filter=Q(messages__status='failed'))
        )

        #Формируем JSON-ответ
        response = {
            'total_mailings': mailing_stats['total_mailings'],
            'total_messages': mailing_stats['total_messages'],
            'delivered_messages': mailing_stats['delivered_messages'],
            'failed_messages': mailing_stats['failed_messages']
        }
        return JsonResponse(response)


@api_view(['POST'])
def create_client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response({'error': 'Не найден'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(client, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


