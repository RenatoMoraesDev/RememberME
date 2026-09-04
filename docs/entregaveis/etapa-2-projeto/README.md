# Etapa 2 — Arquitetura, Tecnologias e Planeamento

> Atividade do ciclo de vida: **projeto** (*design*). A análise está na Etapa 1; a
> implementação começa na Etapa 3.

**Entrega:** 04/09/2026

O enunciado lista sete itens no entregável. Onde está cada um:

| # | Item exigido | Onde está |
|:---:|---|---|
| 1 | Tecnologias escolhidas | [`stack.md`](stack.md) |
| 2 | Justificação das tecnologias | [`stack.md`](stack.md) — um motivo por escolha |
| 3 | Arquitetura da solução | [`01-arquitetura.d2`](01-arquitetura.d2) · [diagrama](diagrama_atividades.png) |
| 3 | Ciclo de vida do processo | [`03-ciclo-de-vida.d2`](03-ciclo-de-vida.d2) · [diagrama](diagrama_ciclo_de_vida.svg) |
| 4 | Estrutura prevista do projeto | [`plano-desenvolvimento.md`](plano-desenvolvimento.md) § 2 |
| 5 | Distribuição de responsabilidades | [`plano-desenvolvimento.md`](plano-desenvolvimento.md) § 4 · [`02-responsabilidades.d2`](02-responsabilidades.d2) |
| 6 | Lista de tarefas | [`docs/tasks.md`](../../tasks.md) — ver nota abaixo |
| 7 | Plano de desenvolvimento | [`plano-desenvolvimento.md`](plano-desenvolvimento.md) §§ 7 e 9 |

## Nota sobre os itens 6 e 7

O enunciado separa "lista de tarefas" e "plano de desenvolvimento" no entregável, mas
descreve apenas o primeiro, em "Planeamento do trabalho". A leitura adotada:

- **Item 6, lista de tarefas:** *o quê* e *quem*, com os cinco campos exigidos.
- **Item 7, plano de desenvolvimento:** *em que ordem*, *o que bloqueia o quê* e *até onde* — a sequência de fases com critério de conclusão, os milestones e o alinhamento com as Etapas 3 a 5.

## Nota sobre a localização do `tasks.md`

O quadro é atualizado a cada tarefa concluída. Guardá-lo nesta pasta congelava-o na
data da entrega e tornava-o inútil para o trabalho seguinte — e o enunciado pede
precisamente que permita "conhecer o atual estado do projeto entre expectativas e
realizações". Fica em `docs/tasks.md`, vivo; o estado nesta data está preservado pela
etiqueta `etapa-2`.

## Diagramas

Os `.d2` são a fonte; as imagens são geradas a partir deles e não se editam à mão:

```bash
d2 03-ciclo-de-vida.d2 diagrama_ciclo_de_vida.svg
```

| Ficheiro | O que mostra |
|---|---|
| `01-arquitetura.d2` | Os blocos da aplicação e como se ligam |
| `02-responsabilidades.d2` | Quem é dono de cada bloco |
| `03-ciclo-de-vida.d2` | Estados do processo residente: arranque, instância única e paragem (decisão D7) |
