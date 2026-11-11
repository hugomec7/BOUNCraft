# BOUNCraft

Bounce and overshoot for [EffectCraft](https://github.com/storytold/effectcraft) in one click.

Select a layer, pick **Position**, **Scale** or **Rotation** (or **Selected** for any property you
selected, including the Transform effect's), choose **Overshoot** or **Bounce Back**, and press
**Bounce It**. BOUNCraft adds the expression and the controls to tweak it.

*[Português abaixo](#português)*

## Install

1. Download `BOUNCraft.jsx` from the [latest release](../../releases/latest).
2. In EffectCraft: **File ▸ Scripts ▸ Install ScriptUI Panel…** and pick `BOUNCraft.jsx`.
3. Open it from the bottom of the **Window** menu (**Window ▸ BOUNCraft.jsx**). It docks like any panel.

To try it without installing: **File ▸ Scripts ▸ Run Script File…** opens it as a floating window.

## Use

1. Animate the property with at least two keyframes (for example Scale from 0 to 100).
2. Select the layer (or, for **Selected**, the property itself in the timeline).
3. Pick the property and the type, then **Bounce It**.

The motion starts at the last keyframe and keeps the speed the property had when it got there.

### Overshoot (swings like a pendulum)

| Control | Default | What it does |
|---|---|---|
| Overshoot - Amplitude | 50 | How far it swings past the keyframe. |
| Overshoot - Frequency | 2 | Swings per second. |
| Overshoot - Decay | 4 | How fast it settles. Higher stops sooner. |
| Overshoot - Floor | off | Swings only to one side, as if it hits a floor. |

### Bounce Back (bounces like a ball on the floor)

| Control | Default | What it does |
|---|---|---|
| Bounce - Elasticity | 50 | How bouncy it is. |
| Bounce - Gravity | 50 | How hard it's pulled back. Lower gives bigger, slower bounces. |
| Bounce - Max Bounces | 10 | Stops after this many bounces. |

Bounce Back is subtle with the defaults on fast moves: lower Gravity or raise Elasticity to see more.

### Good to know

- Applying to more properties of the same layer shares one set of controls.
- Switching a property from Overshoot to Bounce Back (or back) removes the old controls once
  nothing uses them.
- Each apply is one undo step.
- Messages show at the bottom of the panel.

## Feedback

Found a bug or have an idea? Open an [issue](../../issues).

## Credits

- Made by **Hugo Mec** — [@hugoeditor_](https://x.com/hugoeditor_)
- The bounce maths follow Dan Ebberts' inertial bounce and bounce-back expressions
  ([motionscript.com](https://www.motionscript.com)).
- Inspired by the BOUNCr script by pixelbot. BOUNCraft is a new script written from scratch; it
  shares no code with BOUNCr.

License: [MIT](LICENSE)

---

## Português

Bounce e overshoot no [EffectCraft](https://github.com/storytold/effectcraft) com um clique.

Selecione uma layer, escolha **Position**, **Scale** ou **Rotation** (ou **Selected** para qualquer
propriedade selecionada, inclusive as do efeito Transform), escolha **Overshoot** ou **Bounce Back** e
clique em **Bounce It**. O BOUNCraft coloca a expressão e os controles para ajustar.

### Instalar

1. Baixe o `BOUNCraft.jsx` na [última versão](../../releases/latest).
2. No EffectCraft: **File ▸ Scripts ▸ Install ScriptUI Panel…** e escolha o `BOUNCraft.jsx`.
3. Abra pelo fim do menu **Window** (**Window ▸ BOUNCraft.jsx**). Ele encaixa como qualquer painel.

Para testar sem instalar: **File ▸ Scripts ▸ Run Script File…** abre como janela solta.

### Usar

1. Anime a propriedade com pelo menos dois keyframes (por exemplo Scale de 0 a 100).
2. Selecione a layer (ou, no modo **Selected**, a propriedade na timeline).
3. Escolha a propriedade e o tipo e clique em **Bounce It**.

O movimento começa no último keyframe e continua com a velocidade que a propriedade tinha ao chegar nele.

**Overshoot** (balança como pêndulo): Amplitude (quanto passa do keyframe), Frequency (balanços por
segundo), Decay (quanto mais alto, mais rápido para) e Floor (balança só para um lado, como se batesse
no chão).

**Bounce Back** (quica como bola): Elasticity (quanto quica), Gravity (quanto puxa de volta; mais
baixo dá quiques maiores) e Max Bounces (para depois desse número de quiques). Com os valores padrão o
quique é sutil em movimentos rápidos: diminua o Gravity ou aumente o Elasticity.

- Várias propriedades da mesma layer usam os mesmos controles.
- Trocar de Overshoot para Bounce Back remove os controles antigos quando nada mais usa eles.
- Cada aplicação é um passo de desfazer (Ctrl+Z).
- As mensagens aparecem no rodapé do painel.

### Feedback

Achou um bug ou tem uma ideia? Abra uma [issue](../../issues).

### Créditos

- Feito por **Hugo Mec** — [@hugoeditor_](https://x.com/hugoeditor_)
- As contas do bounce seguem as expressões de inertial bounce e bounce-back do Dan Ebberts
  ([motionscript.com](https://www.motionscript.com)).
- Inspirado no script BOUNCr, do pixelbot. O BOUNCraft é um script novo, escrito do zero, sem código
  do BOUNCr.

Licença: [MIT](LICENSE)
