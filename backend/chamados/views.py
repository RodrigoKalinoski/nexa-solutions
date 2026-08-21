from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chamado
from .serializers import ChamadoSerializer


class ChamadoListCreateView(generics.ListCreateAPIView):
    serializer_class = ChamadoSerializer

    def get_queryset(self):
        queryset = Chamado.objects.all().order_by("-criado_em")

        status = self.request.query_params.get("status")

        if not status:
            return queryset

        status_validos = Chamado.Status.values

        if status not in status_validos:
            raise ValidationError(
                {
                    "status": (
                        "Status inválido. Utilize ABERTO, "
                        "EM_ANDAMENTO ou CONCLUIDO."
                    )
                }
            )

        return queryset.filter(status=status)


class ChamadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer

class IndicadoresView(APIView):
    def get(self, request):
        dados = {
            "total": Chamado.objects.count(),
            "abertos": Chamado.objects.filter(
                status=Chamado.Status.ABERTO
            ).count(),
            "em_andamento": Chamado.objects.filter(
                status=Chamado.Status.EM_ANDAMENTO
            ).count(),
            "concluidos": Chamado.objects.filter(
                status=Chamado.Status.CONCLUIDO
            ).count(),
        }

        return Response(dados)