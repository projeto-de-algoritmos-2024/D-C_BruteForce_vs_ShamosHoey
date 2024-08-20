# Closest Pair of Points: Força Bruta vs Shamos-Hoey

**Número da Lista**: 29<br>
**Conteúdo da Disciplina**: Divide and conquer<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 22/1008786 |  Mateus Villela Consorte |
| 22/1008679 |  Pablo Serra Carvalho|

# Closest Pair of Points: Força Bruta vs Shamos-Hoey

## Introdução

O problema do par de pontos mais próximos (Closest Pair of Points) é uma das questões mais fundamentais e bem estudadas em geometria computacional. Ele consiste em encontrar os dois pontos mais próximos em um conjunto de $n$ pontos em um espaço métrico, geralmente no plano cartesiano. Este problema é amplamente utilizado em diversas áreas, como processamento de imagens, análise de dados e redes de comunicação. O interesse em resolver este problema de forma eficiente surge da necessidade de otimizar o tempo de processamento, especialmente quando lidamos com grandes quantidades de dados. A solução mais simples e direta, conhecida como abordagem de força bruta, envolve calcular a distância entre todos os pares de pontos e selecionar o par com a menor distância. Embora simples de entender e implementar, essa abordagem se torna ineficiente à medida que o número de pontos aumenta, pois a complexidade de tempo dessa solução é quadrática, ou seja, $O(n^2)$ (CORMEN et al., 2009; KLEINBERG; TARDOS, 2005).

Para superar a ineficiência da abordagem de força bruta, Shamos e Hoey (1975) propuseram uma solução mais sofisticada baseada na técnica de divisão e conquista, que é uma extensão da abordagem clássica utilizada em algoritmos de ordenação como Merge Sort. O algoritmo Shamos-Hoey divide o conjunto de pontos em duas metades, resolve o problema recursivamente em cada metade, e então combina as soluções das subpartes para encontrar o par de pontos mais próximo. Este método aproveita a ordenação dos pontos e a propriedade geométrica de que o par mais próximo pode estar em diferentes metades, mas não muito distante da linha divisória. Com essa abordagem, o algoritmo alcança uma complexidade de tempo $O(n \log n)$, o que representa uma melhoria significativa em relação à força bruta, especialmente para grandes conjuntos de dados (SHAMOS; HOEY, 1975; KLEINBERG; TARDOS, 2005).

O principal objetivo deste trabalho é comparar a eficiência entre o algoritmo de força bruta e o algoritmo de Shamos-Hoey para o problema do par de pontos mais próximos. Para isso, implementaremos ambos os algoritmos, analisaremos suas complexidades teóricas e realizaremos experimentos computacionais para avaliar o desempenho prático de cada abordagem. A motivação para este estudo está no fato de que, embora a força bruta seja suficiente para pequenos conjuntos de dados, a solução de Shamos-Hoey oferece um desempenho muito melhor em aplicações práticas onde a eficiência computacional é crucial, como em sistemas de navegação e controle de tráfego (BENTLEY; FRIEDMAN, 1979; KLEINBERG; TARDOS, 2005).

## Força Bruta

### Premissa:
O algoritmo de força bruta para encontrar o par de pontos mais próximo é a solução mais intuitiva para o problema. A ideia principal é calcular a distância entre todos os pares de pontos possíveis e, em seguida, selecionar o par com a menor distância. Este método, apesar de ser simples de entender e implementar, é computacionalmente custoso, pois requer a verificação de cada possível par de pontos. O algoritmo é eficaz em pequenos conjuntos de dados, mas seu desempenho se deteriora rapidamente à medida que o número de pontos aumenta, devido à sua complexidade de tempo quadrática, ou seja, $O(n^2)$ (CORMEN et al., 2009; KLEINBERG; TARDOS, 2005).

### Pseudo-código:
```pseudo
for i from 1 to n-1
    for j from i+1 to n
        calculate distance between point i and point j
        if distance is smaller than current minimum distance
            update minimum distance and closest pair
return closest pair
```
O algoritmo itera sobre todos os pares possíveis de pontos no conjunto, calculando a distância entre cada par. Se a distância calculada for menor que a distância mínima atual, o par de pontos mais próximos é atualizado. Ao final, o par de pontos com a menor distância é retornado como a solução.

