---
title: 树形DP之最小点覆盖模板
heading: 树形DP之最小点覆盖模板
subtitle: 选最少的点覆盖所有边
tags: 最小点覆盖 树形DP GESP6
topic: GESP6
---

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 10010;
vector<int> adj[N];
// dp[u][0] = 不选u的最小覆盖, dp[u][1] = 选u的最小覆盖
int dp[N][2];

void dfs(int u, int fa) {
    dp[u][0] = 0;
    dp[u][1] = 1;  // 选u则覆盖数+1
    for (int v : adj[u]) {
        if (v == fa) continue;
        dfs(v, u);
        dp[u][0] += dp[v][1];                  // 不选u，子节点必须选（覆盖u-v边）
        dp[u][1] += min(dp[v][0], dp[v][1]);    // 选u，子节点可选可不选
    }
}

int main() {
    int n;
    cin >> n;
    for (int i = 1; i < n; i++) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    dfs(1, 0);
    cout << min(dp[1][0], dp[1][1]) << endl;
    return 0;
}
```

## 📖 要点说明

- 不选 u：子节点必须选，否则 u-v 边无覆盖
- 选 u：子节点可选可不选，取 min
- 与最大独立集的区别：0/1 状态的转移逻辑不同

### ⚠️ 常见错误

- 不选u时子节点也不选（u-v边没覆盖）
- 与最大独立集的转移搞混
- 初始值 dp[u][1] = 1 不是 0
