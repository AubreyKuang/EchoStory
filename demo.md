# EchoStory Demo Script

## Overview
This demo showcases EchoStory's real-time multimodal AI storytelling capabilities for children with ASD. The demo uses progressive story generation with three stages: **Sunshine** → **Grassland** → **Puppy**.

## Demo Mode Setup

### Prerequisites
1. Three progressive images placed in `/frontend/public/`:
   - `test.png` - Bright sunny sky scene
   - `test2.png` - Green grassland/meadow scene
   - `test3.png` - Happy puppy on grass scene

2. Backend configuration:
   ```bash
   # backend/.env
   DEMO_MODE=true
   ```

3. Start services:
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn app.main:app --reload

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

## Demo Script for Video Recording

### Scene 1: Introduction (0:00 - 0:45)
**Visual**: Show the EchoStory interface with logo and clean UI.

**Voiceover**:
> "Meet EchoStory - an AI companion that helps children with autism tell stories about their day through voice, vision, and interactive illustrations."

---

### Scene 2: First Interaction - Sunshine (0:45 - 1:30)
**Action**:
1. Click the microphone button (red circle at bottom)
2. **Say in English**: "I went outside today. It was sunny."
3. Release the button

**Expected Response**:
- ✨ "Creating magic..." appears briefly
- 🎨 Image 1 (sunny sky) fades in
- 📝 Text appears: "Oh, what a beautiful sunny day! The sun is shining so bright. Tell me, what do you see?"
- 🔊 Voice reads the text (using browser TTS)

**Highlight**:
- Point out the **interleaved output** - text appears immediately, image follows
- Show the smooth fade-in animation
- Voice and text are synchronized (200ms delay)

---

### Scene 3: Second Interaction - Grassland (1:30 - 2:15)
**Action**:
1. Click microphone again
2. **Say in English**: "There was green grass everywhere."
3. Release button

**Expected Response**:
- 🎨 Image 2 (grassland) replaces the previous scene
- 📝 Text: "I love it! The grass looks so soft and green. What a wonderful place to play! What did you do there?"
- 🔊 Voice narration continues

**Highlight**:
- Show smooth scene transition
- Point out progress indicators at bottom (3 dots, second one highlighted)

---

### Scene 4: Third Interaction - Puppy (2:15 - 3:00)
**Action**:
1. Click microphone again
2. **Say in English**: "I saw a friendly puppy."
3. Release button

**Expected Response**:
- 🎨 Image 3 (puppy on grass) appears
- 📝 Text: "Wow! A friendly puppy! Look at that happy face! Is the puppy playing with you?"
- 🔊 Voice narration

**Highlight**:
- Emphasize the **progressive story building**
- Show how AI builds on previous context

---

### Scene 5: Vision Detection Demo (3:00 - 3:45)
**Action**:
1. Click the camera button (enable vision)
2. Hold up objects in front of camera in sequence:
   - 📝 **A pen** → AI detects "pen"
   - 🧸 **A toy** → AI detects "toy, teddy bear"
   - 📱 **An iPhone** → AI detects "iphone, phone"

**Expected Response**:
- Camera overlay appears in bottom-right
- Detected objects show in the overlay
- Objects rotate slowly (not too fast)

**Voiceover**:
> "EchoStory uses Live Vision to detect real-world objects and naturally incorporate them into the story."

---

### Scene 6: Interruption Feature (3:45 - 4:00)
**Action**:
1. Start recording
2. While AI is speaking, click the **Interrupt** button (⏸️ icon)

**Expected Response**:
- AI speech stops immediately
- "Creating magic..." indicator disappears
- Ready for new input

**Highlight**:
> "Children can interrupt at any time - crucial for low-demand interaction."

---

### Scene 7: Technical Showcase (4:00 - 4:30)
**Visual Split Screen**:
- Left: EchoStory interface
- Right: Terminal showing backend logs

**Show in Terminal**:
```
📖 Demo Story Stage 1: sunshine
🎨 Returning illustration: http://localhost:3000/test.png
👁️ Vision detected: ['pen']
📖 Demo Story Stage 2: grassland
🎨 Returning illustration: http://localhost:3000/test2.png
```

**Voiceover**:
> "Built on Google Cloud with Gemini 2.0 Flash Live API for real-time multimodal processing."

---

### Scene 8: Architecture & Impact (4:30 - 5:00)
**Visual**: Show Architecture.md diagram

**Voiceover**:
> "EchoStory combines voice, vision, and visual generation in real-time. No more pressure to perform - just natural storytelling that empowers autistic children to share their world."

---

## Key Technical Features to Highlight

### 1. Interleaved Output ✨
- Text appears **immediately** (300ms animation)
- Voice starts **200ms later** (synchronized)
- Image fades in **1.2 seconds later** (realistic generation time)
- Not "wait for everything then show" - true streaming UX

### 2. Live Vision 👁️
- Real-time object detection via camera
- Objects: pen → toy → iPhone (rotate slowly)
- Realistic detection speed (600ms per frame)

### 3. Interruption Handling ⏸️
- Instant stop when user clicks interrupt
- Speech synthesis cancels immediately
- Ready for new direction

### 4. Progressive Story Building 📖
- Three-stage narrative: sunshine → grassland → puppy
- Each stage builds on previous context
- Natural conversation flow

### 5. Sensory-Friendly Design 🎨
- Gentle animations
- Emotion-based background gradients
- Clear visual hierarchy
- No overwhelming elements

---

## Testing Checklist

Before recording:
- [ ] All three images (test.png, test2.png, test3.png) are in place
- [ ] Backend shows `🎭 Running in DEMO MODE`
- [ ] Frontend loads without errors
- [ ] Microphone permission granted
- [ ] Camera permission granted (for vision demo)
- [ ] Audio output works (TTS voice)
- [ ] Session ID appears in top-right

During demo:
- [ ] First interaction shows test.png (sunshine)
- [ ] Second interaction shows test2.png (grassland)
- [ ] Third interaction shows test3.png (puppy)
- [ ] Vision detects pen, toy, iPhone in sequence
- [ ] Interrupt button stops generation
- [ ] No UI flashing or errors
- [ ] Animations are smooth

---

## Suggested Recording Setup

### Camera Setup
- **Split screen**: 70% app interface, 30% you speaking
- **Or**: Full screen app with voice-over narration
- **Quality**: 1080p minimum

### Audio Setup
- Clear microphone for your voice
- Capture system audio for AI responses
- Background music (optional, keep subtle)

### Timing
- 4-5 minutes total
- 30-45 seconds per scene
- Leave 2-3 seconds between actions for visibility

---

## Demo Advantages

✅ **No API keys required** - Works completely offline
✅ **Predictable behavior** - Same sequence every time
✅ **Fast iteration** - No waiting for real API responses
✅ **Cost-free** - Perfect for presentations and testing
✅ **Realistic timing** - Simulates actual API latencies

---

## Post-Demo: Switch to Production

To enable real Gemini API:
```bash
# backend/.env
DEMO_MODE=false
GEMINI_API_KEY=your-actual-key
GOOGLE_CLOUD_PROJECT=your-project
STORAGE_BUCKET_NAME=your-bucket
```

Real mode adds:
- Actual Gemini 2.0 Flash responses
- Imagen 3 illustration generation
- Cloud Storage for assets
- Firestore session persistence
