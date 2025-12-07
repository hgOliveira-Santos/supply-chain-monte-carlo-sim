# Project Blueprint: Inventory Risk & Optimization Engine
> **Nome do Projeto:** supply-chain-mcs

## 1. Visão Geral
Este projeto visa resolver o problema de incerteza no planejamento de estoque. Diferente de modelos tradicionais que prevêem apenas um valor fixo de demanda, esta solução utiliza **Machine Learning** para identificar tendências e **Simulação de Monte Carlo** para modelar riscos, permitindo definir estoques de segurança baseados em probabilidades reais de ruptura (stockouts).

---

## 2. Pipeline de Dados (Inputs)

O sistema deve ingerir dados transacionais e parâmetros logísticos.

### 2.1 Schema Recomendado
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `date` | DateTime | Data da venda |
| `sku_id` | String | Identificador do produto |
| `qty_sold` | Int/Float | Variável alvo (target) |
| `lead_time` | Int | Tempo de entrega do fornecedor (dias) |

### 2.2 Feature Engineering
Antes da modelagem, gerar:
* **Time Features:** `day_of_week`, `month`, `is_holiday`.
* **Lag Features:** Vendas de $t-1$, $t-7$, $t-30$.
* **Rolling Statistics:** Média móvel e desvio padrão móvel (janelas de 7 e 30 dias).

---

## 3. Módulo 1: Forecasting (Machine Learning)
**Objetivo:** Estabelecer a *demanda base* (esperada) e quantificar o *erro do modelo*.

1.  **Modelo:** XGBoost, LightGBM ou Prophet.
2.  **Métrica de Avaliação:** RMSE (Root Mean Squared Error).
3.  **Output Crítico:**
    * Vetor de previsões ($\hat{y}$) para o horizonte de tempo $H$.
    * Desvio Padrão dos Resíduos ($\sigma_{erro}$) no conjunto de teste.
    * *Nota:* O $\sigma_{erro}$ será usado como o parâmetro de volatilidade na simulação.

---

## 4. Módulo 2: Motor de Simulação (Monte Carlo)
**Objetivo:** Simular $N$ cenários futuros para estressar a cadeia de suprimentos.

### 4.1 Definição Estocástica
A demanda diária simulada não é fixa. Ela segue a equação:

$$D_{simulado} = \hat{y}_{ML} + \epsilon$$

Onde $\epsilon$ (ruído) é amostrado de uma distribuição normal $\mathcal{N}(0, \sigma_{erro})$.

### 4.2 Algoritmo de Simulação
Para cada iteração $i$ em $1..10.000$:

1.  **Inicializar:** $Estoque_t = Estoque_{inicial}$
2.  **Loop Diário ($t$):**
    * Gerar demanda aleatória $D_t$ (baseada no ML + Ruído).
    * Gerar Lead Time aleatório $L$ (se aplicável).
    * **Balanço:** $Estoque_{final} = Estoque_{inicial} - D_t + Recebimentos$
    * **Verificação de Ruptura:** Se $Estoque_{final} < 0$, registrar falha.
    * **Reabastecimento:** Se $Estoque_{final} \le PontoPedido$, agendar entrada para $t+L$.

---

## 5. Análise de Risco e Decisão
O resultado das 10.000 simulações gera uma distribuição de probabilidades.

### 5.1 KPIs Principais
* **Stockout Probability:** $\frac{\text{Número de cenários com ruptura}}{\text{Total de cenários}}$
* **Service Level:** $1 - \text{Stockout Probability}$
* **Estoque de Segurança Recomendado:** O nível mínimo de estoque necessário para manter o *Service Level* acima da meta (ex: 95%).

---

## 6. Estrutura do Projeto e Padrões
Seguindo as diretrizes de padronização de código.

```text
inventory-risk-sim/
│
├── data/
│   ├── raw/                  # CSVs originais
│   └── processed/            # Parquets limpos
│
├── src/
│   ├── __init__.py
│   ├── etl.py                # Limpeza e Feature Eng.
│   ├── forecasting.py        # Treino e Inferência ML
│   ├── simulation.py         # Lógica Monte Carlo (Core)
│   └── utils.py              # Helpers de plotagem/stats
│
├── notebooks/                # Prototipagem e EDA
├── dashboard/                # App Streamlit (Visualização)
├── requirements.txt
└── BLUEPRINT.md              # Este arquivo