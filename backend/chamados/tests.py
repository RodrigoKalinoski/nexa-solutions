from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


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