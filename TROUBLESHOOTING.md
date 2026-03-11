# 麦克风和摄像头权限问题诊断

## 快速诊断步骤

### 1. 检查浏览器控制台
打开开发者工具（F12 或 Cmd+Option+I），查看Console标签页是否有错误信息。

常见错误：
- `NotAllowedError`: 权限被拒绝
- `NotFoundError`: 找不到设备
- `NotReadableError`: 设备被其他应用占用

### 2. 检查浏览器地址
确认你访问的是：
- ✅ `http://localhost:3000`
- ✅ `https://...` (任何HTTPS地址)
- ❌ `http://192.168.x.x` (局域网IP不行)
- ❌ `http://127.0.0.1` (可能不行，用localhost)

**解决方案**：如果不是localhost，改用 http://localhost:3000

### 3. 重置浏览器权限

#### Chrome/Edge
1. 点击地址栏左边的🔒或ⓘ图标
2. 找到"麦克风"和"摄像头"
3. 改为"允许"
4. 刷新页面（F5）

或者：
1. 设置 → 隐私和安全 → 网站设置
2. 麦克风 → 找到 localhost:3000 → 改为"允许"
3. 摄像头 → 找到 localhost:3000 → 改为"允许"

#### Safari
1. Safari → 偏好设置 → 网站 → 摄像头/麦克风
2. 找到 localhost → 改为"允许"

#### Firefox
1. 点击地址栏左边的🔒图标
2. 清除权限 → 刷新页面 → 重新授权

### 4. 检查系统权限（macOS）

1. 系统偏好设置 → 安全性与隐私 → 隐私
2. 左侧选择"摄像头"，确保Chrome/Safari有勾选
3. 左侧选择"麦克风"，确保Chrome/Safari有勾选

如果浏览器没有出现在列表中：
- 需要先触发一次权限请求（点击按钮）
- 然后去系统设置勾选

### 5. 检查设备是否被占用

```bash
# macOS: 检查哪些应用在使用摄像头
lsof | grep "AppleCamera"

# 如果有其他应用（Zoom、微信等），关闭它们
```

## 手动测试代码

在浏览器Console中运行：

```javascript
// 测试麦克风
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    console.log('✅ 麦克风权限获取成功', stream);
    stream.getTracks().forEach(track => track.stop());
  })
  .catch(err => console.error('❌ 麦克风权限失败:', err));

// 测试摄像头
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    console.log('✅ 摄像头权限获取成功', stream);
    stream.getTracks().forEach(track => track.stop());
  })
  .catch(err => console.error('❌ 摄像头权限失败:', err));
```

如果这些命令成功，说明权限没问题，可能是代码其他地方的问题。

## 增强版前端代码（显示错误）

如果上述都不行，我可以修改代码显示更清楚的错误信息。
