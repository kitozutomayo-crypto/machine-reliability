# Machine Reliability and Maintenance Optimization

[English Version](README.md)

## 概要

本プロジェクトでは、機械設備の劣化・故障を対象として、信頼性分析、Continuous-Time Markov Chain（CTMC）、最適化、Monte Carlo Simulationを組み合わせた保全意思決定モデルを構築しました。

主な目的は、次の問いに答えることです。

> **機械の劣化が確率的に進行する状況で、長期平均コストを最小化するためには、どの程度の間隔で点検・保全を行うべきか。**

最初に Weibull 分布を用いて故障特性を分析し、その後、年齢ベースの予防保全モデル、CTMC による状態劣化モデル、点検間隔の最適化、感度分析、Monte Carlo Simulationによる検証へと段階的に発展させています。

---

## プロジェクト全体の流れ

```text
Failure Data
    ↓
Weibull Reliability Model
    ↓
Age-Based Maintenance Optimization
    ↓
Intermediate Inspection Prototype
    ↓
CTMC Degradation Model
    ↓
Inspection Policy Optimization
    ↓
Sensitivity Analysis
    ↓
Monte Carlo Validation
```

---

## 1. Weibull Reliability Analysis

機械の故障時間を Weibull 分布でモデル化しました。

推定したパラメータは以下の通りです。

```text
Shape parameter β = 1.9267
Scale parameter η = 474.2850 hours
```

β > 1 であるため、時間の経過とともに hazard rate が上昇する wear-out 型の故障傾向が確認できます。

Reliability function は次式で表されます。

```text
R(t) = exp(-(t / η)^β)
```

Hazard rate は次式です。

```text
h(t) = (β / η) × (t / η)^(β - 1)
```

この Weibull モデルを、後続の保全最適化における故障確率モデルとして利用しました。

---

## 2. Age-Based Preventive Maintenance Optimization

最初の保全モデルでは、機械が故障する前に一定時間 `T` で予防交換を行う age-based maintenance policy を考えます。

このモデルでは、

* 早すぎる交換による予防保全コスト
* 遅すぎる交換による故障コスト

のトレードオフを評価します。

長期平均コスト率は以下で定義します。

```text
C(T) =
[ C_p R(T) + C_f (1 - R(T)) ]
/
[ ∫_0^T R(t) dt ]
```

ここで、

```text
C_p = preventive maintenance cost
C_f = corrective maintenance cost
R(t) = reliability function
```

です。

分母は1サイクルあたりの期待稼働時間を表します。

```text
E[min(X, T)] = ∫_0^T R(t) dt
```

したがって、最適化問題は以下になります。

```text
T* = arg min C(T)
         T > 0
```

コスト条件を、

```text
Preventive maintenance cost = 100
Failure cost = 1000
```

とした場合、以下の結果が得られました。

```text
Optimal preventive maintenance time = 159.43 hours
Minimum expected cost rate = 1.3312 per hour
```

### Maintenance Cost Optimization

![Maintenance Cost Optimization](figures/maintenance_cost_optimization.png)

この結果から、予防保全時期を経験則だけで決めるのではなく、長期平均コストを目的関数とした連続最適化問題として扱えることが分かります。

---

## 3. Intermediate Inspection Prototype

CTMC を導入する前に、Weibull hazard rate が一定の閾値を超えた時点を「劣化状態」とみなす点検モデルを試作しました。

しかし、このモデルでは劣化状態が機械の年齢だけで決まるため、最適化すると点検間隔と交換間隔がほぼ同じ値になりました。

これは、

> **機械の状態が年齢だけで決まる場合、点検によって新たに得られる情報がほとんどない**

ことを示しています。

この結果を踏まえ、同じ稼働時間でも異なる劣化状態を取り得る確率的モデルとして CTMC を導入しました。

---

## 4. CTMC Degradation Model

機械の劣化状態を以下の4状態で表現しました。

```text
Healthy
   ↓
Degraded
   ↓
Critical
   ↓
Failed
```

状態遷移率は以下の値を使用しています。

