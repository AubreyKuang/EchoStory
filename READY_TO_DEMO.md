# ✅ EchoStory - 准备就绪检查表

## 功能完成度检查（对比README.md）

### ✅ 核心功能 - 全部完成

| README.md 功能 | 实现状态 | 文件位置 |
|---------------|---------|---------|
| **1. Real-Time Voice Interaction** | ✅ 完成 | |
| - Gemini Live API | ✅ | `backend/app/services/gemini_service.py` |
| - 语音录制 | ✅ | `frontend/src/hooks/useAudioRecorder.ts` |
| - AI语音输出 | ✅ | `frontend/src/hooks/useSpeechSynthesis.ts` |
| - 打断处理 | ✅ | `gemini_service.py:interrupt_generation()` |
| **2. Live Visual Canvas** | ✅ 完成 | |
| - 交错输出 | ✅ | `websocket_handler.py` + Function Calling |
| - 实时图片生成 | ✅ | `gemini_service.py:generate_illustration()` |
| - 动态更新 | ✅ | `frontend/src/components/LiveCanvas.tsx` |
| **3. Live Vision (See)** | ✅ 完成 | |
| - 摄像头捕获 | ✅ | `frontend/src/hooks/useVideoCapture.ts` |
| - 物体检测 | ✅ | `gemini_service.py:analyze_video_frame()` |
| - 主动提及 | ✅ | System instruction |
| **4. Emotion-Aware Mirroring** | ✅ 完成 | |
| - 情感分析 | ✅ | Function calling: `save_story_segment` |
| - UI背景变化 | ✅ | `LiveCanvas.tsx:emotionGradients` |
| **5. Sensory-Friendly Interface** | ✅ 完成 | |
| - 低饱和度配色 | ✅ | `tailwind.config.js` |
| - 平滑动画 | ✅ | Framer Motion |
| **6. Story Journal** | ✅ 完成 | |
| - Session存储 | ✅ | `firestore_service.py` |
| - 图片存储 | ✅ | `storage_service.py` |
| - 查询接口 | ✅ | REST API endpoints |

## ✅ Demo.md 演示路径 - 完全支持

| 时间段 | 演示内容 | 可以实现 | 说明 |
|--------|---------|---------|------|
| 0:00-0:45 | 场景引入 | ✅ | 准备演示素材 |
| 0:45-1:30 | 实时语音+图片生成 | ✅ | **完整实现** |
| 1:30-2:15 | Vision功能：物体检测 | ✅ | **完整实现** |
| 2:15-3:00 | 打断测试 | ✅ | **完整实现** |
| 3:00-3:30 | GCP控制台 | ✅ | 部署后截屏 |
| 3:30-4:00 | 故事总结 | ✅ | Firestore查询 |

**结论：可以按照demo.md的路径录制！** 🎬

---

# 📖 快速使用指南

## 1. 本地开发设置（首次使用）

### 准备工作
```bash
# 1. 确保你有这些工具
node --version  # 需要 v20+
python3 --version  # 需要 3.11+

# 2. 获取必需的API密钥
# - Google Cloud Project ID
# - Gemini API Key (从 https://makersuite.google.com/app/apikey 获取)
```

### 快速启动
```bash
# 进入项目目录
cd /Users/apple/Developer/EchoStory

# 方式1：使用自动化脚本（推荐）
./scripts/setup-local.sh

# 方式2：手动设置
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥

# Frontend
cd ../frontend
npm install
cp .env.example .env.local
```

### 配置环境变量

**backend/.env**
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GEMINI_API_KEY=your-gemini-api-key-here
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
STORAGE_BUCKET_NAME=echostory-assets-your-project
FIRESTORE_COLLECTION=story_sessions
DEBUG=true
```

**frontend/.env.local**
```bash
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws/story
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 启动应用
```bash
# 终端1：启动后端
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 终端2：启动前端
cd frontend
npm run dev
```

**访问：**
- 前端界面：http://localhost:3000
- 后端API文档：http://localhost:8000/docs
- WebSocket测试：ws://localhost:8000/ws/story

---

## 2. 如何使用软件

### 基本使用流程

1. **打开应用**：访问 http://localhost:3000

2. **开始对话**：
   - 点击橙色麦克风按钮 🎤
   - 开始说话："I went to the park today"
   - AI会实时回应并朗读

3. **启用摄像头（可选）**：
   - 点击蓝色摄像头按钮 📹
   - 拿起一个玩具给摄像头看
   - AI会说："I see your [toy name]!"

