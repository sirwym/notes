---
title: 树形DP之最大独立集模板
heading: 树形DP之最大独立集模板
subtitle: 选不相邻的节点使权值和最大
tags: 最大独立集 树形DP GESP6
topic: GESP6
---

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 10010;
vector<int> adj[N];
// dp[u][0] = 不选u的最大值, dp[u][1] = 选u的最大值
int dp[N][2];
int val[N];  // 节点权值

void dfs(int u, int fa) {
    dp[u][0] = 0;
    dp[u][1] = val[u];  // 选u则加上u的权值
    for (int v : adj[u]) {
        if (v == fa) continue;
        dfs(v, u);
        dp[u][0] += max(dp[v][0], dp[v][1]);  // 不选u，子节点可选可不选
        dp[u][1] += dp[v][0];                  // 选u，子节点必须不选
    }
}

int main() {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> val[i];
    for (int i = 1; i < n; i++) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    dfs(1, 0);
    cout << max(dp[1][0], dp[1][1]) << endl;
    return 0;
}
```

## 📖 要点说明

- `dp[u][0]` = 不选 u，`dp[u][1]` = 选 u
- 不选 u：子节点可选可不选，取 max
- 选 u：子节点必须不选

### ⚠️ 常见错误

- 选u时子节点也选了（应该是 dp[v][0]）
- 根节点答案忘取 max(dp[1][0], dp[1][1])
- dp 初始化错误
