
# The cast (who does what)

* **Next.js frontend (your UI):** one page to start a run, one page to watch status and the final video. It never talks to Akash or Orkes directly—only to your backend.
* **FastAPI backend (your glue/control plane):** single public API. Starts runs, talks to Orkes, calls Akash GPU services, writes/reads artifacts in Cloudflare R2, and streams live status to the frontend.
* **Orkes Conductor (the brain):** workflow engine. It calls your backend step-by-step (facts → script → storyboard → fan-out media → TTS → captions → assemble → optional YouTube → finish). Handles retries/timeouts and optional human-in-the-loop pause.
* **Akash (the muscle):** decentralized GPU host where your model services live as simple HTTP endpoints:

  * `t2i` (text-to-image, e.g., FLUX/SDXL)
  * `i2v` (image-to-video, e.g., AnimateDiff/SVD)
  * `ffmpeg` (stitching, overlays, audio mixdown)
* **Cloudflare R2 (artifacts):** S3-compatible object storage for frames, clips, audio, captions, and the final video. Everything is private; access is via short-lived, pre-signed URLs your backend issues.
* **Vendors (API calls):** LLM for script/storyboard, TTS voice (or self-hosted fallback).

# How they connect (no magic, just HTTP)

* **Frontend → Backend:** HTTPS requests only (start run, get status, stream events). Your browser never touches Akash, Orkes, or R2 directly.
* **Backend → Orkes:** Start workflow via Orkes API. Orkes then **calls back** into your backend’s task URLs for each step.
* **Backend ↔ Akash:** When a step needs GPU, backend calls your warm Akash endpoints. Those GPU services read/write media via **pre-signed R2 URLs** the backend gives them.
* **Backend ↔ R2:** Backend generates short-lived upload/download URLs for every artifact. No public buckets.
* **Backend ↔ LLM/TTS:** Plain API calls with your keys stored server-side.

# The exact life of a “Generate” click

1. **User clicks Generate** in Next.js
   → Frontend sends run options (duration, voice, motion intensity, style) to backend.
   → Backend creates `run_id`, stores light state, starts an **Orkes** workflow for that run, and immediately returns `run_id` to the frontend.

2. **UI navigates to /run/{run\_id}**
   → Subscribes to a server-sent events (SSE) stream from the backend to get live updates. (Polling fallback every \~2–3s if SSE is blocked.)

3. **Orkes starts executing steps** by calling your backend:

   * **CollectFacts:** backend hits news feeds/APIs, picks 5 items, writes a facts JSON to R2, returns success to Orkes, and emits an SSE update.
   * **WriteScript:** backend calls LLM, stores `script.json` (≤120 words), emits update.
   * **StoryboardPlan:** backend creates `shots.json` (prompts, on-screen text, duration, which 1–2 shots get motion), emits update.
   * **GenerateMedia (fan-out, bounded):** for each shot:

     * **t2i:** backend asks Akash `/t2i` to generate a 720×1280 still, writing `frame_i.png` to R2.
     * **i2v (optional):** for 1–2 chosen shots, backend asks Akash `/i2v` to animate `frame_i.png` into a 2–3s clip, writing `clip_i.mp4` to R2.
     * Each success emits a progress event. Concurrency is capped (e.g., 2 at a time) so you don’t OOM the GPU.
   * **TextToSpeech:** backend calls TTS (or self-host), writes `narration.wav` to R2 (+ a simple timing map).
   * **GenerateCaptions:** backend builds `captions.srt` aligned to the TTS map, writes to R2.
   * **AssembleSegments:** backend calls Akash `/ffmpeg` with R2 URLs for frames/clips/audio/captions; service assembles and writes `final/video.mp4` to R2.
   * **(Optional) UploadYouTube:** backend uploads `final.mp4` if OAuth connected; stores returned URL.
   * **NotifyAndComplete:** backend compiles a small audit JSON (models, seeds, GPU minutes, cost estimate), emits final SSE event.

4. **Frontend shows progress and result**
   → As SSE events arrive, step badges flip to RUNNING/DONE/FAILED.
   → When the backend exposes a signed URL for `final.mp4`, the player renders it.
   → A small cost chip shows GPU minutes × hourly rate, plus an “Open in Orkes” link for the live DAG.

# Where each thing actually runs

* **Your laptop/VS Code:** for development only. You run local dev servers, build Docker images, and commit. Nothing “connects” to VS Code in production.
* **Backend (FastAPI):** on a small VM/container with a public URL so Orkes can reach it. Could be Render/Fly/EC2—whatever you spin up quickly.
* **Akash GPU lease:** one warm lease with a 3090/4090. Your container inside exposes three HTTP paths (`/t2i`, `/i2v`, `/ffmpeg`).
* **Orkes:** fully managed SaaS UI/engine. You paste in your backend task URLs, timeouts, and retry counts.
* **R2:** your bucket lives in Cloudflare. Only pre-signed URLs are used; no public reads.

# Identities, keys, and safety

* **Backend env vars:** R2 keys, LLM key, TTS key, (optional) YouTube OAuth secrets. Never in the frontend.
* **Orkes secrets:** if you want Orkes to include auth headers when calling your backend tasks.
* **Akash container:** should not need your API keys. It only receives pre-signed URLs and model settings.
* **CORS:** backend must allow your frontend origin(s).
* **Signed URLs:** expire quickly (e.g., 10–30 minutes). The backend can refresh if needed.
* **Idempotency:** every task gets a `task_id`; retries return the same artifact paths instead of recomputing.

# Cost & performance reality

* **Warm lease** avoids cold-start pain; you keep it up during the hackathon window.
* **Per run:** 5 stills + 1–2 animated clips + ffmpeg ≈ 4–6 GPU minutes on a 3090/4090.
* **Ballpark:** a few cents per video at typical Akash rates.
* **Wall-clock:** \~60–90 seconds for a full run when warm.

# Failure modes (and what happens)

* **t2i/i2v fails or times out:** backend marks that shot as “still” and applies Ken-Burns during assembly; the run continues.
* **LLM/TTS vendor hiccup:** backend immediately switches to a backup provider or a local fallback voice.
* **FFmpeg step fails:** rebuild without background music first; if still failing, burn captions and simplify transitions.
* **Orkes retries a task:** backend returns the already-generated artifact from Redis state (no duplicate work).

# What judges will see

* You click Generate.
* A live **Orkes DAG** fills step-by-step.
* You open your **Akash lease panel/logs** to prove decentralized GPU.
* The final vertical video plays in your app.
* A **cost chip** shows GPU minutes and \$ estimate.
* A tiny **“sources”** overlay appears on each segment (credibility).

# Your clean mental model

* **Frontend = face.**
* **Backend = glue.**
* **Orkes = brain.**
* **Akash = biceps.**
* **R2 = backpack.**

That’s the complete bigger picture. If you want, I’ll lay out the **exact inputs/outputs for each Orkes task** (names, JSON fields, expected artifacts) so you and your backend wire it without second-guessing—still no code.