```text
λ01 = 0.002
λ12 = 0.004
λ23 = 0.008
```

Generator matrix `Q` は以下のように定義します。

```text
Q =
[ -λ01   λ01      0       0   ]
[   0   -λ12    λ12       0   ]
[   0     0    -λ23     λ23  ]
[   0     0      0        0   ]
```

時刻 `t` における transition probability matrix は、

```text
P(t) = exp(Qt)
```

によって求めます。

Age-based model と異なり、CTMC では同じ稼働時間の機械でも Healthy、Degraded、Critical など異なる状態を取る可能性があります。

そのため、点検によって実際の状態を確認することに意味が生まれます。

### State Probabilities

![Markov State Probabilities](figures/markov_state_probabilities.png)

---

## 5. CTMC Inspection and Maintenance Policy

CTMC モデル上で、一定間隔 `T` ごとに点検を行う保全方針を設定しました。

点検時のルールは以下の通りです。

```text
Healthy   → 運転継続
Degraded  → 運転継続
Critical  → 予防交換
Failed    → 故障交換
```

状態確率は、

```text
p(t) = p(0) exp(Qt)
```

によって推移します。

点検間隔 `T` が短い場合は Critical 状態を早期に発見しやすくなりますが、点検コストが増加します。

一方、点検間隔が長い場合は点検コストを抑えられる一方で、故障に至るリスクが高くなります。

長期平均コスト率を、

```text
J(T) =
Expected cost per maintenance cycle
/
Expected cycle length
```

と定義しました。

期待コストには以下を含めています。

```text
inspection cost
+ preventive replacement cost
+ corrective failure cost
```

最適化問題は、

```text
T* = arg min J(T)
         T > 0
```

となります。

以下のコスト条件を設定しました。

```text
Inspection cost = 20
Preventive replacement cost = 100
Failure cost = 1000
```

最適化の結果、

```text
Optimal inspection interval = 85.64 hours
Minimum expected cost rate = 0.6732 per hour
```

となりました。

### CTMC Inspection Optimization

![CTMC Inspection Optimization](figures/ctmc_inspection_optimization.png)

この結果は、点検コストと故障リスクのバランスによって最適な点検間隔が決定されることを示しています。

---

## 6. Sensitivity Analysis

最適点検間隔がコスト条件によってどのように変化するかを確認するため、感度分析を行いました。

### Failure Cost

```text
Failure cost = 300
Optimal inspection interval = 381.73 hours

Failure cost = 500
Optimal inspection interval = 161.37 hours

Failure cost = 1000
Optimal inspection interval = 85.64 hours

Failure cost = 2000
Optimal inspection interval = 53.03 hours
```

Failure cost が高くなるほど、より頻繁な点検が経済的に合理的になります。

### Failure Cost Sensitivity

![Failure Cost Sensitivity](figures/failure_cost_sensitivity.png)

### Inspection Cost

Inspection cost を高くすると、最適点検間隔は長くなる傾向が確認されました。

つまり、

```text
Failure cost ↑
→ 点検頻度 ↑

Inspection cost ↑
→ 点検頻度 ↓
```

というトレードオフが存在します。

### Inspection Cost Sensitivity

![Inspection Cost Sensitivity](figures/inspection_cost_sensitivity.png)

---

## 7. Monte Carlo Validation

理論モデルの妥当性を確認するため、Monte Carlo Simulation を実装しました。

各機械について、

```text
Healthy → Degraded → Critical → Failed
```

の状態遷移時間を exponential distribution に基づいてランダムに生成し、理論モデルと同じ点検・保全ルールを適用しました。

最適点検間隔、

```text
Inspection interval = 85.64 hours
```

に対して、

```text
Theoretical cost rate = 0.6732 per hour
Monte Carlo cost rate = 0.6741 per hour
```

という結果が得られました。

両者の差は約 0.13% であり、CTMC に基づく理論計算と Monte Carlo Simulation が高い精度で一致していることを確認しました。

---

## 8. Policy Comparison

複数の点検間隔について、理論値と Monte Carlo Simulation の結果を比較しました。

