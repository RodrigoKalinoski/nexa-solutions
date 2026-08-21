from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Chamado


class ChamadoCreateTests(APITestCase):
    def setUp(self):
        self.url = reverse("chamado-list-create")

    def test_criar_chamado_valido(self):
        dados = {
            "titulo": "Erro ao acessar sistema",
            "descricao": "Usuário não consegue realizar login",
        }

        response = self.client.post(
            self.url,
            dados,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            response.data["titulo"],
            "Erro ao acessar sistema",
        )
        self.assertEqual(
            response.data["status"],
            "ABERTO",
        )

    def test_nao_permite_criar_chamado_sem_titulo(self):
        dados = {
            "descricao": "Chamado sem título",
        }

        response = self.client.post(
            self.url,
            dados,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("titulo", response.data)

    def test_nao_permite_criar_chamado_com_titulo_vazio(self):
        dados = {
            "titulo": "",
            "descricao": "Chamado com título vazio",
        }

        response = self.client.post(
            self.url,
            dados,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("titulo", response.data)

class ChamadoFiltroStatusTests(APITestCase):
    def setUp(self):
        self.url = reverse("chamado-list-create")

        Chamado.objects.create(
            titulo="Chamado aberto",
            descricao="Teste",
            status=Chamado.Status.ABERTO,
        )

        Chamado.objects.create(
            titulo="Chamado em andamento",
            descricao="Teste",
            status=Chamado.Status.EM_ANDAMENTO,
        )

        Chamado.objects.create(
            titulo="Chamado concluído",
            descricao="Teste",
            status=Chamado.Status.CONCLUIDO,
        )

    def test_filtrar_chamados_por_status_aberto(self):
        response = self.client.get(
            self.url,
            {"status": "ABERTO"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["status"],
            "ABERTO",
        )

    def test_filtrar_chamados_por_status_em_andamento(self):
        response = self.client.get(
            self.url,
            {"status": "EM_ANDAMENTO"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["status"],
            "EM_ANDAMENTO",
        )

    def test_filtrar_chamados_por_status_concluido(self):
        response = self.client.get(
            self.url,
            {"status": "CONCLUIDO"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["status"],
            "CONCLUIDO",
        )

    def test_status_invalido_retorna_400(self):
        response = self.client.get(
            self.url,
            {"status": "INVALIDO"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("status", response.data)
    def test_listar_todos_os_chamados_sem_filtro(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 3)

class IndicadoresTests(APITestCase):
    def setUp(self):
        self.url = reverse("indicadores")

        Chamado.objects.create(
            titulo="Chamado aberto 1",
            status=Chamado.Status.ABERTO,
        )

        Chamado.objects.create(
            titulo="Chamado aberto 2",
            status=Chamado.Status.ABERTO,
        )

        Chamado.objects.create(
            titulo="Chamado em andamento",
            status=Chamado.Status.EM_ANDAMENTO,
        )

        Chamado.objects.create(
            titulo="Chamado concluído",
            status=Chamado.Status.CONCLUIDO,
        )

    def test_retornar_indicadores_dos_chamados(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["total"], 4)
        self.assertEqual(response.data["abertos"], 2)
        self.assertEqual(response.data["em_andamento"], 1)
        self.assertEqual(response.data["concluidos"], 1)

    def test_indicadores_sem_chamados(self):
        Chamado.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["total"], 0)
        self.assertEqual(response.data["abertos"], 0)
        self.assertEqual(response.data["em_andamento"], 0)
        self.assertEqual(response.data["concluidos"], 0)