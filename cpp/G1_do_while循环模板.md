---
title: do-while循环模板
heading: do-while循环模板
subtitle: 先执行后判断——至少执行一次的循环
tags: do-while 循环 至少一次 GESP1
topic: GESP1
---

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    // 输入验证
    int n;
    do { cin >> n; } while (n < 1 || n > 100);
    cout << n << endl;

    // 数字翻转
    int num = 12345, rev = 0, t = num;
    do { rev = rev * 10 + t % 10; t /= 10; } while (t > 0);
    cout << rev << endl;  // 54321

    // 迭代求 gcd
    int a = 48, b = 18;
    do { int r = a % b; a = b; b = r; } while (b != 0);
    cout << a << endl;  // 6

    return 0;
}
```

## 📖 要点说明

- do-while **至少执行一次**，先执行后判断
- 条件后加分号 `while (条件);`
- 适合输入验证等先做一次再决定的场景
- 大部分场景 for/while 更常用

### ⚠️ 常见错误

- 忘写 `while` 后的分号 `;`
- 条件写反导致多执行一次
- 输入验证中忘记更新变量导致死循环
