# semanario NTT 

### 1. A Dualidade entre Tempo e Frequência
A Transformada de Fourier é uma operação matemática que mapeia uma função do domínio do tempo (ou espaço) para o seu domínio dual: a frequência. Essa transição é extremamente útil, pois propriedades que são complexas de analisar no tempo tornam-se claras no espectro de frequências.

Além da análise, essa mudança de espaço possibilita a simplificação de operações fundamentais.
### 2. Aplicabilidade e Importância
Esta ferramenta é um pilar fundamental em diversas áreas do conhecimento:

* **Matemática Pura:** Essencial na Teoria Analítica dos Números e no estudo de Equações Diferenciais Parciais (EDPs).
* **Física Moderna:** É a base matemática do **Princípio da Incerteza de Heisenberg** na Mecânica Quântica, onde a posição e o momento de uma partícula formam um par de variáveis conjugadas de Fourier.
* **Engenharia:** Processamento de sinais, compressão de dados (MP3, JPEG) e telecomunicações.

---
### 3. Transformada de Fourier Contínua (CTFT)
Para uma função contínua $f(t)$, a transformada é definida pela integral:

$$F(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} \, dt$$

Apesar de sua elegância teórica, a CTFT apresenta desafios para a aplicação prática em sistemas digitais:

1.  **Natureza Analítica:** A resolução de integrais impróprias exige uma manipulação simbólica que é difícil de automatizar em computadores comuns.
2.  **Limite Infinito:** A definição pressupõe que conhecemos o sinal de $-\infty$ a $+\infty$, o que é impossível em cenários reais.
3.  **Amostragem Finita:** Na prática, os sinais são capturados de forma discreta (amostras) e por um tempo limitado, o que torna a integral contínua inaplicável.

---
### 4. Transformada Discreta de Fourier (DFT)
Para viabilizar o processamento em computadores, utilizamos a **DFT**. Ela opera sobre uma sequência finita de $N$ amostras, mapeando dados discretos no tempo para dados discretos na frequência:

$$X[k] = \sum_{n=0}^{N-1} x[n] e^{-i \frac{2\pi}{N} kn}$$

Para $k = 0, 1, \dots, N-1$.



Diferente da versão contínua, a DFT lida com somatórios e vetores numéricos, permitindo que a teoria de Fourier seja aplicada em qualquer dispositivo digital.
Eh possivel provar que a DFT eh um transformacao linear, logo, pode ser representada matricialmente.


$\omega = \frac{2\pi n}{NT} n =0:N-1$

$$
\begin{bmatrix} X[0] \\ X[1] \\ \vdots \\ X[N-1] \end{bmatrix}
=
\begin{bmatrix}
e^{-i\frac{2\pi}{N}(0\cdot 0)} & e^{-i\frac{2\pi}{N}(0\cdot 1)} & \dots & e^{-i\frac{2\pi}{N}(0\cdot (N-1))} \\
e^{-i\frac{2\pi}{N}(1\cdot 0)} & e^{-i\frac{2\pi}{N}(1\cdot 1)} & \dots & e^{-i\frac{2\pi}{N}(1\cdot (N-1))} \\
\vdots & \vdots & \ddots & \vdots \\
e^{-i\frac{2\pi}{N}((N-1)\cdot 0)} & e^{-i\frac{2\pi}{N}((N-1)\cdot 1)} & \dots & e^{-i\frac{2\pi}{N}((N-1)\cdot (N-1))}
\end{bmatrix}
\begin{bmatrix} x[0] \\ x[1] \\ \vdots \\ x[N-1] \end{bmatrix}
$$
(note que essa matriz eh uma matriz de vandermonde)
### 4. A Multiplicação de Polinômios e a Complexidade Computacional

Um problema simplificado pela mudanca de domino eh a multiplicacao de polinomios. Tome os polinomios $f(x)$ e $g(x)$ de grau $n-1$:

$$f(x) = \sum_{i=0}^{n-1} a_i x^i, \quad g(x) = \sum_{j=0}^{n-1} b_j x^j$$

Na abordagem clássica , o produto $h(x) = f(x) \cdot g(x)$ é obtido distribuindo-se cada termo de $f$ sobre todos os termos de $g$. Este processo resulta em um novo polinômio de grau $2n-2$:

$$h(x) = \sum_{k=0}^{2n-2} c_k x^k$$
onde $c_k = \sum_{i+j=k} a_i b_j$.

Nesta metodologia, o cálculo de cada coeficiente $c_k$ exige múltiplas operações de produto e soma, resultando em uma complexidade assintótica $O(n^2)$. Para polinômios com grandes volumes de coeficientes, este custo computacional torna o metodo inviavel.

---
### 5. O Teorema da Convolução

