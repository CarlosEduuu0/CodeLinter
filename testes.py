"""Testes: 6+ aceitas, 6+ rejeitadas, caso-limite, e equivalência ER (re) x AFNε."""
import random
import unittest

from analisador import EntradaInvalida, analisar, sanitizar_linha, validar_texto
from expressoes import EXPRESSOES


class TestExpressoes(unittest.TestCase):
    def test_quantidades_minimas(self):
        for er in EXPRESSOES:
            with self.subTest(er=er.id):
                self.assertGreaterEqual(len(er.aceitas), 6)
                self.assertGreaterEqual(len(er.rejeitadas), 6)
                self.assertTrue(er.limites)
                self.assertTrue(set(er.limites) <= set(er.aceitas) | set(er.rejeitadas))

    def test_aceitas_e_rejeitadas(self):
        for er in EXPRESSOES:
            for s in er.aceitas:
                with self.subTest(er=er.id, cadeia=s, esperado="aceita"):
                    self.assertTrue(er.reconhece_regex(s), "re")
                    self.assertTrue(er.reconhece_afn(s), "AFNε")
            for s in er.rejeitadas:
                with self.subTest(er=er.id, cadeia=s, esperado="rejeita"):
                    self.assertFalse(er.reconhece_regex(s), "re")
                    self.assertFalse(er.reconhece_afn(s), "AFNε")

    def test_equivalencia_por_mutacao(self):
        rnd = random.Random(2026)
        for er in EXPRESSOES:
            alfabeto = sorted({c for s in er.aceitas + er.rejeitadas for c in s})
            base = er.aceitas + er.rejeitadas
            for _ in range(400):
                s = list(rnd.choice(base))
                for _ in range(rnd.randint(1, 3)):
                    op = rnd.choice("ird") if s else "i"
                    p = rnd.randrange(len(s) + 1)
                    if op == "i":
                        s.insert(p, rnd.choice(alfabeto))
                    elif s:
                        p = min(p, len(s) - 1)
                        if op == "r":
                            s[p] = rnd.choice(alfabeto)
                        else:
                            del s[p]
                s = "".join(s)
                self.assertEqual(er.reconhece_regex(s), er.reconhece_afn(s), f"{er.id}: {s!r}")


class TestAplicacao(unittest.TestCase):
    def test_entrada_vazia(self):
        for t in ("", "   \n  ", None):
            with self.assertRaises(EntradaInvalida):
                validar_texto(t)

    def test_mascara_cpf(self):
        self.assertEqual(sanitizar_linha("cpf=123.456.789-09 e 52998224725"), "cpf=**.***.***-** e **.***.***-**")

    def test_deteccao(self):
        rel, _ = analisar(["1.2.3.4 GET /a?id=1'%20OR%20'1'='1", "5.6.7.8 GET /../../etc/passwd", "ok normal"])
        self.assertEqual(rel["ameacas_por_tipo"], {"SQLi": 1, "Path Traversal": 1})

    def test_fronteira_ip_invalido(self):
        rel, _ = analisar(["999.999.1.1 GET /x"])
        self.assertEqual(rel["resumo"]["linhas_sem_ip"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
