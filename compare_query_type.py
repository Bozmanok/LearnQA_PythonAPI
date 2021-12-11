import requests

# решение по п.1
response_without_method = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"Ответ на запрос без метода: {response_without_method.text}")

# решение по п.2
response_with_head = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"Ответ на запрос с типом HEAD: {response_with_head.text}")

# решение по п.3
method = {"method": "GET"}
response_with_method_get = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=method)
print(f"Ответ на запрос с методом GET: {response_with_method_get.text}")

# решение по п.4
methods = [
    {"method": "GET"},
    {"method": "POST"},
    {"method": "PUT"},
    {"method": "DELETE"}
]


def request_with_method(type_request, url, method):
    if type_request == "GET":
        response = requests.request(type_request, url, params=method)
    else:
        response = requests.request(type_request, url, data=method)
    return response


def enumeration_of_methods(type_request, list_methods):
    m = 0
    while m < len(methods):
        response = request_with_method(
            type_request,
            "https://playground.learnqa.ru/ajax/api/compare_query_type",
            list_methods[m]
        )
        if type_request == list_methods[m]["method"]:
            if response.text == "Wrong method provided":
                print(f"Тип запроса {type_request} и метод {list_methods[m]} совпадают, но сервер отвечает ошибкой")
        else:
            if response.text != "Wrong method provided":
                print(f"Тип запроса {type_request} и метод {list_methods[m]} не совпадают, но сервер считает, что всё ОК")
        m = m + 1


n = 0
while n < len(methods):
    type_request = methods[n]["method"]
    enumeration_of_methods(type_request, methods)
    n = n + 1