A conexão entre a álgebra polinomial e a análise de Fourier reside na observação de que os coeficientes $c_k$ do produto $h(x)$ são, por definição, o resultado da **convolução linear** entre os vetores de coeficientes de $f$ e $g$:

$$c_k = \sum_{i+j=k} a_i b_j$$

> **Teorema da Convolução** : a transformada de uma convolução no domínio do tempo (ou espaço) é equivalente ao produto ponto a ponto (produto de Hadamard) das respectivas transformadas no domínio da frequência:

$$\mathcal{F}(f * g) = \mathcal{F}(f) \cdot \mathcal{F}(g)$$

Logo, a distributiva complicada e custosa se transformou em uma operacao ponto a ponto, contudo, isso vem a custo do calculo da transformada, que tambem eh $O(n^2)$, por isso nao houve ganho de eficiencia algum. 

---
### 6. A Fast Fourier Transform

A FFT (Fast Fourier Transform) eh uma maneira de otimizar o calculo da DFT.

O algoritmo da FFT foi redescoberta por Cooley e Tukey em 1965, uma vez que Gauss ja tinha utilzado um algoritmo semelhante para calcular a orbitas de asteroides em 1805. 

O algoritmo se baseia em **dividir para conquistar**.

> Relembrando

os numeros complexos possuem certas propriedades ciclicas e certas simetria que permite a economia nos calculos, vejamos um exemplo.
$$\zeta_8^1 = e^{i\frac{2\pi}{8}} = e^{i45^\circ}
    \ 
$$

$$
\begin{aligned}
\zeta^2 &= i \qquad\qquad
\zeta^3 = i\cdot\zeta = \zeta^* \qquad\qquad
\zeta^4 = -1 \\[6pt]
\zeta^5 &= -\zeta \qquad\qquad
\zeta^6 = -i \qquad\qquad
\zeta^7 = -i\cdot\zeta = -\zeta^* \qquad\qquad
\zeta^8 = 1
\end{aligned}
$$
por isso percebe-se que a cada 4 "deslocamento"(DFT pode ser visto como o operdor deslocamento) o valor se torna o oposto, como ilustrado na figura:
![Raízes da Unidade](diagrama.svg)

De forma mais geral:


> $
\zeta_N = e^{\frac{2\pi i}{N}}
$,
uma raiz $N$-ésima primitiva da unidade. Então para todo inteiro $a$,
$
{\zeta_N^{a+\frac{N}{2}} = -\,\zeta_N^{a}}.
$

<details>
<summary><strong>Demonstração</strong></summary>


Como $\zeta_N = e^{\frac{2\pi i}{N}}$, temos
$$
\zeta_N^{a+\frac{N}{2}}
= e^{\frac{2\pi i}{N}\left(a+\frac{N}{2}\right)}
= e^{\frac{2\pi i a}{N}} \cdot e^{\frac{2\pi i}{N}\cdot \frac{N}{2}}
= \zeta_N^{a}\cdot e^{\pi i}.
$$
Mas $e^{\pi i} = -1$. Logo,
$$
\zeta_N^{a+\frac{N}{2}} = \zeta_N^{a}\cdot (-1) = -\zeta_N^{a}.
$$
$\square$
</details>
---
O algoritmo decompõe uma DFT de tamanho $N$ em duas sub-transformadas de tamanho $N/2$, separando os índices pares e ímpares da sequência original:

$$X[k] = \sum_{m=0}^{N/2-1} x[2m] \zeta_{N/2}^{mk} + \zeta_N^k \sum_{m=0}^{N/2-1} x[2m+1] \zeta_{N/2}^{mk}$$

Esta estrutura permite calcular dois valores de saída ($X[k]$ e $X[k+N/2]$) utilizando os mesmos resultados intermediários, através da denominada **operação borboleta** (*butterfly operation*):

1. $X[k] = E[k] + \zeta_N^k O[k]$
2. $X[k + N/2] = E[k] - \zeta_N^k O[k]$

como pode ser visto na imagem 
![Butterfly](butterfly.svg)

o a implementacao em python esta a seguir
```python
def fft(a, omega):

    n = len(a)
    if n == 1:
        return a[:]  


    a_par = fft(a[0::2], omega^2)
    a_impar  = fft(a[1::2], omega^2)

    A = [0] * n
    w = 1
    half = n // 2
    for k in range(half):
        t = w * a_impar[k]
        A[k]          = a_par[k] + t
        A[k + half]   = a_par[k] - t
        w *= omega
    return A
                     
```
---
## Problemas da FTT

Grande problema da FTT eh que ela trabalha com ponto flutuante, o que, para computadores, eh um grande problemas que pode causar erro de arredondamentos e, assim causar um falha nos esquemas criptograficos.

> Exemplo 
 
 citar o exemplo das series em ordem diferentes divergindo 

 Solucao: utilizar um transformada que utiliza apenas numeros exatos