4. **查看生成的故事**：
   - 图片会自动出现在屏幕上
   - 背景颜色会根据情绪变化
   - 故事段落会保存到Firestore

5. **打断AI**：
   - 当AI在说话时，点击"Wait!"按钮 ⏸️
   - 或直接再次按麦克风按钮说新的内容
   - AI会停止并听你说

### 前端调用流程

```typescript
// 1. WebSocket连接在页面加载时自动建立
const { isConnected, sessionId, sendAudioChunk } = useWebSocket();

// 2. 录音并发送
const { startRecording, stopRecording } = useAudioRecorder(sendAudioChunk);

// 3. 监听AI响应
on('audio_response', (message) => {
    // 文本显示
    setCurrentText(message.data.text);
    // AI朗读（自动）
    speak(message.data.text);
});

// 4. 处理图片生成
on('illustration_generated', (message) => {
    // 图片URL
    const imageUrl = message.url;
    // 添加到故事段落
    addSegment({ text, imageUrl });
});

// 5. Vision检测
on('vision_detection', (message) => {
    // 检测到的物体
    const objects = message.data.objects_detected;
    // 显示在UI上
});
```

---

## 3. Google Cloud 部署指南

### 前置准备

```bash
# 1. 安装Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# 2. 设置项目ID
export GOOGLE_CLOUD_PROJECT=echostory-demo-2026
export GEMINI_API_KEY=your-gemini-api-key
export STORAGE_BUCKET_NAME=echostory-assets-${GOOGLE_CLOUD_PROJECT}
```

### 方式1：一键部署（推荐）

```bash
cd /Users/apple/Developer/EchoStory

# 确保环境变量已设置
echo $GOOGLE_CLOUD_PROJECT
echo $GEMINI_API_KEY
echo $STORAGE_BUCKET_NAME

# 运行部署脚本
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

脚本会自动：
- ✅ 启用所有必需的GCP API
- ✅ 创建Cloud Storage bucket
- ✅ 初始化Firestore
- ✅ 存储API密钥到Secret Manager
- ✅ 构建并部署到Cloud Run

### 方式2：手动部署

#### 步骤1：启用API
```bash
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    containerregistry.googleapis.com \
    firestore.googleapis.com \
    storage.googleapis.com \
    aiplatform.googleapis.com
```

#### 步骤2：创建存储和数据库
```bash
# 创建Storage bucket
gsutil mb -p $GOOGLE_CLOUD_PROJECT -l us-central1 gs://$STORAGE_BUCKET_NAME
gsutil iam ch allUsers:objectViewer gs://$STORAGE_BUCKET_NAME

# 初始化Firestore
gcloud firestore databases create --region=us-central1
```

#### 步骤3：存储密钥
```bash
echo -n "$GEMINI_API_KEY" | gcloud secrets create gemini-api-key \
    --data-file=- --replication-policy="automatic"
```

#### 步骤4：部署后端
```bash
cd backend

# 构建镜像
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/echostory-backend

# 部署到Cloud Run
gcloud run deploy echostory-backend \
    --image gcr.io/$GOOGLE_CLOUD_PROJECT/echostory-backend \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT \
    --set-env-vars STORAGE_BUCKET_NAME=$STORAGE_BUCKET_NAME \
    --set-secrets GEMINI_API_KEY=gemini-api-key:latest
```

#### 步骤5：获取后端URL
```bash
BACKEND_URL=$(gcloud run services describe echostory-backend \
    --region us-central1 --format='value(status.url)')

echo "Backend URL: $BACKEND_URL"
```

#### 步骤6：部署前端
```bash
cd ../frontend

# 更新环境变量（在Dockerfile或构建时）
# NEXT_PUBLIC_WS_URL=wss://${BACKEND_URL}/ws/story
# NEXT_PUBLIC_API_URL=https://${BACKEND_URL}/api

# 构建镜像
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/echostory-frontend

# 部署
gcloud run deploy echostory-frontend \
    --image gcr.io/$GOOGLE_CLOUD_PROJECT/echostory-frontend \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated
```

#### 步骤7：获取前端URL
```bash
FRONTEND_URL=$(gcloud run services describe echostory-frontend \
    --region us-central1 --format='value(status.url)')

echo "✅ 部署完成！"
echo "前端访问: $FRONTEND_URL"
echo "后端API: $BACKEND_URL"
```

### 部署后验证

```bash
# 检查后端健康
curl $BACKEND_URL/health

# 查看后端日志
gcloud run logs read echostory-backend --region us-central1 --limit 50

