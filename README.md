# Project Proposal

## Project Name

**EchoStory — An AI Live Storytelling Companion for Children with Autism**

## 1. Background

#### **The Communication Gap in Neurodiversity**

Millions of children worldwide are diagnosed with Autism Spectrum Disorder (ASD), a neurodevelopmental condition where the internal world is often much richer than what is expressed externally. For many autistic children, the transition from **internal thought to verbal narration** is not a straight line—it is a complex, often overwhelming barrier.

As a result, a "communication black box" forms:

- **Parental Disconnect:** Parents struggle to grasp the nuances of their child’s day, leading to missed opportunities for emotional bonding.
- **The Frustration Cycle:** Children feel the weight of "failed communication," which can lead to increased anxiety or social withdrawal.
- **Limited Narrative Growth:** Traditional speech therapy is often episodic, failing to capture the spontaneous, lived experiences of a child's daily life.

#### **The Limitation of Static Tools**

Traditional interventions, such as the Picture Exchange Communication System (PECS), have long proven that **visual and verbal channels work better when combined**. However, these tools are often:

- **Static & Manual:** They require heavy adult mediation and lack spontaneity.
- **Transactional, Not Relational:** They focus on "requesting" (e.g., "I want juice") rather than "storytelling" or emotional sharing.
- **High-Pressure:** Traditional therapy can sometimes feel like a "test," where the child is pressured to produce specific verbal outputs to receive a reward.

#### **The EchoStory Philosophy: Encouragement over Pressure**

EchoStory is built on the principle of **Low-Demand Engagement**. We recognize that for a child with ASD, "What did you do today?" can be a high-pressure, terrifying question.

Our approach shifts the paradigm:

- **No Forced Speech:** EchoStory does not demand a response. It is designed to be a "parallel play" companion that follows the child's lead. If a child makes a sound, shows a toy, or says a single word, the AI validates that input by transforming it into a beautiful visual reality.
- **Scaffolding, Not Testing:** The AI provides "scaffolds"—visual and auditory cues—that encourage the child to add the next piece of the story only when they are ready.
- **Validation through Creation:** By instantly turning a child’s fragmented input into an interactive illustration, the system provides **immediate sensory rewards**, reinforcing the joy of communication without the stress of "getting it right."

#### **The Multimodal Breakthrough**

------

# 2. Problem Statement

Children with autism often face three key barriers in communication:

### 1. Difficulty describing daily experiences

Many children struggle to narrate events such as:

- what they did at school
- who they interacted with
- how they felt during the day

### 2. Limited tools for narrative development

Existing communication aids are often:

- static picture cards
- non-interactive tools
- lacking real-time feedback

These tools rarely help children **construct stories or memories** about their experiences.

### 3. Emotional expression challenges

Children may have difficulty identifying or expressing emotions such as:

- happiness
- frustration
- anxiety

Without support, these communication gaps can affect both **emotional wellbeing and family communication**.

------

# 3. Proposed Solution

**EchoStory** is a **multimodal AI live agent** that helps autistic children transform their spoken words into **interactive visual stories**.

The system listens to a child describing their day and instantly generates:

- illustrations
- simple narrative text
- AI narration
- emotional context

This turns everyday experiences into a **visual storybook**.

Instead of asking children to produce complex sentences, the system encourages expression through **short phrases, words, or sounds**, and gradually builds them into a meaningful story.

The AI acts as a **gentle conversational companion**, guiding children to communicate without pressure.

------

# 4. How It Works

### Step 1 — Voice Interaction

The child speaks naturally:

> “I went to the park.”

Gemini Live processes the speech in real time.

------

### Step 2 — Conversational Encouragement

The AI responds:

> “That sounds fun! What did you do in the park?”

This encourages **continued conversation** and helps build narrative skills.

------

### Step 3 — Multimodal Story Generation

The system generates:

- a visual illustration of the park
- simple descriptive text
- audio narration

Example output:

Illustration: child playing on a swing in a park

Text:

> “Today I went to the park and played.”

Narration:

AI reads the story aloud.

------

### Step 4 — Daily Storybook Creation

At the end of the session, the system compiles the interactions into a **visual daily journal**:

