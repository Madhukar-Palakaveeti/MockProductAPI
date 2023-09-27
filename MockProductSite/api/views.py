from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.models import Product
from api.serializers import ProductSerializer

# Create your views here.
@csrf_exempt
def product_list(request):
    '''
        List all the products or create a new one
    '''
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False)
    
@csrf_exempt
def create_product(request):
    '''
        A view for creating a new product
    '''
        
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
@csrf_exempt
def update_product(request,pk):
    '''
        Retrieve or Update a product
    '''
    try:
        product = Product.objects.get(pk=pk)
    except product.DoesNotExist as e:
        return HttpResponse({'message' : e}, status=404)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data, status=200)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    
@csrf_exempt
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except product.DoesNotExist as e:
        return HttpResponse({'message' : e}, status=404)
    
    if request.method == 'DELETE':
        product.delete()
        return JsonResponse({'message' : 'Product Deleted Successfully!!'},status=204)