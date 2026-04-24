---
title: 树的中心之树形DP版本
heading: 树的中心之树形DP版本
subtitle: 树形 DP 求树的中心，本质是换根 DP（Rerooting DP） 的经典应用，目标是求出每个节点的离心率（该节点到树中最远节点的距离），然后取最小的那个。
tags: 树的中心 树形DP 换根DP GESP6
topic: GESP6
---

```cpp
#include <bits/stdc++.h>

using namespace std;

const int MAXN = 100005;
struct Edge {
    int v, w;
};
vector<Edge> adj[MAXN];
int d1[MAXN], d2[MAXN], p1[MAXN], up[MAXN];
int n;

// 第一遍 DFS：自底向上更新 d1 (最远) 和 d2 (次远)
void dfs_down(int u, int fa) {
    d1[u] = d2[u] = 0;
    p1[u] = 0; // 记录 d1 是从哪个儿子传上来的
    for (auto &edge : adj[u]) {
        int v = edge.v, w = edge.w;
        if (v == fa) continue;
        dfs_down(v, u);
        
        if (d1[v] + w > d1[u]) {
            d2[u] = d1[u];
            d1[u] = d1[v] + w;
            p1[u] = v;
        } else if (d1[v] + w > d2[u]) {
            d2[u] = d1[v] + w;
        }
    }
}

// 第二遍 DFS：自顶向下更新 up (换根)
void dfs_up(int u, int fa) {
    for (auto &edge : adj[u]) {
        int v = edge.v, w = edge.w;
        if (v == fa) continue;
        
        // 如果 v 在 u 的最远路径上，则 v 向上走只能选 u 的次远距离或 u 自己的 up
        if (p1[u] == v) {
            up[v] = max(up[u], d2[u]) + w;
        } else {
            // 否则，v 向上走可以选 u 的最远距离或 u 自己的 up
            up[v] = max(up[u], d1[u]) + w;
        }
        dfs_up(v, u);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    cin >> n;
    for (int i = 0; i < n - 1; ++i) {
        int u, v, w = 1; // 默认边权为 1，题目有权值则读入 w
        cin >> u >> v;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }

    dfs_down(1, 0);
    dfs_up(1, 0);

    int min_max_dist = 2e9; // 存储半径
    vector<int> centers;

    for (int i = 1; i <= n; ++i) {
        int max_dist = max(d1[i], up[i]); // 每个点到所有点的最远距离
        if (max_dist < min_max_dist) {
            min_max_dist = max_dist;
            centers.clear();
            centers.push_back(i);
        } else if (max_dist == min_max_dist) {
            centers.push_back(i);
        }
    }

    cout << "树的中心节点: ";
    for (int c : centers) cout << c << " ";
    cout << "\n最小化的最远距离 (半径): " << min_max_dist << endl;

    return 0;
}
```


## 算法核心逻辑
我们需要维护三个核心状态：

1. **$d1[u]$**：以 $u$ 为根的子树中，$u$ 向下走的最远距离。
2. **$d2[u]$**：以 $u$ 为根的子树中，$u$ 向下走的**次远**距离（要求与最远路径不在同一条分支上）。
3. **$up[u]$**：从 $u$ 向上走，经过父节点 $fa$ 后能到达的最远距离。


## 📖 要点说明

1. **为什么需要次远距离 $d2$？**
    当我们在第二遍 DFS 更新儿子 $v$ 的 $up[v]$ 时，如果 $v$ 恰好在父节点 $u$ 的最远路径上（即 $p1[u] == v$），我们就不能用 $d1[u]$ 来更新它，否则就会走回头路。此时必须退而求其次，使用 $d2[u]$。

2. **$p1[u]$ 数组的作用：**
    记录 $u$ 的最远距离是从哪一个子节点传上来的，这是换根 DP 判定路径重合的关键。

3. **优势：**
    - **处理边权：** 该代码原生支持边权（修改 `w` 即可）。
    - **全图信息：** `max(d1[i], up[i])` 给出了树中**每一个点**到其余点的最远距离。这在处理类似“求所有点的离心率”或“多个选址问题”时非常高效。

4. **复杂度：**
    同样是两次 DFS，时间复杂度 $O(N)$。

## 🎬 动画演示

!!animation 树形DP寻找中心.html!!