### Análise assintótica:
A complexidade temporal do algoritmo de força bruta é $O(n^2)$, onde $n$ é o número de pontos. Esta complexidade resulta do fato de que para cada ponto, o algoritmo verifica a distância em relação a todos os outros pontos, o que implica em aproximadamente $\frac{n(n-1)}{2}$ comparações. Como essa abordagem envolve uma análise exaustiva de todos os pares, o desempenho do algoritmo é limitado pela quantidade de pontos, tornando-se ineficiente para grandes conjuntos de dados (CORMEN et al., 2009; KLEINBERG; TARDOS, 2005).

## Shamos-Hoey

### Premissa

O algoritmo de Shamos-Hoey resolve o problema do par de pontos mais próximos em $O(n \log n)$ usando a técnica de divisão e conquista. Este método divide o conjunto de $n$ pontos em duas metades ao longo da mediana da coordenada $x$, resolve recursivamente o problema em cada metade, e depois combina as soluções parciais para encontrar o par de pontos mais próximo, levando em conta pares de pontos que podem estar em diferentes metades, mas próximos o suficiente para serem candidatos à solução global.

### Pseudo-código

O pseudo-código abaixo é baseado no fornecido por Kleinberg e Tardos (2005):

```pseudo
Closest-Pair(P):
    Sort points in P by x-coordinate
    return Closest-Pair-Rec(P)

Closest-Pair-Rec(P):
    if |P| <= 3:
        return brute-force(P)
    mid = floor(|P| / 2)
    Pl = P[1...mid]
    Pr = P[mid+1...|P|]
    d1 = Closest-Pair-Rec(Pl)
    d2 = Closest-Pair-Rec(Pr)
    d = min(d1, d2)
    let L be the vertical line passing through the point P[mid]
    let S = [p in P such that |p.x - L.x| < d]
    sort S by y-coordinate
    dmin = d
    for i = 1 to |S| - 1:
        for j = i + 1 to min(i + 7, |S|):
            dist = distance(S[i], S[j])
            if dist < dmin:
                dmin = dist
    return dmin
```

### Análise Assintótica

O algoritmo Shamos-Hoey opera com complexidade $O(n \log n)$. A ordenação inicial dos pontos por suas coordenadas $x$ requer $O(n \log n)$ tempo. A cada nível da recursão, o conjunto de pontos é dividido em duas metades, cada uma com $\frac{n}{2}$ pontos, e a solução do problema é combinada em $O(n)$ operações. Como a profundidade da recursão é $O(\log n)$, a complexidade total do algoritmo é $O(n \log n)$. Este ganho em eficiência é alcançado pelo fato de que o número de comparações entre pontos é significativamente reduzido ao usar a estrutura geométrica do problema.

### Prova de Corretude

#### Estrutura Geral

A prova de corretude do algoritmo Shamos-Hoey baseia-se na análise de como o algoritmo trata a divisão do problema e a combinação das soluções parciais. O ponto central é mostrar que ao considerar pares de pontos em regiões diferentes (ou seja, um ponto em $P_l$ e outro em $P_r$), o algoritmo não perde nenhuma solução potencialmente ótima.

#### Divisão e Conquista

1. **Divisão**: O algoritmo divide o conjunto de pontos $P$ em duas metades $P_l$ e $P_r$, com base na mediana da coordenada $x$. Cada subconjunto contém aproximadamente $n/2$ pontos. A corretude da etapa de divisão é garantida pela escolha da mediana, que assegura uma divisão balanceada.

2. **Solução Recursiva**: Suponha que o algoritmo funcione corretamente em subconjuntos menores. Então, ao encontrar os pares de pontos mais próximos em $P_l$ e $P_r$, temos garantido que os menores pares em cada subconjunto são, de fato, os mais próximos dentro de cada metade. Denotemos as distâncias mínimas encontradas por $d_1$ e $d_2$, respectivamente.

3. **Combinação**: A parte crítica da prova é demonstrar que, ao combinar as soluções, o algoritmo considera todos os pares de pontos que podem cruzar a linha divisória com uma distância menor que $d = \min(d_1, d_2)$. A chave está na observação de que, se dois pontos em $P'$ (a região de $P$ próxima à linha divisória) estão a uma distância menor que $d$, então eles devem estar dentro de uma faixa estreita, onde $|p_y - q_y| < d$.

