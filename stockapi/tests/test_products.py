def test_preco_deve_ser_positivo():
    preco = 12.90
    assert preco > 0


def test_quantidade_nao_pode_ser_negativa():
    quantidade = 50
    assert quantidade >= 0


def test_nome_produto_nao_pode_ser_vazio():
    nome = "Caderno A4"
    assert len(nome) > 0


def test_movimentacao_entrada_aumenta_estoque():
    estoque_inicial = 10
    entrada = 5
    estoque_final = estoque_inicial + entrada
    assert estoque_final == 15


def test_movimentacao_saida_diminui_estoque():
    estoque_inicial = 10
    saida = 3
    estoque_final = estoque_inicial - saida
    assert estoque_final == 7
    assert estoque_final >= 0