**Today’s Story**

- Scene 1: Going to the park
- Scene 2: Playing on the swings
- Scene 3: Feeling happy

Parents and teachers can review the story with the child.

------

## 5. Key Features

#### 1. Real-Time Conversational Co-creation (Hear & Speak)

Leveraging the **Gemini Live API**, EchoStory moves beyond turn-based chat to a fluid, low-latency dialogue.

- **Active Listening & Interruption Handling:** The agent understands natural speech patterns and allows the child to interrupt or change the story direction mid-sentence, ensuring the interaction feels like a playmate, not a machine.
- **Scaffolded Prompting:** Instead of open-ended questions that might overwhelm a child with ASD, the agent uses "scaffolded" techniques—offering gentle choices and verbal cues to build narrative confidence.

#### 2. Live "Visual Canvas" Interleaved Output (Create)

EchoStory fulfills the **Creative Storyteller** requirement through **native interleaved multimodal generation**.

- **Synchronized Storytelling:** As the child speaks, the system doesn't wait for a "submit" button. It generates a continuous stream of visual assets, narration, and text.
- **Dynamic Visual Evolution:** If a child says, *"The dog is now blue,"* Gemini’s multimodal capabilities update the visual context in real-time. This provides immediate visual reinforcement, which is critical for children who rely on visual learning (Visual Thinkers).

#### 3. Proactive Visual Contextual Awareness (See)

This feature bridges the gap between the physical and digital worlds using **Gemini Live Vision**.

- **Object Integration:** Children can show their physical toys or drawings to the camera. The agent "sees" these items—for example, a teddy bear—and instantly weaves them into the digital story: *"I see your teddy bear is ready for the adventure too! Should he lead the way?"*
- **Environmental Grounding:** The agent can reference the child's environment to initiate conversation, lowering the barrier to starting a dialogue.

#### 4. Emotion-Aware "Mirroring" & Labeling

To support emotional regulation and social-emotional learning (SEL):

- **Multimodal Sentiment Analysis:** The agent analyzes the child’s tone and semantic cues to suggest emotional labels.
- **Empathetic Reflection:** Instead of just "understanding," the AI mirrors the appropriate supportive tone. It might say, *"That sounds like a very loud and scary thunder! It's okay to feel a bit worried,"* while softening the background visuals to a calming palette.

#### 5. Sensory-Friendly Interface & Personalization

Designed with **Responsible AI** for neurodiversity at its core:

- **Customizable Personas:** Parents can adjust the AI’s voice pitch, speaking rate, and visual complexity to prevent sensory overload.
- **The "Silent" Mode:** Supports non-verbal children who prefer to interact via gestures or pointing (captured via Live Vision) while the AI provides the verbal narrative.

#### 6. Dynamic Visual Memory Journal

The output of every session is more than a log; it’s a **Living Diary**.

- **Memory Anchors:** Each session is compiled into a chronologically illustrated journal on Google Cloud, allowing children to revisit their day.
- **Parent-Child Bridge:** Provides parents with a concrete visual tool to discuss the day’s events, turning "How was school?" (to which many autistic children might not respond) into "Tell me about this picture of you and the blue dog!"

------

# 6. Responsible AI Design

EchoStory is designed with a strong emphasis on **ethical and responsible AI**.

Key principles include:

### No forced speech

The system does not pressure children to speak.
Children can interact using:

- single words
- short phrases
- gestures or visual prompts.

### Multimodal expression

The tool supports different communication styles, recognizing that many autistic children prefer **visual communication**.

### Privacy-first design

All conversation data is stored securely and can be controlled by parents or caregivers.

------

# 7. Technical Architecture

### Frontend

Interactive interface supporting:

- microphone input
- camera input (optional)
- real-time visual rendering

------

### Backend

Hosted on **Google Cloud**.

Components include:

- **Gemini Live API** for real-time voice interaction
- **Gemini multimodal generation** for images and text
- **Cloud Run** for backend services
- **Firestore** for story storage
- **Vertex AI** for model access

------

### Agent Workflow

User voice input
↓

Gemini Live speech processing
↓

Conversation agent response
↓

Multimodal generation (image + text + narration)
↓

