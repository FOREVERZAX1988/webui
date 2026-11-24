/**
 * Camera preview modal — road / driver camera popup.
 *
 * Shares the existing WebRTC peer connection from webrtc_stream.js: the modal
 * video element attaches the already-decoded MediaStream instead of opening a
 * second stream, so CPU/network cost stays flat while the modal is open.
 *
 * Used by the device panel buttons (行车预览 / 驾驶员摄像头预览): clicking them
 * opens the preview on the device GUI (via params) AND pops up the picture here.
 */
import { tr } from "./i18n.js?v=3";

let modalRoot = null;
let modalVideo = null;
let modalWrap = null;
let modalStatus = null;
let modalKind = null; // "road" | "driver"
let onCloseCb = null;
let driverSwitchPending = false;

async function modules() {
  // Dynamic import keeps the ?v cache-busting query in sync with onroad.js.
  return await import("./webrtc_stream.js?v=99");
}

function setStatus(msg) {
  if (modalStatus) modalStatus.textContent = msg || "";
  if (modalWrap) modalWrap.classList.toggle("has-status", !!msg);
}

async function attachStream(kind) {
  const { startRoadStream, isRoadStreaming, getRoadMediaStream, switchCamera, CAM } = await modules();

  driverSwitchPending = false;

  if (isRoadStreaming()) {
    // Reuse the live peer connection; no second RTCPeerConnection.
    if (!modalVideo.srcObject && getRoadMediaStream()) {
      modalVideo.srcObject = getRoadMediaStream();
    }
    await modalVideo.play().catch(() => { /* ignore */ });
  } else {
    // Not streaming yet — negotiate on the modal video element.
    try {
      await startRoadStream(modalVideo, modalWrap);
      if (!modalVideo.srcObject && getRoadMediaStream()) {
        modalVideo.srcObject = getRoadMediaStream();
      }
    } catch (err) {
      console.warn("[preview-modal] stream start failed:", err);
      setStatus(tr("Camera preview unavailable") + ` (${err?.message || err})`);
      return;
    }
  }

  if (kind === "driver") {
    driverSwitchPending = true;
    try {
      await switchCamera(CAM.DRIVER);
    } catch (err) {
      console.warn("[preview-modal] driver switch failed:", err);
    }
  }
}

async function detachStream() {
  const { clearManualCamera, switchCamera, CAM } = await modules();
  try {
    if (modalVideo) modalVideo.srcObject = null;
    if (driverSwitchPending) {
      // Give the stream back to the road camera auto-switching.
      await switchCamera(CAM.ROAD).catch(() => {});
      clearManualCamera();
      driverSwitchPending = false;
    }
  } catch { /* ignore */ }
}

function buildDom() {
  modalRoot = document.createElement("div");
  modalRoot.className = "opui-modal opui-modal--preview";
  modalRoot.hidden = true;
  modalRoot.innerHTML = `
    <div class="opui-modal-card opui-modal-card--preview">
      <div class="opui-preview-head">
        <div class="opui-modal-title opui-preview-title"></div>
        <button type="button" class="opui-preview-close" aria-label="Close">✕</button>
      </div>
      <div class="opui-preview-video-wrap">
        <video class="opui-preview-video" autoplay muted playsinline
               disablepictureinpicture disableremoteplayback></video>
        <div class="opui-preview-status"></div>
      </div>
    </div>`;
  document.body.appendChild(modalRoot);

  modalVideo = modalRoot.querySelector(".opui-preview-video");
  modalWrap = modalRoot.querySelector(".opui-preview-video-wrap");
  modalStatus = modalRoot.querySelector(".opui-preview-status");

  modalRoot.querySelector(".opui-preview-close").addEventListener("click", () => closePreview());
  modalRoot.addEventListener("click", (e) => {
    if (e.target === modalRoot) closePreview();
  });
}

export async function openPreview(kind, { onClose } = {}) {
  if (!document.body) return;
  if (!modalRoot) buildDom();

  modalKind = kind;
  onCloseCb = typeof onClose === "function" ? onClose : null;
  modalRoot.querySelector(".opui-preview-title").textContent =
    kind === "driver" ? tr("Driver Camera Preview") : tr("Onroad Preview");

  modalRoot.removeAttribute("hidden");
  modalRoot.setAttribute("aria-hidden", "false");
  document.body.classList.add("opui-modal-open");
  document.body.classList.add("opui-preview-open");

  setStatus(tr("Connecting..."));
  await attachStream(kind);
}

export function closePreview() {
  if (!modalRoot || modalRoot.hidden) return;
  detachStream();
  modalRoot.setAttribute("hidden", "");
  modalRoot.setAttribute("aria-hidden", "true");
  document.body.classList.remove("opui-preview-open");
  if (!document.querySelector(".opui-modal:not([hidden])")) {
    document.body.classList.remove("opui-modal-open");
  }
  const cb = onCloseCb;
  onCloseCb = null;
  modalKind = null;
  if (cb) cb();
}

export function previewOpen(kind) {
  return !!modalRoot && !modalRoot.hidden && (kind == null || modalKind === kind);
}
