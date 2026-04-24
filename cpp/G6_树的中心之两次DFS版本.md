---
title: 树的中心之两次DFS版本
heading: 树的中心之两次DFS版本
subtitle: 两次 DFS 求直径以及在此基础上求出树的中心的逻辑，适用于大多数信息学竞赛（如 CSP-J/S, NOIP）的需求
tags: 树的中心 DFS GESP6
topic: GESP6
---

```cpp
#include <bits/stdc++.h>

using namespace std;

const int MAXN = 100005; // 根据题目要求修改最大节点数
vector<int> adj[MAXN];

int parent[MAXN];   // 存储路径，用于还原直径
int max_dist = -1 ;   // 记录全局最大距离
int farthest_node = -1;  // 记录距离起点最远的节点

int n;

// DFS 寻找最远点
void dfs(int u, int fa, int dist) {
    if (dist > max_dist){
        max_dist = dist;
        farthest_node = u;
    }
    
    parent[u] = fa;    
    for (int v : adj[u]) {
        if (v != fa) {
            // 边权为 1，如果是带权树，则换成 dist + weight
            dfs(v, u, dist + 1);
        }
    }
}

int main() {
    // 假设输入 n 和 n-1 条边
    cin >> n;
    for (int i = 0; i < n - 1; ++i) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    // --- 第一步：从 1 号点出发找直径的一个端点 s ---
    max_dist = -1;
    dfs(1, 0, 0);
    int s = farthest_node;

    // --- 第二步：从 s 出发找另一个端点 e，并记录路径 ---
    max_dist = -1;
    farthest_node = -1;
    dfs(s, 0, 0);
    int e = farthest_node;

    // 直径长度
    int diameter_len = max_dist;
    cout << "树的直径长度: " << diameter_len << endl;

    // --- 第三步：还原直径路径并寻找中心 ---
    vector<int> path;
    int curr = e;
    while (curr != 0) {
        path.push_back(curr);
        curr = parent[curr];
    }
    // path 现在存储了从 e 到 s 的所有节点

    // 寻找中心
    // 如果直径长度为 L，中心在 path[L/2] 附近
    cout << "树的中心节点: ";
    if (diameter_len % 2 == 0) {
        // 奇数个节点，一个中心
        cout << path[diameter_len / 2] << endl;
    } else {
        // 偶数个节点，两个中心
        cout << path[diameter_len / 2] << " 和 " << path[diameter_len / 2 + 1] << endl;
    }

    return 0;
}
```

## 📖 要点说明

- **适用范围**： 两次 DFS 法仅适用于边权为正的树。如果存在负边权，则需要使用树形 DP 求解。
- `parent` 数组的作用： 在第二次 DFS 时，我们记录每个节点的父亲，这样就可以从直径的终点 e 一路回溯到起点 s，从而完整地提取出直径上的所有点。
- **中心的确定**：我们将直径路径提取到 `vector<int> path` 中。
	- path 的大小是 `diameter_len + 1`。
	- 中心节点就是 path 数组中下标最接近中间的元素。
- **复杂度**： 两次 DFS 均为 $O(N)$，路径提取为 $O(N)$，总时间复杂度为线性的 $O(N)$，效率非常高。

## 🎬 动画演示

!!animation 两次DFS寻找中心.html!!

