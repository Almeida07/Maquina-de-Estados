# Máquina de Venda Automática (FSM)

Trabalho prático de Sistemas Computacionais: máquina de estados com testes automatizados
de estados, transições e caminhos independentes.

## Executar

    pip install -r requirements.txt
    pytest -v --cov=vending --cov-branch --cov-report=term-missing

## Arquivos

- `vending.py`: implementação da máquina de estados
- `test_vending.py`: 23 testes (estados, transições, transições inválidas, caminhos)
- `diagrama.png` e `diagrama.dot`: diagrama de estados (o .dot gera o .png com Graphviz)
- `tests.yml`: executa os testes a cada push no GitHub

