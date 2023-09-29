from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.models import Product
from api.serializers import ProductSerializer
from api.helpers import get_links
from bs4 import BeautifulSoup
import asyncio
import aiohttp

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
    
def get_product_urls(request):
    

    def get_title(soup):
        try:
            title_tag = soup.find("span", {"class" : "B_NuCI"})
            title = title_tag.text
        except AttributeError:
            title = ""

        return title

    def get_reviews(soup):
        try:
            review_tag = soup.find("div", {"class" : "_3LWZlK"})
            review = review_tag.text

        except AttributeError:
            review = ""
        
        return review

    def get_price(soup):
        try:
            price_tag = soup.find("div", {"class": "_30jeq3 _16Jk6d"})
            price =  price_tag.text.strip()[1:]

        except AttributeError:
            price = ""
        
        return price

    def get_discount(soup):
        try:
            discount_tag = soup.find("div",{"class" : "_3Ay6Sb _31Dcoz"}).span
            discount = discount_tag.text

        except AttributeError:
            discount = "No Discount"

        return discount

    def parse(results):
        result_list = []
        for html in results:
            product_json = {}
            soup = BeautifulSoup(html, 'html.parser') 
            product_json['title'] = get_title(soup)
            product_json['rating'] = get_reviews(soup)
            product_json['price'] = get_price(soup)
            product_json['discount'] = get_discount(soup)

            result_list.append(product_json)

        return result_list

    async def get_page(session, url):
        async with session.get(url, ssl=False) as r:
            return await r.text()
        

    async def get_all(session, urls):
        tasks = []
        for url in urls:
            task = asyncio.create_task(get_page(session, url))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results

    async def get_product_html(urls):
        async with aiohttp.ClientSession() as session:
            data = await get_all(session, urls)
            return data

    URLS = []
    q = request.GET.get('q')
    for page in range(1,4):
        url = f'https://www.flipkart.com/search?q={q}&page={page}'
        URLS.extend(get_links(url))   
    results = asyncio.run(get_product_html(URLS))
    result = parse(results)
    return JsonResponse(result, safe=False)