# 查看前端日志
gcloud run logs read echostory-frontend --region us-central1 --limit 50
```

---

## 4. 录制Demo视频准备

### 录制前检查清单

```bash
# 1. 确保本地运行正常
cd /Users/apple/Developer/EchoStory
# 启动后端和前端
# 访问 http://localhost:3000
# 测试：语音、摄像头、打断功能

# 2. 准备演示道具
# - 找一个玩具（泰迪熊、积木等）
# - 测试摄像头能否检测到

# 3. 清理浏览器
# - 清除缓存和cookies
# - 关闭其他标签页
# - 允许麦克风和摄像头权限

# 4. 测试完整流程
# - 说话 → AI回应 → 图片生成
# - 显示玩具 → AI提及玩具
# - 打断AI → AI停止并重新听
```

### Demo录制脚本

**0:00-0:45 场景引入**
> "这是一个患有自闭症的孩子，他想描述今天在学校发生的事情，但是很难用语言表达..."

**0:45-1:30 核心演示**
```
[操作]
1. 点击麦克风按钮
2. 说："I went to the park today"
3. AI回应："That sounds fun! What did you do in the park?"
4. 说："I played on the swings"
5. 观察：文字出现 + AI朗读 + 图片生成

[展示点]
- 实时文字显示
- AI语音朗读
- 图片与文字同时出现（交错输出）
```

**1:30-2:15 Vision功能**
```
[操作]
1. 点击摄像头按钮
2. 拿起泰迪熊对着摄像头
3. AI说："I see your teddy bear! Should he join the adventure?"
4. 说："Yes! He is my friend"

[展示点]
- 摄像头实时画面
- 物体检测标签
- AI主动提及物体
```

**2:15-3:00 打断测试**
```
[操作]
1. AI正在生成故事
2. 点击"Wait!"按钮或直接说话
3. 说："No, the dog should be blue!"
4. AI停止，回应："Oh, a blue dog! That's creative!"

[展示点]
- 实时打断
- AI立即停止
- 无缝切换话题
```

**3:00-3:30 技术证明**
```
[屏幕录制]
1. 切换到Google Cloud Console
2. 显示Cloud Run服务运行中
3. 显示实时日志
4. 显示架构图（ARCHITECTURE.md）
```

**3:30-4:00 情感升华**
```
[展示]
1. 回到应用，显示完整的故事
2. 展示Firestore中保存的session
3. 说明：父母可以和孩子一起回顾今天的故事
```

---

## 5. 常见问题解决

### WebSocket连接失败
```bash
# 检查后端是否运行
curl http://localhost:8000/health

# 检查端口占用
lsof -i :8000

# 检查CORS配置
# backend/app/main.py 中的 CORS_ORIGINS
```

### 麦克风不工作
```bash
# 浏览器必须是HTTPS或localhost
# 检查浏览器权限设置
# Chrome: 设置 → 隐私和安全 → 网站设置 → 麦克风
```

### 摄像头不工作
```bash
# 同样需要HTTPS或localhost
# 检查浏览器摄像头权限
# 确保没有其他应用占用摄像头
```

### 图片生成失败
```bash
# 检查Vertex AI API是否启用
gcloud services list --enabled | grep aiplatform

# 检查服务账号权限
gcloud projects get-iam-policy $GOOGLE_CLOUD_PROJECT

# 检查配额
# GCP Console → Vertex AI → 配额
```

### Firestore权限错误
```bash
# 确保Firestore已初始化
gcloud firestore databases list

# 检查服务账号角色
# 需要 roles/datastore.user
```

---

## 6. 性能优化建议

### 本地开发
- 使用`docker-compose up`避免环境问题
- Backend开启`--reload`自动重启
- Frontend使用`npm run dev`热更新

### 生产环境
- Cloud Run自动扩缩容，无需手动配置
- 图片生成2-5秒是正常的
- WebSocket连接建议使用wss://（HTTPS）

---

## ✅ 总结

你现在可以：

1. ✅ **本地运行**
   ```bash
   # 终端1
   cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload
   # 终端2
   cd frontend && npm run dev
   ```

2. ✅ **部署到GCP**
   ```bash
   ./scripts/deploy.sh
   ```

3. ✅ **录制Demo视频**
   - 按照demo.md的4分钟结构
   - 所有功能都已实现
   - 重点展示：实时性、交错输出、Vision、打断

4. ✅ **提交黑客松**
   - GitHub: https://github.com/your-username/EchoStory
   - Demo视频：4分钟
   - 部署URL：从Cloud Run获取

**祝你黑客松顺利！🚀**