```text
T = 50.00 h
Theoretical = 0.7315
Monte Carlo = 0.7287

T = 85.64 h
Theoretical = 0.6732
Monte Carlo = 0.6741

T = 150.00 h
Theoretical = 0.7203
Monte Carlo = 0.7210

T = 250.00 h
Theoretical = 0.8173
Monte Carlo = 0.8216
```

最適化によって得られた約 85.64 時間の点検方針が、比較した中で最も低い長期平均コストを示しました。

また、各点検間隔において理論値と Simulation の結果が近いことも確認できます。

### Maintenance Policy Comparison

![Maintenance Policy Comparison](figures/policy_comparison.png)

---

## 主な結果

本プロジェクトで得られた主な結果は以下の通りです。

1. Weibull 分析から、機械の故障リスクが稼働時間とともに増加する wear-out 型の傾向を確認しました。

2. Age-based maintenance により、予防交換時期を長期平均コストの最小化問題として定式化しました。

3. CTMC を導入することで、機械の劣化状態を確率的に表現しました。

4. 同じ稼働時間でも異なる状態を取り得るため、点検による状態観測に価値が生まれることを示しました。

5. 現在のコスト条件では、最適点検間隔は約 85.6 時間となりました。

6. Failure cost が高いほど点検頻度を高くする方が合理的であることを確認しました。

7. Inspection cost が高いほど点検頻度を下げる方が合理的であることを確認しました。

8. Monte Carlo Simulation により、理論 CTMC モデルの結果を数値的に検証しました。

---

## Project Structure

```text
machine-reliability/
│
├── data/
│   └── failure_data.csv
│
├── figures/
│   ├── maintenance_cost_optimization.png
│   ├── markov_state_probabilities.png
│   ├── ctmc_inspection_optimization.png
│   ├── failure_cost_sensitivity.png
│   ├── inspection_cost_sensitivity.png
│   └── policy_comparison.png
│
├── src/
│   ├── __init__.py
│   ├── simulate_data.py
│   ├── weibull.py
│   ├── fit_weibull.py
│   ├── reliability.py
│   ├── maintenance.py
│   ├── inspection_optimization.py
│   ├── markov_model.py
│   ├── markov_maintenance.py
│   ├── monte_carlo_validation.py
│   └── model_api.py
│
├── notebooks/
├── tests/
├── README.md
├── README_JP.md
├── requirements.txt
└── .gitignore
```

---

## 使用技術・手法

* Python
* NumPy
* SciPy
* Matplotlib
* Weibull Reliability Analysis
* Continuous-Time Markov Chain
* Numerical Optimization
* Monte Carlo Simulation

---

## 現在のモデルにおける主な仮定

本モデルでは、分析しやすさと解釈性を重視し、以下の仮定を置いています。

* 劣化状態は `Healthy → Degraded → Critical → Failed` の順に遷移する
* 各状態の transition rate は一定
* 点検によって現在の状態を完全に観測できる
* 予防交換後は Healthy 状態に戻る
* 故障交換後も Healthy 状態に戻る
* 点検費用、予防交換費用、故障費用は固定

---

## 今後の拡張

今後は以下の拡張が考えられます。

* 実際の condition-monitoring data から CTMC transition rate を推定
* Imperfect inspection の導入
* 複数の maintenance action
* Downtime cost の導入
* Repairable system への拡張
* State-dependent maintenance decision
* Markov Decision Process
* Dynamic Programming
* Multi-machine maintenance scheduling
* Stochastic Optimization

---

## まとめ

本プロジェクトでは、故障確率を推定するだけでなく、

**Reliability Analysis → Stochastic Modeling → Optimization → Simulation**

という流れで、機械保全の意思決定問題をモデル化しました。

特に CTMC を用いて劣化状態を確率的に表現し、その状態情報を基に点検間隔を最適化することで、単純な年齢ベース保全から condition-based maintenance へとモデルを発展させました。

最終的に得られた最適点検方針について、Monte Carlo Simulation により理論値と近い結果が得られることも確認しました。
