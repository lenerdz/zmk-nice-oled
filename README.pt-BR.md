# nice!oled - nice!epaper - nice!custom

[English](./README.md) | **Português (Brasil)**

> Tradução para o português (Brasil) do [README.md](./README.md) deste fork. Em
> caso de divergência, vale o original em inglês.

![nice_oled_demo](./assets/nice_oled_demo.GIF)
![nice_epaper_demo](./assets/nice_epaper_demo.GIF)
![nice_epaper_demo](./assets/nice_custom_demo.GIF)

## Sumário

<a name="top"></a>

- [Visão geral](#visão-geral)
- [Galeria](#galeria)
- [Instalação rápida](#instalação-rápida)
- [Configuração](#configuração)
- [Implementação do ZMK RAW HID](#implementação-do-zmk-raw-hid)
- [Sugestões](#sugestões)
- [Limitações](#limitações)
- [Agradecimentos e créditos](#agradecimentos)
- [Apoio](#se-você-gosta-das-minhas-contribuições-não-se-esqueça-do-seguinte)
- [Meus outros projetos](#meus-outros-projetos)

# Visão geral
> [!WARNING]
> TESTADO USANDO ZMK main (Zephyr 4.1 + LVGL 9), consulte [Pin your ZMK version](https://zmk.dev/blog/2025/06/20/pinned-zmk)

Widgets verticais para telas [oled] e [niceview] usando zmk (para teclados split e não split)


## Resumo da arquitetura do sistema e da implementação

## Estratégia de design modular e submodular
Este módulo do ZMK implementa uma arquitetura altamente desacoplada, projetada para máxima flexibilidade e extensibilidade.

*   **Widgets modulares**: A camada de visualização é totalmente modular, permitindo a seleção e a composição, em tempo de execução, de qualquer widget disponível, sem acoplamento forte com a lógica central do display.
*   **RAW HID submodular**: A implementação do RAW HID é granular. Submódulos como Temperatura, Hora, Layout e Volume podem ser compilados e ativados de forma independente via Kconfig, minimizando o uso de flash e a sobrecarga de processamento ao excluir a lógica não utilizada.

## Camada de abstração: shield `nice_custom`
Uma camada de abstração de hardware dedicada, o shield `nice_custom`, foi desenvolvida para desacoplar o posicionamento dos drivers das definições de hardware físico.
*   **Sistema de coordenadas de driver independente**: Todas as coordenadas X/Y de renderização são configuráveis pelo sistema de configuração (runtime/Kconfig), de forma totalmente independente da definição do shield subjacente.
*   **Personalização sem código**: Os usuários podem reposicionar drivers e elementos para se adequar a layouts fora do padrão ou a preferências pessoais apenas por meio de variáveis de configuração, eliminando a necessidade de fazer fork ou modificar o código-fonte C do driver do display.

## Integração no lado do host (Rust)

O aplicativo host complementar, `zmk-hid-host`, fornece a ponte de dados necessária para os recursos universais de Raw HID (hora do sistema, volume, layout) em Linux, Windows e macOS.

*   **Contribuições técnicas (melhorias para macOS)**:
    *   **Suporte a temperatura no macOS**: Implementado monitoramento de temperatura específico da plataforma para macOS dentro da base de código Rust.
    *   **Integração com o Spotify**: Desenvolvida uma ponte nativa AppleScript/Rust para obter, em tempo real, os metadados da faixa do Spotify e exibi-los no periférico (somente macOS).
    *   **Suporte a múltiplas arquiteturas**: Desenvolvido um wrapper universal de aplicativo para macOS, empacotando binários nativos para as arquiteturas Intel (`x86_64`) e Apple Silicon (`arm64`), garantindo uma implantação transparente em todo o ecossistema Apple.

## Shields suportados:

- `nice_oled`
- `nice_epaper`
- `nice_custom`

## Características gerais:

### Geral
- **Layout vertical**: Otimizado para telas OLED/e-Ink/ePaper de teclados split.
- **Design compacto**: Maximiza a densidade de informação.
- **Widgets modulares**: Habilite/desabilite componentes de forma independente.
- **Shield `nice_custom`**: Posicione drivers via configuração, sem necessidade de código.
- **Redução da tensão no pescoço**: Veja as informações no teclado em vez de no monitor.
- **Compatível com modo escuro**: Otimizado para o nice!oled.
- **Layout em tempo de execução (opcional)**: com o módulo [lenerdz/zmk-rgb-matrix](https://github.com/lenerdz/zmk-rgb-matrix), o ZMK Studio escolhe quais widgets são desenhados, onde, qual animação o periférico toca, e como essa imagem é girada, recortada em um pedaço e misturada com os widgets que ficam sobre ela; veja [Layout das telas OLED em tempo de execução](#layout-das-telas-oled-em-tempo-de-execução-central-e-periférico).
- **Anti burn-in (opcional)**: com o mesmo módulo, as duas telas movem tudo o que mostram um pixel de cada vez por um caminho curto (o deslocamento de pixels), e o módulo pode escurecer e apagar as telas quando ninguém digita; veja [Anti burn-in: deslocamento de pixels](#anti-burn-in-deslocamento-de-pixels-central-e-periférico).

### Tela central
- **Widgets de WPM**: Gráficos, velocímetro, Luna, Bongo Cat.
- **Indicadores HID**: Status do CapsLock com animações da Luna/Bongo Cat.
- **Widget de modificadores**: Exibição em tempo real de Ctrl, Shift, Alt, Gui.
- **Integração com Raw HID**:
    - **Spotify (macOS)**: Informações da faixa em tempo real.
    - **Clima**: Exibição da temperatura atual.
    - **Sincronização com o sistema**: Volume, hora e layout do teclado.

### Tela periférica
- **Animações verticais**: Gem, Cat, Head, Pokemon, Spaceman.
- **Bateria inteligente**: Animação eficiente do status da bateria.
- **Sleep Art**: Imagens personalizadas durante o idle/sleep (ocioso/repouso).
- **Imagens estáticas**: Vim, logotipos personalizados (modo de baixo consumo).
- **Mais imagens (opcional, com o layout em tempo de execução)**: 31 animações a mais e 6 imagens estáticas a mais, desenhadas por `scripts/pictures/`, que o ZMK Studio pode escolher, girar, recortar em um pedaço e misturar com os widgets; veja [Novas imagens da tela direita](#novas-imagens-da-tela-direita).

# Galeria

### [Clique aqui para ver mais fotos ou vá para a seção de fotos da galeria](./fotos)

<div align="center">

  <img align="center" alt="demo3" width="400px" src="./assets/demo3.jpg" />
  <img align="center" alt="demo2" width="400px" src="./assets/demo2.jpg" />
  <img align="center" alt="demo1" width="400px" src="./assets/demo1.jpg" />
  <img align="center" alt="demo4" width="400px" src="./assets/demo4.jpg" />
  <img align="center" alt="Animation Preview" width="400px" src="./assets/animation.gif" />
  <img align="center" alt="preview1" width="400px" src="./assets/preview1.JPG" />

</div>

# Instalação rápida
> [!WARNING]
>
> TESTADO USANDO ZMK main (Zephyr 4.1 + LVGL 9), consulte [Pin your ZMK version](https://zmk.dev/blog/2025/06/20/pinned-zmk)

> [!TIP]
>
> Todos os widgets estão habilitados `hid`,` modifiers`, `wpm` etc.; se você
> quiser desabilitá-los, veja a seção de configuração

Instalação em 4 passos simples:

0. Exemplo de configuração? Você deve ver isto `->` [zmk-config]

1. Certifique-se de habilitar a tela de status personalizada no seu arquivo `*.conf`:

```conf
CONFIG_ZMK_DISPLAY=y
CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y
```

2. Copie e cole isto no seu arquivo `config/west.yml`:

```yaml
manifest:
  remotes:
    - name: zmkfirmware
      url-base: https://github.com/zmkfirmware
    # suporte a nice_oled e nice_epaper
    - name: mctechnology17
      url-base: https://github.com/mctechnology17
  projects:
    - name: zmk
      remote: zmkfirmware
      revision: main
      import: app/west.yml
    # suporte a nice_oled e nice_epaper
    - name: zmk-nice-oled
      remote: mctechnology17
      revision: main
  self:
    path: config
```

3. No arquivo `build.yaml`, adicione o shield `nice_oled` (usando o corne como
   exemplo, mas pode ser outro shield).

Para tela [oled]:
```yaml
---
include:
  - board: nice_nano_v2
    shield: corne_left nice_oled
  - board: nice_nano_v2
    shield: corne_right nice_oled
```

Para tela [niceview]:
```yaml
---
include:
  - board: nice_nano_v2
    shield: corne_left nice_view_adapter nice_epaper
  - board: nice_nano_v2
    shield: corne_right nice_view_adapter nice_epaper
```

4. Compile o firmware, grave-o no seu teclado e aproveite!

# Configuração
> [!IMPORTANT]
> Certifique-se de habilitar a tela de status personalizada na sua configuração do ZMK:

Certifique-se de habilitar a tela de status personalizada na sua configuração do ZMK:

```conf
CONFIG_ZMK_DISPLAY=y
CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y
```

Anatomia das variáveis deste repositório

Este documento lista as opções de configuração disponíveis para o shield `nice_oled`. Essas variáveis podem ser definidas no seu arquivo `.conf` para personalizar o comportamento dos widgets do display.

## Configuração geral

| Variável | Tipo | Padrão | Descrição |
|----------|------|--------|-----------|
| `CONFIG_NICE_OLED_ON` | bool | `y` | Habilita a compatibilidade com o widget nice oled |
| `CONFIG_NICE_EPAPER_ON` | bool | `n` | Habilita a compatibilidade com o widget nice view |
| `CONFIG_LV_Z_VDB_SIZE` | int | `64` (OLED), `100` (ePaper) | Tamanho do buffer do LVGL |
| `CONFIG_LV_DPI_DEF` | int | `148` (OLED), `161` (ePaper) | Configuração de pontos por polegada (DPI) |
| `CONFIG_LV_Z_BITS_PER_PIXEL` | int | `1` | Bits por pixel |
| `CONFIG_LV_COLOR_DEPTH` | choice | `LV_COLOR_DEPTH_1` | Profundidade de cor |
| `CONFIG_ZMK_DISPLAY_WORK_QUEUE` | choice | `ZMK_DISPLAY_WORK_QUEUE_DEDICATED` | Tipo de work queue |
| `CONFIG_ZMK_DISPLAY_STATUS_SCREEN` | choice | `ZMK_DISPLAY_STATUS_SCREEN_CUSTOM` | Tipo de tela de status |
| `CONFIG_ZMK_DISPLAY_BLANK_ON_IDLE` | bool | `n` (OLED), `y` (ePaper) | Controla o apagamento do display quando ocioso (idle) para nice_custom/nice_epaper |
| `CONFIG_LV_Z_MEM_POOL_SIZE` | int | `8192` | Tamanho do pool de memória |
| `CONFIG_ZMK_DISPLAY_DEDICATED_THREAD_STACK_SIZE` | int | `2560` (`3072` com RAW HID) | Tamanho da pilha da thread do display |
| `CONFIG_ZMK_DISPLAY_DEDICATED_THREAD_PRIORITY` | int | `5` | Prioridade da thread do display (menor = maior prioridade) |
| `CONFIG_NICE_OLED_WIDGET_STATUS` | bool | - | Widget de status personalizado do nice oled (seleciona recursos do LVGL) |
| `CONFIG_NICE_OLED_WIDGET_INVERTED` | bool | `n` | Inverte as cores do display |
| `CONFIG_NICE_OLED_WIDGET_OUTPUT_BACKGROUND` | bool | `n` (OLED), `y` (ePaper) | Habilita o fundo da saída (output) no central e no periférico |
| `CONFIG_NICE_OLED_CUSTOM_CANVAS_WIDTH` | int | `68` (ePaper), `32` (OLED) | Largura personalizada do canvas, substituindo o cálculo padrão |
| `CONFIG_NICE_OLED_CUSTOM_CANVAS_HEIGHT` | int | `160` (ePaper), `128` (OLED) | Altura personalizada do canvas, substituindo o cálculo padrão |

## Repouso e animação (central e periférico)

| Variável | Tipo | Padrão | Descrição |
|----------|------|--------|-----------|
| `CONFIG_NICE_OLED_SHOW_SLEEP_ART_ON_IDLE` | bool | `n` | Se a arte de repouso deve ser exibida quando ocioso (idle) |
| `CONFIG_NICE_OLED_SHOW_SLEEP_ART_ON_SLEEP` | bool | `n` | Se a arte de repouso deve ser exibida ao entrar em repouso (sleep) |
| `CONFIG_NICE_OLED_SLEEP_STATUS_BOOTLOADER` | bool | `n` | Exibe brevemente a imagem do bootloader ao despertar (variante de status de repouso; substitui o widget padrão de arte de repouso) |

## Específico do periférico

| Variável | Tipo | Padrão | Descrição |
|----------|------|--------|-----------|
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_SMART_BATTERY` | bool | `n` | Habilita a animação de bateria inteligente no periférico |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_WPM` | bool | `n` | Habilita a compatibilidade com o widget de WPM no PERIFÉRICO |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL` | bool | `y` | Habilita a animação no periférico |
| `CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL` | bool | `y` (se não houver animação) | Habilita a imagem estática no periférico |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_GEM` | bool | `n` | Habilita a animação gem no periférico |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CAT` | bool | `y` | Habilita a animação cat no periférico |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_HEAD` | bool | `n` | Habilita a animação head no periférico |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_POKEMON` | bool | `n` | Habilita a animação pokemon no periférico |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_SPACEMAN` | bool | `n` | Habilita a animação spaceman no periférico |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_MS` | int | varia | Duração da animação em milissegundos |
| `CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL_VIM` | bool | `n` | Habilita o vim estático no periférico |
| `CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL_VIP_MARCOS` | bool | `n` | Habilita o vim_marcos estático no periférico |
| `CONFIG_NICE_OLED_WIDGET_PERIPHERAL` | bool | `n` | Habilita o widget de teste no periférico |
| `CONFIG_NICE_OLED_WIDGET_LED_TOAST` | bool | `n` | Mostra por um instante as mudanças nas luzes (efeito, brilho, cor) na tela do periférico; veja [Toast de RGB](#toast-de-rgb-periférico). Precisa do OLED e do módulo `zmk-behavior-rgb-matrix` de [lenerdz/zmk-rgb-matrix](https://github.com/lenerdz/zmk-rgb-matrix) (`CONFIG_KEYPAW_RGB_MATRIX_CHANGE_EVENT`) |
| `CONFIG_NICE_OLED_WIDGET_LED_TOAST_MS` | int | `1500` | Por quanto tempo o toast fica na tela, em milissegundos (200 a 10000). Não é usada quando as configurações de tela do módulo estão ligadas (`CONFIG_KEYPAW_DISPLAY_SETTINGS`): então quem define o tempo é o ZMK Studio |
| `CONFIG_NICE_OLED_WIDGET_LED_TOAST_LANGUAGE_EN` / `CONFIG_NICE_OLED_WIDGET_LED_TOAST_LANGUAGE_PT_BR` | choice | `..._EN` | Idioma dos textos do toast |

### Toast de RGB (periférico)

Com `CONFIG_NICE_OLED_WIDGET_LED_TOAST=y`, a tela do periférico mostra, por `CONFIG_NICE_OLED_WIDGET_LED_TOAST_MS` depois que um comando de luz mudou algo, o que mudou. Ele usa duas linhas da fonte de 8 pixels na faixa abaixo da animação do gato (8 caracteres por linha, apenas ASCII). Uma mudança mais nova substitui a que está na tela e reinicia o temporizador.

| O que mudou | Primeira linha | Segunda linha |
|---|---|---|
| Efeito | `EFFECT 4` (ou `FX 12` a partir do décimo) | o nome do efeito, p. ex. `RAINBOW` |
| Ligar/desligar | `LIGHTS` | `ON` ou `OFF` |
| Brilho | `BRIGHT` | `70%` |
| Matiz | `HUE` | `210 deg` |
| Saturação | `SATUR.` | `100%` |
| Período da animação | `PERIOD` | `3000 ms` |
| Reset | `LIGHTS` | `RESET` |

Os textos estão em inglês por padrão; `CONFIG_NICE_OLED_WIDGET_LED_TOAST_LANGUAGE_PT_BR=y` seleciona o português (`EFEITO`, `LUZES`, `LIGADAS`, `APAGADAS`, `BRILHO`, `MATIZ`, `SATUR.`, `CICLO`).

- O evento vem do módulo de RGB e é disparado nas **duas** metades, então uma tecla apertada em qualquer uma das metades mostra o toast na tela do periférico. Veja "Evento de mudança" no README do módulo.
- Ele não aparece na inicialização, quando a central envia seu estado ao periférico na conexão, nem para as edições dos mapas de cor do ZMK Studio.
- Com `CONFIG_KEYPAW_DISPLAY_SETTINGS=y` no módulo (as configurações de tela, veja "Configurações da tela (OLED)" no README do módulo), o toast pode ser desligado e o seu tempo mudado no ZMK Studio (as configurações "Toast" e "Duração do toast"). `CONFIG_NICE_OLED_WIDGET_LED_TOAST_MS` deixa então de ser usada: o tempo inicial é `CONFIG_KEYPAW_DISPLAY_TOAST_MS_DEFAULT` do módulo. Ainda não testado em um teclado de verdade.
- O toast existe apenas na tela do periférico: a opção depende de um build split que não seja a metade central.
- A posição padrão (`CONFIG_NICE_OLED_WIDGET_LED_TOAST_CUSTOM_X`/`_Y`, veja [Posição do widget do toast de RGB](#posição-do-widget-do-toast-de-rgb)) foi calculada para o OLED de 128x32 com a animação padrão do gato, e não foi testada em outros displays ou animações. Ainda não testado em um teclado de verdade.

## Anti burn-in: deslocamento de pixels (central e periférico)

Um OLED que mostra a mesma imagem por horas envelhece os pixels que ficam acesos mais rápido que os apagados, e estas telas desenham os mesmos widgets nos mesmos lugares o dia todo. Com `CONFIG_KEYPAW_DISPLAY_SETTINGS=y` (uma opção do módulo [lenerdz/zmk-rgb-matrix](https://github.com/lenerdz/zmk-rgb-matrix); veja "Display (OLED) settings" no README dele) as duas telas movem tudo o que mostram, um pixel de cada vez, por um caminho curto: é o **deslocamento de pixels** (`widgets/pixel_shift.c`). O ZMK Studio o edita (a aba Display do app [lenerdz/zmk-studio](https://github.com/lenerdz/zmk-studio)), cada metade guarda as configurações na própria flash (a central as copia para a periférica), e ele não precisa de `CONFIG_KEYPAW_OLED_LAYOUT`. O módulo faz a outra metade da proteção (escurece e apaga as telas quando ninguém digita); veja o README dele.

| Configuração | Id | O que faz | Padrão |
|---|---|---|---|
| `KP_DISPLAY_SHIFT` | 11 | 0 ou 1: o deslocamento de pixels desligado ou ligado | 1 |
| `KP_DISPLAY_SHIFT_EVERY_S` | 12 | segundos entre dois passos do caminho, de 10 a 3600 | 60 |
| `KP_DISPLAY_SHIFT_PX` | 13 | quanto a tela se afasta do seu lugar, de 1 a 4 pixels para cada lado | 2 |

Como funciona:

- O que se move é o canvas da tela de status (`lv_obj_align()` do canvas dentro do seu contêiner), então os widgets, a animação ou imagem e o toast se movem juntos. O caminho é o `kp_display_shift_offset()` do módulo: ele percorre os quadrados de uma grade de (2 x px + 1) por (2 x px + 1), linha por linha (as linhas ímpares da direita para a esquerda) e depois volta pelo mesmo caminho, então a tela só se move um pixel de cada vez, nada pula, e todo quadrado tem a sua vez. O passo 0 é o meio: o lugar onde a tela começou.
- Um timer do LVGL olha as três configurações a cada segundo, então uma mudança no ZMK Studio vale em até um segundo: desligar o deslocamento põe o canvas de volta no lugar dele, ligá-lo espera um tempo inteiro antes do primeiro passo, e uma distância menor leva o canvas de imediato ao quadrado que o mesmo passo tem no caminho menor. Uma olhada atrasada (o teclado estava ocupado) dá um passo, nunca mais que um.
- A margem que se abre de um lado é a cor de fundo da tela (o contêiner do canvas usa `LVGL_BACKGROUND` e não tem borda), e o que passa da borda do painel do outro lado fica cortado por um tempo. Um widget bem na borda da tela perde até `KP_DISPLAY_SHIFT_PX` linhas ou colunas de pixels enquanto o caminho está daquele lado; a distância padrão é de 2 pixels, e 1 perde menos. Não conferido em uma tela real.
- `python tests/pixel_shift/test_pixel_shift.py` compila o `widgets/pixel_shift.c` como ele é, com stubs do LVGL e do Zephyr (`tests/pixel_shift/stubs`) e o `zmk/display_settings.h` verdadeiro do módulo (um checkout do [lenerdz/zmk-rgb-matrix](https://github.com/lenerdz/zmk-rgb-matrix), na pasta da variável de ambiente `KEYPAW_RGB_MATRIX_DIR` ou ao lado deste repositório como `../zmk-rgb-matrix`; sem ele o teste é pulado), e verifica o tempo: nenhum passo antes de um tempo inteiro, um pixel de cada vez dentro da distância, desligar devolve o canvas ao lugar, uma olhada atrasada dá um passo, e uma mudança das configurações vale na próxima olhada. O que a tela realmente mostra **não foi experimentado em um teclado real**: o canvas se movendo dentro do seu contêiner, e o contêiner mostrando o fundo onde o canvas saiu.

## Layout das telas OLED em tempo de execução (central e periférico)

Com `CONFIG_KEYPAW_OLED_LAYOUT=y` (uma opção do módulo [lenerdz/zmk-rgb-matrix](https://github.com/lenerdz/zmk-rgb-matrix); veja "Layout das telas OLED" no README dele) os widgets deixam de tirar só do build o lugar onde ficam e se aparecem. Toda vez que desenham, eles leem do módulo se são mostrados e onde e, no periférico, qual animação ou imagem aparece e quanto tempo dura um ciclo. O [ZMK Studio](https://zmk.dev/docs/features/studio) edita esses valores (a aba OLED do app [lenerdz/zmk-studio](https://github.com/lenerdz/zmk-studio)), cada metade os guarda na sua própria flash, e a tela desenha de novo assim que um deles muda (o módulo dispara o evento `zmk_display_settings_changed`).

As opções `CONFIG_NICE_OLED_WIDGET_*_CUSTOM_X` e `_Y` e as opções `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_*` continuam existindo, como os **padrões**: até que algo seja mudado, as telas ficam como estavam sem a opção. Sem a opção nada é lido em tempo de execução e os widgets são desenhados como antes.

Ela precisa do OLED (o shield `nice_oled` com o widget de status) e de `CONFIG_KEYPAW_DISPLAY_SETTINGS=y` no módulo (que por sua vez precisa de `CONFIG_ZMK_DISPLAY_BLANK_ON_IDLE=n`), e precisa estar ligada no build das duas metades: o central guarda as configurações das duas telas e envia as da direita ao periférico. Defina as opções da tela direita (a animação, a bateria, o ícone de Bluetooth e a posição do toast) na configuração das **duas** metades, para que os padrões que o central lista sejam os que o periférico desenha. As telas e-paper não são suportadas.

| Tela | Widget | Padrão | O que se move junto |
|---|---|---|---|
| direita | animação ou imagem | `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CUSTOM_X` e `_Y`; o tipo vem de `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_*` e o tempo do ciclo de `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_MS` | o tipo e o tempo do ciclo também são configurações |
| direita | bateria | `CONFIG_NICE_OLED_WIDGET_BATTERY_CUSTOM_X` e `_Y` | o raio de carregamento |
| direita | ícone de Bluetooth | `CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_CUSTOM_X` e `_Y` | os ícones de sem sinal e de não pareado mantêm a distância dele |
| direita | toast de RGB | `CONFIG_NICE_OLED_WIDGET_LED_TOAST_CUSTOM_X` e `_Y` | a segunda linha, 8 pixels abaixo; só o lugar é uma configuração do layout, porque ligar e desligar o toast e o tempo dele são as configurações "Toast" e "Duração do toast" |
| esquerda | ícone de saída | `CONFIG_NICE_OLED_WIDGET_OUTPUT_USB_CUSTOM_X` e `_Y` | os ícones de Bluetooth e o fundo da saída mantêm a distância dele |
| esquerda | bateria | `CONFIG_NICE_OLED_WIDGET_BATTERY_CUSTOM_X` e `_Y`; x 0 e y 19 quando o build mostra as baterias das duas metades como texto | o raio de carregamento |
| esquerda | pontos dos perfis | `CONFIG_NICE_OLED_WIDGET_PROFILE_CUSTOM_X` e `_Y` (x 0 e y 129 com `CONFIG_NICE_OLED_WIDGET_PROFILE_BIG`) | as cinco marcas e a ativa |
| esquerda | número do perfil | `CONFIG_NICE_OLED_WIDGET_PROFILE_TEXT_CUSTOM_X` e `_Y` | |
| esquerda | nome da camada | `CONFIG_NICE_OLED_WIDGET_LAYER_CUSTOM_X` e `_Y` | |
| esquerda | velocímetro de WPM | `CONFIG_NICE_OLED_WIDGET_WPM_GAUGE_CUSTOM_X` e `_Y` | o ponteiro |
| esquerda | número de WPM | `CONFIG_NICE_OLED_WIDGET_WPM_LABEL_CUSTOM_X` e `_Y` | |
| esquerda | gráfico de WPM | x -1 e y 95, a grade embaixo dele (ela não tem opção) | os pontos do gráfico |

**Animações e imagens.** Com a opção ligada, todas as animações e imagens do periférico são compiladas, seja qual for o que `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_*` diz, então o ZMK Studio pode alternar entre elas com o teclado funcionando; as opções só escolhem a que aparece no início. São 42: as 5 animações do shield original (crystal, cat, head, spaceman e pokemon) e as 37 de [Novas imagens da tela direita](#novas-imagens-da-tela-direita) (31 animações e 6 imagens estáticas). Os tipos são numerados até 65 (66 números), porque um tipo mantém o seu número quando a imagem dele é retirada: 24 estão **aposentados** (as imagens estáticas vim e vip_marcos do shield original e 22 das novas; veja [Tipos aposentados](#tipos-aposentados)). Um tipo aposentado não tem imagem no firmware, o teclado não o aceita como configuração, e um teclado que tinha guardado um deles o esquece e volta ao padrão do build. Um ciclo leva o tempo que pertence a cada animação (960 ms para crystal e cat, 4800 ms para head e spaceman, 10000 ms para pokemon, e o da tabela das imagens novas para essas), exceto a que o build escolheu, que mantém `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_MS`; o ZMK Studio pode definir outro tempo, de 100 a 60000 ms. Com `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_SMART_BATTERY` a animação não faz parte do layout. A imagem também pode ser girada, recortada em um pedaço e misturada com os widgets: veja [Imagem no canvas](#imagem-no-canvas-girar-recortar-e-misturar).

**Custo.** Medido com o Corne do [lenerdz/corne-zmk](https://github.com/lenerdz/corne-zmk) (o build das revisões do `config/west.yml` dele), em comparação com o mesmo build sem o layout: a metade direita cresce 244.964 bytes de flash (todas as animações e imagens são compiladas: 160.768 bytes delas são os dados das 37 imagens que o `make_pictures.py` desenha, e o resto são os descritores das imagens e o código que coloca a imagem no canvas) e 624 bytes de RAM, e a metade esquerda 1.528 bytes de flash e 240 bytes de RAM. O crescimento da metade direita era de 254.652 bytes (com 59 imagens) antes de as 22 imagens fixas serem tiradas.

**Fora do escopo.** O bongo cat, o cachorro luna, o bongo cat responsivo, os indicadores de HID e de modificadores, os widgets de Raw HID, a arte de repouso e a animação de bateria inteligente não fazem parte do layout: eles são desenhados onde o build diz.

**Situação.** Compila para as duas metades no CI do [lenerdz/corne-zmk](https://github.com/lenerdz/corne-zmk), e o código que coloca a imagem no canvas e os arquivos que o `make_pictures.py` escreve são testados em um computador (veja abaixo). A primeira versão do layout (os widgets se movendo e sumindo, a animação alternando) foi usada em um Corne de verdade, e o dono dele relatou que funcionou, sem detalhes sobre cada operação. O que veio depois ainda não foi experimentado em um teclado real: a imagem no canvas (um widget sobre ela, o giro, o recorte e a mistura), as imagens novas, o deslocamento de pixels, os quadros que agora vêm de um work item que desenha a tela de novo a cada quadro (com que frequência ele faz isso, e quanto isso custa em bateria, não foi medido), e o redesenho do periférico quando essas configurações chegam a ele.

### Imagem no canvas: girar, recortar e misturar

Com `CONFIG_KEYPAW_OLED_LAYOUT=y` a imagem da tela direita deixa de ser um objeto de animação do LVGL sobre o canvas. O `widgets/picture.c` (C puro, sem LVGL e sem Zephyr) coloca o quadro no canvas, pixel a pixel, **depois** que os widgets foram desenhados e o canvas foi girado para o painel (`animation_composite()` de `widgets/animation.c`), então um widget pode ficar sobre a imagem (a bateria da metade direita inclusive) e a imagem pode ser girada e recortada. Os quadros vêm de um work item com atraso da work queue do display, que avança o quadro (no mínimo 20 ms cada) e desenha a tela de novo. O toast de RGB é escrito no canvas junto com os outros widgets, então a imagem vai por cima dele também. Sem a opção a animação é desenhada como antes.

Mais quatro configurações do módulo (os ids e as faixas estão no README dele, em "Layout das telas OLED") dizem como a imagem é colocada:

| Configuração | Id | Valores | Padrão |
|---|---|---|---|
| `KP_OLED_R_ANIM_ROT` | 112 | quartos de volta no sentido horário, como se olha a tela: de 0 a 3 | 0 |
| `KP_OLED_R_ANIM_MIX` | 113 | como um pixel aceso da imagem se mistura com o canvas: 0 soma (o pixel fica aceso seja qual for o que havia ali, então um widget some onde a imagem é clara), 1 inverte (um widget sobre a imagem aparece em reverso, então continua legível) | 1 |
| `KP_OLED_R_ANIM_CROP_XY` | 114 | o canto do pedaço que aparece, `x \| y << 8`, em pixels da imagem em pé (um canto além da imagem é tomado como o último pixel dela) | 0 |
| `KP_OLED_R_ANIM_CROP_WH` | 115 | o tamanho do pedaço, `w \| h << 8`; uma largura ou uma altura 0 é a imagem inteira, e o que passa da imagem é cortado | 0 |

Os pixels apagados de uma imagem nunca tocam o canvas. As imagens são guardadas giradas um quarto de volta no sentido horário (o canvas é girado 270 graus para o painel), então se fala de três imagens: a **guardada** (os pixels do arquivo), a **em pé** (a guardada girada um quarto de volta no sentido anti-horário, e depois girada pelos quartos de volta da configuração: o recorte é um pedaço desta) e a **exibida** (a em pé girada de novo um quarto de volta no sentido horário: o que vai parar no canvas). A posição (`CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CUSTOM_X` e `_Y`, ou a configuração do ZMK Studio) é o canto superior esquerdo da imagem exibida **inteira**, e um recorte só esconde o resto, então o pedaço não pula quando muda.

`python tests/picture/test_picture.py` compila o `picture.c` como ele é, o chama a partir do Python e o compara com um modelo que gira arrays inteiros em vez de calcular índices, em 1.500 imagens aleatórias (tamanhos, giros, recortes, posições e misturas aleatórios, com a tinta escura ou clara); outros testes verificam que nada fora do canvas é tocado, que argumentos inválidos não desenham nada e que um recorte que começa além da imagem mantém o último pixel dela (precisa de numpy, Pillow e de um compilador C, ou do pacote `ziglang`: `python -m ziglang cc`). Nada disso foi visto em uma tela real.

### Novas imagens da tela direita

Os tipos de 7 a 65 são desenhados por `scripts/pictures/make_pictures.py` em dois lotes: o primeiro (tipos de 7 a 25, em `animations.py` e `stills.py`: 11 animações, depois 8 imagens estáticas, 4 delas aposentadas) e o segundo (tipos de 26 a 65, em `animations2.py` e `stills2.py`: 20 animações, depois 20 imagens estáticas, 18 delas aposentadas). Dos 59 tipos, 37 têm imagem: 31 animações e 6 imagens estáticas (`mountains`, `skyline`, `circuit`, `keyboard`, `moon_cat` e `planet`); os outros 22 estão [aposentados](#tipos-aposentados) e não estão na tabela abaixo. São em pé e com 32 pixels de largura (a largura do painel), e escritos como arquivos LVGL de 1 bit por pixel como os outros assets (`assets/pictures/<name>.c`), com a lista `widgets/pictures.h` (a tabela `PICTURES(X)` que o `widgets/animation.c` transforma na sua tabela de tipos) e o manifesto `assets/pictures/pictures.json` (o tipo, o tamanho, os quadros e o ciclo de cada uma, que o app do ZMK Studio lê para fazer os sprites dele).

| Tipo | Imagem | Tamanho | Quadros | Um ciclo | O que é |
|---|---|---|---|---|---|
| 7 | `equalizer` | 32 x 64 | 16 | 1200 ms | Oito barras de um equalizador de som que sobem e descem, cada uma com uma marca que cai devagar atrás dela |
| 8 | `radar` | 32 x 32 | 24 | 2400 ms | Uma varredura de radar com um rastro que se apaga, e três pontos que acendem quando ela passa |
| 9 | `heartbeat` | 32 x 64 | 16 | 1600 ms | O traçado de um monitor cardíaco, rolando para baixo e se apagando conforme envelhece |
| 10 | `rain` | 32 x 128 | 32 | 3200 ms | Chuva digital: riscos que caem pela tela inteira, brilhantes na ponta e piscando atrás |
| 11 | `cube` | 32 x 32 | 16 | 1600 ms | Um cubo de arame que gira, com as arestas de trás pontilhadas |
| 12 | `atom` | 32 x 32 | 24 | 2400 ms | Um núcleo com três órbitas e um elétron em cada uma |
| 13 | `helix` | 32 x 128 | 16 | 1600 ms | As duas fitas de uma hélice de DNA girando em torno do eixo, com os degraus entre elas |
| 14 | `warp` | 32 x 64 | 24 | 2400 ms | Estrelas que voam do meio, mais rápidas e mais longas quando se aproximam |
| 15 | `sonar` | 32 x 32 | 16 | 1600 ms | Anéis que se espalham do meio e se apagam |
| 16 | `bounce` | 32 x 64 | 24 | 1200 ms | Uma bola que quica, se achata no chão e tem uma sombra |
| 17 | `flame` | 32 x 64 | 16 | 1200 ms | Um fogo que tremula |
| 18 | `mountains` | 32 x 128 | estática | nenhum | Um céu noturno com uma lua, e três cadeias de montanhas |
| 19 | `skyline` | 32 x 128 | estática | nenhum | Uma cidade à noite, com as janelas acesas e algumas estrelas |
| 20 | `circuit` | 32 x 128 | estática | nenhum | As trilhas de uma placa de circuito, com um chip |
| 23 | `keyboard` | 32 x 64 | estática | nenhum | As duas metades de um Corne, vistas de cima |
| 26 | `waterfall` | 32 x 128 | 16 | 1600 ms | Água que cai de uma saliência entre dois penhascos, com névoa e uma poça que ondula |
| 27 | `lava` | 32 x 128 | 16 | 3200 ms | Uma lâmpada de lava: bolhas de cera que sobem, se esticam e afundam de novo em um vidro com base |
| 28 | `lightning` | 32 x 64 | 16 | 1600 ms | Uma tempestade: uma nuvem, chuva inclinada e dois raios que piscam um depois do outro |
| 29 | `snow` | 32 x 64 | 24 | 2400 ms | Neve que cai ao lado de um pinheiro em uma colina, sob uma lua |
| 30 | `jellyfish` | 32 x 64 | 16 | 1600 ms | Uma água-viva que pulsa, com tentáculos que ondulam e alguns pontinhos que flutuam para cima |
| 31 | `tetris` | 32 x 64 | 20 | 2000 ms | Peças que caem por um tabuleiro de oito colunas, girando no caminho, como o protetor de tela de um jogo de blocos que caem (elas passam umas pelas outras e saem por baixo) |
| 32 | `pong` | 32 x 64 | 24 | 1500 ms | Uma partida de pong jogada de cima para baixo: duas raquetes que seguem a bola, a rede e o placar |
| 33 | `invaders` | 32 x 64 | 8 | 1600 ms | Uma formação de alienígenas que marcha de um lado para o outro, um canhão que derruba um deles a tiros e um disco voador que cruza o topo |
| 34 | `pacman` | 32 x 32 | 16 | 1600 ms | Um disco com uma boca come uma fileira de pontos perseguindo um fantasma assustado, e um fantasma o persegue na fileira seguinte |
| 35 | `life` | 32 x 64 | 30 | 3000 ms | O Jogo da Vida de Conway em um campo pequeno: um pulsar, um pentadecatlo, um sapo, um farol, semáforos e algumas formas estáveis; tudo volta onde começou depois de 30 gerações, que é o laço |
| 36 | `plasma` | 32 x 64 | 24 | 2400 ms | O plasma das demos antigas: ondas que se somam, desenhadas com um pontilhado ordenado |
| 37 | `spiral` | 32 x 32 | 16 | 1600 ms | Uma espiral de três braços que gira, dentro de um anel |
| 38 | `newton` | 32 x 32 | 16 | 1600 ms | O pêndulo de Newton: a bola de um lado balança para dentro, a do outro lado balança para fora e volta, e a primeira responde |
| 39 | `gears` | 32 x 32 | 12 | 1000 ms | Duas engrenagens que se encaixam e giram |
| 40 | `hourglass` | 32 x 64 | 20 | 2000 ms | Uma ampulheta: a areia escorre pelo gargalo e, no fim de cada ciclo, o vidro vira de ponta-cabeça |
| 41 | `windmill` | 32 x 64 | 16 | 1600 ms | Um moinho de vento cujas pás giram sob nuvens que passam e voltam |
| 42 | `fireworks` | 32 x 64 | 24 | 2400 ms | Foguetes que sobem e estouram em faíscas que caem; três explosões se revezam, então sempre há algo estourando |
| 43 | `ufo` | 32 x 64 | 16 | 1600 ms | Um disco voador que paira sobre um campo e levanta uma vaca com o seu feixe, e depois a devolve |
| 44 | `eye` | 32 x 32 | 24 | 2400 ms | Um olho que olha em volta desenhando um oito e pisca uma vez por ciclo |
| 45 | `keywave` | 32 x 64 | 24 | 2400 ms | Uma onda de toques de tecla que varre um campo de teclas |
| 49 | `moon_cat` | 32 x 64 | estática | nenhum | Um gato sentado em um muro diante da lua cheia, visto de costas |
| 51 | `planet` | 32 x 64 | estática | nenhum | Um planeta com anéis e uma pequena lua, entre as estrelas |

| Comando | O que faz |
|---|---|
| `python scripts/pictures/make_pictures.py` | lista o que existe |
| `python scripts/pictures/make_pictures.py --preview DIR` | escreve em `DIR` folhas de PNG para olhar, e nenhum outro arquivo |
| `python scripts/pictures/make_pictures.py --write` | escreve os arquivos C, o `pictures.h` e o `pictures.json` |
| `python scripts/pictures/make_pictures.py --check` | falha quando os arquivos não são o que `--write` faz |
| `python scripts/pictures/make_pictures.py --check --module <zmk-rgb-matrix>` | também verifica que o enum do módulo tem as imagens |

O número de um tipo é o que o teclado guarda na sua flash, então uma imagem nova é **só acrescentada no fim**, em um lote novo: escreva o desenho dela em um novo par de arquivos (como `animations2.py` e `stills2.py`), liste o par em `BATCHES` do `make_pictures.py` (as animações de um lote vêm primeiro, depois as imagens estáticas dele; um nome não pode se repetir, nem ser o de um dos tipos originais), ponha o mesmo nome com o mesmo número em `enum kp_oled_anim_kind` do módulo (`include/zmk/display_settings.h`), aumente `KP_OLED_ANIM_KIND_COUNT`, rode `--write` e gere de novo os sprites do app (`scripts/oled-assets/convert.py` do [lenerdz/zmk-studio](https://github.com/lenerdz/zmk-studio), que lê o `pictures.json`). Para retirar uma imagem, mantenha o nome e o número dela: ponha `None` no lugar dela em `STILLS`, marque o tipo como aposentado em `kp_oled_anim_kind_retired()` do módulo, rode `--write` (ele apaga o arquivo antigo) e gere de novo os sprites do app. `python tests/picture/test_generated.py` verifica que os arquivos são o que o script faz, que um compilador C lê neles os mesmos bytes que um analisador do texto lê (e que eles voltam a ser as imagens que foram desenhadas), que a lista é consistente, e que todo tipo que existe mantém o seu nome e o seu número (um tipo aposentado também os mantém, e não tem arquivo). A aparência dos desenhos foi conferida em folhas de arquivos PNG, não em uma tela real.

#### Tipos aposentados

Vinte e duas das imagens estáticas foram retiradas do gerador e do firmware (só seis foram mantidas: `mountains`, `skyline`, `circuit`, `keyboard`, `moon_cat` e `planet`), e o mesmo aconteceu com `vim` (5) e `vip_marcos` (6), as duas imagens estáticas do shield original, no layout em tempo de execução. Um tipo mantém o seu número e o seu nome quando a imagem dele sai, porque o número é o que o teclado tem na sua flash e o enum do módulo é feito dos nomes:

- em `stills.py` e `stills2.py` a função sumiu e a entrada de `STILLS` é `None`;
- o `make_pictures.py` não escreve arquivo nem linha de `PICTURES(X)` para ele (então a tabela do `widgets/animation.c` tem uma entrada vazia: sem quadros), e o lista em `"retired"` no `pictures.json`;
- o `animation_apply()` nunca escolhe um tipo que não tem quadros: ele desenha o padrão do build no lugar (que o módulo faz ser `crystal` quando o build pediu um tipo aposentado), então a tela nunca desenha a partir do nada;
- no módulo, `kp_oled_anim_kind_retired()` diz que ele está aposentado: o teclado não o aceita como configuração e descarta um que tinha guardado. `python scripts/pictures/make_pictures.py --check --module <zmk-rgb-matrix>` falha quando as duas listas discordam.

As opções `CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL_VIM` e `CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL_VIP_MARCOS` continuam valendo em um build **sem** o layout. Com `CONFIG_KEYPAW_OLED_LAYOUT=y`, um build que pede uma delas começa com `crystal`.

| Tipo | Imagem | Tamanho | O que era |
|---|---|---|---|
| 21 | `alien` | 32 x 32 | Um pequeno alienígena robô em um chão estrelado |
| 22 | `heart` | 32 x 32 | Um coração com um brilho |
| 24 | `pulsar` | 32 x 128 | Linhas de um sinal, uma acima da outra, que escondem as de trás, como a capa de um disco antigo |
| 25 | `rocket` | 32 x 64 | Um foguete decolando |
| 46 | `coffee` | 32 x 64 | Uma xícara de café com a marca ZMK e vapor, no pires |
| 47 | `cactus` | 32 x 64 | Um cacto saguaro no deserto, com o sol baixo sobre as dunas |
| 48 | `lighthouse` | 32 x 128 | Um farol sobre a sua rocha, varrendo a noite com o seu feixe |
| 50 | `robot` | 32 x 64 | Um robô simpático com uma antena |
| 52 | `castle` | 32 x 64 | Um castelo com duas torres e uma torre de menagem, sob a lua |
| 53 | `tree` | 32 x 128 | Uma árvore grande em uma colina, com maçãs, um oco e um casal de pássaros |
| 54 | `skull` | 32 x 64 | Uma caveira com ossos cruzados |
| 55 | `sword` | 32 x 128 | Uma espada longa com uma gema na guarda |
| 56 | `key` | 32 x 64 | Uma chave antiga com a argola de três lóbulos |
| 57 | `antenna` | 32 x 128 | Uma torre de rádio emitindo o seu sinal |
| 58 | `potion` | 32 x 64 | Um frasco redondo com uma poção borbulhante e um coração |
| 59 | `sailboat` | 32 x 64 | Um veleiro nas ondas, com o sol e uma gaivota |
| 60 | `compass` | 32 x 32 | Uma rosa dos ventos dentro de dois anéis |
| 61 | `crown` | 32 x 32 | Uma coroa com cinco pontas e joias |
| 62 | `cassette` | 32 x 32 | Uma fita cassete de áudio, com a etiqueta MIX e os seus dois carretéis |
| 63 | `floppy` | 32 x 32 | Um disquete, com a sua aba de metal e uma etiqueta que diz ZMK |
| 64 | `phases` | 32 x 128 | As oito fases da lua, uma acima da outra |
| 65 | `mushroom` | 32 x 32 | Um cogumelo de chapéu manchado e com rosto, como nos jogos antigos |

## Específico do central

| Variável | Tipo | Padrão | Descrição |
|----------|------|--------|-----------|
| `CONFIG_NICE_OLED_WIDGET_WPM` | bool | `y` | Habilita o widget de WPM do Nice OLED |
| `CONFIG_NICE_OLED_WIDGET_WPM_NUMBER` | bool | `y` | Habilita NUMBER (número) para o WPM |
| `CONFIG_NICE_OLED_WIDGET_WPM_SPEEDOMETER` | bool | `y` (OLED) | Habilita SPEEDOMETER (velocímetro) para o WPM |
| `CONFIG_NICE_OLED_WIDGET_WPM_GRAPH` | bool | `n` (OLED) | Habilita GRAPH (gráfico) para o medidor/gráfico de WPM |
| `CONFIG_NICE_OLED_WIDGET_WPM_GRAPH_FIXED_RANGE` | bool | `y` | Habilita faixa fixa para o medidor/gráfico de WPM |
| `CONFIG_NICE_OLED_WIDGET_WPM_GRAPH_FIXED_RANGE_MAX` | int | `100` | Máximo da faixa fixa para o medidor/gráfico de WPM |
| `CONFIG_NICE_OLED_WIDGET_WPM_LUNA` | bool | `y` | Habilita o wpm luna |
| `CONFIG_NICE_OLED_WIDGET_WPM_LUNA_ANIMATION_MS` | int | `300` | Animação da Luna, em ms, para o widget de WPM |
| `CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT` | bool | `n` | Habilita o wpm bongo cat |
| `CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT_ANIMATION_MS` | int | `300` | Animação do Bongo Cat, em ms, para o widget de WPM |
| `CONFIG_NICE_OLED_WIDGET_RESPONSIVE` | bool | `n` | Habilita o widget responsivo (sobrescreve a pilha para `4096` e a prioridade para `3`) |
| `CONFIG_NICE_OLED_WIDGET_RESPONSIVE_BONGO_CAT` | bool | `n` | Habilita o bongo cat do widget responsivo |

## Indicadores HID

| Variável                                                         | Tipo | Padrão  | Descrição                                         |
|------------------------------------------------------------------|------|---------|---------------------------------------------------|
| `CONFIG_NICE_OLED_WIDGET_HID_INDICATORS`                         | bool | `y`     | Habilita os indicadores HID                       |
| `CONFIG_ZMK_HID_INDICATORS`                                      | bool | `y`     | Habilita os indicadores HID (núcleo do ZMK)       |
| `CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_LUNA`                    | bool | `n`     | Habilita a luna dos indicadores HID               |
| `CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_LUNA_ONLY_CAPSLOCK`      | bool | `y`     | Habilita a luna dos indicadores HID apenas no CapsLock |
| `CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_LUNA_ANIMATION_MS`       | int  | `300`   | Animação da Luna, em ms, para os indicadores HID  |
| `CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_BONGO_CAT`               | bool | `n`     | Habilita o bongo cat dos indicadores HID          |
| `CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_BONGO_CAT_ONLY_CAPSLOCK` | bool | `y`     | Habilita o bongo cat dos indicadores HID apenas no CapsLock |
| `CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_BONGO_CAT_ANIMATION_MS`  | int  | `300`   | Animação da Luna, em ms, para o bongo cat dos indicadores HID |

## Raw HID

| Variável | Tipo | Padrão | Descrição |
|----------|------|--------|-----------|
| `CONFIG_NICE_OLED_WIDGET_RAW_HID` | bool | - | Habilita o RAW HID |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_DRIVER` | bool | `y` | Habilita o Raw HID |
| `CONFIG_USB_HID_DEVICE_COUNT` | int | `2` | Habilita CONFIG USB HID DEVICE COUNT |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_TIME` | bool | `y` | Exibe a hora |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_VOLUME` | bool | `y` | Exibe o volume |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_USAGE_PAGE` | hex | `0xFF60` | Usage Page do Raw HID |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_USAGE` | hex | `0x61` | Usage do Raw HID |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_REPORT_SIZE` | int | `32` | Tamanho do report do Raw HID |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_DEVICE` | string | `HID_1` | Dispositivo do Raw HID |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_LAYOUT` | bool | `y` | Exibe o layout |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_LAYOUT_LIST` | string | `"DE,US,LA,AB"` | Lista de layouts separados por vírgula |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_WEATHER` | bool | `n` | Widget de clima do nice!OLED |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_MEDIA_PLAYER_SPOTIFY_MACOS` | bool | `n` | Widget de media player Spotify para macOS do nice!OLED |

## Indicadores de modificadores

| Variável | Tipo | Padrão | Descrição |
|----------|------|--------|-----------|
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS` | bool | `y` | Habilita os indicadores de modificadores |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED` | bool | `y` | Habilita os indicadores de modificadores fixos |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_LETTER` | bool | `n` | Estilo: Letras (texto C/S/A/G) |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_SYMBOL` | bool | `y` | Estilo: Ícones reais (padrão) |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_HOR` | bool | `n` | Layout: Horizontal |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_VER` | bool | `n` | Layout: Vertical |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_BOX` | bool | `y` | Layout: Caixa/Grade (padrão) |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_VER_ALIGN_LEFT` | bool | `n` | Alinhamento vertical: Esquerda |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_VER_ALIGN_CENTER` | bool | `y` | Alinhamento vertical: Centro (padrão) |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_VER_ALIGN_RIGHT` | bool | `n` | Alinhamento vertical: Direita |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_SYMBOL_MACOS` | bool | `y` | Estilo do SO: macOS (padrão) |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_SYMBOL_WINDOWS` | bool | `n` | Estilo do SO: Windows |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_LUNA` | bool | `n` | Habilita a luna dos indicadores de modificadores |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_LUNA_ANIMATION_MS` | int | `300` | Animação da Luna, em ms, para os indicadores de modificadores |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_BONGO_CAT` | bool | `n` | Habilita a animação do Bongo Cat para os indicadores de modificadores |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_BONGO_CAT_ANIMATION_MS` | int | `300` | Velocidade da animação (ms) do Bongo Cat dos modificadores |

### Ícones de símbolos

Ao usar o estilo `SYMBOL`, os seguintes ícones reais são exibidos:

**Modo macOS (padrão):**
- Control: `⌃` (símbolo de circunflexo)
- Shift: `⇧` (seta para cima)
- Option: `⌥` (símbolo da tecla option)
- Command: `⌘` (símbolo de command/trevo)

**Modo Windows:**
- Control: `⌃` (símbolo de circunflexo)
- Shift: `⇧` (seta para cima)
- Alt: ícone de texto `Alt`
- Win: logotipo do Windows

## Outros widgets (central)

| Variável | Tipo | Padrão | Descrição |
|----------|------|--------|-----------|
| `CONFIG_NICE_OLED_WIDGET_LAYER` | bool | `y` | Habilita o widget de camada |
| `CONFIG_NICE_OLED_WIDGET_PROFILE_BIG` | bool | `n` | Habilita exibir o widget de perfil maior |
| `CONFIG_NICE_OLED_WIDGET_CENTRAL` | bool | `n` | Habilita o widget de teste no central |

## Widget de bateria (experimental)

| Variável | Tipo | Padrão | Descrição |
|----------|------|--------|-----------|
| `CONFIG_NICE_OLED_WIDGET_CENTRAL_SHOW_BATTERY_PERIPHERAL_ALL` | bool | `n` | Exibe todas as baterias disponíveis na tela central, incluindo a bateria do central |
| `CONFIG_NICE_OLED_WIDGET_CENTRAL_SHOW_BATTERY_PERIPHERAL_ONLY` | bool | `n` | Exibe todas as baterias dos periféricos, mas não a bateria do central |
| `CONFIG_NICE_OLED_WIDGET_CENTRAL_SHOW_BATTERY_PERIPHERAL_AND_CENTRAL` | bool | `n` | Exibe apenas 1 bateria de periférico e a bateria do central |

## Coordenadas de posição dos widgets

Essas variáveis permitem que os usuários personalizem as posições dos widgets. Cada widget tem coordenadas X e Y que podem ser definidas no seu arquivo `.conf`. Os padrões são definidos por shield (OLED vs ePaper). Com `CONFIG_KEYPAW_OLED_LAYOUT=y` esses valores são apenas os padrões: veja [Layout das telas OLED em tempo de execução](#layout-das-telas-oled-em-tempo-de-execução-central-e-periférico).

### Posição do widget de camada

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_LAYER_CUSTOM_X` | int | `0` | `0` | Posição X do widget de camada |
| `CONFIG_NICE_OLED_WIDGET_LAYER_CUSTOM_Y` | int | `146` | `146` | Posição Y do widget de camada |

### Posição do widget de bateria

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_BATTERY_CUSTOM_X` | int | `0` | `26` | Posição X do widget de bateria |
| `CONFIG_NICE_OLED_WIDGET_BATTERY_CUSTOM_Y` | int | `50` | `19` | Posição Y do widget de bateria |

### Posição do widget de perfil

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_PROFILE_CUSTOM_X` | int | `0` | `18` | Posição X do widget de perfil |
| `CONFIG_NICE_OLED_WIDGET_PROFILE_CUSTOM_Y` | int | `137` | `129` | Posição Y do widget de perfil |
| `CONFIG_NICE_OLED_WIDGET_PROFILE_TEXT_CUSTOM_X` | int | `25` | `25` | Posição X do texto do perfil |
| `CONFIG_NICE_OLED_WIDGET_PROFILE_TEXT_CUSTOM_Y` | int | `32` | `32` | Posição Y do texto do perfil |

### Posição do widget de saída (output)

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_OUTPUT_USB_CUSTOM_X` | int | `0` | `45` | Posição X do ícone de USB da saída |
| `CONFIG_NICE_OLED_WIDGET_OUTPUT_USB_CUSTOM_Y` | int | `34` | `2` | Posição Y do ícone de USB da saída |
| `CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_CUSTOM_X` | int | `4` | `49` | Posição X do ícone de BT da saída |
| `CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_CUSTOM_Y` | int | `32` | `0` | Posição Y do ícone de BT da saída |
| `CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_UNBONDED_CUSTOM_X` | int | `-1` | `44` | Posição X do ícone de BT não pareado da saída |
| `CONFIG_NICE_OLED_WIDGET_OUTPUT_BT_UNBONDED_CUSTOM_Y` | int | `32` | `0` | Posição Y do ícone de BT não pareado da saída |

### Posição do widget de WPM

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_WPM_GAUGE_CUSTOM_X` | int | `0` | `16` | Posição X do medidor de WPM |
| `CONFIG_NICE_OLED_WIDGET_WPM_GAUGE_CUSTOM_Y` | int | `70` | `43` | Posição Y do medidor de WPM |
| `CONFIG_NICE_OLED_WIDGET_WPM_NEEDLE_CENTER_CUSTOM_X` | int | `12` | `33` | Posição X do centro do ponteiro do WPM |
| `CONFIG_NICE_OLED_WIDGET_WPM_NEEDLE_CENTER_CUSTOM_Y` | int | `90` | `66` | Posição Y do centro do ponteiro do WPM |
| `CONFIG_NICE_OLED_WIDGET_WPM_LABEL_CUSTOM_X` | int | `0` | `0` | Posição X do rótulo do WPM |
| `CONFIG_NICE_OLED_WIDGET_WPM_LABEL_CUSTOM_Y` | int | `75` | `103` | Posição Y do rótulo do WPM |

### Posição do widget Luna

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_LUNA_CUSTOM_X` | int | `65` | `100` | Posição X do widget Luna |
| `CONFIG_NICE_OLED_WIDGET_LUNA_CUSTOM_Y` | int | `0` | `15` | Posição Y do widget Luna |

### Posição do widget Bongo Cat

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_BONGO_CAT_CUSTOM_X` | int | `64` (POS1) / `33` (POS2) | `100` | Posição X do widget Bongo Cat |
| `CONFIG_NICE_OLED_WIDGET_BONGO_CAT_CUSTOM_Y` | int | `-9` | `8` | Posição Y do widget Bongo Cat |

### Posição do widget de indicadores HID

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_CUSTOM_X` | int | `36` | `100` | Posição X do widget de indicadores HID |
| `CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_CUSTOM_Y` | int | `0` | `15` (Luna) / `8` (Bongo) | Posição Y do widget de indicadores HID |

### Posição do widget de modificadores

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_CUSTOM_X` | int | `0` | `2` | Posição X do widget de modificadores |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_CUSTOM_Y` | int | `100` | `110` | Posição Y do widget de modificadores |

### Posição da animação do periférico

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CUSTOM_X` | int | `18` | `36` | Posição X da animação do periférico |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CUSTOM_Y` | int | `-18` | `0` | Posição Y da animação do periférico |

### Posição do widget do toast de RGB

A posição da primeira linha do [Toast de RGB](#toast-de-rgb-periférico); a segunda linha fica 8 pixels abaixo. No OLED de 128x32 a parte visível do canvas de 68x160 é x de 0 a 31 e y de 32 a 159, e a faixa abaixo da animação padrão do gato é y de 142 a 159.

| Variável | Tipo | Padrão | Descrição |
|----------|------|--------|-----------|
| `CONFIG_NICE_OLED_WIDGET_LED_TOAST_CUSTOM_X` | int | `0` | Posição X do toast de RGB |
| `CONFIG_NICE_OLED_WIDGET_LED_TOAST_CUSTOM_Y` | int | `143` | Posição Y do toast de RGB |

### Posição do widget Raw HID

O widget Raw HID tem vários submódulos que podem ser posicionados de forma independente.

#### Posição base (fallback para a mensagem "HID not found")

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_CUSTOM_X` | int | `0` | `0` | Posição X base do Raw HID |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_CUSTOM_Y` | int | `62` | `38` | Posição Y base do Raw HID |

#### Submódulo de clima (temperatura)

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_WEATHER_CUSTOM_X` | int | `0` | `0` | Posição X do clima |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_WEATHER_CUSTOM_Y` | int | `62` | `38` | Posição Y do clima |

#### Submódulo de hora

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_TIME_CUSTOM_X` | int | `0` | `0` | Posição X da hora |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_TIME_CUSTOM_Y` | int | `74` | `50` | Posição Y da hora |

#### Submódulo de layout

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_LAYOUT_CUSTOM_X` | int | `0` | `0` | Posição X do layout |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_LAYOUT_CUSTOM_Y` | int | `86` | `62` | Posição Y do layout |

#### Submódulo de volume

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_VOLUME_CUSTOM_X` | int | `0` | `0` | Posição X do volume |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_VOLUME_CUSTOM_Y` | int | `98` | `74` | Posição Y do volume |

#### Submódulo de media player (Spotify)

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_MEDIA_PLAYER_CUSTOM_X` | int | `0` | `0` | Posição X do media player |
| `CONFIG_NICE_OLED_WIDGET_RAW_HID_MEDIA_PLAYER_CUSTOM_Y` | int | `110` | `86` | Posição Y do media player |

### Posição do widget Bongo Cat responsivo

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_RESPONSIVE_BONGO_CAT_CUSTOM_X` | int | `64` | `64` | Posição X do widget Bongo Cat responsivo |
| `CONFIG_NICE_OLED_WIDGET_RESPONSIVE_BONGO_CAT_CUSTOM_Y` | int | `-9` | `-9` | Posição Y do widget Bongo Cat responsivo |

### Posição do widget de status de repouso

| Variável | Tipo | Padrão OLED | Padrão ePaper | Descrição |
|----------|------|-------------|---------------|-----------|
| `CONFIG_NICE_OLED_WIDGET_SLEEP_STATUS_CUSTOM_X` | int | `0` | `0` | Posição X do widget de status de repouso |
| `CONFIG_NICE_OLED_WIDGET_SLEEP_STATUS_CUSTOM_Y` | int | `0` | `0` | Posição Y do widget de status de repouso |


# Implementação do ZMK RAW HID

Este documento descreve a implementação do RAW HID para o nice!OLED, o nice!view e o nice!custom.

## 0. Início rápido
1. Compile o seu `.uf2` e grave-o no teclado incluindo o shield `zmk-nice-oled`, conforme indicado nas instruções do README.md
   - não se esqueça de ativar a flag `CONFIG_NICE_OLED_WIDGET_RAW_HID=y`
2. Baixe e instale o programa `zmk-hid-host` no seu computador e configure-o para iniciar sempre no login
   - `zmk-hid-host` não gasta muitos recursos de CPU, `0%`!
   - modifique o arquivo `json` se necessário!
   - o `zmk-hid-host` é compatível com processadores `intel` e com a série `m` da Apple, é um binário universal!
3. Aproveite o seu teclado!!!
   - lembre-se de personalizar ao seu gosto.
   - DICA: você pode ativar a exibição do clima e da música do seu Spotify no macOS!

## 1. Introdução ao RAW HID

O RAW HID oferece uma forma flexível de enviar e receber dados personalizados entre o teclado e o computador host. Isso permite recursos avançados que não são cobertos pelos perfis HID padrão.

Para habilitar o RAW HID, você precisa definir as seguintes opções no seu `Kconfig.defconfig`:

```
CONFIG_NICE_OLED_WIDGET_RAW_HID=y
```

Isso habilitará a interface RAW HID e os widgets correspondentes.

## 2. Recursos RAW HID disponíveis

Os seguintes recursos são implementados usando RAW HID:

### 2.1. Troca de layout

Este recurso permite exibir o layout de teclado atual na tela OLED. O layout pode ser enviado a partir do computador host.

**Opções do Kconfig:**

```
CONFIG_NICE_OLED_WIDGET_RAW_HID_LAYOUT=y
CONFIG_NICE_OLED_WIDGET_RAW_HID_LAYOUT_LIST="DE,US,LA,AB"
CONFIG_NICE_OLED_WIDGET_RAW_HID_LAYOUT_CUSTOM_X=0
CONFIG_NICE_OLED_WIDGET_RAW_HID_LAYOUT_CUSTOM_Y=86
```

O `LAYOUT_LIST` é uma lista, separada por vírgulas, de nomes de layouts que serão exibidos na tela com base no índice recebido do host.

### 2.2. Widget de clima (somente macOS)

Este widget exibe a temperatura atual recebida do computador host.

**Opções do Kconfig:**

```
CONFIG_NICE_OLED_WIDGET_RAW_HID_WEATHER=y
CONFIG_NICE_OLED_WIDGET_RAW_HID_WEATHER_CUSTOM_X=0
CONFIG_NICE_OLED_WIDGET_RAW_HID_WEATHER_CUSTOM_Y=62
```

O aplicativo host precisa enviar o valor da temperatura ao teclado. **Este recurso está atualmente otimizado para macOS.**

### 2.3. Widget de media player do Spotify (somente macOS)

Este widget exibe a música que está tocando no Spotify em um computador macOS.

**Opções do Kconfig:**

```
CONFIG_NICE_OLED_WIDGET_RAW_HID_MEDIA_PLAYER_SPOTIFY_MACOS=y
CONFIG_NICE_OLED_WIDGET_RAW_HID_MEDIA_PLAYER_CUSTOM_X=0
CONFIG_NICE_OLED_WIDGET_RAW_HID_MEDIA_PLAYER_CUSTOM_Y=110
```

É necessário um aplicativo host para ler as informações da música no Spotify e enviá-las ao teclado. **Este recurso é exclusivo do macOS.**

### 2.4. Widget de hora do sistema

Este widget exibe a hora atual do sistema, sincronizada com o computador host.

**Opções do Kconfig:**

```
CONFIG_NICE_OLED_WIDGET_RAW_HID_TIME=y
CONFIG_NICE_OLED_WIDGET_RAW_HID_TIME_CUSTOM_X=0
CONFIG_NICE_OLED_WIDGET_RAW_HID_TIME_CUSTOM_Y=74
```

**Este recurso é compatível com Windows, Linux e macOS.**

### 2.5. Widget de volume do sistema

Este widget exibe o volume de áudio atual do sistema.

**Opções do Kconfig:**

```
CONFIG_NICE_OLED_WIDGET_RAW_HID_VOLUME=y
CONFIG_NICE_OLED_WIDGET_RAW_HID_VOLUME_CUSTOM_X=0
CONFIG_NICE_OLED_WIDGET_RAW_HID_VOLUME_CUSTOM_Y=98
```

**Este recurso é compatível com Windows, Linux e macOS.**

## 3. Aplicativo no lado do host

O aplicativo host complementar, `qmk-hid-host`, fornece a ponte de dados necessária para os recursos universais de Raw HID (hora do sistema, volume, layout) em Linux, Windows e macOS.

*   **Contribuições técnicas (melhorias para macOS)**:
    *   **Suporte a temperatura no macOS**: Implementado monitoramento de temperatura específico da plataforma para macOS dentro da base de código Rust.
    *   **Integração com o Spotify**: Desenvolvida uma ponte nativa AppleScript/Rust para obter, em tempo real, os metadados da faixa do Spotify e exibi-los no periférico (somente macOS).
    *   **Suporte a múltiplas arquiteturas**: Desenvolvido um wrapper universal de aplicativo para macOS, empacotando binários nativos para as arquiteturas Intel (`x86_64`) e Apple Silicon (`arm64`), garantindo uma implantação transparente em todo o ecossistema Apple.

Você pode compilar o aplicativo a partir do código-fonte seguindo estes passos:

1.  Clone o repositório original:
    ```bash
    git clone https://github.com/zzeneg/qmk-hid-host.git
    ```
2.  Navegue até o diretório do projeto:
    ```bash
    cd qmk-hid-host
    ```
3.  Compile o projeto em modo release:
    ```bash
    cargo build --release
    ```
4.  O binário estará disponível em `target/release/`.

Depois de compilado, você pode executar o aplicativo. Ele detectará automaticamente o seu teclado e começará a enviar os dados necessários.

## 4. Criando um `.dmg` para o aplicativo macOS

Depois de ter o seu aplicativo no lado do host, você pode criar um arquivo `.dmg` para facilitar a distribuição e a instalação.

Você pode usar a ferramenta `create-dmg`, que pode ser instalada via Homebrew:

```bash
brew install create-dmg
```

Em seguida, você pode criar o arquivo `.dmg` com o seguinte comando:

```bash
create-dmg \
  --volname "ZMK RAW HID Host" \
  --background "path/to/your/background.png" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "YourApp.app" 170 200 \
  --hide-extension "YourApp.app" \
  --app-drop-link 430 200 \
  "ZMK_RAW_HID_Host.dmg" \
  "source_folder/"
```

Substitua `"YourApp.app"` e `"source_folder/"` pelo seu aplicativo e pela sua pasta de origem reais.

## 5. Executando o aplicativo na inicialização

Para fazer o aplicativo host executar automaticamente toda vez que você iniciar o seu Mac, você pode adicioná-lo aos "Itens de login" ("Login Items").

1.  Abra os **Ajustes do Sistema** (**System Settings**).
2.  Vá para **Geral** (**General**) > **Itens de login** (**Login Items**).
3.  Clique no botão **+**.
4.  Selecione o seu aplicativo na pasta `/Applications`.
5.  Clique em **Abrir** (**Open**).

Agora, o aplicativo iniciará automaticamente quando você fizer login, garantindo que os recursos RAW HID do seu teclado estejam sempre disponíveis.

## 6. Atualizando o aplicativo no lado do host

Se você precisar atualizar o aplicativo no lado do host com um novo binário ou arquivo de configuração, pode fazê-lo substituindo os arquivos dentro do pacote (bundle) do aplicativo.

1.  Vá para a sua pasta `Applications`.
2.  Clique com o botão direito em `ZMK HID Runner.app` e selecione "Mostrar Conteúdo do Pacote" ("Show Package Contents").
3.  Navegue até `Contents/Resources/`.
4.  Você verá a seguinte estrutura:
    ```
    .
    ├── applet.icns
    ├── applet.rsrc
    ├── description.rtfd
    │   └── TXT.rtf
    ├── Scripts
    │   └── main.scpt
    ├── zmk-hid-host
    └── zmk-hid-host.json
    ```
5.  Você pode substituir o binário `zmk-hid-host` e o arquivo de configuração `zmk-hid-host.json` pelas suas novas versões. Certifique-se de que os novos arquivos tenham os mesmos nomes.

> [!NOTE]
> Você também pode usar o comando `cp` para substituir os arquivos. Por exemplo, se os seus novos arquivos estiverem no diretório atual, você pode usar os seguintes comandos:
> ```bash
> cp zmk-hid-host "/Applications/ZMK HID Runner.app/Contents/Resources/zmk-hid-host"
> cp zmk-hid-host.json "/Applications/ZMK HID Runner.app/Contents/Resources/zmk-hid-host.json"
> ```
> Se por algum motivo o aplicativo não funcionar depois de substituir os arquivos, verifique as permissões dos arquivos. O binário deve ter permissão de execução. Você pode defini-la com `chmod +x`.
> ```bash
> chmod +x "/Applications/ZMK HID Runner.app/Contents/Resources/zmk-hid-host"
> ```

## Autor e contribuições

O projeto original `qmk-hid-host` foi criado por **zzeneg**, e você pode encontrar o repositório aqui: [https://github.com/zzeneg/qmk-hid-host](https://github.com/zzeneg/qmk-hid-host).

As funcionalidades de **Spotify** e de **Clima** descritas neste documento foram adicionadas neste pull request: [https://github.com/zzeneg/qmk-hid-host/pull/24/files](https://github.com/zzeneg/qmk-hid-host/pull/24/files).

A funcionalidade RAW HID neste projeto é uma implementação personalizada, portada a partir do ótimo trabalho de **@zzeneg** nos seguintes repositórios:
- [zmk-raw-hid](https://github.com/zzeneg/zmk-raw-hid)
- [zmk-nice-view-hid](https://github.com/zzeneg/zmk-nice-view-hid)

Esta implementação é 100% independente e é ativada apenas com as seguintes flags, sem precisar de nenhum outro arquivo:
```
CONFIG_NICE_OLED_WIDGET_RAW_HID=y
```

# Sugestões
Se você tiver alguma sugestão de implementação ou algo parecido, abra uma
discussão

# Limitações
Embora o `nice_oled` ofereça recursos avançados, há restrições de hardware e de software a considerar.

- Uso de memória (RAM) Este shield usa a biblioteca gráfica LVGL, que pode consumir muita memória.
  *   **Alto consumo**: Habilitar vários widgets grandes (gráfico de WPM, Bongo Cat, Raw HID) pode esgotar a RAM disponível no microcontrolador (nRF52840).
  *   **Sintomas**: Se a memória estiver baixa, você pode observar artefatos no display, travamentos ou instabilidade do Bluetooth.
  *   **Mitigação**: Use as predefinições "Balanced" ou "Minimal" descritas em `OPTIMIZE.md` se encontrar problemas.
- Duração da bateria Displays OLED e animações contínuas consomem energia.
  *   **Impacto no periférico**: Executar animações complexas (como Pokemon ou Bongo Cat) na metade periférica (que tem uma bateria menor em algumas montagens) reduzirá significativamente a duração da bateria.
  *   **Taxa de atualização**: Velocidades de animação maiores (valores de ms menores) aumentam o uso de CPU, impedindo o processador de entrar em repouso.
  *   **Mitigação**: Use `CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL=y` para uma melhor duração da bateria em periféricos split.
- Compatibilidade de plataforma (Raw HID) Os recursos Raw HID dependem de um aplicativo no lado do host para enviar dados ao teclado.
  *   **Suporte universal (macOS, Linux, Windows)**: O shield `nice_oled` e seus módulos centrais de Raw HID (**volume do sistema**, **hora**, **layout**) são totalmente compatíveis com macOS, Linux e Windows.
  *   **Recursos exclusivos do macOS**: As integrações específicas para as informações da faixa do **Spotify** e para o **clima** estão atualmente otimizadas e disponíveis **somente para macOS**.
- Desempenho e latência O display roda em recursos de hardware compartilhados.
  *   **Latência de digitação**: Se a prioridade da thread do display for definida alta demais (`1` ou `2`), ela pode interromper a varredura das teclas, causando atraso perceptível na entrada durante animações pesadas.
  *   **Bateria inteligente**: A animação experimental "Smart Battery" usa recursos computacionais significativos e **não é recomendada** para builds focadas em estabilidade.
  *   **Mitigação**: Mantenha `CONFIG_ZMK_DISPLAY_DEDICATED_THREAD_PRIORITY` no padrão (`5`) ou menor (`10`).
- Estratégia de rotação de imagens Para maximizar a eficiência no nRF52840, **evita-se a rotação de imagens em tempo real**.
  *   **Pré-processamento**: Todos os assets animados são pré-rotacionados no computador host durante a fase de design.
  *   **Justificativa**: Realizar transformações geométricas (rotação) em tempo de execução é computacionalmente caro e consome muita memória nesta arquitetura.
  *   **Implementação**: Ao armazenar os assets como bitmaps pré-rotacionados e prontos para renderizar, tiramos a carga de processamento do MCU, garantindo uma reprodução fluida com sobrecarga mínima de CPU.

# Agradecimentos

Este projeto é construído sobre a base de inúmeras contribuições inovadoras da comunidade ZMK. Estendemos nossa sincera gratidão aos seguintes desenvolvedores, cujo trabalho foi fonte de inspiração e cujos drivers ou métodos foram portados ou adaptados para este módulo.

## Inspiração central e drivers

*   **@M165437**: Pelo [nice-view-gem](https://github.com/M165437/nice-view-gem), que inspirou as implementações de animação.
*   **@zzeneg**: Pelo trabalho pioneiro em [zmk-raw-hid](https://github.com/zzeneg/zmk-raw-hid) e [zmk-nice-view-hid](https://github.com/zzeneg/zmk-nice-view-hid). A funcionalidade Raw HID neste módulo é uma implementação personalizada fortemente inspirada e portada a partir do ótimo trabalho dele.
*   **@englmaxi**: Pelo [zmk-dongle-display](https://github.com/englmaxi/zmk-dongle-display.git), uma referência fundamental para o gerenciamento de display.
*   **@infely**: Pelo [nice-view-battery](https://github.com/infely/nice-view-battery).
*   **@tobiasarndt**: Pelo [zmk-config](https://github.com/tobiasarndt/zmk-config) e pela implementação do status de repouso.
*   **@infused-kim**: Pelo [Nice Peripheral View (tmp-npv)](https://github.com/infused-kim/tmp-npv).
*   **@codyd51**: Pelo [Mighty-Mitts](https://github.com/codyd51/Mighty-Mitts).
*   **@badjeff**: Pelo [zmk-hid-io](https://github.com/badjeff/zmk-hid-io).
*   **@carrefinho**: Pelo [prospector-zmk-module](https://github.com/carrefinho/prospector-zmk-module).

As suas contribuições foram fundamentais para tornar este sistema modular de shields possível. Obrigado por abrir o código do seu trabalho e impulsionar o ecossistema ZMK.

# Se você gosta das minhas contribuições, não se esqueça do seguinte:

Agradeço se você me seguir no [<img align="center" alt="GitHub" width="22px" src="https://github.com/mctechnology17/mctechnology17/blob/main/src/github.png" />][github] e no [<img align="center" alt="YouTube" width="22px" src="https://github.com/mctechnology17/mctechnology17/blob/main/src/youtube.png" />][youtube] !

![Star](./assets/star.GIF)

# Meus outros projetos:
- [zmk-dongle-display-view]: Use o seu [niceview] na vertical com widgets muito bonitos
- [zmk-oled-adapter]: Este módulo é um adaptador para telas OLED de 128x32, 128x64 e 128x128,
  para ser usado em teclados com ZMK sem precisar modificar os
  shields dos teclados.
- [qmk-config] será atualizado em breve
- [qmk_userspace] será atualizado em breve
- [vimtools] canivete suíço para o vim (recursos e configurações que vão facilitar a sua vida)
- [gm] gerenciador de git multiplataforma com interface amigável
- [vim-better-header] o melhor template automatizado
- [vim-executor] executor de código multilinguagem

Se você gosta das minhas contribuições, sinta-se à vontade para doar.
- [paypal]
- [sponsor]

<p align="right">
  <a href="#top">↑  voltar ao Sumário</a>
</p>

<p align="center">
        <img src="./assets/Bottom.svg" alt="Bottom" />
</p>

[zmk-config]: https://github.com/mctechnology17/zmk-config
[zmk-dongle-display-view]: https://github.com/mctechnology17/zmk-dongle-display-view
[zmk-oled-adapter]: https://github.com/mctechnology17/zmk-oled-adapter

[niceview]: https://nicekeyboards.com/nice-view/
[oled]: https://keycapsss.com/keyboard-parts/parts/80/0.91-oled-lcd-display-128x32-ssd1306-i2c
[nice-view]: https://nicekeyboards.com/nice-view
[puchi_ble_v1]: (https://keycapsss.com/keyboard-parts/mcu-controller/202/puchi-ble-wireless-microcontroller-pro-micro-replacement?number=KC10157_SWITCH&c=18)
[seeeduino_xiao_ble]: (https://keycapsss.com/keyboard-parts/mcu-controller/212/seeed-studio-xiao-nrf52840-rp2040-esp32c3?number=KC10167_NRF)
[nice_nano_v2]: (https://nicekeyboards.com/nice-nano)
[keymap-editor]: https://nickcoutsos.github.io/keymap-editor/
[ZMK firmware]: https://github.com/zmkfirmware/zmk/
[ZMK documentation]: https://zmk.dev/docs/user-setup
[ZMK keycodes]: https://zmk.dev/docs/codes
[ZMK Discord]: https://zmk.dev/community/discord/invite

[qmk-config]: https://github.com/mctechnology17/qmk-config
[qmk_userspace]: https://github.com/mctechnology17/qmk_userspace

[git]: (https://github.com/git-guides/install-git)

[github]: https://github.com/mctechnology17
[twitter]: https://twitter.com/mctechnology17
[youtube]: https://www.youtube.com/c/mctechnology17
[instagram]: https://www.instagram.com/mctechnology17/
[facebook]: https://m.facebook.com/mctechnology17/
[reddit]: https://www.reddit.com/user/mctechnology17

[vim-executor]: https://github.com/mctechnology17/vim-executor
[vim-better-header]: https://github.com/mctechnology17/vim-better-header
[gm]: https://github.com/mctechnology17/gm
[vimtools]: https://github.com/mctechnology17/vimtools

[jailbreakrepo]: https://mctechnology17.github.io/
[uiglitch]: https://repo.packix.com/package/com.mctechnology.uiglitch/
[uiswitches]: https://repo.packix.com/package/com.mctechnology.uiswitches/
[uibadge]: https://repo.packix.com/package/com.mctechnology.uibadge/

[youtuberepo]: https://github.com/mctechnology17/youtube_repo_mc_technology

[sponsor]: https://github.com/sponsors/mctechnology17
[paypal]: https://www.paypal.me/mctechnology17
