---
title: C++框架模板
heading: C++框架模板
subtitle: 竞赛最基础的模板：主函数框架，所有题目的起点
tags: C++框架 main GESP1
topic: GESP1
---

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // ====== 在这里写你的代码 ======


    // =============================
    return 0;
}
```

## 📖 要点说明

- `bits/stdc++.h` 万能头文件，竞赛中常用，省去逐个引入
- `ios::sync_with_stdio(false); cin.tie(nullptr);` 加速输入输出
- `int main()` 是程序入口，`return 0` 表示正常结束

### ⚠️ 常见错误

- 忘记写 `using namespace std;` 导致 `cout` 无法识别
- 万能头在部分评测系统不可用，建议比赛前确认
