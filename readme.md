# Forest Fire Model

## Resumo

O [Forest Fire Model](http://en.wikipedia.org/wiki/Forest-fire_model) é uma simulação simples de autômato celular de um incêndio se espalhando por uma floresta. A floresta é uma grade de células, cada uma das quais pode estar vazia ou conter uma árvore. As árvores podem estar não queimadas, em chamas ou queimadas. O fogo se espalha de cada árvore em chamas para os vizinhos não queimados; a árvore em chamas então fica queimada. Isso continua até que o fogo se extingue.

## Como Executar o Programa 

Para executar o modelo interativamente, execute ``mesa runserver`` no diretório do próprio

```
    $ mesa runserver
```

Em seguida, abra seu navegador para [http://127.0.0.1:8521/](http://127.0.0.1:8521/) e pressione Reset, em seguida, Run.

Para visualizar e executar as análises de modelo, use o Notebook ``Forest Fire Model``.

## Arquivos

### ``forest_fire/model.py``

Isso define o modelo. Existe uma classe de agente, **TreeCell**. Cada objeto TreeCell que possui coordenadas (x, y) na grade e sua condição é *Fine* por padrão. A cada passo, se a condição da árvore for *On Fire*, ela espalha o fogo para qualquer árvore *Fine* em seu [Von Neumann neighborhood](http://en.wikipedia.org/wiki/Von_Neumann_neighborhood) antes de mudar sua própria condição para *Burned Out*.

A classe **ForestFire** é o contêiner do modelo. Ele é instanciado com parâmetros de largura e altura que definem o tamanho da grade e densidade, que é a probabilidade de qualquer célula ter uma árvore nela. Quando um novo modelo é instanciado, as células são preenchidas aleatoriamente com árvores com probabilidade igual à densidade. Todas as árvores na coluna da esquerda (x=0) estão configuradas para *On Fire*.

A cada passo do modelo, as árvores são ativadas em ordem aleatória, espalhando o fogo e queimando. Isso continua até que não haja mais árvores pegando fogo - o fogo se extinguiu completamente.

### ``forest_fire/server.py``

Esse código define e inicia a visualização no navegador para o modelo ForestFire. Ele inclui o método **forest_fire_draw**, que recebe um objeto TreeCell como argumento e o transforma em uma representação a ser desenhada no navegador. Cada árvore é desenhada como um retângulo preenchendo toda a célula, com uma cor baseada em sua condição. As árvores *Fine* são verdes, as árvores *On Fire* vermelhas e as árvores *Burned Out* são pretas.

### VARIAÇÕES ADICIONADAS AO MODELO

A fim de apresentar uma variação coerente às narrativas e comportamento do modelo, foi adicionada uma variável na qual alterou tal comportamento segundo as pesquisas relacionádas às plantas pirófitas. Essas plantas são altamente resistentes ao fogo e às chamas causadas pelos incêndios pelo fato de possuírem folhas extrmamentes húmidas. Para exemplificar tal evidência, propus colocar uma variável de humidade (humidity) na qual, caso a humidade das folhas das árvores seja maior que 50%, a árvore é avaliada como pirófifita e então não entrará em chamas. Com isso, percebe-se uma diferença na aglomeração das chamas e número de árvores queimadas. A variável capaz de ser alterada pelo usuário é a humidade e conforme ela é alterada, os gráficos e árvores queimadas diminuem, conforme a lógica proposta pelos estudos das plantas pirófitas.