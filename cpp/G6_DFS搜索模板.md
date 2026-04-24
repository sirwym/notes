---
title: DFS搜索模板
heading: DFS搜索模板
subtitle: 深度优先搜索——一条路走到底再回溯
tags: DFS 深度优先 回溯 搜索 GESP6
topic: GESP6
---

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 25;
bool vis[N];
vector<int> path;

// 全排列 DFS
void dfs_perm(int n, int depth) {
    if (depth == n) {
        for (int x : path) cout << x << " ";
        cout << endl;
        return;
    }
    for (int i = 1; i <= n; i++) {
        if (vis[i]) continue;
        vis[i] = true;
        path.push_back(i);
        dfs_perm(n, depth + 1);
        path.pop_back();   // 回溯
        vis[i] = false;
    }
}

// 组合 DFS：从 n 个中选 k 个
void dfs_comb(int n, int k, int start) {
    if (path.size() == k) {
        for (int x : path) cout << x << " ";
        cout << endl;
        return;
    }
    for (int i = start; i <= n; i++) {
        path.push_back(i);
        dfs_comb(n, k, i + 1);
        path.pop_back();
    }
}

int main() {
    dfs_perm(3, 0);     // 1~3 的全排列
    dfs_comb(4, 2, 1);  // C(4,2) 组合
    return 0;
}
```

## 📖 要点说明

- DFS 三步：选一个方向→走到底→回溯
- 全排列：每个位置试遍所有未用数字
- 组合：从 start 开始选，避免重复（如 12 和 21）

### ⚠️ 常见错误

- 回溯忘撤销选择（pop_back / vis=false）
- 组合忘传 start 导致重复
- DFS 栈溢出（递归太深）
