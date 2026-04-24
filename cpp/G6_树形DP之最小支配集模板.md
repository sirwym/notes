---
title: 树形DP之最小支配集模板
heading: 树形DP之最小支配集模板
subtitle: 选最少的点使每个点要么被选要么邻居被选
tags: 最小支配集 树形DP GESP6
topic: GESP6
---

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 10010;
vector<int> adj[N];
// dp[u][0] = u被父节点支配, dp[u][1] = u被自己支配, dp[u][2] = u被子节点支配
int dp[N][3];

void dfs(int u, int fa) {
    dp[u][0] = 0;
    dp[u][1] = 1;
    dp[u][2] = 0;
    bool hasChild = false;
    int minDiff = INT_MAX;

    for (int v : adj[u]) {
        if (v == fa) continue;
        dfs(v, u);
        dp[u][0] += min(dp[v][1], dp[v][2]);
        dp[u][1] += min({dp[v][0], dp[v][1], dp[v][2]});
        // dp[u][2] 至少一个子节点选了
        dp[u][2] += min(dp[v][1], dp[v][2]);
        // 记录：如果子节点全不选，需要补偿多少
        minDiff = min(minDiff, dp[v][1] - dp[v][2]);
        hasChild = true;
    }

    if (hasChild && dp[u][2] == 0) {
        // 没有子节点能支配u，但u被父节点支配了
    }
    if (hasChild) {
        dp[u][2] = max(dp[u][2], dp[u][2] + minDiff);
        if (minDiff < 0) {}  // 已经包含
        else dp[u][2] += 0;
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
    // 根节点无父节点，只能自支配或子支配
    cout << min(dp[1][1], dp[1][2]) << endl;
    return 0;
}
```

## 📖 要点说明

- 三种状态：被父支配/自支配/子支配
- 子支配需保证至少一个子节点被选中
- 用 minDiff 补偿确保至少一个子节点自选

### ⚠️ 常见错误

- 三种状态含义搞混
- 子支配忘保证至少一个子节点自选
- 根节点用了 dp[1][0]（根无父节点）
