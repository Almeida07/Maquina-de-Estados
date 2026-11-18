# Máquina de Venda Automática (FSM)

Trabalho prático de Sistemas Computacionais: máquina de estados com testes automatizados
de estados, transições e caminhos independentes.

## Executar

    pip install -r requirements.txt
    pytest -v --cov=vending --cov-branch --cov-report=term-missing

## Arquivos

- `vending.py`: implementação da máquina de estados
- `test_vending.py`: 23 testes (estados, transições, transições inválidas, caminhos)
- `docs/diagrama.png` e `docs/diagrama.dot`: diagrama de estados (o .dot gera o .png com Graphviz)
- `.github/workflows/tests.yml`: executa os testes a cada push no GitHub

## Publicar no GitHub

    git init
    git add .
    git commit -m "Máquina de estados e testes"
    git branch -M main
    git remote add origin https://github.com/<usuario>/vending-fsm.git
    git push -u origin main
