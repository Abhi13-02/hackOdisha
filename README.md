# AI Science Shorts Studio 🎬🤖

**HackOdisha 5.0 Project | Team: [Your Team Name]**

## 🎯 Project Overview

AI Science Shorts Studio is an automated video generation platform that creates engaging 30-60 second vertical videos from scripts using AI-powered workflows. Built with **Orkes Conductor** for workflow orchestration and **Akash Network** for decentralized GPU compute.

## 🚀 What It Does

**One-Click Video Generation:**
- Input: Text script or topic
- Output: Professional vertical video with AI-generated visuals, voiceover, and captions
- Perfect for: Educational content, social media, science communication

**Two Generation Modes:**
1. **Script Provided**: User provides script → Generate visuals + audio
2. **AI-Written Script**: Topic input → AI writes script → Generate complete video

## 🏗️ Architecture

### **Orkes Conductor (Workflow Brain)**
- Orchestrates entire video generation pipeline
- Handles task routing, retries, and error recovery
- Manages human-in-the-loop approvals
- Provides real-time workflow monitoring

### **Akash Network (GPU Muscle)**
- Hosts AI models on decentralized infrastructure
- **Text-to-Image**: FLUX.1/SDXL for visual generation
- **Image-to-Video**: Stable Video Diffusion for motion
- **Video Assembly**: FFmpeg for final production
- **Cost Advantage**: ~$0.03 per video vs $2+ on traditional cloud

### **Workflow Pipeline**
```
Input Script → Validate → Storyboard Planning → 
Generate Images (Akash GPU) → Text-to-Speech → 
Generate Captions → Video Assembly (Akash) → 
Final Output
```

## 💰 Why Akash Network?

**Cost Efficiency:**
- Traditional Cloud: $2-5 per video
- **Akash Network**: $0.02-0.03 per video
- 60-100x cost reduction

**Decentralized Benefits:**
- No vendor lock-in
- Permissionless access to GPU compute
- Global distribution of processing power
- Censorship-resistant content creation

**Technical Requirements:**
- GPU-intensive AI models (FLUX.1, Stable Video Diffusion)
- Parallel processing for multiple video segments
- Scalable infrastructure for batch processing

## 🎯 Target Market & Impact

**Primary Users:**
- Educators and science communicators
- Content creators and influencers
- Educational institutions
- Science organizations and NGOs

**Market Problem:**
- High cost of professional video production
- Technical barriers to AI-powered content creation
- Centralized platforms limiting creative freedom

**Our Solution:**
- Democratizes professional video creation
- Reduces production cost by 99%
- Enables rapid content iteration and testing

## 🏆 HackOdisha 5.0 Track Alignment

**Orkes Conductor AI Track:**
- Complex AI workflow orchestration
- Multi-step pipeline with conditional logic
- Real-time monitoring and error handling
- Human-in-the-loop capabilities

**Akash Network Tracks:**
- **Best Use of Akash GPUs**: Multiple GPU-intensive AI models
- **Best Use of Akash AI**: Complete AI pipeline deployment
- **Best Deployment**: Auto-scaling, cost-optimized infrastructure
- **Ready to Launch**: Clear business model and market demand

## 🛠️ Technical Stack

**Frontend:** React.js, Tailwind CSS
**Backend:** Node.js, Python Flask
**Workflow:** Orkes Conductor
**Compute:** Akash Network (GPU instances)
**AI Models:** FLUX.1, Stable Video Diffusion, Coqui TTS
**Storage:** Cloudflare R2
**Video Processing:** FFmpeg

## 🚧 Development Plan (36-Hour Hackathon)

### **Phase 1: Core Infrastructure (Hours 0-12)**
- Set up Orkes Conductor workflow with basic tasks
- Deploy AI services on Akash using our SDL configuration
- Create simple web interface for script input

### **Phase 2: AI Integration (Hours 12-24)**
- Integrate SDXL image generation service
- Add text-to-speech capabilities
- Implement video assembly pipeline with FFmpeg

### **Phase 3: Demo Polish (Hours 24-36)**
- End-to-end workflow testing
- Create compelling demo scenarios
- Prepare presentation materials

## 📊 Planned Demo Scenarios

1. **Live Video Generation**: Input script → Watch workflow execute in Orkes → Final video
2. **Cost Comparison**: Show Akash ($0.03) vs AWS/GCP ($2+) pricing
3. **Workflow Visualization**: Real-time Orkes Conductor dashboard
4. **Decentralized Benefits**: Multiple Akash providers handling different tasks

## 🎬 Expected Output

**Input**: "Explain quantum computing in 45 seconds"
**Output**: Professional video with:
- 5 AI-generated visuals from SDXL
- Synchronized voiceover from TTS
- Ken Burns transitions
- Professional captions
- Vertical format (720x1280)

## 🔮 Future Roadmap

**Phase 1 (Post-Hackathon):**
- Multi-language support
- Advanced animation options
- Social media platform integration

**Phase 2:**
- Live streaming integration
- Collaborative editing features
- Analytics and performance tracking

**Phase 3:**
- Enterprise white-label solutions
- API marketplace for developers
- Advanced AI personalization

## 👥 Team

- **[Your Name]**: Workflow Architecture & Integration
- **[Teammate 2]**: AI Models & Akash Deployment  
- **[Teammate 3]**: Frontend & Video Assembly

## 🙏 Akash Network Credit Request

We're requesting Akash credits to:
- Deploy and test AI models during development
- Run extensive demos during HackOdisha 5.0
- Showcase cost comparison against traditional cloud providers
- Demonstrate real-world scalability of decentralized compute

**Estimated Usage:**
- Development: 20 GPU hours
- Testing: 15 GPU hours  
- Demo