from django.urls import path
from . import views
from .views import UsuarioPorCorreoApi, DetallePorIdApi, VentaPorIdApi, UsuarioPorRutApi

urlpatterns=[
    path('api/categorias/', views.listaCategoriasApi.as_view(), name='api-categorias'),
    path('api/roles/', views.listaRolesApi.as_view(), name='api-roles'),
    path('api/usuarios/', views.listaUsuariosApi.as_view(), name='api-usuarios'),
    path('api/productos/', views.listaProductosApi.as_view(), name='api-productos'),
    path('api/ventas/', views.listaVentasApi.as_view(), name='api-ventas'),
    path('api/detalles/', views.listaDetallesApi.as_view(), name='api-detalles'),
    path('api/compras/', views.listaComprasApi.as_view(), name='api-compras'),
    path('api/transacciones/', views.listaTransaccionesApi.as_view(), name='api-transacciones'),
    path('api/consultas/', views.listaConsultasApi.as_view(), name='api-consultas'),
    path('api/producto/', views.productoApi.as_view(), name='api-producto'),
    path('api/detallesProducto/', views.listaDetallesProductoApi.as_view(), name='api-detalles-producto'),
    path('api/usuarioC/<str:correo>/', UsuarioPorCorreoApi.as_view(), name='usuario-por-correo'),
    path('api/usuarioR/<str:rut>/', UsuarioPorRutApi.as_view(), name='usuario-por-rut'),
    path('api/filtrar-carrito/', views.FiltrarCarritoAPI.as_view(), name='filtrar-carrito'),
    path('api/detalles-carrito/', views.DetallesCarritoAPI.as_view(), name='detalles-carrito'),
    path('api/detalles-id-carrito/', views.DetallesCarritoPorIdAPI.as_view(), name='detalles-id-carrito'),
    path('api/delete-detalle/', views.DeleteDetallePorIdApi.as_view(), name='delete-detalle'),
    path('api/detalles-buscar-carrito/', views.DetallesBuscarCarritoAPI.as_view(), name='detalles-buscar-carrito'),
    path('api/detalle/<str:id_detalle>/', DetallePorIdApi.as_view(), name='detalle-por-id'),
    path('api/venta/<str:id_venta>/', VentaPorIdApi.as_view(), name='venta-por-id'),
    path('api/crear-detalle/', views.CrearDetalleAPI.as_view(), name='crear-detalle'),
    path('api/crear-venta/', views.CrearVentaAPI.as_view(), name='crear-venta'),
    path('api/crear-usuario/', views.CrearUsuarioAPI.as_view(), name='crear-usuario'),
    path('api/transacciones-producto/', views.transaccionesProductoApi.as_view(), name='transacciones-producto'),
    path('api/stock-producto/', views.StockProductoApi.as_view(), name='stock-producto'),
]