Storybook assembly
↓

Journal storage

------

# 8. Innovation

EchoStory pushes beyond traditional chatbot interfaces by combining:

- **live conversation**
- **visual storytelling**
- **emotion-aware interaction**
- **memory creation**

The result is a **living storytelling agent** that transforms everyday communication into an engaging creative experience.

------

# 9. Testing Guide

EchoStory supports two modes for testing and development: **Demo Mode** (no API keys required) and **Production Mode** (with real Gemini API).

## Demo Mode (Recommended for Testing)

### ✅ Advantages

- **No API Keys Required** - Works completely offline without any Google Cloud credentials
- **Perfect for Restricted Regions** - Ideal if Gemini API is not available in your region
- **Zero Cost** - No API usage fees
- **Predictable Behavior** - Consistent responses for presentations and demos
- **Fast Iteration** - Instant responses without waiting for API calls
- **Privacy-Friendly** - No data sent to external services

### 🚀 Quick Start (Demo Mode)

#### 1. Prerequisites
```bash
# Install Node.js 18+ and Python 3.11+
node --version  # Should be 18.x or higher
python --version  # Should be 3.11 or higher
```

#### 2. Prepare Demo Images
Place three progressive story images in `/frontend/public/`:
- `test.png` - Sunny sky scene (Stage 1)
- `test2.png` - Green grassland scene (Stage 2)
- `test3.png` - Happy puppy scene (Stage 3)

#### 3. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DEMO_MODE=true
APP_NAME=EchoStory
STORAGE_BUCKET_NAME=demo-bucket
EOF

# Start backend
uvicorn app.main:app --reload
```

You should see:
```
🎭 Running in DEMO MODE - using simulated responses
```

#### 4. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### 5. Access Application
Open browser and navigate to:
```
http://localhost:3000
```

### 🎬 Demo Features

**Progressive Story Generation:**
1. **First interaction** → Sunny sky image + "Oh, what a beautiful sunny day!"
2. **Second interaction** → Grassland image + "The grass looks so soft and green!"
3. **Third interaction** → Puppy image + "Wow! A friendly puppy!"

**Vision Detection:**
- Camera detects objects in sequence: pen → toy → iPhone
- Objects rotate slowly for realistic demo experience

**Realistic Timing:**
- Audio processing: 800ms delay
- Image generation: 1.2s delay
- Vision analysis: 600ms delay

---

## Production Mode (Real Gemini API)

### 📋 Prerequisites

1. **Google Cloud Project** with billing enabled
2. **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/)
3. **Vertex AI enabled** in your GCP project
4. **Service Account** with permissions:
   - Vertex AI User
   - Storage Admin
   - Firestore User

### 🔑 API Key Setup

#### Option A: Using Gemini API (Recommended for Testing)

```bash
# Get API key from: https://aistudio.google.com/app/apikey
# Note: Gemini API availability varies by region

cd backend

cat > .env << EOF
DEMO_MODE=false
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash-exp
GOOGLE_CLOUD_PROJECT=your-project-id
VERTEX_AI_LOCATION=us-central1
IMAGEN_MODEL=imagegeneration@006
STORAGE_BUCKET_NAME=your-bucket-name
FIRESTORE_COLLECTION=story_sessions
CORS_ORIGINS=["http://localhost:3000"]
EOF
```

#### Option B: Using Vertex AI (Full Production)

```bash
# Download service account key from Google Cloud Console
# Place at: backend/credentials.json

cat > .env << EOF
DEMO_MODE=false
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
GOOGLE_CLOUD_PROJECT=your-project-id
GEMINI_MODEL=gemini-2.0-flash-exp
VERTEX_AI_LOCATION=us-central1
IMAGEN_MODEL=imagegeneration@006
STORAGE_BUCKET_NAME=your-bucket-name
FIRESTORE_COLLECTION=story_sessions
EOF
```

### 🏗️ Google Cloud Setup

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable \
  aiplatform.googleapis.com \
  storage.googleapis.com \
  firestore.googleapis.com \
  run.googleapis.com

# Create storage bucket
gsutil mb -l us-central1 gs://your-bucket-name
gsutil iam ch allUsers:objectViewer gs://your-bucket-name

# Initialize Firestore
gcloud firestore databases create --region=us-central1
```

