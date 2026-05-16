---
title: 树上倍增之最近公共祖先 (LCA) 模板
heading: 树上倍增之最近公共祖先 (LCA) 模板
subtitle: 利用二进制拆分思想在 O(log N) 时间内求树上两点的最近公共祖先
tags: 最近公共祖先 LCA 倍增算法 树 CSP-J
topic: GESP6
---

```cpp
#include <iostream>
#include <vector>
#include <algorithm> // 必带：为 std::swap 提供支持

using namespace std;

const int MAXN = 500005;
int depth[MAXN];     // 记录每个节点的深度（楼层）
int pa[MAXN][22];    // fa[x][i] 表示节点 x 往上跳 2^i 步到达的祖先
vector<int> tree[MAXN]; 

// DFS 预处理：计算每个节点的深度，并预处理倍增数组
void dfs(int u, int fa) {
    depth[u] = depth[fa] + 1; // 当前节点的深度是父节点 + 1
    pa[u][0] = fa;            // 往上跳 2^0 = 1 步就是父节点
    
    // 预处理倍增数组 (核心状态转移)
    for (int i = 1; (1 << i) <= depth[u]; ++i) {
        pa[u][i] = pa[pa[u][i - 1]][i - 1]; // 先跳一半，再跳一半
    }
    
    // 遍历所有子节点进行深搜
    for (int v : tree[u]) {
        if ( v != fa) {
            dfs(v, u);
        }
    }
}

// 求解 x 和 y 的 LCA
int lca(int x, int y) {
    // 始终让 x 成为深度较深（楼层较低）的那个节点
    if (depth[x] < depth[y]) {
        swap(x, y); 
    }
    
    // 1. 深度对齐：让 x 向上跳，直到和 y 处于同一层
    for (int i = 20; i >= 0; --i) {
        if (depth[pa[x][i]] >= depth[y]) {
            x = pa[x][i];
        }
    }
    
    // 如果对齐后就在同一个节点了，那 y 本身就是 LCA
    if (x == y) return x;
    
    // 2. 齐头并进：两人一起向上跳，寻找 LCA 的下一层
    for (int i = 20; i >= 0; --i) {
        // 如果跳上去不相等，说明还没到公共祖先，放心跳
        if (pa[x][i] != pa[y][i]) {
            x = pa[x][i];
            y = pa[y][i];
        }
    }
    
    // 最后 x 的父亲就是 LCA
    return pa[x][0]; 
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
    
    // 从根节点开始预处理
    dfs(root, 0);
    
    // 处理查询
    for (int i = 0; i < m; ++i) {
        int a, b;
        cin >> a >> b;
        cout << lca(a, b) << '\n';
    }
    
    return 0;
}

```

## 📖 要点说明

* **核心思想**：利用二进制拆分将 $O(N)$ 的“一步步爬树”优化为 $O(\log N)$ 的“跳远神功”。
* **预处理状态转移**：`pa[x][i] = pa[pa[x][i - 1]][i - 1]`，即往上跳 $2^i$ 步，等价于先跳 $2^{i-1}$ 步，再跳 $2^{i-1}$ 步。
* **查询两步走**：先让较深的节点**对齐深度**（逼近目标高度），然后两个节点**齐头并进**向上跳，直到刚好在 LCA 的子节点停下。

### ⚠️ 常见错误

* **头文件缺失报错**：忘记加 `#include <algorithm>`，导致 `std::swap` 或 `std::max/min` 在评测机环境下报 Compile Error（特别是 testlib 环境）。
* **倍增数组越界**：`pa[MAXN][22]` 的第二维开得不够大，通常 $N=500000$ 时开到 20 到 22 之间即可，太小会导致越界。
* **查询时最后一步返回错**：在齐头并进跳跃结束后，`x` 和 `y` 停在 LCA 的正下方一层，所以最后必须返回 `pa[x][0]` 而不是 `x`。
* **位运算优先级混淆**：在写 `(1 << i) <= depth[now]` 时，忘记加括号，导致位运算和比较运算符的执行顺序出错。