#### Análise da Faixa (Strip)

O número de comparações necessárias na faixa $P'$ é reduzido ao ordenar $P'$ pela coordenada $y$. A prova detalha que cada ponto $p$ só precisa ser comparado com no máximo 7 outros pontos (usando a propriedade geométrica de que, dentro de uma faixa de largura $d$, os pontos vizinhos em $y$ podem ser no máximo 7), mantendo o número total de comparações dentro de $O(n)$.


#### Conclusão da Prova

Portanto, o algoritmo garante que o par de pontos mais próximo será encontrado, seja dentro de $P_l$, $P_r$, ou através da combinação de pontos em $P'$. Como o número total de operações no pior caso é $O(n \cdot \log n)$, o algoritmo é não só correto como também eficiente (KLEINBERG; TARDOS, 2005).

## Discussões e Conclusão

O estudo comparativo entre os algoritmos de força bruta e Shamos-Hoey para o problema do par de pontos mais próximos evidencia as vantagens e desvantagens de cada abordagem. O algoritmo de força bruta, embora simples de implementar, é limitado pela sua complexidade quadrática, tornando-se impraticável para grandes conjuntos de dados. Por outro lado, o algoritmo de Shamos-Hoey, apesar de ser mais complexo em termos de implementação, oferece uma solução muito mais eficiente, com uma complexidade de $O(n \log n)$, tornando-o adequado para aplicações que envolvem grandes volumes de dados. Em suma, enquanto a força bruta pode ser útil para pequenos conjuntos de dados ou para fins didáticos, o algoritmo de Shamos-Hoey é a escolha preferida em contextos onde a eficiência computacional é crítica (CORMEN et al., 2009; SHAMOS; HOEY, 1975; PREPARATA; SHAMOS, 1985; KLEINBERG; TARDOS, 2005).

## Referências

- CORMEN, T. H.; LEISERSON, C. E.; RIVEST, R. L.; STEIN, C. *Introduction to Algorithms*. 3rd ed. MIT Press, 2009.
- SHAMOS, M. I.; HOEY, D. *Closest-point problems*. Proceedings of the 16th Annual Symposium on Foundations of Computer Science, 1975.
- PREPARATA, F. P.; SHAMOS, M. I. *Computational Geometry: An Introduction*. Springer-Verlag, 1985.
- BENTLEY, J. L.; FRIEDMAN, J. H. *Data structures for range searching*. ACM Computing Surveys, 1979.
- KLEINBERG, J.; TARDOS, É. *Algorithm Design*. Pearson/Addison-Wesley, 2005.


## Screenshots
Adicione 3 ou mais screenshots do projeto em funcionamento.
<br>
**ESSE É O DIVIDIR E CONQUISTAR COM 30 PONTOS - FPS**
![Captura de tela 2024-08-19 233700](https://github.com/user-attachments/assets/9de56b2e-7545-4e4c-9d9e-ba23bf7852cb)
<br>
**ESSE É O FORÇA BRUTA COM 30 PONTOS**
![Captura de tela 2024-08-19 233738](https://github.com/user-attachments/assets/ff5763a5-d5f0-4816-ba4b-9fa9585aa3ea)
<br>
**ESSE É O DIVIDIR E CONQUISTAR COM 400 PONTOS FPS - 59.88**
![Captura de tela 2024-08-19 231132](https://github.com/user-attachments/assets/95fe7aeb-7382-4386-967b-16e64500bfad)
<br>
**ESSE É O FORÇA BRUTA COM 400 PONTOS - FPS 2.41** 
![Captura de tela 2024-08-19 231159](https://github.com/user-attachments/assets/53708a3d-f9cb-4172-be0d-203a1fe6356b)

## Instalação 
**Linguagem**: Python<br>

## Uso 
O software mostra visualmente a diferença entre o algoritimo por força bruta e o algoritimo ótimo por divisão e conquista, basta apertar a tecla ``` SPACE ``` para alternar entre elas.
Além disso, na parte superior, é possível visualizar a quantidade de pontos utilizadas e o FPS, o qual está associado diretamente a eficiência do algoritimo.

[Link para o vídeo de apresentação do projeto](https://youtu.be/FyiUfEFkPuY).



