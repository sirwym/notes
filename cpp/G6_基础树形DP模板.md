---
title: 基础树形DP模板
heading: 基础树形DP模板
subtitle: 在树上做动态规划——从叶子到根递推
tags: 树形DP 递推 DFS GESP6
topic: GESP6
---

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 10010;
vector<int> adj[N];
int dp[N];  // dp[u] = 以 u 为根的子树的结果

void dfs(int u, int fa) {
    dp[u] = 1;  // 初始值：至少包含自己
    for (int v : adj[u]) {
        if (v == fa) continue;
        dfs(v, u);
        dp[u] += dp[v];  // 累加子树结果
    }
}

// 经典：求树的重心
int sz[N], n, centroid, minBalance;

void findCentroid(int u, int fa) {
    sz[u] = 1;
    int maxSub = 0;
    for (int v : adj[u]) {
        if (v == fa) continue;
        findCentroid(v, u);
        sz[u] += sz[v];
        maxSub = max(maxSub, sz[v]);
    }
    maxSub = max(maxSub, n - sz[u]);  // 父节点方向的子树
    if (maxSub < minBalance) {
        minBalance = maxSub;
        centroid = u;
    }
}

int main() {
    cin >> n;
    for (int i = 1; i < n; i++) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    minBalance = n;
    findCentroid(1, 0);
    cout << centroid << " " << minBalance << endl;
    return 0;
}
```

## 📖 要点说明

- 树形 DP 核心：DFS 后序遍历，先算子树再算当前
- dp[u] 依赖所有子节点 dp[v] 的结果
- 树的重心：删去后最大连通块最小的节点

### ⚠️ 常见错误

- DFS 忘跳过父节点导致死循环
- dp 初始值设错
- 求重心忘算父节点方向的子树大小
