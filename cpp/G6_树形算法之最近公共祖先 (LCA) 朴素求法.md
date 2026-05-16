---
title: 树形算法之最近公共祖先 (LCA) 朴素求法
heading: 树形算法之最近公共祖先 (LCA) 朴素求法
subtitle: 一步一步往上爬的直觉解法（暴力法）
tags: 最近公共祖先 LCA 朴素算法 暴力求解 树 CSP-J
topic: GESP6
---

```cpp
#include <bits/stdc++.h>


using namespace std;

const int MAXN = 500005;
int depth[MAXN];     // 记录每个节点的深度（楼层）
int pa[MAXN];     // 记录每个节点的直接父节点 (不需要倍增数组了)
vector<int> tree[MAXN]; 

// DFS 预处理：只计算深度和直接父节点
void dfs(int u, int fa) {
    depth[u] = depth[fa] + 1; // 楼层 = 父亲楼层 + 1
    pa[u] = fa;               // 记录直接老爸是谁
    
    // 遍历所有子节点
    for (int v : tree[u]) {
        if (v != fa) {
            dfs(v, u);
        }
    }
}

// 求解 x 和 y 的 LCA (朴素法：一步步爬楼梯)
int lca_naive(int x, int y) {
    // 1. 深度对齐：让比较深的节点（楼层低的）先往上爬
    // 确保 x 始终是更深的那个
    if (depth[x] < depth[y]) {
        swap(x, y); 
    }
    
    // x 一步一步往上爬，直到和 y 在同一层
    while (depth[x] > depth[y]) {
        x = pa[x];
    }
    
    // 如果对齐高度后，俩人已经在同一个位置了，那这就是 LCA
    if (x == y) return x;
    
    // 2. 手拉手一起走：两人一起一步一步往上爬，直到相遇
    while (x != y) {
        x = pa[x];
        y = pa[y];
    }
    
    // 相遇的地方就是最近公共祖先
    return x; 
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, m, root;
    cin >> n >> m >> root;
    
    // 建树
    for (int i = 1; i < n; ++i) {
        int u, v;
        cin >> u >> v;
        tree[u].push_back(v);
        tree[v].push_back(u);
    }
    
    // 预处理
    dfs(root, 0);
    
    // 处理查询
    for (int i = 0; i < m; ++i) {
        int a, b;
        cin >> a >> b;
        cout << lca_naive(a, b) << '\n';
    }
    
    return 0;
}

```

## 📖 要点说明

* **核心思想**：完全模拟人类找族谱的直觉。先让辈分小（层数深）的往上找，等到两人辈分一样了，再一起往上找长辈。
* **时间复杂度**：
* 预处理 (DFS)：$O(N)$
* 单次查询：最坏情况要从树底走到树根，走 $N$ 步，时间复杂度 $O(N)$。如果有 $M$ 次查询，总复杂度是 $O(NM)$。


* **适用场景**：逻辑非常清晰，完全正确。在 CSP-J 比赛中，如果数据范围很小（比如 $N, M \le 1000$），可以直接用这种方法拿部分分。

### ⚠️ 常见错误

* **不对齐高度直接爬**：忘记第一步“深度对齐”，直接让两人一起往上走，会导致永远错过交汇点。
* **TLE（超时）误解**：如果在洛谷模板题（数据量 $5 \times 10^5$）提交这段代码会看到满屏的 TLE（Time Limit Exceeded）。告诉自己这不是写错了，只是因为走得太慢了，需要升级成“跳远神功（倍增法）”。
