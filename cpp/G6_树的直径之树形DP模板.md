---
title: 树的直径之树形DP模板
heading: 树的直径之树形DP模板
subtitle: 一次 DFS 求直径——维护最长链和次长链
tags: 树的直径 树形DP 最长链 GESP6
topic: GESP6
---

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 100010;
vector<pair<int,int>> adj[N];
long long diameter = 0;

// 返回从 u 向下的最长链
long long dfs(int u, int fa) {
    long long maxLen = 0;  // 最长链
    for (auto [v, w] : adj[u]) {
        if (v == fa) continue;
        long long childLen = dfs(v, u) + w;
        // 经过 u 的最长路径 = 最长链 + 次长链
        diameter = max(diameter, maxLen + childLen);
        maxLen = max(maxLen, childLen);
    }
    return maxLen;
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

    dfs(1, 0);
    cout << diameter << endl;
    return 0;
}
```

## 📖 要点说明

- 维护最长链和次长链：`diameter = max(maxLen + childLen)`
- 只需一次 DFS，更高效
- 边权可为负（但需额外处理）

### ⚠️ 常见错误

- 忘更新 diameter（只返回了最长链）
- 最长链和次长链来自同一个子节点
- diameter 初始值设为0而非负无穷（负边权时）
