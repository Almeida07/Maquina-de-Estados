import pytest
from vending import MaquinaVenda, Estado, TransicaoInvalida


# ---------- helpers: levam a máquina a cada estado ----------
def em_ociosa():
    return MaquinaVenda()


def em_com_credito(valor=100):
    m = MaquinaVenda()
    m.inserir_moeda(valor)
    return m


def em_dispensando():
    m = em_com_credito(500)
    m.selecionar()
    return m


def em_fora_de_servico():
    m = em_dispensando()
    m.falha_mecanica()
    return m


# ---------- 3.1 Testes de ESTADOS ----------
@pytest.mark.parametrize("fabrica, esperado", [
    (em_ociosa, Estado.OCIOSA),
    (em_com_credito, Estado.COM_CREDITO),
    (em_dispensando, Estado.DISPENSANDO),
    (em_fora_de_servico, Estado.FORA_DE_SERVICO),
])
def test_todos_os_estados_sao_alcancaveis(fabrica, esperado):
    assert fabrica().estado == esperado


# ---------- 3.2 Testes de TRANSIÇÕES (T1..T8) ----------
def test_T1():
    m = em_ociosa()
    m.inserir_moeda(100)
    assert (m.estado, m.credito) == (Estado.COM_CREDITO, 100)


def test_T2():
    m = em_com_credito(100)
    m.inserir_moeda(50)
    assert (m.estado, m.credito) == (Estado.COM_CREDITO, 150)


def test_T3():
    m = em_com_credito(300)
    m.selecionar()
    assert m.estado == Estado.DISPENSANDO


def test_T4():
    m = em_com_credito(100)
    m.selecionar()
    assert m.estado == Estado.COM_CREDITO


def test_T5():
    m = em_com_credito(100)
    m.cancelar()
    assert (m.estado, m.credito, m.devolvido) == (Estado.OCIOSA, 0, 100)


def test_T6():
    m = em_dispensando()
    m.dispensa_ok()
    assert (m.estado, m.credito, m.devolvido) == (Estado.OCIOSA, 0, 200)


def test_T7():
    m = em_dispensando()
    m.falha_mecanica()
    assert (m.estado, m.devolvido) == (Estado.FORA_DE_SERVICO, 500)


def test_T8():
    m = em_fora_de_servico()
    m.reparar()
    assert m.estado == Estado.OCIOSA


# Transições inválidas (evento não previsto no estado)
@pytest.mark.parametrize("fabrica, evento, args", [
    (em_ociosa, "selecionar", ()),
    (em_ociosa, "cancelar", ()),
    (em_com_credito, "dispensa_ok", ()),
    (em_dispensando, "inserir_moeda", (100,)),
    (em_fora_de_servico, "inserir_moeda", (100,)),
    (em_fora_de_servico, "selecionar", ()),
])
def test_transicoes_invalidas(fabrica, evento, args):
    with pytest.raises(TransicaoInvalida):
        getattr(fabrica(), evento)(*args)


# ---------- 3.3 Testes de CAMINHOS (C1..C5) ----------
def test_C1_insere_e_cancela():
    m = MaquinaVenda()
    m.inserir_moeda(100)
    m.cancelar()
    assert m.estado == Estado.OCIOSA and m.devolvido == 100


def test_C2_compra_com_sucesso():
    m = MaquinaVenda()
    m.inserir_moeda(500)
    m.selecionar()
    m.dispensa_ok()
    assert m.estado == Estado.OCIOSA and m.devolvido == 200


def test_C3_duas_moedas_e_cancela():
    m = MaquinaVenda()
    m.inserir_moeda(100)
    m.inserir_moeda(100)
    m.cancelar()
    assert m.estado == Estado.OCIOSA and m.devolvido == 200


def test_C4_credito_insuficiente_e_cancela():
    m = MaquinaVenda()
    m.inserir_moeda(100)
    m.selecionar()
    m.cancelar()
    assert m.estado == Estado.OCIOSA and m.devolvido == 100


def test_C5_falha_e_reparo():
    m = MaquinaVenda()
    m.inserir_moeda(300)
    m.selecionar()
    m.falha_mecanica()
    m.reparar()
    assert m.estado == Estado.OCIOSA and m.devolvido == 300
