---
title: for循环模板
heading: for循环模板
subtitle: 已知循环次数时使用：累加、遍历、枚举
tags: for循环 遍历 累加 枚举 GESP1
topic: GESP1
---

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    // 基本循环
    for (int i = 1; i <= 10; i++)
        cout << i << " ";
    cout << endl;

    // 累加求和 1+2+...+100
    int sum = 0;
    for (int i = 1; i <= 100; i++) sum += i;
    cout << sum << endl;  // 5050

    // 倒序循环
    for (int i = 10; i >= 1; i--)
        cout << i << " ";
    cout << endl;

    // 步长循环：偶数
    for (int i = 2; i <= 100; i += 2)
        cout << i << " ";
    cout << endl;

    // 嵌套：九九乘法表
    for (int i = 1; i <= 9; i++) {
        for (int j = 1; j <= i; j++)
            cout << j << "×" << i << "=" << i*j << "\t";
        cout << endl;
    }

    // break 和 continue
    for (int i = 1; i <= 10; i++) {
        if (i == 5) break;       // 跳出循环
        if (i % 3 == 0) continue; // 跳过本次
        cout << i << " ";
    }

    return 0;
}
```

## 📖 要点说明

- `for` 适合循环次数已知的场景
- 循环变量 `i` 作用域仅限 for 内部
- `break` 完全跳出，`continue` 跳过本次
- 嵌套循环时间复杂度是各层相乘

### ⚠️ 常见错误

- 循环条件写错导致死循环
- 循环变量在 for 外使用未声明
- 嵌套循环内外层用同一变量名