### 🚀 Start Production Mode

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

You should see:
```
Running with real Gemini API
```

---

## 🌍 Region Availability

### Gemini API Regions
Gemini API is currently available in:
- United States
- European Union countries
- United Kingdom
- Canada
- Australia
- Japan
- South Korea
- Singapore

**If Gemini API is NOT available in your region:**
- ✅ Use **Demo Mode** for full functionality testing
- ✅ Demo Mode works identically to production for presentations
- ✅ Consider VPN for API testing (if allowed by terms of service)

---

## 🧪 Testing Checklist

### Demo Mode Testing
- [ ] Backend shows `🎭 Running in DEMO MODE`
- [ ] First recording returns sunny sky image (test.png)
- [ ] Second recording returns grassland image (test2.png)
- [ ] Third recording returns puppy image (test3.png)
- [ ] Camera detects: pen, toy, iPhone in sequence
- [ ] Interruption button stops generation immediately
- [ ] Voice synthesis works (browser TTS)
- [ ] No console errors

### Production Mode Testing
- [ ] Backend shows `Running with real Gemini API`
- [ ] Gemini processes voice input and responds
- [ ] Vision API detects real objects from camera
- [ ] Imagen generates illustrations (2-5 seconds)
- [ ] Images saved to Cloud Storage
- [ ] Sessions saved to Firestore
- [ ] No API errors in logs

---

## 🔍 Troubleshooting

### Demo Mode Issues

**Problem**: Images not loading
```bash
# Ensure images are in correct location
ls frontend/public/test*.png
# Should show: test.png, test2.png, test3.png
```

**Problem**: Backend not starting
```bash
# Check Python version
python --version  # Must be 3.11+

# Reinstall dependencies
cd backend
pip install --upgrade -r requirements.txt
```

### Production Mode Issues

**Problem**: "API key not valid"
```bash
# Verify API key at: https://aistudio.google.com/app/apikey
# Ensure no extra spaces in .env file
cat backend/.env | grep GEMINI_API_KEY
```

**Problem**: "Permission denied" for Cloud Storage
```bash
# Check bucket permissions
gsutil iam get gs://your-bucket-name

# Add public access
gsutil iam ch allUsers:objectViewer gs://your-bucket-name
```

**Problem**: Firestore errors
```bash
# Verify Firestore is initialized
gcloud firestore databases list

# Check service account has Firestore User role
```

---

## 📊 Comparison: Demo vs Production

| Feature | Demo Mode | Production Mode |
|---------|-----------|-----------------|
| **API Keys** | ❌ Not required | ✅ Required |
| **Cost** | 🆓 Free | 💰 Pay per use |
| **Response Quality** | 📝 Pre-written | 🤖 AI-generated |
| **Image Generation** | 🖼️ Static images | 🎨 Real-time Imagen |
| **Vision Detection** | 👁️ Simulated | 👁️ Real Gemini Vision |
| **Latency** | ⚡ <1 second | ⏱️ 2-5 seconds |
| **Region Restrictions** | 🌍 Works everywhere | ⚠️ Region-dependent |
| **Best For** | Testing, demos, presentations | Production, real users |

---

## 🎥 Recording Demo Video

For hackathon submissions or presentations:

1. **Use Demo Mode** for predictable, polished demos
2. Follow the script in `demo.md`
3. Prepare demo objects: pen, toy, iPhone
4. Expected runtime: 4-5 minutes
5. Show terminal logs alongside UI for technical credibility

See `demo.md` for detailed scene-by-scene script.

---

## 🚢 Deployment

### Deploy to Google Cloud Run

```bash
cd backend
gcloud run deploy echostory-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Deploy Frontend to Vercel

```bash
cd frontend
npm install -g vercel
vercel --prod
```

---

## 📚 Additional Resources

- **Architecture Details**: See `Architecture.md`
- **Demo Script**: See `demo.md`
- **Gemini API Docs**: https://ai.google.dev/docs
- **Vertex AI Docs**: https://cloud.google.com/vertex-ai/docs

