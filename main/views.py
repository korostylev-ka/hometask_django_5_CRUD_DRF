from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Book, Order
from main.serializers import BookSerializer, OrderSerializer


@api_view(['GET'])
def books_list(request):
    """получите список книг из БД
    отсериализуйте и верните ответ
    """
    books = Book.objects.all()
    ser = BookSerializer(books, many=True)
    return Response(ser.data)


class CreateBookView(APIView):
    # http_method_names = ['GET', 'POST']
    def post(self, request):
        book = request.data
        # получите данные из запроса
        serializer = BookSerializer(data=book) #передайте данные из запроса в сериализатор
        if serializer.is_valid(raise_exception=True): #если данные валидны
            book_saved = serializer.save()
            return Response('Книга успешно создана') # возвращаем ответ об этом

class BookDetailsView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUpdateView(UpdateAPIView):
    # реализуйте логику обновления объявления
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()
    # реализуйте логику удаления объявления
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # реализуйте CRUD для заказов
    def create(self, request, *args, **kwargs):
        order = request.data
        serializer = OrderSerializer(data=order)
        if serializer.is_valid(raise_exception=True): #если данные валидны
            order_saved = serializer.save()
            return Response('Заказ успешно оформлен')
        return request
    def destroy(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        order = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, order)
        if serializer.is_valid(raise_exception=True):  # если данные валидны
            serializer.save()
            return Response('Заказ успешно обновлен')
        return request

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)


