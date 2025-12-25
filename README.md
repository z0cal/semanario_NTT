
# semanario_NTT
arquivos usados no seminario NTT

veja o repositorio
 https://github.com/SheafificationOfG/Fibsonisheaf
=======
## Inicialização para o Fibsonicsheaf

Após clonar o repositório, certifique-se de executar:

```bash
make init
```

para inicializar as pastas de saída. Este passo é **necessário** antes de tentar compilar qualquer outra coisa.

---

## Computando um número de Fibonacci

Para calcular um número específico de Fibonacci (usando uma das implementações suportadas), use:

```bash
# Gerar o binário
make bin/$(algo).hex.out

# Uso:
./bin/$(algo).hex.out $(fibonacci_index) $(output_file)
# Se output_file não for fornecido, a saída vai para stdout
```

Por preguiça, não foi implementada nenhuma conversão “inteligente” de hexadecimal para decimal.
Se você não curte hex, pode converter a saída hexadecimal com `scripts/hex2dec.py`:

```bash
./bin/$(algo).hex.out $(fibonacci_index) | python3 scripts/hex2dec.py $(output_file)
# Se output_file não for fornecido, a saída vai para stdout
```

Por padrão, o `hex2dec` imprime no máximo **32 dígitos significativos**. Para imprimir **todos os dígitos**, passe `-n0` ou `--ndigits=0` como argumento.

---

## Configurando builds

Os algoritmos atuais possuem valores padrão que fazem mais sentido no meu hardware, mas você pode sobrescrever algumas configurações via `make`.

```bash
# CC: compilador C
# PY: interpretador Python
# DEFINES: definições de macros em C
#   (ex.: DIGIT_BIT: número de bits em um único "dígito"
#    da representação de inteiros grandes)
# FLAGS: flags do compilador C
# AUTOHEADER_FLAGS: flags passadas para o gerador automático de headers
make CC=gcc-14 PY=python3.14 DEFINES="DEBUG DIGIT_BIT=$(bits)" FLAGS="-g" AUTOHEADER_FLAGS="--verbose" bin/$(whatever).out
```

Existem, claro, outras flags.

---

## Plotando desempenho


Para gerar dados para plotagem, rode:

```bash
# Para gerar dados de um algoritmo específico
make data/$(algo).dat

# Ou, para gerar todos os dados
make all-data
```

Para plotar os dados, é necessário um arquivo JSON de configuração no seguinte formato:

```json
{
  "Nome do algoritmo (para a legenda)": {
    "path": "data/$(algo).dat",
    "colour": "$(alguma_cor_do_matplotlib)"
  }
}
```

**Nota:** os caminhos para os arquivos `*.dat` são relativos ao JSON de configuração que você definir.

**Dica:** você também pode plotar usando arquivos de dados gerados pelo projeto original (*OG Fibsonicci*). O script de animação consegue interpretar ambos os formatos.

Depois, você deve conseguir rodar:

```bash
python3 scripts/anim.py $(config).json
```

Se você fornecer `--output=foobar`, a animação do gráfico será salva em `foobar.mp4` e o gráfico final em `foobar.png`.

> **Importante**
> O script `anim.py` requer `matplotlib` e `ffmpeg` (para salvar `.mp4`).

---

## Problemas conhecidos

* O compilador padrão é o `clang-18`, porque eu gosto do gosto de ferro (e por outros motivos), mas isso pode não funcionar em **ARM64**; veja a issue #1. De qualquer forma, o build deve funcionar bem com `gcc`.

## Animation plot

para plotar a animação é necessário algumas bibliotecas
```bash
sudo pacman -S ffmpeg freeglut pkgconf pango scipy python-pip
```
Além do latex.
o comando para executar a animação em alta qualidade é 
```bash
manim -pqh convolution.py  CirculoCrescente
```

