---
title: while循环模板
heading: while循环模板
subtitle: 未知循环次数时使用：条件驱动型循环
tags: while循环 条件循环 GESP1
topic: GESP1
---

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    // 求位数
    int n = 12345, temp = n, digits = 0;
    while (temp > 0) { digits++; temp /= 10; }
    cout << digits << endl;  // 5

    // 读入直到条件满足
    int x, sum = 0;
    while (cin >> x && x != 0) sum += x;

    // while(true) + break
    int target = 42, guess;
    while (true) {
        cin >> guess;
        if (guess == target) break;
    }

    // 牛顿迭代法求 √2
    double a = 2.0, x0 = 1.0;
    while (fabs(x0 * x0 - a) > 1e-9)
        x0 = (x0 + a / x0) / 2.0;

    return 0;
}
```

## 📖 要点说明

- `while` 适合循环次数未知的场景
- `while(true)` + `break` 是常见模式
- 循环体内必须改变条件变量，否则死循环
- for 和 while 可以互相转换

### ⚠️ 常见错误

- 忘记更新循环变量导致死循环
- 条件一开始就 false，循环体不执行
- while 体内忘 `break` 程序卡住
