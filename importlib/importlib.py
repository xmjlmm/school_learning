import importlib
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response

class Creat(APIView):
    def post(self, request):
        try:
            pay_method = "Wxpay"  # 示例中的支付方式
            pay_module = f"app01.Pay.{pay_method}"
            pay_file = importlib.import_module(pay_module)
            pay_class = getattr(pay_file, pay_method)
            order_data = {
                'open_id': request.data.get('openid'),
                'ip': request.data.get('host_ip')
            }
            data = pay_class().pay(order_data)
            return Response(data)
        except ModuleNotFoundError:
            return Response({"code": 201, "msg": "未知支付方式"})
        except Exception as e:
            # 记录详细的错误日志
            print(f"Error occurred: {str(e)}")
            return Response({"code": 500, "msg": "支付失败，请联系客服"})

class Notify(APIView):
    def post(self, request, paymethod):
        try:
            pay_module = f"app01.Pay.{paymethod}"
            pay_file = importlib.import_module(pay_module)
            pay_class = getattr(pay_file, paymethod)
            with transaction.atomic():
                data = pay_class().notify(request.data)
                if data.get("status") == "success":
                    models.Order.objects.filter(order_id=data['order_id']).update(pay_status=1)
                return Response(data.get("print"))
        except ModuleNotFoundError:
            return Response({"code": 201, "msg": "未知支付方式"})
        except Exception as e:
            # 记录详细的错误日志
            print(f"Error occurred: {str(e)}")
            return Response({"code": 500, "msg": "支付状态更新失败，请联系客服"})
