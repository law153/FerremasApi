from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, F
from .serializers import categoriaSerializer, usuarioSerializer, productoSerializer, consultaSerializer, ventaSerializer, detalleSerializer, detalleCompradoSerializer, detalleConProductoSerializer, transaccionSerializer
from .models import Categoria, Consulta, Usuario, Producto, Venta, Detalle,  Detalle_comprado, Transaccion


# Create your views here.
class listaCategoriasApi(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = categoriaSerializer

class listaUsuariosApi(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = usuarioSerializer

class UsuarioPorCorreoApi(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = usuarioSerializer
    lookup_field = 'correo'

class listaProductosApi(generics.ListAPIView):
    serializer_class = productoSerializer

    def get_queryset(self):
        queryset = Producto.objects.all()
        categoria = self.request.query_params.get('categoria')
        if categoria is not None:
            queryset = queryset.filter(categoria=categoria)
        return queryset
    
class productoApi(generics.ListAPIView):
    serializer_class = productoSerializer

    def get_queryset(self):
        queryset = Producto.objects.all()
        codigo = self.request.query_params.get('cod_prod')
        if codigo is not None:
            queryset = queryset.filter(cod_prod=codigo)
        return queryset

class listaVentasApi(generics.ListAPIView):
    queryset = Venta.objects.all()
    serializer_class = ventaSerializer

class listaConsultasApi(generics.ListAPIView):
    queryset = Consulta.objects.all()
    serializer_class = consultaSerializer

class listaDetallesApi(generics.ListAPIView):
    queryset = Detalle.objects.all()
    serializer_class = detalleSerializer

class DetallePorIdApi(generics.RetrieveUpdateAPIView):
    queryset = Detalle.objects.all()
    serializer_class = detalleSerializer
    lookup_field = 'id_detalle'

class DeleteDetallePorIdApi(APIView):
    def delete(self, request):
        id_detalle = request.GET.get('id_detalle')

        try:
            detalle = Detalle.objects.get(id_detalle=id_detalle)
        except Detalle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        detalle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class listaDetallesProductoApi(generics.ListAPIView):
    queryset = Detalle.objects.all()
    serializer_class = detalleConProductoSerializer

class listaComprasApi(generics.ListAPIView):
    queryset = Detalle_comprado.objects.all()
    serializer_class = detalleCompradoSerializer

class FiltrarCarritoAPI(APIView):
    def get(self, request):
        # Obtener los parámetros de consulta de la URL
        usuario = request.GET.get('usuario')
        estado = request.GET.get('estado')

        # Filtrar usuarios basados en los parámetros
        carrito = Venta.objects.all()
        if carrito:
            carrito = carrito.filter(usuario=usuario)
        if estado:
            carrito = carrito.filter(estado=estado)

        # Serializar los resultados y devolver la respuesta
        serializer = ventaSerializer(carrito, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DetallesCarritoAPI(APIView):
    def get(self, request):
        # Obtener el ID de la venta desde los parámetros de la URL
        id_venta = request.GET.get('venta')

        # Buscar todos los detalles del carrito basados en el ID de la venta
        detalles_carrito = Detalle.objects.filter(venta=id_venta)

        # Serializar los resultados y devolver la respuesta
        serializer = detalleConProductoSerializer(detalles_carrito, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DetallesCarritoPorIdAPI(APIView):
    def get(self, request):
        id_detalle = request.GET.get('id_detalle')

        detalles_carrito = Detalle.objects.filter(id_detalle=id_detalle)

        serializer = detalleConProductoSerializer(detalles_carrito, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VentaPorIdApi(generics.RetrieveUpdateAPIView):
    queryset = Venta.objects.all()
    serializer_class =ventaSerializer
    lookup_field = 'id_venta'

class DetallesBuscarCarritoAPI(APIView):
    def get(self, request):
        # Obtener el ID de la venta y el código del producto desde los parámetros de la URL
        id_venta = request.GET.get('venta')
        cod_producto = request.GET.get('producto')

        # Filtrar los detalles del carrito basados en el ID de la venta y el código del producto
        detalles_carrito = Detalle.objects.filter(venta=id_venta, producto__cod_prod=cod_producto)

        # Serializar los resultados y devolver la respuesta
        serializer = detalleConProductoSerializer(detalles_carrito, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CrearDetalleAPI(APIView):
    def post(self, request):
        serializer = detalleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CrearVentaAPI(APIView):
    def post(self, request):
        serializer = ventaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class listaTransaccionesApi(generics.ListAPIView):
    queryset = Transaccion.objects.all()
    serializer_class = transaccionSerializer

class transaccionesProductoApi(APIView):
    def get(self, request):
        producto = request.GET.get('producto')
        print("Código de producto recibido:", producto)  # Impresión para depurar

        transacciones = Transaccion.objects.filter(producto=producto)
        print("Número de transacciones encontradas:", transacciones.count())  # Impresión para depurar

        serializer = transaccionSerializer(transacciones, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StockProductoApi(APIView):
    def get(self, request):
        producto = request.GET.get('producto')

        stock_agregar = Transaccion.objects.filter(producto=producto, tipo_transaccion='Agregar').aggregate(Sum('cantidad'))['cantidad__sum'] or 0
        stock_retirar = Transaccion.objects.filter(producto=producto, tipo_transaccion='Retirar').aggregate(Sum('cantidad'))['cantidad__sum'] or 0

        stock_total = stock_agregar - stock_retirar

        return Response({'stock_total': stock_total}, status=status.HTTP_200_OK)
