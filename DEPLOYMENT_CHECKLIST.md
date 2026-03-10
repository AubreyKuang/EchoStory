# EchoStory - Hackathon Deployment Checklist

## Pre-Deployment (Setup Phase)

### Google Cloud Project Setup
- [ ] Create GCP project with billing enabled
- [ ] Enable required APIs:
  - [ ] Cloud Run API
  - [ ] Cloud Build API
  - [ ] Vertex AI API
  - [ ] Firestore API
  - [ ] Cloud Storage API
  - [ ] Secret Manager API
- [ ] Create service account with proper permissions
- [ ] Download service account credentials JSON

### API Keys & Credentials
- [ ] Obtain Gemini API key from Google AI Studio
- [ ] Store Gemini API key in Secret Manager
- [ ] Configure GOOGLE_APPLICATION_CREDENTIALS path

### Storage & Database
- [ ] Create Cloud Storage bucket for assets
- [ ] Set bucket to publicly readable (for generated images)
- [ ] Initialize Firestore database
- [ ] Create Firestore collection: `story_sessions`

### Environment Variables
- [ ] Update `backend/.env` with production values
- [ ] Update `frontend/.env.local` with production WebSocket URL
- [ ] Verify all secrets are in Secret Manager

## Deployment Phase

### Build & Deploy
- [ ] Test locally with Docker Compose first
- [ ] Run `./scripts/deploy.sh` or manual Cloud Build
- [ ] Verify backend deployment on Cloud Run
- [ ] Verify frontend deployment on Cloud Run
- [ ] Test WebSocket connection to deployed backend
- [ ] Test API endpoints via deployed URL

### Post-Deployment Configuration
- [ ] Update frontend environment variables with backend URL
- [ ] Configure custom domain (optional)
- [ ] Enable Cloud CDN for faster asset delivery (optional)
- [ ] Set up Cloud Monitoring and Logging
- [ ] Configure alerts for errors and latency

## Testing Phase

### Functionality Tests
- [ ] Test voice recording and speech recognition
- [ ] Test video capture and object detection
- [ ] Test real-time illustration generation
- [ ] Test interruption handling (speak while AI is talking)
- [ ] Test story segment saving to Firestore
- [ ] Test story retrieval and display
- [ ] Test emotion-based background changes

### Performance Tests
- [ ] Verify WebSocket latency <500ms
- [ ] Check image generation time (2-5s acceptable)
- [ ] Test with multiple concurrent users
- [ ] Monitor Cloud Run instance scaling

### Browser Compatibility
- [ ] Test on Chrome/Edge (recommended)
- [ ] Test on Safari (macOS/iOS)
- [ ] Test on Firefox
- [ ] Test on mobile devices
- [ ] Verify camera and microphone permissions

### Error Handling
- [ ] Test with denied camera permissions
- [ ] Test with denied microphone permissions
- [ ] Test with network interruption
- [ ] Test with invalid API keys
- [ ] Test with expired credentials

## Demo Recording Preparation

### Recording Checklist
- [ ] Prepare demo script following the 4-minute structure
- [ ] Set up good lighting and audio
- [ ] Clear browser cache and cookies
- [ ] Close unnecessary tabs and applications
- [ ] Test microphone and camera before recording
- [ ] Have backup toys/objects for vision demo

### Demo Content (4 Minutes)
1. **0:00-0:45**: Problem introduction
   - [ ] Show child struggling to describe their day
   - [ ] Explain communication challenges

2. **0:45-1:30**: Core interaction demo
   - [ ] Show live voice interaction
   - [ ] Demonstrate interleaved output (text + images)
   - [ ] Show real-time response

3. **1:30-2:15**: Live Vision feature
   - [ ] Show camera detecting a toy
   - [ ] AI mentions the toy in the story
   - [ ] Visual integration into narrative

4. **2:15-3:00**: Interruption & Re-contextualization
   - [ ] Interrupt AI mid-sentence
   - [ ] Change story direction
   - [ ] Show seamless adaptation

5. **3:00-3:30**: Technical proof (REQUIRED)
   - [ ] Show Google Cloud Console
   - [ ] Show Cloud Run services running
   - [ ] Show live logs during interaction
   - [ ] Display architecture diagram

6. **3:30-4:00**: Impact summary
   - [ ] Show compiled story journal
   - [ ] Explain parent-child bonding benefit
   - [ ] Closing statement

### Screen Recording Tools
- [ ] Choose recording tool: OBS Studio / QuickTime / Loom
- [ ] Set resolution: 1920x1080 (Full HD)
- [ ] Enable microphone audio
- [ ] Test recording quality before final take

