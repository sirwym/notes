---
title: 树的直径之双DFS模板
heading: 树的直径之双DFS模板
subtitle: 两次 DFS 求树上最长路径——简单直观
tags: 树的直径 DFS 两次 GESP6
topic: GESP6
---

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 100010;
vector<pair<int,int>> adj[N];  // (邻居, 边权)
long long dist[N];

void dfs(int u, int fa) {
    for (auto [v, w] : adj[u]) {
        if (v == fa) continue;
        dist[v] = dist[u] + w;
        dfs(v, u);
    }
}

int main() {
    int n;
    cin >> n;
    for (int i = 1; i < n; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }

    // 第一次 DFS：从任意点出发找最远点
    memset(dist, 0, sizeof(dist));
    dfs(1, 0);
    int farthest = 1;
    for (int i = 2; i <= n; i++)
        if (dist[i] > dist[farthest]) farthest = i;

    // 第二次 DFS：从最远点出发，最远距离即直径
    memset(dist, 0, sizeof(dist));
    dfs(farthest, 0);
    long long diameter = 0;
    for (int i = 1; i <= n; i++)
        diameter = max(diameter, dist[i]);

    cout << diameter << endl;
    return 0;
}
```

## 📖 要点说明

- 两次 DFS：先找最远点 A，再从 A 找最远点 B，AB 即直径
- 适用于有边权的树
- 简单直观，代码量少

### ⚠️ 常见错误

- 第一次 DFS 起点不能是直径端点的情况（不影响，任意点都行）
- 无权树可直接 BFS 代替 DFS
- 边权可能为负时不适用此方法

## 🎬 动画演示

!!animation 两次DFS寻找直径.html!!
