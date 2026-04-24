---
title: BFS搜索模板
heading: BFS搜索模板
subtitle: 广度优先搜索——逐层扩展，天然求最短路径
tags: BFS 广度优先 最短路径 队列 GESP6
topic: GESP6
---

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 1010;
int dist[N][N];
int dx[] = {-1, 1, 0, 0}, dy[] = {0, 0, -1, 1};

// 网格 BFS 求最短路
void bfs(int sx, int sy, int n, int m) {
    memset(dist, -1, sizeof(dist));
    queue<pair<int,int>> q;
    q.push({sx, sy});
    dist[sx][sy] = 0;

    while (!q.empty()) {
        auto [x, y] = q.front(); q.pop();
        for (int d = 0; d < 4; d++) {
            int nx = x + dx[d], ny = y + dy[d];
            if (nx < 0 || nx >= n || ny < 0 || ny >= m) continue;
            if (dist[nx][ny] != -1) continue;  // 已访问
            dist[nx][ny] = dist[x][y] + 1;
            q.push({nx, ny});
        }
    }
}

int main() {
    bfs(0, 0, 5, 5);
    cout << dist[4][4] << endl;  // 从(0,0)到(4,4)的最短距离
    return 0;
}
```

## 📖 要点说明

- BFS 用队列，逐层扩展，天然求无权图最短路
- `dist` 初始化为 -1 表示未访问
- 方向数组 `dx/dy` 简化四方向移动

### ⚠️ 常见错误

- 忘标记已访问导致重复入队
- BFS 起点忘设 `dist=0`
- 边界检查遗漏