### Post-Production
- [ ] Trim any dead air or mistakes
- [ ] Add title slide with project name
- [ ] Add text overlays for key features
- [ ] Add background music (optional, low volume)
- [ ] Export in MP4 format
- [ ] Keep under 100MB file size

## Submission Checklist

### Required Deliverables
- [ ] 4-minute demo video (MP4)
- [ ] GitHub repository link
- [ ] Live deployment URL (Cloud Run)
- [ ] Architecture diagram (ARCHITECTURE.md)
- [ ] README with setup instructions
- [ ] Proof of Google Cloud deployment (screenshot)

### Repository Requirements
- [ ] Clean commit history
- [ ] Comprehensive README.md
- [ ] Clear directory structure
- [ ] All code properly commented
- [ ] .env.example files included
- [ ] No secrets committed to Git
- [ ] License file (MIT recommended)

### Documentation Requirements
- [ ] Technical architecture document
- [ ] API documentation (FastAPI auto-docs)
- [ ] Setup and deployment guide
- [ ] Troubleshooting section
- [ ] Technology stack list
- [ ] Innovation highlights

### Proof of Deployment
- [ ] Screenshot of Cloud Run services
- [ ] Screenshot of backend logs during demo
- [ ] Screenshot of Firestore with saved sessions
- [ ] Screenshot of Cloud Storage with generated images
- [ ] Screenshot of Vertex AI API calls

### Hackathon Category Alignment
- [ ] **Creative Storyteller**: Interleaved multimodal output ✓
- [ ] **Live Agent**: Real-time voice + vision interaction ✓
- [ ] **See, Hear, Speak**: All modalities demonstrated ✓
- [ ] **Google Cloud**: Full GCP stack utilized ✓
- [ ] **Responsible AI**: Low-demand, child-safe design ✓

## Final Review

### Code Quality
- [ ] No console.log in production code
- [ ] Error handling in all critical paths
- [ ] Clean code formatting
- [ ] Type safety (TypeScript in frontend)
- [ ] Security best practices followed

### User Experience
- [ ] Sensory-friendly colors and animations
- [ ] Clear instructions for users
- [ ] Accessible UI elements
- [ ] Mobile-responsive design
- [ ] Loading states for async operations

### Performance
- [ ] Cloud Run cold start time acceptable (<10s)
- [ ] WebSocket connection stable
- [ ] Image generation doesn't block voice
- [ ] Proper error messages
- [ ] Graceful degradation

### Hackathon-Specific
- [ ] Demo highlights all innovation points
- [ ] Clear explanation of "Low-Demand" approach
- [ ] Evidence of real-time capabilities
- [ ] Proof of multimodal interleaving
- [ ] Social impact clearly communicated

## Backup Plan

### If Deployment Fails
- [ ] Have local Docker Compose demo ready
- [ ] Record backup demo video in advance
- [ ] Prepare ngrok tunnel as backup
- [ ] Have architecture slides ready

### If APIs Go Down
- [ ] Pre-generate sample images
- [ ] Have mock responses ready
- [ ] Record a complete demo beforehand

## Day-of-Submission

### 2 Hours Before Deadline
- [ ] Final deployment verification
- [ ] Run full demo end-to-end
- [ ] Check all links work
- [ ] Upload demo video
- [ ] Submit application

### 1 Hour Before Deadline
- [ ] Take final screenshots
- [ ] Download backup of repository
- [ ] Save deployment URLs
- [ ] Prepare Q&A answers

### 30 Minutes Before Deadline
- [ ] Triple-check submission form
- [ ] Verify video is viewable
- [ ] Confirm all links are public
- [ ] Submit!

## Post-Submission

### After Submitting
- [ ] Tweet about your submission
- [ ] Share on LinkedIn
- [ ] Post in hackathon Discord/Slack
- [ ] Document lessons learned
- [ ] Plan improvements for future

### If Selected as Finalist
- [ ] Prepare live demo
- [ ] Practice pitch (2-3 minutes)
- [ ] Anticipate technical questions
- [ ] Test on multiple devices
- [ ] Have backup plan ready

---

**Remember**: The judges want to see:
1. **Real-time interaction** (not just request-response)
2. **Multimodal integration** (voice + vision + images simultaneously)
3. **Technical execution** (actually works, not just slides)
4. **Social impact** (solves a real problem)
5. **Google Cloud usage** (full stack deployed and demonstrated)

**Good luck!** 🚀✨
