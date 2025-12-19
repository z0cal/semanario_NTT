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